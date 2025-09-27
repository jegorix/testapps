import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Импортируем модули маршрутов
import authRoutes from './modules/auth'
import postRoutes from './modules/posts'
import categoryRoutes from './modules/categories'
import commentRoutes from './modules/comments'
import subscriptionRoutes from './modules/subscription'

// Lazy loading основных компонентов
const Home = () => import('@/views/HomeView.vue')
const NotFound = () => import('@/views/NotFoundView.vue')

// Основные маршруты
const baseRoutes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Главная'
    }
  },
  
  // 404 - должен быть последним
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: 'Страница не найдена'
    }
  }
]

// Объединяем все маршруты
const routes = [
  ...baseRoutes.slice(0, -1), // Все базовые маршруты кроме 404
  ...authRoutes,
  ...postRoutes,
  ...categoryRoutes,
  ...commentRoutes,
  ...subscriptionRoutes,
  ...baseRoutes.slice(-1) // 404 маршрут в конце
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Инициализируем аутентификацию при первом переходе
  if (!authStore.isInitialized) {
    try {
      await authStore.initializeAuth()
    } catch (error) {
      console.error('Ошибка инициализации аутентификации:', error)
    }
  }
  
  // Обновляем заголовок страницы
  document.title = to.meta.title ? `${to.meta.title} | News Site` : 'News Site'
  
  // Проверяем требования аутентификации
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({
      name: 'Login',
      query: { redirect: to.fullPath }
    })
    return
  }
  
  // Проверяем требования гостевого доступа
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'Home' })
    return
  }
  
  next()
})

router.afterEach((to, from) => {
  // Можно добавить аналитику или другие действия после навигации
  if (process.env.NODE_ENV === 'development') {
    console.log(`Navigated from ${from.path} to ${to.path}`)
  }
})

// Обработчик ошибок роутера
router.onError((error) => {
  console.error('Router error:', error)
  
  // Если ошибка связана с отсутствующим параметром, перенаправляем на 404
  if (error.message.includes('Missing required param')) {
    router.push({ name: 'NotFound' })
  }
})

export default router