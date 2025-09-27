<!-- src/views/auth/ChangePasswordView.vue -->
<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-narrow">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200">
        <div class="card-header">
          <h1 class="text-2xl font-bold text-gray-900">Смена пароля</h1>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label class="form-label">Текущий пароль</label>
              <input
                v-model="form.old_password"
                type="password"
                required
                class="form-input"
                :class="{ 'border-red-300': errors.old_password }"
              />
              <div v-if="errors.old_password" class="form-error">
                {{ errors.old_password }}
              </div>
            </div>
            
            <div>
              <label class="form-label">Новый пароль</label>
              <input
                v-model="form.new_password"
                type="password"
                required
                class="form-input"
                :class="{ 'border-red-300': errors.new_password }"
              />
              <div v-if="errors.new_password" class="form-error">
                {{ errors.new_password }}
              </div>
            </div>
            
            <div>
              <label class="form-label">Подтверждение нового пароля</label>
              <input
                v-model="form.new_password_confirm"
                type="password"
                required
                class="form-input"
                :class="{ 'border-red-300': errors.new_password_confirm }"
              />
              <div v-if="errors.new_password_confirm" class="form-error">
                {{ errors.new_password_confirm }}
              </div>
            </div>
            
            <div v-if="errors.general" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {{ errors.general }}
            </div>
            
            <div class="flex justify-end space-x-3">
              <router-link to="/profile" class="btn-outline">
                Отмена
              </router-link>
              <button
                type="submit"
                :disabled="authStore.isLoading"
                class="btn-primary"
              >
                <div v-if="authStore.isLoading" class="loading-spinner mr-2"></div>
                Изменить пароль
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

export default {
  name: 'ChangePasswordView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const toast = useToast()
    
    const form = reactive({
      old_password: '',
      new_password: '',
      new_password_confirm: ''
    })
    
    const errors = ref({})
    
    const handleSubmit = async () => {
      errors.value = {}
      
      if (form.new_password !== form.new_password_confirm) {
        errors.value.new_password_confirm = 'Пароли не совпадают'
        return
      }
      
      try {
        await authStore.changePassword(form)
        toast.success('Пароль успешно изменен')
        router.push('/profile')
      } catch (error) {
        if (error.response?.data) {
          Object.assign(errors.value, error.response.data)
        } else {
          errors.value.general = 'Ошибка изменения пароля'
        }
      }
    }
    
    return {
      authStore,
      form,
      errors,
      handleSubmit
    }
  }
}
</script>