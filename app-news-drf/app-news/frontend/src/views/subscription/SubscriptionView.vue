<template>
    <div class="min-h-screen bg-gray-50 py-8">
      <div class="container-content max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Заголовок -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-4">Управление подпиской</h1>
          <p class="text-gray-600">
            Управляйте своей подпиской и получайте доступ к дополнительным возможностям
          </p>
        </div>
  
        <!-- Текущая подписка -->
        <div v-if="subscriptionStore.hasSubscription" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-gray-900">Текущая подписка</h2>
            <div class="flex items-center space-x-2">
              <div 
                class="w-3 h-3 rounded-full"
                :class="subscriptionStore.isActive ? 'bg-green-500' : 'bg-red-500'"
              ></div>
              <span 
                class="text-sm font-medium"
                :class="subscriptionStore.isActive ? 'text-green-700' : 'text-red-700'"
              >
                {{ subscriptionStore.isActive ? 'Активна' : 'Неактивна' }}
              </span>
            </div>
          </div>
  
          <div v-if="subscriptionStore.subscription" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Тарифный план</label>
                <p class="text-lg font-semibold text-gray-900">
                  {{ subscriptionStore.subscription.plan_info?.name || 'Неизвестный план' }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Статус</label>
                <p class="text-lg">
                  <span 
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                    :class="getStatusClasses(subscriptionStore.subscription.status)"
                  >
                    {{ getStatusText(subscriptionStore.subscription.status) }}
                  </span>
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Дата начала</label>
                <p class="text-lg text-gray-900">
                  {{ formatDate(subscriptionStore.subscription.start_date) }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Дата окончания</label>
                <p class="text-lg text-gray-900">
                  {{ formatDate(subscriptionStore.subscription.end_date) }}
                </p>
              </div>
            </div>
  
            <!-- Информация о закрепленном посте -->
            <div v-if="subscriptionStore.isActive" class="border-t border-gray-200 pt-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-3">Закрепленный пост</h3>
              <div v-if="subscriptionStore.pinnedPost" class="bg-blue-50 rounded-lg p-4">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h4 class="text-md font-medium text-blue-900 mb-1">
                      {{ subscriptionStore.pinnedPost.post_info?.title || 'Без названия' }}
                    </h4>
                    <p class="text-sm text-blue-700 mb-2">
                      {{ getPostExcerpt(subscriptionStore.pinnedPost.post_info?.content) }}
                    </p>
                    <p class="text-xs text-blue-600">
                      Закреплен: {{ formatDate(subscriptionStore.pinnedPost.pinned_at) }}
                    </p>
                  </div>
                  <button
                    @click="unpinPost"
                    :disabled="subscriptionStore.isSubmitting"
                    class="ml-4 text-red-600 hover:text-red-700 text-sm font-medium"
                  >
                    Открепить
                  </button>
                </div>
              </div>
              <div v-else class="text-center py-4 text-gray-500">
                <p>У вас нет закрепленных постов</p>
                <router-link to="/posts/my" class="text-blue-600 hover:text-blue-700 text-sm">
                  Перейти к моим постам
                </router-link>
              </div>
            </div>
  
            <!-- Действия с подпиской -->
            <div class="border-t border-gray-200 pt-4">
              <div class="flex flex-col sm:flex-row gap-3">
                <button
                  v-if="subscriptionStore.isActive"
                  @click="cancelSubscription"
                  :disabled="subscriptionStore.isSubmitting"
                  class="py-2 px-4 border border-red-300 rounded-md text-red-700 hover:bg-red-50 text-sm font-medium transition-colors disabled:opacity-50"
                >
                  {{ subscriptionStore.isSubmitting ? 'Отмена...' : 'Отменить подписку' }}
                </button>
                <router-link
                  to="/posts/my"
                  class="py-2 px-4 border border-blue-300 rounded-md text-blue-700 hover:bg-blue-50 text-sm font-medium transition-colors text-center"
                >
                  Управлять постами
                </router-link>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Доступные планы -->
        <div v-if="!subscriptionStore.hasSubscription || !subscriptionStore.isActive">
          <h2 class="text-2xl font-semibold text-gray-900 mb-6 text-center">
            {{ subscriptionStore.hasSubscription ? 'Продлить подписку' : 'Выберите план подписки' }}
          </h2>
  
          <!-- Загрузка планов -->
          <div v-if="subscriptionStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="i in 3" :key="i" class="animate-pulse">
              <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div class="h-6 bg-gray-200 rounded mb-4"></div>
                <div class="h-8 bg-gray-200 rounded mb-4"></div>
                <div class="space-y-2 mb-6">
                  <div class="h-4 bg-gray-200 rounded"></div>
                  <div class="h-4 bg-gray-200 rounded"></div>
                  <div class="h-4 bg-gray-200 rounded"></div>
                </div>
                <div class="h-10 bg-gray-200 rounded"></div>
              </div>
            </div>
          </div>
  
          <!-- Список планов -->
          <div v-else-if="subscriptionStore.plans.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="plan in subscriptionStore.plans"
              :key="plan.id"
              class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div class="text-center">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ plan.name }}</h3>
                <div class="mb-4">
                  <span class="text-3xl font-bold text-gray-900">${{ plan.price }}</span>
                  <span class="text-gray-500">/месяц</span>
                </div>
                
                <!-- Список возможностей -->
                <div class="mb-6">
                  <ul class="space-y-2 text-sm text-gray-600">
                    <li v-if="plan.features?.pin_posts" class="flex items-center justify-center">
                      <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
                      Закрепление постов
                    </li>
                    <li v-if="plan.features?.priority_support" class="flex items-center justify-center">
                      <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
                      Приоритетная поддержка
                    </li>
                    <li v-if="plan.features?.analytics" class="flex items-center justify-center">
                      <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
                      Аналитика постов
                    </li>
                    <li class="flex items-center justify-center">
                      <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
                      Создание постов
                    </li>
                    <li class="flex items-center justify-center">
                      <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
                      Комментарии
                    </li>
                  </ul>
                </div>
  
                <button
                  @click="selectPlan(plan)"
                  :disabled="subscriptionStore.isSubmitting"
                  class="w-full py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors disabled:opacity-50"
                >
                  {{ subscriptionStore.isSubmitting ? 'Обработка...' : 'Выбрать план' }}
                </button>
              </div>
            </div>
          </div>
  
          <!-- Нет доступных планов -->
          <div v-else class="text-center py-12">
            <CreditCardIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 mb-2">Планы недоступны</h3>
            <p class="text-gray-500">В данный момент нет доступных планов подписки</p>
          </div>
        </div>
  
        <!-- Информация о преимуществах -->
        <div class="mt-12 bg-blue-50 rounded-lg p-6">
          <h3 class="text-lg font-semibold text-blue-900 mb-4 text-center">
            Преимущества подписки
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="text-center">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                <StarIcon class="w-6 h-6 text-blue-600" />
              </div>
              <h4 class="font-medium text-blue-900 mb-2">Закрепление постов</h4>
              <p class="text-sm text-blue-700">
                Закрепляйте важные посты в топе ленты для большей видимости
              </p>
            </div>
            <div class="text-center">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                <ChartBarIcon class="w-6 h-6 text-blue-600" />
              </div>
              <h4 class="font-medium text-blue-900 mb-2">Аналитика</h4>
              <p class="text-sm text-blue-700">
                Получайте подробную статистику просмотров и взаимодействий
              </p>
            </div>
            <div class="text-center">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                <LifebuoyIcon class="w-6 h-6 text-blue-600" />
              </div>
              <h4 class="font-medium text-blue-900 mb-2">Поддержка</h4>
              <p class="text-sm text-blue-700">
                Приоритетная техническая поддержка и помощь
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useSubscriptionStore } from '@/stores/subscription'
  import { useToast } from 'vue-toastification'
  import {
    CheckIcon,
    CreditCardIcon,
    StarIcon,
    ChartBarIcon,
    LifebuoyIcon
  } from '@heroicons/vue/24/outline'
  
  export default {
    name: 'SubscriptionView',
    components: {
      CheckIcon,
      CreditCardIcon,
      StarIcon,
      ChartBarIcon,
      LifebuoyIcon
    },
    setup() {
      const router = useRouter()
      const subscriptionStore = useSubscriptionStore()
      const toast = useToast()
  
      const loadData = async () => {
        try {
          await Promise.all([
            subscriptionStore.fetchPlans(),
            subscriptionStore.fetchSubscriptionStatus()
          ])
        } catch (error) {
          console.error('Ошибка загрузки данных подписки:', error)
          toast.error('Ошибка загрузки данных')
        }
      }
  
      const selectPlan = async (plan) => {
        try {
          const checkoutData = await subscriptionStore.createCheckoutSession(plan.id)
          if (checkoutData?.checkout_url) {
            window.location.href = checkoutData.checkout_url
          }
        } catch (error) {
          console.error('Ошибка создания сессии оплаты:', error)
          toast.error('Ошибка при создании сессии оплаты')
        }
      }
  
      const cancelSubscription = async () => {
        if (!confirm('Вы уверены, что хотите отменить подписку?')) {
          return
        }
  
        try {
          await subscriptionStore.cancelSubscription()
          toast.success('Подписка отменена')
        } catch (error) {
          console.error('Ошибка отмены подписки:', error)
          toast.error('Ошибка при отмене подписки')
        }
      }
  
      const unpinPost = async () => {
        try {
          await subscriptionStore.unpinPost()
          toast.success('Пост откреплен')
        } catch (error) {
          console.error('Ошибка при открепления поста:', error)
          toast.error('Ошибка при открепления поста')
        }
      }
  
      const formatDate = (dateString) => {
        if (!dateString) return 'Не указано'
        
        try {
          const date = new Date(dateString)
          return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
          })
        } catch (error) {
          return 'Некорректная дата'
        }
      }
  
      const getStatusClasses = (status) => {
        const classes = {
          'active': 'bg-green-100 text-green-800',
          'expired': 'bg-red-100 text-red-800',
          'cancelled': 'bg-yellow-100 text-yellow-800',
          'pending': 'bg-blue-100 text-blue-800'
        }
        return classes[status] || 'bg-gray-100 text-gray-800'
      }
  
      const getStatusText = (status) => {
        const texts = {
          'active': 'Активна',
          'expired': 'Истекла',
          'cancelled': 'Отменена',
          'pending': 'Ожидает'
        }
        return texts[status] || 'Неизвестно'
      }
  
      const getPostExcerpt = (content) => {
        if (!content) return 'Нет описания'
        return content.length > 100 ? content.substring(0, 100) + '...' : content
      }
  
      onMounted(() => {
        loadData()
      })
  
      return {
        subscriptionStore,
        selectPlan,
        cancelSubscription,
        unpinPost,
        formatDate,
        getStatusClasses,
        getStatusText,
        getPostExcerpt
      }
    }
  }
  </script>