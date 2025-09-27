<template>
  <article class="card hover:shadow-md transition-all duration-300 group">
    <div class="card-body">
      <div class="flex items-start space-x-4">
        <!-- Миниатюра -->
        <div class="flex-shrink-0">
          <div
            v-if="post.image"
            class="w-20 h-20 rounded-lg overflow-hidden bg-gray-200"
          >
            <img
              :src="post.image"
              :alt="post.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
              @error="handleImageError"
            />
          </div>
          <div
            v-else
            class="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex items-center justify-center"
          >
            <DocumentTextIcon class="w-8 h-8 text-gray-400" />
          </div>
        </div>

        <!-- Содержимое -->
        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <!-- Заголовок и категория -->
              <div class="flex items-start justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-900 line-clamp-2 group-hover:text-accent-600 transition-colors">
                  <router-link
                    :to="{ name: 'PostDetail', params: { slug: post.slug } }"
                    class="hover:underline"
                  >
                    {{ post.title }}
                  </router-link>
                </h3>
                
                <div class="flex items-center space-x-2 ml-4 flex-shrink-0">
                  <!-- Статус -->
                  <span
                    v-if="post.status === 'draft'"
                    class="badge bg-warning-100 text-warning-800 text-xs"
                  >
                    Черновик
                  </span>
                  
                  <!-- Категория -->
                  <router-link
                    v-if="post.category && getCategorySlug(post.category)"
                    :to="{ name: 'CategoryPosts', params: { slug: getCategorySlug(post.category) } }"
                    class="badge badge-primary text-xs hover:bg-accent-200 transition-colors"
                    @click.stop
                  >
                    {{ getCategoryName(post.category) }}
                  </router-link>
                  <span
                    v-else-if="post.category"
                    class="badge badge-primary text-xs cursor-default"
                  >
                    {{ getCategoryName(post.category) }}
                  </span>
                </div>
              </div>
              
              <!-- Краткое описание -->
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">
                {{ truncatedContent }}
              </p>
              
              <!-- Метаданные -->
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4 text-xs text-gray-500">
                  <!-- Автор -->
                  <div class="flex items-center space-x-1">
                    <UserIcon class="w-4 h-4" />
                    <span>{{ post.author }}</span>
                  </div>
                  
                  <!-- Дата -->
                  <div class="flex items-center space-x-1">
                    <CalendarIcon class="w-4 h-4" />
                    <time :datetime="post.created_at">
                      {{ formatDate(post.created_at) }}
                    </time>
                  </div>
                  
                  <!-- Статистика -->
                  <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-1">
                      <EyeIcon class="w-4 h-4" />
                      <span>{{ formatNumber(post.views_count) }}</span>
                    </div>
                    <div class="flex items-center space-x-1">
                      <ChatBubbleLeftIcon class="w-4 h-4" />
                      <span>{{ formatNumber(post.comments_count) }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- Действия -->
                <div class="flex items-center space-x-2">
                  <router-link
                    :to="{ name: 'PostDetail', params: { slug: post.slug } }"
                    class="text-accent-600 hover:text-accent-700 font-medium text-sm transition-colors"
                  >
                    Читать →
                  </router-link>
                  
                  <!-- Меню действий для автора -->
                  <div v-if="canEdit" class="relative">
                    <button
                      @click="showActions = !showActions"
                      class="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors"
                    >
                      <EllipsisVerticalIcon class="w-4 h-4" />
                    </button>
                    
                    <!-- Выпадающее меню -->
                    <transition name="fade">
                      <div
                        v-if="showActions"
                        v-click-outside="() => showActions = false"
                        class="absolute right-0 top-8 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10"
                      >
                        <router-link
                          :to="{ name: 'PostEdit', params: { slug: post.slug } }"
                          class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          @click="showActions = false"
                        >
                          <PencilIcon class="w-4 h-4 mr-3" />
                          Редактировать
                        </router-link>
                        <button
                          @click="handleDelete"
                          class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                        >
                          <TrashIcon class="w-4 h-4 mr-3" />
                          Удалить
                        </button>
                      </div>
                    </transition>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>

<script>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import { useToast } from 'vue-toastification'
import {
  DocumentTextIcon,
  UserIcon,
  CalendarIcon,
  EyeIcon,
  ChatBubbleLeftIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'PostListItem',
  components: {
    DocumentTextIcon,
    UserIcon,
    CalendarIcon,
    EyeIcon,
    ChatBubbleLeftIcon,
    EllipsisVerticalIcon,
    PencilIcon,
    TrashIcon
  },
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const authStore = useAuthStore()
    const postsStore = usePostsStore()
    const toast = useToast()
    
    const showActions = ref(false)
    
    const canEdit = computed(() => {
      return authStore.canEditPost(props.post)
    })
    
    const truncatedContent = computed(() => {
      if (!props.post.content) return ''
      
      const plainText = props.post.content.replace(/<[^>]*>/g, '')
      return plainText.length > 120 
        ? plainText.substring(0, 120) + '...'
        : plainText
    })
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffInMs = now - date
      const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))
      
      if (diffInDays === 0) {
        return 'Сегодня'
      } else if (diffInDays === 1) {
        return 'Вчера'
      } else if (diffInDays < 7) {
        return `${diffInDays} дн. назад`
      } else {
        return date.toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'short',
          year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
        })
      }
    }
    
    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }
    
    const getCategoryName = (category) => {
      if (!category) return 'Без категории'
      
      if (typeof category === 'string') {
        return category
      }
      return category?.name || 'Без категории'
    }
    
    const getCategorySlug = (category) => {
      if (!category) return null
      
      if (typeof category === 'object' && category?.slug) {
        return category.slug
      }
      
      if (typeof category === 'string') {
        const categoryObj = postsStore.categories.find(cat => cat.name === category)
        return categoryObj?.slug || null
      }
      
      return null
    }
    
    const handleImageError = (event) => {
      event.target.style.display = 'none'
    }
    
    const handleDelete = async () => {
      if (!confirm('Вы уверены, что хотите удалить этот пост?')) {
        return
      }
      
      try {
        await postsStore.deletePost(props.post.slug)
        toast.success('Пост успешно удален')
        showActions.value = false
      } catch (error) {
        console.error('Ошибка удаления поста:', error)
        toast.error('Не удалось удалить пост')
      }
    }
    
    return {
      authStore,
      showActions,
      canEdit,
      truncatedContent,
      formatDate,
      formatNumber,
      getCategoryName,
      getCategorySlug,
      handleImageError,
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

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>