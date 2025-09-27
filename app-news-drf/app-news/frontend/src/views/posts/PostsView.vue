<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Заголовок и фильтры -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900 mb-2">Все статьи</h1>
          <p class="text-sm text-gray-600">
            Найдено {{ pagination.count }} {{ pluralize(pagination.count, 'статья', 'статьи', 'статей') }}
          </p>
        </div>
        
        <!-- Кнопка создания поста -->
        <div v-if="authStore.isAuthenticated" class="mt-4 lg:mt-0">
          <router-link
            to="/posts/create"
            class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
          >
            <PlusIcon class="w-5 h-5 mr-2" />
            Создать пост
          </router-link>
        </div>
      </div>

      <!-- Панель фильтров -->
      <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6 mb-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Поиск -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700">Поиск</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Поиск по заголовку и содержанию..."
                class="block w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                @keyup.enter="applyFilters"
              />
            </div>
          </div>

          <!-- Категория -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Категория</label>
            <select
              v-model="selectedCategory"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
            >
              <option value="">Все категории</option>
              <option
                v-for="category in categories"
                :key="category.id"
                :value="category.id"
              >
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Сортировка -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Сортировка</label>
            <select
              v-model="selectedOrdering"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
            >
              <option value="-created_at">Сначала новые</option>
              <option value="created_at">Сначала старые</option>
              <option value="-views_count">По популярности</option>
              <option value="title">По алфавиту</option>
              <option value="-updated_at">Недавно обновленные</option>
            </select>
          </div>
        </div>

        <!-- Кнопки действий -->
        <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
          <div class="flex items-center space-x-2">
            <button
              @click="applyFilters"
              class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
            >
              Применить
            </button>
            <button
              @click="clearFilters"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            >
              Сбросить
            </button>
          </div>
          
          <!-- Переключатель вида -->
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-600">Вид:</span>
            <button
              @click="viewMode = 'grid'"
              class="p-2 rounded-md transition-colors"
              :class="viewMode === 'grid' ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:text-gray-600'"
            >
              <Squares2X2Icon class="w-5 h-5" />
            </button>
            <button
              @click="viewMode = 'list'"
              class="p-2 rounded-md transition-colors"
              :class="viewMode === 'list' ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:text-gray-600'"
            >
              <ListBulletIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <!-- Список постов -->
      <div v-if="isLoading && posts.length === 0" class="space-y-6">
        <PostCardSkeleton v-for="i in 6" :key="i" />
      </div>
      
      <div v-else-if="posts.length > 0">
        <!-- Сетка постов -->
        <div
          v-if="viewMode === 'grid'"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8"
        >
          <PostCard
            v-for="post in posts"
            :key="post.id"
            :post="post"
          />
        </div>
        
        <!-- Список постов -->
        <div
          v-else
          class="space-y-4 mb-8"
        >
          <PostListItem
            v-for="post in posts"
            :key="post.id"
            :post="post"
          />
        </div>

        <!-- Пагинация -->
        <PaginationComponent
          :current-page="pagination.currentPage"
          :total-pages="totalPages"
          :has-next="hasNextPage"
          :has-previous="hasPreviousPage"
          @page-change="goToPage"
        />
      </div>
      
      <!-- Пустое состояние -->
      <div v-else class="text-center py-16">
        <DocumentTextIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Статьи не найдены</h3>
        <p class="text-sm text-gray-500 mb-6">
          {{ searchQuery || selectedCategory ? 'Попробуйте изменить параметры поиска' : 'Пока нет опубликованных статей' }}
        </p>
        <div v-if="authStore.isAuthenticated" class="flex justify-center">
          <router-link
            to="/posts/create"
            class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
          >
            Создать первую статью
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import PostCard from '@/components/posts/PostCard.vue'
import PostListItem from '@/components/posts/PostListItem.vue'
import PostCardSkeleton from '@/components/ui/PostCardSkeleton.vue'
import PaginationComponent from '@/components/ui/PaginationComponent.vue'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  Squares2X2Icon,
  ListBulletIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'PostsView',
  components: {
    PostCard,
    PostListItem,
    PostCardSkeleton,
    PaginationComponent,
    PlusIcon,
    MagnifyingGlassIcon,
    Squares2X2Icon,
    ListBulletIcon,
    DocumentTextIcon
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const postsStore = usePostsStore()
    
    const viewMode = ref('grid')
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const selectedOrdering = ref('-created_at')
    
    const posts = computed(() => postsStore.posts)
    const categories = computed(() => postsStore.categories)
    const pagination = computed(() => postsStore.pagination)
    const isLoading = computed(() => postsStore.isLoading)
    const hasNextPage = computed(() => postsStore.hasNextPage)
    const hasPreviousPage = computed(() => postsStore.hasPreviousPage)
    const totalPages = computed(() => postsStore.totalPages)
    
    const initializeFromQuery = () => {
      searchQuery.value = route.query.search || ''
      selectedCategory.value = route.query.category || ''
      selectedOrdering.value = route.query.ordering || '-created_at'
    }
    
    const updateQueryParams = () => {
      const query = {}
      if (searchQuery.value) query.search = searchQuery.value
      if (selectedCategory.value) query.category = selectedCategory.value
      if (selectedOrdering.value && selectedOrdering.value !== '-created_at') {
        query.ordering = selectedOrdering.value
      }
      if (pagination.value.currentPage > 1) {
        query.page = pagination.value.currentPage
      }
      
      router.replace({ query })
    }
    
    const loadPosts = async () => {
      const params = {
        search: searchQuery.value,
        category: selectedCategory.value,
        ordering: selectedOrdering.value,
        page: route.query.page || 1
      }
      
      await postsStore.fetchPosts(params)
      updateQueryParams()
    }
    
    const applyFilters = async () => {
      await loadPosts()
    }
    
    const clearFilters = async () => {
      searchQuery.value = ''
      selectedCategory.value = ''
      selectedOrdering.value = '-created_at'
      await loadPosts()
    }
    
    const goToPage = async (page) => {
      await postsStore.goToPage(page)
      updateQueryParams()
    }
    
    const pluralize = (count, one, few, many) => {
      const mod10 = count % 10
      const mod100 = count % 100
      
      if (mod100 >= 11 && mod100 <= 19) {
        return many
      }
      if (mod10 === 1) {
        return one
      }
      if (mod10 >= 2 && mod10 <= 4) {
        return few
      }
      return many
    }
    
    // Загружаем данные при монтировании
    onMounted(async () => {
      initializeFromQuery()
      await Promise.all([
        postsStore.fetchCategories(),
        loadPosts()
      ])
    })
    
    // Отслеживаем изменения в URL
    watch(() => route.query, () => {
      if (route.name === 'Posts') {
        initializeFromQuery()
        loadPosts()
      }
    })
    
    return {
      authStore,
      postsStore,
      viewMode,
      searchQuery,
      selectedCategory,
      selectedOrdering,
      posts,
      categories,
      pagination,
      isLoading,
      hasNextPage,
      hasPreviousPage,
      totalPages,
      applyFilters,
      clearFilters,
      goToPage,
      pluralize
    }
  }
}
</script>