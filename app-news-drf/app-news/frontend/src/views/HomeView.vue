<template>
  <div class="min-h-screen bg-white">
    <!-- Hero секция -->
    <section class="bg-white border-b border-gray-200">
      <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-16 text-center">
          <h1 class="text-4xl md:text-5xl font-semibold text-gray-900 mb-6">
            Добро пожаловать в
            <span class="text-blue-600">News Site</span>
          </h1>
          <p class="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Современная платформа для создания и чтения новостных статей. 
            Делитесь идеями, обсуждайте события и оставайтесь в курсе последних новостей.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <router-link
              to="/posts"
              class="btn bg-blue-600 text-white hover:bg-blue-700 px-6 py-3 rounded-md font-medium transition-colors"
            >
              Читать статьи
            </router-link>
            <router-link
              v-if="!authStore.isAuthenticated"
              to="/register"
              class="btn border-2 border-blue-600 text-blue-600 hover:bg-blue-50 hover:text-blue-700 px-6 py-3 rounded-md font-medium transition-colors"
            >
              Присоединиться
            </router-link>
            <router-link
              v-else
              to="/posts/create"
              class="btn border-2 border-blue-600 text-blue-600 hover:bg-blue-50 hover:text-blue-700 px-6 py-3 rounded-md font-medium transition-colors"
            >
              Создать пост
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Популярные посты -->
    <section class="py-12 bg-white">
      <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-2xl font-semibold text-gray-900">
            Популярные статьи
            <span v-if="pinnedPostsCount > 0" class="text-sm font-normal text-gray-500">
              ({{ pinnedPostsCount }} закреплено)
            </span>
          </h2>
          <router-link
            to="/posts"
            class="text-blue-600 hover:text-blue-700 font-medium text-sm"
          >
            Смотреть все →
          </router-link>
        </div>
        
        <div v-if="postsStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <PostCardSkeleton v-for="i in 6" :key="i" />
        </div>
        
        <div v-else-if="popularPosts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <PostCard
            v-for="post in popularPosts"
            :key="post.id"
            :post="post"
          />
        </div>
        
        <div v-else class="text-center py-12">
          <DocumentTextIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500 text-sm">Пока нет популярных статей</p>
        </div>
      </div>
    </section>

    <!-- Последние посты -->
    <section class="py-12 bg-gray-50">
      <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-2xl font-semibold text-gray-900">Последние статьи</h2>
          <router-link
            to="/posts"
            class="text-blue-600 hover:text-blue-700 font-medium text-sm"
          >
            Смотреть все →
          </router-link>
        </div>
        
        <div v-if="postsStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <PostCardSkeleton v-for="i in 6" :key="i" />
        </div>
        
        <div v-else-if="recentPosts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <PostCard
            v-for="post in recentPosts"
            :key="post.id"
            :post="post"
          />
        </div>
        
        <div v-else class="text-center py-12">
          <DocumentTextIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500 text-sm">Пока нет статей</p>
        </div>
      </div>
    </section>

    <!-- Категории -->
    <section class="py-12 bg-white">
      <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-2xl font-semibold text-gray-900">Категории</h2>
          <router-link
            to="/categories"
            class="text-blue-600 hover:text-blue-700 font-medium text-sm"
          >
            Смотреть все →
          </router-link>
        </div>
        
        <div v-if="postsStore.isLoadingCategories" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <CategoryCardSkeleton v-for="i in 8" :key="i" />
        </div>
        
        <div v-else-if="categories.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <CategoryCard
            v-for="category in categories.slice(0, 8)"
            :key="category.id"
            :category="category"
          />
        </div>
        
        <div v-else class="text-center py-12">
          <TagIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500 text-sm">Пока нет категорий</p>
        </div>
      </div>
    </section>

    <!-- Статистика -->
    <section class="py-12 bg-gray-50">
      <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-10">
          <h2 class="text-2xl font-semibold text-gray-900 mb-3">Наша платформа в цифрах</h2>
          <p class="text-gray-600 text-sm max-w-2xl mx-auto">
            Присоединяйтесь к растущему сообществу авторов и читателей
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="bg-white rounded-lg p-6 border border-gray-100">
              <div class="w-10 h-10 bg-blue-50 rounded-md flex items-center justify-center mx-auto mb-4">
                <DocumentTextIcon class="w-5 h-5 text-blue-600" />
              </div>
              <div class="text-xl font-semibold text-gray-900 mb-1">
                {{ stats.postsCount }}
              </div>
              <div class="text-gray-500 text-sm">Статей</div>
            </div>
          </div>
          
          <div class="text-center">
            <div class="bg-white rounded-lg p-6 border border-gray-100">
              <div class="w-10 h-10 bg-blue-50 rounded-md flex items-center justify-center mx-auto mb-4">
                <UserGroupIcon class="w-5 h-5 text-blue-600" />
              </div>
              <div class="text-xl font-semibold text-gray-900 mb-1">
                {{ stats.usersCount }}
              </div>
              <div class="text-gray-500 text-sm">Авторов</div>
            </div>
          </div>
          
          <div class="text-center">
            <div class="bg-white rounded-lg p-6 border border-gray-100">
              <div class="w-10 h-10 bg-blue-50 rounded-md flex items-center justify-center mx-auto mb-4">
                <ChatBubbleLeftIcon class="w-5 h-5 text-blue-600" />
              </div>
              <div class="text-xl font-semibold text-gray-900 mb-1">
                {{ stats.commentsCount }}
              </div>
              <div class="text-gray-500 text-sm">Комментариев</div>
            </div>
          </div>
          
          <div class="text-center">
            <div class="bg-white rounded-lg p-6 border border-gray-100">
              <div class="w-10 h-10 bg-blue-50 rounded-md flex items-center justify-center mx-auto mb-4">
                <TagIcon class="w-5 h-5 text-blue-600" />
              </div>
              <div class="text-xl font-semibold text-gray-900 mb-1">
                {{ stats.categoriesCount }}
              </div>
              <div class="text-gray-500 text-sm">Категорий</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA секция -->
    <section v-if="!authStore.isAuthenticated" class="py-12 bg-white border-t border-gray-200">
      <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-2xl font-semibold text-gray-900 mb-3">
            Готовы начать писать?
          </h2>
          <p class="text-gray-600 text-sm mb-8 max-w-2xl mx-auto">
            Создайте аккаунт и начните делиться своими идеями с миром. 
            Это займет всего несколько минут.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <router-link
              to="/register"
              class="btn bg-blue-600 text-white hover:bg-blue-700 px-6 py-3 rounded-md font-medium transition-colors"
            >
              Зарегистрироваться
            </router-link>
            <router-link
              to="/login"
              class="btn border-2 border-gray-300 text-gray-600 hover:bg-gray-50 hover:text-gray-700 px-6 py-3 rounded-md font-medium transition-colors"
            >
              Уже есть аккаунт?
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import PostCard from '@/components/posts/PostCard.vue'
import PostCardSkeleton from '@/components/ui/PostCardSkeleton.vue'
import CategoryCard from '@/components/categories/CategoryCard.vue'
import CategoryCardSkeleton from '@/components/ui/CategoryCardSkeleton.vue'
import {
  DocumentTextIcon,
  TagIcon,
  UserGroupIcon,
  ChatBubbleLeftIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'HomeView',
  components: {
    PostCard,
    PostCardSkeleton,
    CategoryCard,
    CategoryCardSkeleton,
    DocumentTextIcon,
    TagIcon,
    UserGroupIcon,
    ChatBubbleLeftIcon
  },
  setup() {
    const authStore = useAuthStore()
    const postsStore = usePostsStore()
    
    // Реактивные данные
    const pinnedPostsCount = ref(0)
    const stats = ref({
      postsCount: '1.2K',
      usersCount: '350',
      commentsCount: '2.8K',
      categoriesCount: '24'
    })
    
    // Computed properties
    const popularPosts = computed(() => postsStore.popularPosts || [])
    const recentPosts = computed(() => postsStore.recentPosts || [])
    const categories = computed(() => postsStore.categories || [])
    
    // Функция загрузки данных
    const loadData = async () => {
      try {
        // Загружаем данные параллельно
        await Promise.all([
          postsStore.fetchPopularPosts?.() || Promise.resolve(),
          postsStore.fetchRecentPosts?.() || Promise.resolve(),
          postsStore.fetchCategories?.() || Promise.resolve()
        ])
        
        // Подсчитываем закрепленные посты
        pinnedPostsCount.value = popularPosts.value.filter(post => post.is_pinned).length
      } catch (error) {
        console.error('Ошибка загрузки данных главной страницы:', error)
      }
    }
    
    // Загружаем данные при монтировании
    onMounted(() => {
      loadData()
    })
    
    return {
      authStore,
      postsStore,
      popularPosts,
      recentPosts,
      categories,
      stats,
      pinnedPostsCount
    }
  }
}
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  outline: none;
  focus: outline-none;
}

.btn:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
</style>