import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { postsAPI, categoriesAPI } from '@/services/api'

export const usePostsStore = defineStore('posts', () => {
  // Состояние
  const posts = ref([])
  const currentPost = ref(null)
  const categories = ref([])
  const popularPosts = ref([])
  const recentPosts = ref([])
  const myPosts = ref([])
  
  // Пагинация
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
    pageSize: 20
  })
  
  // Фильтры и поиск
  const filters = ref({
    search: '',
    category: null,
    author: null,
    status: 'published',
    ordering: '-created_at'
  })
  
  // Состояния загрузки
  const isLoading = ref(false)
  const isLoadingPost = ref(false)
  const isLoadingCategories = ref(false)
  const isSubmitting = ref(false)

  // Вычисляемые свойства
  const publishedPosts = computed(() => 
    posts.value.filter(post => post.status === 'published')
  )
  
  const draftPosts = computed(() => 
    posts.value.filter(post => post.status === 'draft')
  )
  
  const hasNextPage = computed(() => !!pagination.value.next)
  const hasPreviousPage = computed(() => !!pagination.value.previous)
  
  const totalPages = computed(() => 
    Math.ceil(pagination.value.count / pagination.value.pageSize)
  )

  // Действия для постов
  const fetchPosts = async (params = {}) => {
    isLoading.value = true
    try {
      const queryParams = {
        ...filters.value,
        ...params,
        page: params.page || pagination.value.currentPage,
        page_size: params.page_size || pagination.value.pageSize
      }
      
      // Удаляем пустые параметры
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await postsAPI.getAll(queryParams)
      const data = response.data
      
      posts.value = data.results || []
      pagination.value = {
        count: data.count || 0,
        next: data.next,
        previous: data.previous,
        currentPage: params.page || pagination.value.currentPage,
        pageSize: params.page_size || pagination.value.pageSize
      }
      
      return data
    } catch (error) {
      console.error('Ошибка загрузки постов:', error)
      posts.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchPostBySlug = async (slug) => {
    isLoadingPost.value = true
    try {
      const response = await postsAPI.getById(slug)
      currentPost.value = response.data
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки поста:', error)
      currentPost.value = null
      throw error
    } finally {
      isLoadingPost.value = false
    }
  }

  const createPost = async (postData) => {
    isSubmitting.value = true
    try {
      // Определяем тип данных и настройки запроса
      const isFormData = postData instanceof FormData
      const config = isFormData ? {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      } : {}
      
      const response = await postsAPI.create(postData, config)
      const newPost = response.data
      
      // Добавляем новый пост в начало списка
      posts.value.unshift(newPost)
      pagination.value.count += 1
      
      return newPost
    } catch (error) {
      console.error('Ошибка создания поста:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const updatePost = async (slug, postData) => {
    isSubmitting.value = true
    try {
      const response = await postsAPI.update(slug, postData)
      const updatedPost = response.data
      
      // Обновляем пост в списке
      const index = posts.value.findIndex(post => post.slug === slug)
      if (index !== -1) {
        posts.value[index] = updatedPost
      }
      
      // Обновляем текущий пост
      if (currentPost.value && currentPost.value.slug === slug) {
        currentPost.value = updatedPost
      }
      
      return updatedPost
    } catch (error) {
      console.error('Ошибка обновления поста:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const updatePostPartial = async (slug, postData) => {
    isSubmitting.value = true
    try {
      const response = await postsAPI.updatePartial(slug, postData)
      const updatedPost = response.data
      
      // Обновляем пост в списке
      const index = posts.value.findIndex(post => post.slug === slug)
      if (index !== -1) {
        posts.value[index] = updatedPost
      }
      
      // Обновляем текущий пост
      if (currentPost.value && currentPost.value.slug === slug) {
        currentPost.value = updatedPost
      }
      
      return updatedPost
    } catch (error) {
      console.error('Ошибка обновления поста:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const deletePost = async (slug) => {
    isSubmitting.value = true
    try {
      await postsAPI.delete(slug)
      
      // Удаляем пост из списка
      const index = posts.value.findIndex(post => post.slug === slug)
      if (index !== -1) {
        posts.value.splice(index, 1)
        pagination.value.count -= 1
      }
      
      // Очищаем текущий пост
      if (currentPost.value && currentPost.value.slug === slug) {
        currentPost.value = null
      }
      
      return true
    } catch (error) {
      console.error('Ошибка удаления поста:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const fetchMyPosts = async (params = {}) => {
    isLoading.value = true
    try {
      const response = await postsAPI.getMyPosts(params)
      myPosts.value = response.data.results || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки моих постов:', error)
      myPosts.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchPopularPosts = async () => {
    try {
      const response = await postsAPI.getPopular()
      popularPosts.value = response.data || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки популярных постов:', error)
      popularPosts.value = []
      throw error
    }
  }

  const fetchRecentPosts = async () => {
    try {
      const response = await postsAPI.getRecent()
      recentPosts.value = response.data || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки последних постов:', error)
      recentPosts.value = []
      throw error
    }
  }

  // Действия для категорий
  const fetchCategories = async (params = {}) => {
    isLoadingCategories.value = true
    try {
      const response = await categoriesAPI.getAll(params)
      categories.value = response.data.results || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки категорий:', error)
      categories.value = []
      throw error
    } finally {
      isLoadingCategories.value = false
    }
  }

  const createCategory = async (categoryData) => {
    isSubmitting.value = true
    try {
      const response = await categoriesAPI.create(categoryData)
      const newCategory = response.data
      
      categories.value.unshift(newCategory)
      return newCategory
    } catch (error) {
      console.error('Ошибка создания категории:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const fetchPostsByCategory = async (categorySlug, params = {}) => {
    isLoading.value = true
    try {
      const response = await categoriesAPI.getPosts(categorySlug, params)
      posts.value = response.data.posts || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки постов категории:', error)
      posts.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // Утилиты для фильтрации и поиска
  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.currentPage = 1 // Сбрасываем на первую страницу
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      category: null,
      author: null,
      status: 'published',
      ordering: '-created_at'
    }
    pagination.value.currentPage = 1
  }

  const searchPosts = async (searchQuery) => {
    setFilters({ search: searchQuery })
    return await fetchPosts()
  }

  const filterByCategory = async (categoryId) => {
    setFilters({ category: categoryId })
    return await fetchPosts()
  }

  const sortPosts = async (ordering) => {
    setFilters({ ordering })
    return await fetchPosts()
  }

  // Пагинация
  const goToPage = async (page) => {
    if (page < 1 || page > totalPages.value) return
    
    pagination.value.currentPage = page
    return await fetchPosts({ page })
  }

  const nextPage = async () => {
    if (hasNextPage.value) {
      return await goToPage(pagination.value.currentPage + 1)
    }
  }

  const previousPage = async () => {
    if (hasPreviousPage.value) {
      return await goToPage(pagination.value.currentPage - 1)
    }
  }

  // Очистка состояния
  const clearPosts = () => {
    posts.value = []
    pagination.value = {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1,
      pageSize: 20
    }
  }

  const clearCurrentPost = () => {
    currentPost.value = null
  }

  // Получение поста из кэша
  const getPostFromCache = (slug) => {
    return posts.value.find(post => post.slug === slug) || null
  }

  // Получение категории по ID
  const getCategoryById = (id) => {
    return categories.value.find(category => category.id === id) || null
  }

  return {
    // Состояние
    posts,
    currentPost,
    categories,
    popularPosts,
    recentPosts,
    myPosts,
    pagination,
    filters,
    isLoading,
    isLoadingPost,
    isLoadingCategories,
    isSubmitting,
    
    // Вычисляемые свойства
    publishedPosts,
    draftPosts,
    hasNextPage,
    hasPreviousPage,
    totalPages,
    
    // Действия для постов
    fetchPosts,
    fetchPostBySlug,
    createPost,
    updatePost,
    updatePostPartial,
    deletePost,
    fetchMyPosts,
    fetchPopularPosts,
    fetchRecentPosts,
    
    // Действия для категорий
    fetchCategories,
    createCategory,
    fetchPostsByCategory,
    
    // Фильтрация и поиск
    setFilters,
    clearFilters,
    searchPosts,
    filterByCategory,
    sortPosts,
    
    // Пагинация
    goToPage,
    nextPage,
    previousPage,
    
    // Утилиты
    clearPosts,
    clearCurrentPost,
    getPostFromCache,
    getCategoryById
  }
})