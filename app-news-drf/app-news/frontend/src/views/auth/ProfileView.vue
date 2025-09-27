<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white rounded-md shadow-sm border border-gray-200">
        <!-- Заголовок -->
        <div class="p-6 border-b border-gray-200">
          <h1 class="text-2xl font-semibold text-gray-900">Мой профиль</h1>
        </div>
        
        <!-- Содержимое -->
        <div class="p-6">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Аватар -->
            <div class="flex items-center space-x-6">
              <div class="relative">
                <div v-if="previewAvatar" class="w-20 h-20 rounded-full overflow-hidden">
                  <img :src="previewAvatar" alt="Avatar" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center text-white text-xl font-medium">
                  {{ authStore.userInitials }}
                </div>
                <label class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-sm border border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors">
                  <CameraIcon class="w-4 h-4 text-gray-600" />
                  <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleAvatarChange"
                  />
                </label>
              </div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ authStore.userFullName || 'Пользователь' }}</h3>
                <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
              </div>
            </div>
            
            <!-- Поля формы -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700">Имя</label>
                <input
                  v-model="form.first_name"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                  placeholder="Ваше имя"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Фамилия</label>
                <input
                  v-model="form.last_name"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                  placeholder="Ваша фамилия"
                />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">О себе</label>
              <textarea
                v-model="form.bio"
                rows="4"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                placeholder="Расскажите о себе..."
              ></textarea>
            </div>
            
            <!-- Кнопки -->
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="resetForm"
                class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
              >
                Отмена
              </button>
              <button
                type="submit"
                :disabled="authStore.isLoading"
                class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
                :class="{ 'opacity-50 cursor-not-allowed': authStore.isLoading }"
              >
                <div v-if="authStore.isLoading" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Сохранить
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import { CameraIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'ProfileView',
  components: { CameraIcon },
  setup() {
    const authStore = useAuthStore()
    const toast = useToast()
    const previewAvatar = ref(null)
    const avatarFile = ref(null)
    
    const form = reactive({
      first_name: '',
      last_name: '',
      bio: ''
    })
    
    const initForm = () => {
      if (authStore.user) {
        form.first_name = authStore.user.first_name || ''
        form.last_name = authStore.user.last_name || ''
        form.bio = authStore.user.bio || ''
        previewAvatar.value = authStore.user.avatar || null
      }
    }
    
    const handleAvatarChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 10 * 1024 * 1024) {
          toast.error('Размер файла не должен превышать 10MB')
          return
        }
        if (!file.type.startsWith('image/')) {
          toast.error('Можно загружать только изображения')
          return
        }
        avatarFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
          previewAvatar.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const handleSubmit = async () => {
      try {
        const formData = new FormData()
        formData.append('first_name', form.first_name)
        formData.append('last_name', form.last_name)
        formData.append('bio', form.bio)
        
        if (avatarFile.value) {
          formData.append('avatar', avatarFile.value)
        }
        
        await authStore.updateProfile(formData)
        toast.success('Профиль успешно обновлен')
      } catch (error) {
        toast.error('Ошибка обновления профиля')
      }
    }
    
    const resetForm = () => {
      initForm()
      avatarFile.value = null
    }
    
    onMounted(() => {
      initForm()
    })
    
    return {
      authStore,
      form,
      previewAvatar,
      handleAvatarChange,
      handleSubmit,
      resetForm
    }
  }
}
</script>