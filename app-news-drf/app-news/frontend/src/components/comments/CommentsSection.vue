<template>
  <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-semibold text-gray-900">
        Комментарии ({{ totalCommentsCount }})
      </h2>
    </div>
    
    <!-- Форма добавления комментария -->
    <div v-if="authStore.isAuthenticated" class="mb-8">
      <form @submit.prevent="handleSubmitComment" class="space-y-4">
        <textarea
          v-model="newComment"
          rows="3"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
          placeholder="Оставьте ваш комментарий..."
        ></textarea>
        <div class="flex justify-end">
          <button
            type="submit"
            :disabled="!newComment.trim() || commentsStore.isSubmitting"
            class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
            :class="{ 'opacity-50 cursor-not-allowed': !newComment.trim() || commentsStore.isSubmitting }"
          >
            <div v-if="commentsStore.isSubmitting" class="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
            Отправить
          </button>
        </div>
      </form>
    </div>
    
    <div v-else class="mb-8 p-4 bg-gray-50 rounded-md text-center">
      <p class="text-gray-600 mb-4 text-sm">Войдите, чтобы оставить комментарий</p>
      <router-link
        to="/login"
        class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
      >
        Войти
      </router-link>
    </div>
    
    <!-- Список комментариев -->
    <div v-if="comments.length > 0" class="space-y-6">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :post-id="postId"
        @reply="handleReply"
      />
    </div>
    
    <div v-else class="text-center py-8">
      <ChatBubbleLeftIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
      <p class="text-gray-500 text-sm">Пока нет комментариев. Будьте первым!</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCommentsStore } from '@/stores/comments'
import { useToast } from 'vue-toastification'
import CommentItem from './CommentItem.vue'
import { ChatBubbleLeftIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'CommentsSection',
  components: { CommentItem, ChatBubbleLeftIcon },
  props: {
    postId: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const authStore = useAuthStore()
    const commentsStore = useCommentsStore()
    const toast = useToast()
    
    const newComment = ref('')
    
    const comments = computed(() => commentsStore.topLevelComments)
    const totalCommentsCount = computed(() => commentsStore.totalCommentsCount)
    
    const handleSubmitComment = async () => {
      if (!newComment.value.trim()) return
      
      try {
        await commentsStore.createComment({
          post: props.postId,
          content: newComment.value.trim(),
          parent: null
        })
        
        newComment.value = ''
        toast.success('Комментарий добавлен')
      } catch (error) {
        console.error('Ошибка добавления комментария:', error)
        toast.error('Не удалось добавить комментарий')
      }
    }
    
    const handleReply = (parentComment) => {
      // Логика для ответа на комментарий
      console.log('Reply to comment:', parentComment)
    }
    
    onMounted(() => {
      commentsStore.fetchPostComments(props.postId)
    })
    
    return {
      authStore,
      commentsStore,
      newComment,
      comments,
      totalCommentsCount,
      handleSubmitComment,
      handleReply
    }
  }
}
</script>