  <!-- frontend/src/views/subscription/PaymentCancelView.vue -->
  <template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="max-w-md w-full bg-white rounded-lg shadow p-8 text-center">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <XMarkIcon class="w-8 h-8 text-red-600" />
        </div>
        <h1 class="text-2xl font-semibold text-gray-900 mb-2">Оплата отменена</h1>
        <p class="text-gray-600 mb-6">Вы можете попробовать еще раз</p>
        
        <div class="space-y-3">
          <router-link
            to="/subscription"
            class="btn btn-primary w-full"
          >
            Попробовать снова
          </router-link>
          <router-link
            to="/"
            class="btn btn-outline w-full"
          >
            На главную
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { XMarkIcon } from '@heroicons/vue/24/outline'
  
  export default {
    name: 'PaymentCancelView',
    components: { XMarkIcon }
  }
  </script>