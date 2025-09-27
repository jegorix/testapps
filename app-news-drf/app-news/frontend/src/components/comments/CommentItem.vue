<template>
  <div class="flex space-x-3">
    <!-- Аватар -->
    <div class="flex-shrink-0">
      <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
        {{ getAuthorInitials(comment.author_info) }}
      </div>
    </div>
    
    <!-- Содержимое комментария -->
    <div class="flex-1 min-w-0">
      <div class="bg-gray-50 rounded-md p-4">
        <!-- Заголовок -->
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center space-x-2">
            <span class="font-medium text-gray-900 text-sm">
              {{ comment.author_info?.full_name || comment.author_info?.username }}
            </span>
            <span class="text-sm text-gray-500">
              {{ formatDate(comment.created_at) }}
            </span>
          </div>
          
          <!-- Меню действий -->
          <div v-if="canEdit" class="relative">
            <button
              @click="showActions = !showActions"
              class="p-1 text-gray-400 hover:text-gray-600 rounded-md"
            >
              <EllipsisVerticalIcon class="w-4 h-4" />
            </button>
            
            <div
              v-if="showActions"
              v-click-outside="() => showActions = false"
              class="absolute right-0 top-6 w-32 bg-white rounded-md shadow-sm border border-gray-200 py-1 z-10"
            >
              <button
                @click="startEdit"
                class="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600"
              >
                <PencilIcon class="w-3 h-3 mr-2" />
                Изменить
              </button>
              <button
                @click="handleDelete"
                class="flex items-center w-full px-3 py-2 text-sm text-red-600 hover:bg-red-50 hover:text-red-700"
              >
                <TrashIcon class="w-3 h-3 mr-2" />
                Удалить
              </button>
            </div>
          </div>
        </div>
        
        <!-- Содержимое -->
        <div v-if="!isEditing" class="text-gray-700 text-sm mb-3">
          {{ comment.content }}
        </div>
        
        <!-- Форма редактирования -->
        <div v-else class="mb-3">
          <textarea
            v-model="editContent"
            rows="3"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
          ></textarea>
          <div class="flex items-center space-x-2 mt-2">
            <button
              @click="saveEdit"
              class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
            >
              Сохранить
            </button>
            <button
              @click="cancelEdit"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            >
              Отмена
            </button>
          </div>
        </div>
        
        <!-- Действия -->
        <div class="flex items-center space-x-4 text-sm">
          <button
            v-if="authStore.isAuthenticated"
            @click="$emit('reply', comment)"
            class="text-gray-500 hover:text-blue-600 transition-colors"
          >
            Ответить
          </button>
          
          <span v-if="comment.replies_count > 0" class="text-gray-500">
            {{ comment.replies_count }} {{ pluralize(comment.replies_count, 'ответ', 'ответа', 'ответов') }}
          </span>
        </div>
      </div>
      
      <!-- Ответы -->
      <div v-if="comment.replies && comment.replies.length > 0" class="mt-4 space-y-4">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :post-id="postId"
          @reply="$emit('reply', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCommentsStore } from '@/stores/comments'
import { useToast } from 'vue-toastification'
import {
  EllipsisVerticalIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'CommentItem',
  components: {
    EllipsisVerticalIcon,
    PencilIcon,
    TrashIcon
  },
  props: {
    comment: {
      type: Object,
      required: true
    },
    postId: {
      type: Number,
      required: true
    }
  },
  emits: ['reply'],
  setup(props) {
    const authStore = useAuthStore()
    const commentsStore = useCommentsStore()
    const toast = useToast()
    
    const showActions = ref(false)
    const isEditing = ref(false)
    const editContent = ref('')
    
    const canEdit = computed(() => {
      return authStore.canEditComment(props.comment)
    })
    
    const getAuthorInitials = (authorInfo) => {
      if (!authorInfo) return '?'
      
      if (authorInfo.full_name) {
        return authorInfo.full_name
          .split(' ')
          .map(name => name.charAt(0).toUpperCase())
          .join('')
          .slice(0, 2)
      }
      
      return authorInfo.username?.charAt(0).toUpperCase() || '?'
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffInMs = now - date
      const diffInMinutes = Math.floor(diffInMs / (1000 * 60))
      const diffInHours = Math.floor(diffInMinutes / 60)
      const diffInDays = Math.floor(diffInHours / 24)
      
      if (diffInMinutes < 1) {
        return 'только что'
      } else if (diffInMinutes < 60) {
        return `${diffInMinutes} мин. назад`
      } else if (diffInHours < 24) {
        return `${diffInHours} ч. назад`
      } else if (diffInDays === 1) {
        return 'вчера'
      } else if (diffInDays < 7) {
        return `${diffInDays} дн. назад`
      } else {
        return date.toLocaleDateString('ru-RU')
      }
    }
    
    const pluralize = (count, one, few, many) => {
      const mod10 = count % 10
      const mod100 = count % 100
      
      if (mod100 >= 11 && mod100 <= 19) return many
      if (mod10 === 1) return one
      if (mod10 >= 2 && mod10 <= 4) return few
      return many
    }
    
    const startEdit = () => {
      editContent.value = props.comment.content
      isEditing.value = true
      showActions.value = false
    }
    
    const cancelEdit = () => {
      isEditing.value = false
      editContent.value = ''
    }
    
    const saveEdit = async () => {
      if (!editContent.value.trim()) {
        toast.error('Комментарий не может быть пустым')
        return
      }
      
      try {
        await commentsStore.updateCommentPartial(props.comment.id, {
          content: editContent.value.trim()
        })
        
        isEditing.value = false
        toast.success('Комментарий обновлен')
      } catch (error) {
        console.error('Ошибка обновления комментария:', error)
        toast.error('Не удалось обновить комментарий')
      }
    }
    
    const handleDelete = async () => {
      if (!confirm('Вы уверены, что хотите удалить этот комментарий?')) {
        return
      }
      
      try {
        await commentsStore.deleteComment(props.comment.id)
        showActions.value = false
        toast.success('Комментарий удален')
      } catch (error) {
        console.error('Ошибка удаления комментария:', error)
        toast.error('Не удалось удалить комментарий')
      }
    }
    
    return {
      authStore,
      showActions,
      isEditing,
      editContent,
      canEdit,
      getAuthorInitials,
      formatDate,
      pluralize,
      startEdit,
      cancelEdit,
      saveEdit,
      handleDelete
    }
  },
  directives: {
    'click-outside': {
      beforeMount(el, binding) {
        el.clickOutsideEvent = function(event) {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value()
          }
        }
        document.addEventListener('click', el.clickOutsideEvent)
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
      }
    }
  }
}
</script>