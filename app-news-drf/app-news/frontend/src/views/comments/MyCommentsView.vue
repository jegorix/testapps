<!-- src/views/comments/MyCommentsView.vue -->
<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-content">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Мои комментарии</h1>
        <p class="text-gray-600">Управляйте своими комментариями</p>
      </div>
      
      <div v-if="commentsStore.isLoading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="card animate-pulse">
          <div class="card-body">
            <div class="h-4 bg-gray-300 rounded mb-2"></div>
            <div class="h-3 bg-gray-200 rounded w-3/4"></div>
          </div>
        </div>
      </div>
      
      <div v-else-if="myComments.length > 0" class="space-y-4">
        <div
          v-for="comment in myComments"
          :key="comment.id"
          class="card"
        >
          <div class="card-body">
            <p class="text-gray-900 mb-2">{{ comment.content }}</p>
            <div class="flex items-center justify-between text-sm text-gray-500">
              <div>
                К статье: 
                <router-link 
                  :to="{ name: 'PostDetail', params: { slug: comment.post_slug } }"
                  class="text-accent-600 hover:text-accent-700"
                >
                  {{ comment.post_title }}
                </router-link>
              </div>
              <div>{{ formatDate(comment.created_at) }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-16">
        <ChatBubbleLeftIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">У вас пока нет комментариев</h3>
        <p class="text-gray-500">Начните обсуждение, оставив комментарий к статье</p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useCommentsStore } from '@/stores/comments'
import { ChatBubbleLeftIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'MyCommentsView',
  components: { ChatBubbleLeftIcon },
  setup() {
    const commentsStore = useCommentsStore()
    const myComments = computed(() => commentsStore.myComments)
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }
    
    onMounted(() => {
      commentsStore.fetchMyComments()
    })
    
    return {
      commentsStore,
      myComments,
      formatDate
    }
  }
}
</script>