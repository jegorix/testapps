<!-- frontend/src/views/subscription/PaymentSuccessView.vue -->
<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="max-w-md w-full bg-white rounded-lg shadow p-8 text-center">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckIcon class="w-8 h-8 text-green-600" />
        </div>
        <h1 class="text-2xl font-semibold text-gray-900 mb-2">Оплата успешна!</h1>
        <p class="text-gray-600 mb-6">Ваша подписка активирована</p>
        
        <div class="space-y-3">
          <router-link
            to="/subscription"
            class="btn btn-primary w-full"
          >
            Управление подпиской
          </router-link>
          <router-link
            to="/posts/my"
            class="btn btn-outline w-full"
          >
            Мои посты
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { CheckIcon } from '@heroicons/vue/24/outline'
  import { useSubscriptionStore } from '@/stores/subscription'
  import { onMounted } from 'vue'
  
  export default {
    name: 'PaymentSuccessView',
    components: { CheckIcon },
    setup() {
      const subscriptionStore = useSubscriptionStore()
  
      onMounted(() => {
        // Обновляем статус подписки после успешной оплаты
        subscriptionStore.fetchSubscriptionStatus()
      })
  
      return {
        subscriptionStore
      }
    }
  }
  </script>
  
