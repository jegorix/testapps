<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Заголовок -->
      <div class="text-center">
        <div class="mx-auto h-10 w-10 bg-blue-50 rounded-md flex items-center justify-center">
          <LockClosedIcon class="h-5 w-5 text-blue-600" />
        </div>
        <h2 class="mt-6 text-2xl font-semibold text-gray-900">
          Вход в аккаунт
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Или
          <router-link
            to="/register"
            class="font-medium text-blue-600 hover:text-blue-700"
          >
            создайте новый аккаунт
          </router-link>
        </p>
      </div>

      <!-- Форма входа -->
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email адрес
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <EnvelopeIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="email"
                v-model="form.email"
                type="email"
                name="email"
                autocomplete="email"
                required
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.email }"
                placeholder="your@email.com"
              />
            </div>
            <div v-if="errors.email" class="mt-1 text-xs text-red-600">
              {{ errors.email }}
            </div>
          </div>

          <!-- Пароль -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Пароль
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockClosedIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                autocomplete="current-password"
                required
                class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': errors.password }"
                placeholder="Введите пароль"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
                <EyeSlashIcon v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
              </button>
            </div>
            <div v-if="errors.password" class="mt-1 text-xs text-red-600">
              {{ errors.password }}
            </div>
          </div>
        </div>

        <!-- Дополнительные опции -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              v-model="form.rememberMe"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-600">
              Запомнить меня
            </label>
          </div>

          <div class="text-sm">
            <a
              href="#"
              class="font-medium text-blue-600 hover:text-blue-700"
              @click.prevent="showForgotPassword = true"
            >
              Забыли пароль?
            </a>
          </div>
        </div>

        <!-- Общие ошибки -->
        <div v-if="errors.general" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
          {{ errors.general }}
        </div>

        <!-- Кнопка входа -->
        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
            :class="{ 'opacity-50 cursor-not-allowed': authStore.isLoading }"
          >
            <div v-if="authStore.isLoading" class="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
            {{ authStore.isLoading ? 'Вход...' : 'Войти' }}
          </button>
        </div>

        <!-- Разделитель -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-gray-50 text-gray-500">Или войдите через</span>
          </div>
        </div>

        <!-- Социальные кнопки -->
        <div class="grid grid-cols-2 gap-3">
          <button
            type="button"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            @click="handleSocialLogin('google')"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Google
          </button>
          
          <button
            type="button"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
            @click="handleSocialLogin('github')"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.236 1.911 1.236 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </button>
        </div>
      </form>

      <!-- Модальное окно восстановления пароля -->
      <teleport to="body">
        <div
          v-if="showForgotPassword"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          @click.self="showForgotPassword = false"
        >
          <div class="bg-white rounded-md p-6 w-full max-w-md">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">
              Восстановление пароля
            </h3>
            <p class="text-gray-600 mb-4 text-sm">
              Введите ваш email адрес и мы отправим инструкции по восстановлению пароля.
            </p>
            <form @submit.prevent="handleForgotPassword">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700">Email адрес</label>
                <input
                  v-model="forgotPasswordEmail"
                  type="email"
                  required
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                  placeholder="your@email.com"
                />
              </div>
              <div class="flex gap-3">
                <button
                  type="button"
                  @click="showForgotPassword = false"
                  class="flex-1 py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
                >
                  Отмена
                </button>
                <button
                  type="submit"
                  class="flex-1 py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
                >
                  Отправить
                </button>
              </div>
            </form>
          </div>
        </div>
      </teleport>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import {
  LockClosedIcon,
  EnvelopeIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'LoginView',
  components: {
    LockClosedIcon,
    EnvelopeIcon,
    EyeIcon,
    EyeSlashIcon
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const toast = useToast()
    
    const showPassword = ref(false)
    const showForgotPassword = ref(false)
    const forgotPasswordEmail = ref('')
    
    const form = reactive({
      email: '',
      password: '',
      rememberMe: false
    })
    
    const errors = ref({})
    
    const validateForm = () => {
      const newErrors = {}
      
      if (!form.email) {
        newErrors.email = 'Email обязателен'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        newErrors.email = 'Некорректный email адрес'
      }
      
      if (!form.password) {
        newErrors.password = 'Пароль обязателен'
      } else if (form.password.length < 6) {
        newErrors.password = 'Пароль должен содержать минимум 6 символов'
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    const handleSubmit = async () => {
      errors.value = {}
      
      if (!validateForm()) {
        return
      }
      
      try {
        await authStore.login({
          email: form.email,
          password: form.password
        })
        
        toast.success('Добро пожаловать!')
        
        // Перенаправляем на страницу, с которой пришел пользователь, или на главную
        const redirectPath = route.query.redirect || '/'
        router.push(redirectPath)
        
      } catch (error) {
        console.error('Ошибка входа:', error)
        
        if (error.response?.status === 400) {
          const data = error.response.data
          if (data.non_field_errors) {
            errors.value.general = data.non_field_errors[0]
          } else {
            // Обрабатываем ошибки полей
            Object.keys(data).forEach(key => {
              if (Array.isArray(data[key])) {
                errors.value[key] = data[key][0]
              }
            })
          }
        } else {
          errors.value.general = 'Произошла ошибка при входе. Попробуйте позже.'
        }
      }
    }
    
    const handleSocialLogin = (provider) => {
      // Заглушка для социальной авторизации
      toast.info(`Авторизация через ${provider} будет доступна в ближайшее время`)
    }
    
    const handleForgotPassword = () => {
      if (!forgotPasswordEmail.value) {
        toast.error('Введите email адрес')
        return
      }
      
      // Заглушка для восстановления пароля
      toast.success('Инструкции по восстановлению пароля отправлены на ваш email')
      showForgotPassword.value = false
      forgotPasswordEmail.value = ''
    }
    
    return {
      authStore,
      form,
      errors,
      showPassword,
      showForgotPassword,
      forgotPasswordEmail,
      handleSubmit,
      handleSocialLogin,
      handleForgotPassword
    }
  }
}
</script>