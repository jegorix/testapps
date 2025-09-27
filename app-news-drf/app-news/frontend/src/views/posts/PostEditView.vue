<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div v-if="postsStore.isLoadingPost" class="text-center py-16">
        <div class="inline-block w-8 h-8 border-2 border-gray-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p class="text-sm text-gray-600 mt-4">Загрузка поста...</p>
      </div>
      
      <div v-else-if="post">
        <div class="mb-8">
          <h1 class="text-2xl font-semibold text-gray-900 mb-2">Редактировать статью</h1>
          <p class="text-sm text-gray-600">Внесите изменения в вашу статью</p>
        </div>

        <!-- Используем ту же форму, что и для создания -->
        <PostFormComponent
          :initial-data="post"
          :is-editing="true"
          @submit="handleUpdate"
          @cancel="handleCancel"
        />
      </div>
      
      <div v-else class="text-center py-16">
        <ExclamationTriangleIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Пост не найден</h2>
        <p class="text-sm text-gray-600 mb-6">Запрашиваемая статья не существует или вы не имеете прав на её редактирование.</p>
        <router-link
          to="/posts"
          class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
        >
          Вернуться к статьям
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import { useToast } from 'vue-toastification'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import PostFormComponent from '@/components/posts/PostFormComponent.vue'

export default {
  name: 'PostEditView',
  components: { PostFormComponent, ExclamationTriangleIcon },
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const postsStore = usePostsStore()
    const toast = useToast()
    
    const post = computed(() => postsStore.currentPost)
    
    const loadPost = async () => {
      try {
        await postsStore.fetchPostBySlug(props.slug)
        
        // Проверяем права доступа
        if (post.value && !authStore.canEditPost(post.value)) {
          toast.error('У вас нет прав на редактирование этого поста')
          router.push('/posts')
        }
      } catch (error) {
        console.error('Ошибка загрузки поста:', error)
        if (error.response?.status === 404) {
          // Пост не найден
        }
      }
    }
    
    const handleUpdate = async (formData) => {
      try {
        const updatedPost = await postsStore.updatePost(props.slug, formData)
        toast.success('Статья успешно обновлена!')
        router.push({ name: 'PostDetail', params: { slug: updatedPost.slug } })
      } catch (error) {
        console.error('Ошибка обновления поста:', error)
        throw error
      }
    }
    
    const handleCancel = () => {
      router.push({ name: 'PostDetail', params: { slug: props.slug } })
    }
    
    onMounted(() => {
      loadPost()
    })
    
    return {
      authStore,
      postsStore,
      post,
      handleUpdate,
      handleCancel
    }
  }
}
</script>