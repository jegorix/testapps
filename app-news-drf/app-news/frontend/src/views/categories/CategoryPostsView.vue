<!-- src/views/categories/CategoryPostsView.vue -->
<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-content">
      <div v-if="category" class="text-center mb-8">
        <div class="w-16 h-16 bg-accent-100 rounded-xl flex items-center justify-center mx-auto mb-4">
          <component :is="getCategoryIcon(category.name)" class="w-8 h-8 text-accent-600" />
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ category.name }}</h1>
        <p v-if="category.description" class="text-gray-600 mb-4">{{ category.description }}</p>
        <p class="text-gray-500">
          {{ posts.length }} {{ pluralize(posts.length, 'статья', 'статьи', 'статей') }}
        </p>
      </div>
      
      <div v-if="postsStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PostCardSkeleton v-for="i in 6" :key="i" />
      </div>
      
      <div v-else-if="posts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>
      
      <div v-else class="text-center py-16">
        <DocumentTextIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Статьи не найдены</h3>
        <p class="text-gray-500">В этой категории пока нет опубликованных статей</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePostsStore } from '@/stores/posts'
import PostCard from '@/components/posts/PostCard.vue'
import PostCardSkeleton from '@/components/ui/PostCardSkeleton.vue'
import { DocumentTextIcon, TagIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'CategoryPostsView',
  components: { PostCard, PostCardSkeleton, DocumentTextIcon },
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const route = useRoute()
    const postsStore = usePostsStore()
    
    const category = ref(null)
    const posts = ref([])
    
    const getCategoryIcon = (categoryName) => {
      // Возвращаем TagIcon по умолчанию
      return 'TagIcon'
    }
    
    const pluralize = (count, one, few, many) => {
      const mod10 = count % 10
      const mod100 = count % 100
      
      if (mod100 >= 11 && mod100 <= 19) return many
      if (mod10 === 1) return one
      if (mod10 >= 2 && mod10 <= 4) return few
      return many
    }
    
    onMounted(async () => {
      try {
        const data = await postsStore.fetchPostsByCategory(props.slug)
        category.value = data.category
        posts.value = data.posts
      } catch (error) {
        console.error('Ошибка загрузки постов категории:', error)
      }
    })
    
    return {
      postsStore,
      category,
      posts,
      getCategoryIcon,
      pluralize
    }
  }
}
</script>