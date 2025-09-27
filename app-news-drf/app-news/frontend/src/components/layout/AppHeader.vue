<template>
  <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
    <div class="container-content max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Логотип и навигация -->
        <div class="flex items-center space-x-8">
          <!-- Логотип -->
          <router-link
            to="/"
            class="flex items-center space-x-2 text-lg font-semibold text-gray-900 hover:text-blue-600 transition-colors"
          >
            <div class="w-8 h-8 bg-blue-50 rounded-md flex items-center justify-center">
              <NewspaperIcon class="w-5 h-5 text-blue-600" />
            </div>
            <span>News Site</span>
          </router-link>
          
          <!-- Главная навигация -->
          <nav class="hidden md:flex items-center space-x-6">
            <router-link
              to="/"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
              :class="{ 'text-blue-600': $route.name === 'Home' }"
            >
              Главная
            </router-link>
            <router-link
              to="/posts"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
              :class="{ 'text-blue-600': $route.name === 'Posts' }"
            >
              Все посты
            </router-link>
            <router-link
              to="/categories"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors"
              :class="{ 'text-blue-600': $route.name === 'Categories' }"
            >
              Категории
            </router-link>
          </nav>
        </div>
        
        <!-- Поиск -->
        <div class="hidden lg:flex flex-1 max-w-lg mx-8">
          <div class="relative w-full">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Поиск постов..."
              class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
              @keyup.enter="handleSearch"
            />
            <button
              v-if="searchQuery"
              @click="clearSearch"
              class="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <XMarkIcon class="h-5 w-5 text-gray-400 hover:text-gray-600" />
            </button>
          </div>
        </div>
        
        <!-- Пользовательское меню -->
        <div class="flex items-center space-x-4">
          <!-- Мобильный поиск -->
          <button
            @click="showMobileSearch = !showMobileSearch"
            class="lg:hidden p-2 text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-50 transition-colors"
          >
            <MagnifyingGlassIcon class="w-5 h-5" />
          </button>
          
          <!-- Уведомления (заглушка) -->
          <button
            v-if="authStore.isAuthenticated"
            class="relative p-2 text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-50 transition-colors"
          >
            <BellIcon class="w-5 h-5" />
            <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          
          <!-- Меню пользователя -->
          <div v-if="authStore.isAuthenticated" class="relative">
            <button
              @click.stop="toggleUserMenu"
              class="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                {{ authStore.userInitials }}
              </div>
              <span class="hidden sm:block text-sm font-medium text-gray-700">
                {{ authStore.userFullName }}
              </span>
              <ChevronDownIcon 
                class="w-4 h-4 text-gray-400 transition-transform duration-200"
                :class="{ 'rotate-180': showUserMenu }"
              />
            </button>
            
            <!-- Выпадающее меню -->
            <transition name="dropdown">
              <div
                v-if="showUserMenu"
                v-click-outside="closeUserMenu"
                class="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50"
              >
                <!-- Информация о пользователе -->
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ authStore.userFullName }}</p>
                  <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
                </div>
                
                <!-- Статус подписки -->
                <div class="px-4 py-2 border-b border-gray-100">
                  <div v-if="subscriptionStore.isActive" class="flex items-center text-sm">
                    <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    <span class="text-green-700">Подписка активна</span>
                  </div>
                  <div v-else class="flex items-center text-sm">
                    <div class="w-2 h-2 bg-gray-400 rounded-full mr-2"></div>
                    <span class="text-gray-500">Нет подписки</span>
                  </div>
                </div>
                
                <!-- Ссылки меню -->
                <router-link
                  to="/profile"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                  @click="closeUserMenu"
                >
                  <UserIcon class="w-4 h-4 mr-3" />
                  Профиль
                </router-link>
                
                <router-link
                  to="/subscription"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                  @click="closeUserMenu"
                >
                  <CreditCardIcon class="w-4 h-4 mr-3" />
                  Подписка
                  <span v-if="subscriptionStore.isActive" class="ml-auto">
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                      Активна
                    </span>
                  </span>
                </router-link>
                
                <router-link
                  to="/posts/my"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                  @click="closeUserMenu"
                >
                  <DocumentTextIcon class="w-4 h-4 mr-3" />
                  Мои посты
                </router-link>
                
                <router-link
                  to="/comments/my"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                  @click="closeUserMenu"
                >
                  <ChatBubbleLeftIcon class="w-4 h-4 mr-3" />
                  Мои комментарии
                </router-link>
                
                <router-link
                  to="/posts/create"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                  @click="closeUserMenu"
                >
                  <PlusIcon class="w-4 h-4 mr-3" />
                  Создать пост
                </router-link>
                
                <div class="border-t border-gray-100 my-1"></div>
                
                <router-link
                  to="/change-password"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                  @click="closeUserMenu"
                >
                  <KeyIcon class="w-4 h-4 mr-3" />
                  Сменить пароль
                </router-link>
                
                <button
                  @click="handleLogout"
                  class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 hover:text-red-700 transition-colors"
                >
                  <ArrowRightOnRectangleIcon class="w-4 h-4 mr-3" />
                  Выйти
                </button>
              </div>
            </transition>
          </div>
          
          <!-- Кнопки входа/регистрации -->
          <div v-else class="flex items-center space-x-3">
            <router-link
              to="/login"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            >
              Войти
            </router-link>
            <router-link
              to="/register"
              class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 text-sm font-medium transition-colors"
            >
              Регистрация
            </router-link>
          </div>
          
          <!-- Мобильное меню -->
          <button
            @click="showMobileMenu = !showMobileMenu"
            class="md:hidden p-2 text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-50 transition-colors"
          >
            <Bars3Icon v-if="!showMobileMenu" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
      
      <!-- Мобильный поиск -->
      <transition name="slide-down">
        <div v-if="showMobileSearch" class="lg:hidden py-4 border-t border-gray-200">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Поиск постов..."
              class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
              @keyup.enter="handleSearch"
            />
          </div>
        </div>
      </transition>
      
      <!-- Мобильная навигация -->
      <transition name="slide-down">
        <div v-if="showMobileMenu" class="md:hidden py-4 border-t border-gray-200">
          <nav class="flex flex-col space-y-2">
            <router-link
              to="/"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors"
              :class="{ 'text-blue-600 bg-blue-50': $route.name === 'Home' }"
              @click="showMobileMenu = false"
            >
              Главная
            </router-link>
            <router-link
              to="/posts"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors"
              :class="{ 'text-blue-600 bg-blue-50': $route.name === 'Posts' }"
              @click="showMobileMenu = false"
            >
              Все посты
            </router-link>
            <router-link
              to="/categories"
              class="text-sm font-medium text-gray-600 hover:text-blue-600 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors"
              :class="{ 'text-blue-600 bg-blue-50': $route.name === 'Categories' }"
              @click="showMobileMenu = false"
            >
              Категории
            </router-link>
            
            <!-- Мобильные ссылки для авторизованных пользователей -->
            <div v-if="authStore.isAuthenticated" class="border-t border-gray-200 pt-2 mt-2">
              <router-link
                to="/profile"
                class="text-sm font-medium text-gray-600 hover:text-blue-600 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors flex items-center"
                @click="showMobileMenu = false"
              >
                <UserIcon class="w-4 h-4 mr-2" />
                Профиль
              </router-link>
              <router-link
                to="/posts/create"
                class="text-sm font-medium text-gray-600 hover:text-blue-600 py-2 px-4 rounded-md hover:bg-gray-50 transition-colors flex items-center"
                @click="showMobileMenu = false"
              >
                <PlusIcon class="w-4 h-4 mr-2" />
                Создать пост
              </router-link>
            </div>
          </nav>
        </div>
      </transition>
    </div>
  </header>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSubscriptionStore } from '@/stores/subscription'
import { useToast } from 'vue-toastification'
import {
  NewspaperIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  BellIcon,
  UserIcon,
  DocumentTextIcon,
  ChatBubbleLeftIcon,
  PlusIcon,
  KeyIcon,
  ArrowRightOnRectangleIcon,
  ChevronDownIcon,
  Bars3Icon,
  CreditCardIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'AppHeader',
  components: {
    NewspaperIcon,
    MagnifyingGlassIcon,
    XMarkIcon,
    BellIcon,
    UserIcon,
    DocumentTextIcon,
    ChatBubbleLeftIcon,
    PlusIcon,
    KeyIcon,
    ArrowRightOnRectangleIcon,
    ChevronDownIcon,
    Bars3Icon,
    CreditCardIcon
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const subscriptionStore = useSubscriptionStore()
    const toast = useToast()
    
    const searchQuery = ref('')
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const showMobileSearch = ref(false)
    
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
      console.log('User menu toggled:', showUserMenu.value) // Для отладки
    }
    
    const closeUserMenu = () => {
      showUserMenu.value = false
    }
    
    const handleSearch = () => {
      if (searchQuery.value.trim()) {
        router.push({
          name: 'Posts',
          query: { search: searchQuery.value.trim() }
        })
        showMobileSearch.value = false
      }
    }
    
    const clearSearch = () => {
      searchQuery.value = ''
    }
    
    const handleLogout = async () => {
      try {
        await authStore.logout()
        closeUserMenu()
        toast.success('Вы успешно вышли из системы')
        router.push({ name: 'Home' })
      } catch (error) {
        console.error('Ошибка при выходе:', error)
        toast.error('Произошла ошибка при выходе')
      }
    }
    
    // Загружаем статус подписки при монтировании
    onMounted(async () => {
      if (authStore.isAuthenticated) {
        try {
          await subscriptionStore.fetchSubscriptionStatus()
        } catch (error) {
          console.error('Ошибка загрузки статуса подписки:', error)
        }
      }
    })
    
    return {
      authStore,
      subscriptionStore,
      searchQuery,
      showUserMenu,
      showMobileMenu,
      showMobileSearch,
      toggleUserMenu,
      closeUserMenu,
      handleSearch,
      clearSearch,
      handleLogout
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
/* Анимации для выпадающих меню */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
  transform-origin: top right;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.dropdown-enter-to,
.dropdown-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Анимации для мобильных меню */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
  max-height: 200px;
  overflow: hidden;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-10px);
}

.slide-down-enter-to,
.slide-down-leave-from {
  opacity: 1;
  max-height: 200px;
  transform: translateY(0);
}

/* Анимация поворота стрелки */
.rotate-180 {
  transform: rotate(180deg);
}

/* Дополнительные стили для улучшения UX */
.relative button:focus {
  outline: none;
}

.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Hover эффекты */
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}

.hover\:bg-red-50:hover {
  background-color: #fef2f2;
}

.hover\:text-blue-600:hover {
  color: #2563eb;
}

.hover\:text-red-700:hover {
  color: #b91c1c;
}

/* Фокус стили */
.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.focus\:ring-blue-500:focus {
  --tw-ring-color: rgba(59, 130, 246, 0.5);
}
</style>