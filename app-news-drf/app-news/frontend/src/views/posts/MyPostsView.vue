<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900 mb-2">Мои статьи</h1>
          <p class="text-sm text-gray-600">
            Управляйте своими публикациями
          </p>
        </div>
        
        <router-link
          to="/posts/create"
          class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Создать статью
        </router-link>
      </div>

      <!-- Информация о подписке -->
      <div class="bg-white rounded-md shadow-sm border border-gray-200 p-4 mb-8">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- Существующие фильтры -->
            <select
              v-model="statusFilter"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
            >
              <option value="">Все статьи</option>
              <option value="published">Опубликованные</option>
              <option value="draft">Черновики</option>
            </select>
            
            <select
              v-model="categoryFilter"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
            >
              <option value="">Все категории</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            
            <button
              @click="applyFilters"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            >
              Применить
            </button>
          </div>
          
          <!-- Информация о подписке -->
          <div v-if="authStore.isAuthenticated" class="text-sm">
            <div v-if="subscriptionStore.isActive" class="flex items-center text-green-600">
              <CheckIcon class="w-4 h-4 mr-1" />
              Подписка активна
              <span v-if="subscriptionStore.pinnedPost" class="ml-2 text-gray-500">
                • Закреплен: {{ getPinnedPostTitle() }}
              </span>
            </div>
            <div v-else class="flex items-center text-gray-500">
              <ExclamationTriangleIcon class="w-4 h-4 mr-1" />
              Нет подписки
              <router-link to="/subscription" class="ml-2 text-blue-600 hover:underline">
                Подписаться
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Список постов -->
      <div v-if="postsStore.isLoading" class="space-y-4">
        <PostCardSkeleton v-for="i in 5" :key="i" />
      </div>

      <div v-else-if="myPosts.length > 0" class="space-y-4">
        <div
          v-for="post in myPosts"
          :key="post.id"
          class="bg-white rounded-md shadow-sm border border-gray-200 p-6"
        >
          <div class="flex items-start justify-between">
            <!-- Информация о посте -->
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-2">
                <router-link
                  :to="{ name: 'PostDetail', params: { slug: post.slug } }"
                  class="text-lg font-medium text-gray-900 hover:text-blue-600 transition-colors"
                >
                  {{ post.title }}
                </router-link>
                
                <!-- Статусы -->
                <div class="flex items-center space-x-2">
                  <span
                    v-if="post.status === 'draft'"
                    class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-50 text-yellow-800"
                  >
                    Черновик
                  </span>
                  <span
                    v-if="post.is_pinned"
                    class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-50 text-yellow-800"
                  >
                    <StarIcon class="w-3 h-3 mr-1 fill-current" />
                    Закреплен
                  </span>
                </div>
              </div>
              
              <!-- Краткое содержание -->
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">
                {{ getPostExcerpt(post.content) }}
              </p>
              
              <!-- Метаданные -->
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span>{{ formatDate(post.created_at) }}</span>
                <span class="flex items-center space-x-1">
                  <EyeIcon class="w-4 h-4" />
                  <span>{{ post.views_count || 0 }}</span>
                </span>
                <span class="flex items-center space-x-1">
                  <ChatBubbleLeftIcon class="w-4 h-4" />
                  <span>{{ post.comments_count || 0 }}</span>
                </span>
                <span v-if="post.category" class="text-blue-600">
                  {{ post.category }}
                </span>
              </div>
            </div>
            
            <!-- Действия -->
            <div class="flex items-center space-x-2 ml-4">
              <!-- Кнопка закрепления -->
              <button
                v-if="post.status === 'published'"
                @click="togglePostPin(post)"
                :disabled="pinActionLoading[post.id]"
                class="p-2 rounded-md transition-colors"
                :class="[
                  post.is_pinned 
                    ? 'text-yellow-600 bg-yellow-50 hover:bg-yellow-100' 
                    : subscriptionStore.isActive 
                      ? 'text-gray-400 hover:text-yellow-600 hover:bg-yellow-50' 
                      : 'text-gray-300 cursor-not-allowed'
                ]"
                :title="getPinButtonTitle(post)"
              >
                <div v-if="pinActionLoading[post.id]" class="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                <StarIcon v-else :class="['w-5 h-5', post.is_pinned ? 'fill-current' : '']" />
              </button>
              
              <!-- Редактировать -->
              <router-link
                :to="{ name: 'PostEdit', params: { slug: post.slug } }"
                class="p-2 text-gray-400 hover:text-blue-600 rounded-md hover:bg-blue-50 transition-colors"
                title="Редактировать"
              >
                <PencilIcon class="w-5 h-5" />
              </router-link>
              
              <!-- Удалить -->
              <button
                @click="deletePost(post)"
                class="p-2 text-gray-400 hover:text-red-600 rounded-md hover:bg-red-50 transition-colors"
                title="Удалить"
              >
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { usePostsStore } from '@/stores/posts'
import { useAuthStore } from '@/stores/auth'
import { useSubscriptionStore } from '@/stores/subscription'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
import PostListItem from '@/components/posts/PostListItem.vue'
import PostCardSkeleton from '@/components/ui/PostCardSkeleton.vue'
import { 
  PlusIcon, 
  DocumentTextIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  StarIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  ChatBubbleLeftIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'MyPostsView',
  components: { 
    PostListItem, 
    PostCardSkeleton, 
    PlusIcon, 
    DocumentTextIcon,
    CheckIcon,
    ExclamationTriangleIcon,
    StarIcon,
    PencilIcon,
    TrashIcon,
    EyeIcon,
    ChatBubbleLeftIcon
  },
  setup() {
    const postsStore = usePostsStore()
    const authStore = useAuthStore()
    const subscriptionStore = useSubscriptionStore()
    const toast = useToast()
    const router = useRouter()
    const statusFilter = ref('')
    const categoryFilter = ref('')
    const pinActionLoading = ref({})
    
    const myPosts = computed(() => postsStore.myPosts)
    const categories = computed(() => postsStore.categories)
    
    const applyFilters = async () => {
      const params = {}
      if (statusFilter.value) params.status = statusFilter.value
      if (categoryFilter.value) params.category = categoryFilter.value
      
      await postsStore.fetchMyPosts(params)
    }
    
    const getPinnedPostTitle = () => {
      if (!subscriptionStore.pinnedPost?.post_info) return ''
      const title = subscriptionStore.pinnedPost.post_info.title
      return title.length > 30 ? title.substring(0, 30) + '...' : title
    }
    
    const togglePostPin = async (post) => {
      if (!subscriptionStore.isActive) {
        toast.error('Для закрепления постов необходима активная подписка')
        router.push('/subscription')
        return
      }
      
      pinActionLoading.value[post.id] = true
      
      try {
        if (post.is_pinned) {
          await subscriptionStore.unpinPost()
          toast.success('Пост откреплен')
        } else {
          if (subscriptionStore.pinnedPost) {
            if (!confirm('У вас уже есть закрепленный пост. Хотите заменить его?')) {
              return
            }
          }
          
          await subscriptionStore.pinPost(post.id)
          toast.success('Пост закреплен')
        }
        
        await postsStore.fetchMyPosts()
        await subscriptionStore.fetchSubscriptionStatus()
        
      } catch (error) {
        console.error('Ошибка при работе с закреплением:', error)
        toast.error('Ошибка при изменении статуса закрепления')
      } finally {
        pinActionLoading.value[post.id] = false
      }
    }
    
    const deletePost = async (post) => {
      if (!confirm('Вы уверены, что хотите удалить этот пост?')) {
        return
      }
      
      try {
        await postsStore.deletePost(post.slug)
        toast.success('Пост успешно удален')
        await postsStore.fetchMyPosts()
      } catch (error) {
        console.error('Ошибка удаления поста:', error)
        toast.error('Не удалось удалить пост')
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    }
    
    const getPostExcerpt = (content) => {
      if (!content) return 'Нет содержания'
      return content.length > 150 ? content.substring(0, 150) + '...' : content
    }
    
    const getPinButtonTitle = (post) => {
      if (post.is_pinned) return 'Открепить пост'
      if (!subscriptionStore.isActive) return 'Требуется активная подписка'
      return 'Закрепить пост'
    }
    
    onMounted(async () => {
      await Promise.all([
        postsStore.fetchMyPosts(),
        postsStore.fetchCategories(),
        subscriptionStore.fetchSubscriptionStatus()
      ])
    })
    
    return {
      postsStore,
      authStore,
      subscriptionStore,
      myPosts,
      categories,
      statusFilter,
      categoryFilter,
      pinActionLoading,
      applyFilters,
      getPinnedPostTitle,
      togglePostPin,
      deletePost,
      formatDate,
      getPostExcerpt,
      getPinButtonTitle
    }
  }
}
</script>