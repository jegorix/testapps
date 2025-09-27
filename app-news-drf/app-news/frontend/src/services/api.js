import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'
import { useToast } from 'vue-toastification'

const toast = useToast()

// Базовая конфигурация API
const API_BASE_URL = 'http://localhost:8000'

// Создание экземпляра axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Интерцептор запросов - добавляем токен авторизации
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)


// Интерцептор ответов - обработка ошибок и обновление токена
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const authStore = useAuthStore()
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // Попытка обновить токен
      if (authStore.refreshToken) {
        try {
          await authStore.refreshAccessToken()
          originalRequest.headers.Authorization = `Bearer ${authStore.token}`
          return api(originalRequest)
        } catch (refreshError) {
          authStore.logout()
          router.push({ name: 'Login' })
          toast.error('Сессия истекла. Пожалуйста, войдите снова.')
          return Promise.reject(refreshError)
        }
      } else {
        authStore.logout()
        router.push({ name: 'Login' })
        toast.error('Необходима авторизация.')
      }
    }
    
    // Обработка других ошибок
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          if (data.detail) {
            toast.error(data.detail)
          } else if (typeof data === 'object') {
            // Показываем первую ошибку валидации
            const firstError = Object.values(data)[0]
            if (Array.isArray(firstError)) {
              toast.error(firstError[0])
            }
          }
          break
        case 403:
          toast.error('У вас нет прав для выполнения этого действия.')
          break
        case 404:
          toast.error('Запрашиваемый ресурс не найден.')
          break
        case 429:
          toast.error('Слишком много запросов. Попробуйте позже.')
          break
        case 500:
          toast.error('Внутренняя ошибка сервера. Попробуйте позже.')
          break
        default:
          toast.error('Произошла неожиданная ошибка.')
      }
    } else if (error.request) {
      toast.error('Не удается подключиться к серверу.')
    } else {
      toast.error('Произошла ошибка при отправке запроса.')
    }
    
    return Promise.reject(error)
  }
)

// API методы
export const authAPI = {
  register: (data) => api.post('/api/v1/auth/register/', data),
  login: (data) => api.post('/api/v1/auth/login/', data),
  logout: (data) => api.post('/api/v1/auth/logout/', data),
  refreshToken: (data) => api.post('/api/v1/auth/token/refresh/', data),
  getProfile: () => api.get('/api/v1/auth/profile/'),
  updateProfile: (data) => api.put('/api/v1/auth/profile/', data),
  updateProfilePartial: (data) => api.patch('/api/v1/auth/profile/', data),
  changePassword: (data) => api.put('/api/v1/auth/change-password/', data)
}

export const categoriesAPI = {
  getAll: (params) => api.get('/api/v1/posts/categories/', { params }),
  getById: (slug) => api.get(`/api/v1/posts/categories/${slug}/`),
  create: (data) => api.post('/api/v1/posts/categories/', data),
  update: (slug, data) => api.put(`/api/v1/posts/categories/${slug}/`, data),
  updatePartial: (slug, data) => api.patch(`/api/v1/posts/categories/${slug}/`, data),
  delete: (slug) => api.delete(`/api/v1/posts/categories/${slug}/`),
  getPosts: (slug, params) => api.get(`/api/v1/posts/categories/${slug}/posts/`, { params })
}

export const postsAPI = {
  getAll: (params) => api.get('/api/v1/posts/', { params }),
  getById: (slug) => api.get(`/api/v1/posts/${slug}/`),
  create: (data) => api.post('/api/v1/posts/', data),
  update: (slug, data) => api.put(`/api/v1/posts/${slug}/`, data),
  updatePartial: (slug, data) => api.patch(`/api/v1/posts/${slug}/`, data),
  delete: (slug) => api.delete(`/api/v1/posts/${slug}/`),
  getMyPosts: (params) => api.get('/api/v1/posts/my-posts/', { params }),
  getPopular: () => api.get('/api/v1/posts/popular/'),
  getRecent: () => api.get('/api/v1/posts/recent/')
}

export const subscriptionAPI = {
  getPlans: () => api.get('/api/v1/subscribe/plans/'),
  getStatus: () => api.get('/api/v1/subscribe/status/'),
  getMySubscription: () => api.get('/api/v1/subscribe/my-subscription/'),
  cancelSubscription: () => api.post('/api/v1/subscribe/cancel/'),
  
  // Pinned posts
  getPinnedPost: () => api.get('/api/v1/subscribe/pinned-post/'),
  pinPost: (data) => api.post('/api/v1/subscribe/pin-post/', data),
  unpinPost: () => api.post('/api/v1/subscribe/unpin-post/'),
  getPinnedPosts: () => api.get('/api/v1/subscribe/pinned-posts/'),
  canPinPost: (postId) => api.get(`/api/v1/subscribe/can-pin/${postId}/`)
}

export const paymentAPI = {
  createCheckoutSession: (data) => api.post('/api/v1/payment/create-checkout-session/', data),
  getPaymentStatus: (paymentId) => api.get(`/api/v1/payment/payments/${paymentId}/status/`),
  getPaymentHistory: () => api.get('/api/v1/payment/payments/history/'),
  cancelPayment: (paymentId) => api.post(`/api/v1/payment/payments/${paymentId}/cancel/`)
}

export const commentsAPI = {
  getAll: (params) => api.get('/api/v1/comments/', { params }),
  getById: (id) => api.get(`/api/v1/comments/${id}/`),
  create: (data, config = {}) => api.post('/api/v1/posts/', data, config),
  update: (id, data) => api.put(`/api/v1/comments/${id}/`, data),
  updatePartial: (id, data) => api.patch(`/api/v1/comments/${id}/`, data),
  delete: (id) => api.delete(`/api/v1/comments/${id}/`),
  getMyComments: (params) => api.get('/api/v1/comments/my-comments/', { params }),
  getPostComments: (postId) => api.get(`/api/v1/comments/post/${postId}/`),
  getCommentReplies: (commentId) => api.get(`/api/v1/comments/${commentId}/replies/`)
}

// Утилиты для загрузки файлов
export const uploadAPI = {
  uploadImage: (file, onProgress) => {
    const formData = new FormData()
    formData.append('image', file)
    
    return api.post('/api/v1/upload/image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      }
    })
  }
}

// Утилиты для работы с данными
export const apiUtils = {
  // Создание FormData для загрузки файлов
  createFormData: (data) => {
    const formData = new FormData()
    
    Object.keys(data).forEach(key => {
      const value = data[key]
      if (value !== null && value !== undefined) {
        if (value instanceof File) {
          formData.append(key, value)
        } else if (typeof value === 'object') {
          formData.append(key, JSON.stringify(value))
        } else {
          formData.append(key, value)
        }
      }
    })
    
    return formData
  },
  
  // Построение query параметров
  buildQueryParams: (params) => {
    const searchParams = new URLSearchParams()
    
    Object.keys(params).forEach(key => {
      const value = params[key]
      if (value !== null && value !== undefined && value !== '') {
        if (Array.isArray(value)) {
          value.forEach(item => searchParams.append(key, item))
        } else {
          searchParams.append(key, value)
        }
      }
    })
    
    return searchParams.toString()
  },
  
  // Безопасное извлечение данных из ответа
  extractData: (response, defaultValue = null) => {
    return response?.data || defaultValue
  },
  
  // Безопасное извлечение пагинации
  extractPagination: (response) => {
    const data = response?.data
    return {
      count: data?.count || 0,
      next: data?.next || null,
      previous: data?.previous || null,
      results: data?.results || []
    }
  }
}

export default api