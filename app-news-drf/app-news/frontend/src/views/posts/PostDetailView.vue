<template>
  <div class="min-h-screen bg-gray-50">
    <div v-if="postsStore.isLoadingPost" class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <PostDetailSkeleton />
    </div>
    
    <div v-else-if="post" class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Навигация -->
      <nav class="flex items-center space-x-2 text-sm text-gray-500 mb-6">
        <router-link to="/" class="hover:text-blue-600 transition-colors">Главная</router-link>
        <ChevronRightIcon class="w-4 h-4" />
        <router-link to="/posts" class="hover:text-blue-600 transition-colors">Статьи</router-link>
        <ChevronRightIcon class="w-4 h-4" />
        <router-link
          v-if="post.category_info"
          :to="{ name: 'CategoryPosts', params: { slug: post.category_info.slug } }"
          class="hover:text-blue-600 transition-colors"
        >
          {{ post.category_info.name }}
        </router-link>
        <ChevronRightIcon v-if="post.category_info" class="w-4 h-4" />
        <span class="text-gray-900 truncate">{{ post.title }}</span>
      </nav>

      <!-- Основной контент -->
      <article class="bg-white rounded-md shadow-sm border border-gray-200 overflow-hidden">
        <!-- Изображение поста -->
        <div v-if="post.image" class="aspect-w-16 aspect-h-9">
          <img
            :src="post.image"
            :alt="post.title"
            class="w-full h-64 md:h-80 object-cover"
          />
        </div>

        <div class="p-6 md:p-8">
          <!-- Заголовок и метаданные -->
          <header class="mb-8">
            <!-- Статус и категория -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <span
                  v-if="post.status === 'draft'"
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-50 text-yellow-800"
                >
                  Черновик
                </span>
                <router-link
                  v-if="post.category_info"
                  :to="{ name: 'CategoryPosts', params: { slug: post.category_info.slug } }"
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
                >
                  {{ post.category_info.name }}
                </router-link>
              </div>
              
              <!-- Статус закрепления и меню действий -->
              <div class="flex items-center space-x-3">
                <!-- Статус закрепления -->
                <span
                  v-if="post.is_pinned"
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-50 text-yellow-800"
                >
                  <StarIcon class="w-3 h-3 mr-1 fill-current" />
                  Закреплен
                </span>
                
                <!-- Меню действий для автора -->
                <div v-if="canEdit" class="relative">
                  <button
                    @click="toggleActions"
                    class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-50 transition-colors"
                  >
                    <EllipsisVerticalIcon class="w-5 h-5" />
                  </button>
                  
                  <!-- Выпадающее меню -->
                  <transition
                    enter-active-class="transition ease-out duration-100"
                    enter-from-class="transform opacity-0 scale-95"
                    enter-to-class="transform opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="transform opacity-100 scale-100"
                    leave-to-class="transform opacity-0 scale-95"
                  >
                    <div
                      v-show="showActions"
                      class="absolute right-0 top-10 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-20"
                    >
                      <router-link
                        :to="{ name: 'PostEdit', params: { slug: post.slug } }"
                        class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                        @click="showActions = false"
                      >
                        <PencilIcon class="w-4 h-4 mr-3" />
                        Редактировать
                      </router-link>
                      
                      <button
                        @click="handleTogglePin"
                        :disabled="pinActionLoading"
                        class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
                      >
                        <StarIcon 
                          :class="['w-4 h-4 mr-3', post.is_pinned ? 'text-yellow-500 fill-current' : '']" 
                        />
                        {{ pinActionLoading ? 'Обработка...' : (post.is_pinned ? 'Открепить' : 'Закрепить') }}
                      </button>
                      
                      <div class="border-t border-gray-100 my-1"></div>
                      
                      <button
                        @click="handleDelete"
                        class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 hover:text-red-700 transition-colors"
                      >
                        <TrashIcon class="w-4 h-4 mr-3" />
                        Удалить
                      </button>
                    </div>
                  </transition>
                </div>
              </div>
            </div>

            <!-- Заголовок -->
            <h1 class="text-2xl md:text-3xl font-semibold text-gray-900 mb-6 leading-tight">
              {{ post.title }}
            </h1>

            <!-- Информация об авторе и статистика -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <!-- Автор -->
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {{ getAuthorInitials(post.author_info) }}
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">
                      {{ post.author_info?.full_name || post.author }}
                    </p>
                    <div class="flex items-center space-x-2 text-sm text-gray-500">
                      <time :datetime="post.created_at">
                        {{ formatDate(post.created_at) }}
                      </time>
                      <span v-if="post.updated_at !== post.created_at">
                        • обновлено {{ formatDate(post.updated_at) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Статистика -->
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <div class="flex items-center space-x-1">
                  <EyeIcon class="w-4 h-4" />
                  <span>{{ formatNumber(post.views_count) }}</span>
                </div>
                <div class="flex items-center space-x-1">
                  <ChatBubbleLeftIcon class="w-4 h-4" />
                  <span>{{ formatNumber(post.comments_count) }}</span>
                </div>
                <button
                  @click="sharePost"
                  class="flex items-center space-x-1 hover:text-blue-600 transition-colors"
                >
                  <ShareIcon class="w-4 h-4" />
                  <span>Поделиться</span>
                </button>
              </div>
            </div>
          </header>

          <!-- Содержимое поста -->
          <div class="prose prose-sm md:prose-lg max-w-none mb-12 text-gray-700">
            <div v-html="formattedContent"></div>
          </div>

          <!-- Теги (если есть) -->
          <div v-if="post.tags && post.tags.length" class="mb-8">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in post.tags"
                :key="tag"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700"
              >
                <TagIcon class="w-3 h-3 mr-1" />
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- Действия -->
          <div class="flex items-center justify-between pt-6 border-t border-gray-200">
            <div class="flex items-center space-x-4">
              <button
                @click="toggleLike"
                class="flex items-center space-x-2 px-4 py-2 rounded-md transition-colors"
                :class="isLiked ? 'bg-red-50 text-red-600 hover:bg-red-100' : 'bg-gray-50 text-gray-600 hover:bg-gray-100'"
              >
                <HeartIcon :class="['w-5 h-5', isLiked ? 'fill-current' : '']" />
                <span>{{ likesCount }}</span>
              </button>
              
              <button
                @click="scrollToComments"
                class="flex items-center space-x-2 px-4 py-2 rounded-md bg-gray-50 text-gray-600 hover:bg-gray-100 transition-colors"
              >
                <ChatBubbleLeftIcon class="w-5 h-5" />
                <span>Комментарии</span>
              </button>
            </div>

            <div class="flex items-center space-x-2">
              <button
                @click="sharePost"
                class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-50 transition-colors"
              >
                <ShareIcon class="w-5 h-5" />
              </button>
              <button
                @click="toggleBookmark"
                class="p-2 rounded-md transition-colors"
                :class="isBookmarked ? 'text-blue-600 bg-blue-50 hover:bg-blue-100' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'"
              >
                <BookmarkIcon :class="['w-5 h-5', isBookmarked ? 'fill-current' : '']" />
              </button>
            </div>
          </div>
        </div>
      </article>

      <!-- Кнопка закрепления поста (если автор) -->
      <PostPinButton v-if="canEdit" :post="post" class="mt-4" />

      <!-- Комментарии -->
      <div id="comments" class="mt-8">
        <CommentsSection :post-id="post.id" />
      </div>

      <!-- Похожие посты -->
      <div v-if="relatedPosts.length" class="mt-12">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">Похожие статьи</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <PostCard
            v-for="relatedPost in relatedPosts"
            :key="relatedPost.id"
            :post="relatedPost"
          />
        </div>
      </div>
    </div>

    <!-- Пост не найден -->
    <div v-else class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
      <ExclamationTriangleIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
      <h2 class="text-xl font-semibold text-gray-900 mb-2">Пост не найден</h2>
      <p class="text-sm text-gray-600 mb-6">Запрашиваемая статья не существует или была удалена.</p>
      <router-link
        to="/posts"
        class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
      >
        Вернуться к статьям
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import { useSubscriptionStore } from '@/stores/subscription'
import { useToast } from 'vue-toastification'
import PostCard from '@/components/posts/PostCard.vue'
import PostPinButton from '@/components/posts/PostPinButton.vue'
import CommentsSection from '@/components/comments/CommentsSection.vue'
import PostDetailSkeleton from '@/components/ui/PostDetailSkeleton.vue'
import {
  ChevronRightIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  ChatBubbleLeftIcon,
  ShareIcon,
  HeartIcon,
  BookmarkIcon,
  TagIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import { StarIcon } from '@heroicons/vue/24/solid'

export default {
  name: 'PostDetailView',
  components: {
    PostCard,
    PostPinButton,
    CommentsSection,
    PostDetailSkeleton,
    ChevronRightIcon,
    EllipsisVerticalIcon,
    PencilIcon,
    TrashIcon,
    EyeIcon,
    ChatBubbleLeftIcon,
    ShareIcon,
    HeartIcon,
    BookmarkIcon,
    TagIcon,
    ExclamationTriangleIcon,
    StarIcon
  },
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
    const subscriptionStore = useSubscriptionStore()
    const toast = useToast()
    
    const showActions = ref(false)
    const isLiked = ref(false)
    const isBookmarked = ref(false)
    const likesCount = ref(0)
    const relatedPosts = ref([])
    const pinActionLoading = ref(false)
    
    const post = computed(() => postsStore.currentPost)
    const canEdit = computed(() => {
      return post.value && authStore.canEditPost && authStore.canEditPost(post.value)
    })
    
    const formattedContent = computed(() => {
      if (!post.value?.content) return ''
      
      return post.value.content
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p>')
        .replace(/$/, '</p>')
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
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }
    
    const loadPost = async () => {
      try {
        await postsStore.fetchPostBySlug(props.slug)
        
        if (post.value?.category_info) {
          const categoryPosts = await postsStore.fetchPostsByCategory(
            post.value.category_info.slug,
            { page_size: 4 }
          )
          relatedPosts.value = categoryPosts.posts
            .filter(p => p.id !== post.value.id)
            .slice(0, 3)
        }
      } catch (error) {
        console.error('Ошибка загрузки поста:', error)
        if (error.response?.status === 404) {
          // Пост не найден
        }
      }
    }
    
    const handleDelete = async () => {
      if (!confirm('Вы уверены, что хотите удалить этот пост?')) {
        return
      }
      
      try {
        await postsStore.deletePost(post.value.slug)
        toast.success('Пост успешно удален')
        router.push('/posts')
      } catch (error) {
        console.error('Ошибка удаления поста:', error)
        toast.error('Не удалось удалить пост')
      }
    }
    
    const toggleLike = () => {
      if (!authStore.isAuthenticated) {
        toast.info('Войдите, чтобы поставить лайк')
        return
      }
      
      isLiked.value = !isLiked.value
      likesCount.value += isLiked.value ? 1 : -1
      
      toast.success(isLiked.value ? 'Лайк добавлен' : 'Лайк убран')
    }
    
    const toggleBookmark = () => {
      if (!authStore.isAuthenticated) {
        toast.info('Войдите, чтобы добавить в закладки')
        return
      }
      
      isBookmarked.value = !isBookmarked.value
      
      toast.success(
        isBookmarked.value 
          ? 'Добавлено в закладки' 
          : 'Убрано из закладок'
      )
    }
    
    const toggleActions = () => {
      showActions.value = !showActions.value
    }
    
    const handleTogglePin = async () => {
      if (!subscriptionStore.isActive) {
        toast.error('Для закрепления постов необходима активная подписка')
        router.push('/subscription')
        return
      }
      
      pinActionLoading.value = true
      showActions.value = false
      
      try {
        if (post.value.is_pinned) {
          await subscriptionStore.unpinPost()
          toast.success('Пост откреплен')
        } else {
          await subscriptionStore.pinPost(post.value.id)
          toast.success('Пост закреплен')
        }
        
        await postsStore.fetchPostBySlug(props.slug)
        
      } catch (error) {
        console.error('Ошибка при работе с закреплением:', error)
        toast.error('Ошибка при изменении статуса закрепления')
      } finally {
        pinActionLoading.value = false
      }
    }
    
    const sharePost = async () => {
      if (navigator.share && post.value) {
        try {
          await navigator.share({
            title: post.value.title,
            text: post.value.content.substring(0, 100) + '...',
            url: window.location.href
          })
        } catch (err) {
          copyToClipboard()
        }
      } else {
        copyToClipboard()
      }
    }
    
    const copyToClipboard = () => {
      navigator.clipboard.writeText(window.location.href)
      toast.success('Ссылка скопирована в буфер обмена')
    }
    
    const scrollToComments = () => {
      document.getElementById('comments')?.scrollIntoView({ 
        behavior: 'smooth' 
      })
    }
    
    onMounted(async () => {
      await loadPost()
      await subscriptionStore.fetchSubscriptionStatus()
      
      if (post.value) {
        document.title = `${post.value.title} | News Site`
        
        const metaDescription = document.querySelector('meta[name="description"]')
        if (metaDescription) {
          metaDescription.content = post.value.content.substring(0, 160)
        }
      }
      
      const handleClickOutside = (event) => {
        if (showActions.value && !event.target.closest('.relative')) {
          showActions.value = false
        }
      }
      
      document.addEventListener('click', handleClickOutside)
      
      onUnmounted(() => {
        document.removeEventListener('click', handleClickOutside)
      })
    })
    
    return {
      authStore,
      postsStore,
      subscriptionStore,
      post,
      showActions,
      isLiked,
      isBookmarked,
      likesCount,
      relatedPosts,
      canEdit,
      formattedContent,
      getAuthorInitials,
      formatDate,
      formatNumber,
      handleDelete,
      toggleLike,
      toggleBookmark,
      toggleActions,
      handleTogglePin,
      pinActionLoading,
      sharePost,
      scrollToComments
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
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>