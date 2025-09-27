<template>
  <article class="card hover:shadow-lg transition-all duration-300 group overflow-hidden">
    <!-- Изображение поста -->
    <div class="relative overflow-hidden">
      <div
        v-if="post.image"
        class="aspect-w-16 aspect-h-9 bg-gray-200"
      >
        <img
          :src="post.image"
          :alt="post.title"
          class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
          @error="handleImageError"
        />
      </div>
      <div
        v-else
        class="h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center"
      >
        <DocumentTextIcon class="w-12 h-12 text-gray-400" />
      </div>
      
      <!-- Статус поста -->
      <div class="absolute top-3 left-3">
        <span
          v-if="post.status === 'draft'"
          class="badge bg-warning-100 text-warning-800 text-xs"
        >
          Черновик
        </span>
      </div>
      
      <!-- Категория -->
      <div v-if="post.category && getCategorySlug(post.category)" class="absolute top-3 right-3">
        <router-link
          :to="{ name: 'CategoryPosts', params: { slug: getCategorySlug(post.category) } }"
          class="badge badge-primary text-xs hover:bg-accent-200 transition-colors"
          @click.stop
        >
          {{ getCategoryName(post.category) }}
        </router-link>
      </div>
      <div v-else-if="post.category" class="absolute top-3 right-3">
        <span class="badge badge-primary text-xs cursor-default">
          {{ getCategoryName(post.category) }}
        </span>
      </div>

      <div v-if="post.is_pinned" class="absolute top-3 left-3">
        <span class="badge bg-yellow-100 text-yellow-800 text-xs flex items-center">
          <PinIcon class="w-3 h-3 mr-1" />
          Закреплен
        </span>
      </div>
    </div>

    <!-- Содержимое карточки -->
    <div class="card-body">
      <!-- Заголовок -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-accent-600 transition-colors">
        <router-link
          :to="{ name: 'PostDetail', params: { slug: post.slug } }"
          class="hover:underline"
        >
          {{ post.title }}
        </router-link>
      </h3>
      
      <!-- Краткое содержание -->
      <p class="text-gray-600 text-sm mb-4 line-clamp-3">
        {{ truncatedContent }}
      </p>
      
      <!-- Метаданные поста -->
      <div class="flex items-center justify-between text-xs text-gray-500 mb-4">
        <div class="flex items-center space-x-4">
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
        </div>
        
        <!-- Статистика -->
        <div class="flex items-center space-x-3">
          <!-- Просмотры -->
          <div class="flex items-center space-x-1">
            <EyeIcon class="w-4 h-4" />
            <span>{{ formatNumber(post.views_count) }}</span>
          </div>
          
          <!-- Комментарии -->
          <div class="flex items-center space-x-1">
            <ChatBubbleLeftIcon class="w-4 h-4" />
            <span>{{ formatNumber(post.comments_count) }}</span>
          </div>
        </div>
      </div>
      
      <!-- Действия -->
      <div class="flex items-center justify-between">
        <router-link
          :to="{ name: 'PostDetail', params: { slug: post.slug } }"
          class="text-accent-600 hover:text-accent-700 font-medium text-sm transition-colors"
        >
          Читать далее →
        </router-link>
        
        <!-- Меню действий для автора -->
        <div v-if="canEdit" class="relative">
          <button
            @click="showActions = !showActions"
            class="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors"
          >
            <EllipsisVerticalIcon class="w-5 h-5" />
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
        <PostPinButton v-if="canEdit" :post="post" />
      </div>
    </div>
  </article>
</template>

<script>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import { useToast } from 'vue-toastification'
import PostPinButton from './PostPinButton.vue'
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

const PinIcon = {
  template: `
    <svg viewBox="0 0 20 20" fill="currentColor" class="w-3 h-3">
      <path d="M10 2L12 4V8L14 10V12L10 16L6 12V10L8 8V4L10 2Z"/>
    </svg>
  `
}

export default {
  name: 'PostCard',
  components: {
    DocumentTextIcon,
    UserIcon,
    CalendarIcon,
    EyeIcon,
    ChatBubbleLeftIcon,
    EllipsisVerticalIcon,
    PencilIcon,
    TrashIcon,
    PostPinButton,
    PinIcon
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
      
      // Убираем HTML теги и обрезаем текст
      const plainText = props.post.content.replace(/<[^>]*>/g, '')
      return plainText.length > 150 
        ? plainText.substring(0, 150) + '...'
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
      
      // Если категория передана как строка, пытаемся найти её в store
      if (typeof category === 'string') {
        const categoryObj = postsStore.categories.find(cat => cat.name === category)
        return categoryObj?.slug || null
      }
      
      return null
    }
    
    const handleImageError = (event) => {
      // Скрываем изображение при ошибке загрузки
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

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.aspect-w-16 > * {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>