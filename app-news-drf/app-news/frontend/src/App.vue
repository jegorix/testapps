<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Навигация -->
    <AppHeader />
    
    <!-- Основной контент -->
    <main class="min-h-screen">
      <router-view v-slot="{ Component, route }">
        <transition
          :name="getTransitionName(route)"
          mode="out-in"
          appear
        >
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>
    
    <!-- Футер -->
    <AppFooter />
    
    <!-- Loading overlay -->
    <div
      v-if="isGlobalLoading"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 flex items-center space-x-3">
        <div class="loading-spinner"></div>
        <span class="text-gray-600">Загрузка...</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useSubscriptionStore } from '@/stores/subscription' // Добавить
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
  },
  setup() {
    const authStore = useAuthStore()
    const subscriptionStore = useSubscriptionStore() // Добавить
    const isInitializing = ref(true)
    
    const isGlobalLoading = computed(() => {
      return isInitializing.value && !authStore.isInitialized
    })
    
    const getTransitionName = (route) => {
      if (route.meta?.transition) {
        return route.meta.transition
      }
      
      if (route.name === 'PostDetail') {
        return 'slide-up'
      }
      
      if (route.name === 'Login' || route.name === 'Register') {
        return 'fade'
      }
      
      return 'fade'
    }
    
    onMounted(async () => {
      try {
        await authStore.initializeAuth()
        
        // Если пользователь авторизован, загружаем статус подписки
        if (authStore.isAuthenticated) {
          subscriptionStore.fetchSubscriptionStatus()
        }
      } catch (error) {
        console.error('Ошибка инициализации приложения:', error)
      } finally {
        isInitializing.value = false
      }
    })
    
    return {
      isGlobalLoading,
      getTransitionName
    }
  }
}
</script>

<style scoped>
/* Переходы между страницами */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active {
  transition: all 0.3s ease-out;
}

.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
}

.slide-right-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.slide-right-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}
</style>