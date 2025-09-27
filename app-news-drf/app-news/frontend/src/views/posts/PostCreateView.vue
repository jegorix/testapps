<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Заголовок -->
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900 mb-2">Создать новую статью</h1>
        <p class="text-sm text-gray-600">Поделитесь своими мыслями и идеями с сообществом</p>
      </div>

      <!-- Форма создания поста -->
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Основная информация -->
        <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Основная информация</h2>
          
          <div class="space-y-6">
            <!-- Заголовок -->
            <div>
              <label class="block text-sm font-medium text-gray-700">
                Заголовок статьи <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                required
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.title }"
                placeholder="Введите заголовок статьи..."
                maxlength="200"
              />
              <div v-if="errors.title" class="mt-1 text-xs text-red-600">
                {{ errors.title }}
              </div>
              <div class="mt-1 text-xs text-gray-500">
                {{ form.title.length }}/200 символов
              </div>
            </div>

            <!-- Категория -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Категория</label>
              <select
                v-model="form.category"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.category }"
              >
                <option value="">Выберите категорию</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
              <div v-if="errors.category" class="mt-1 text-xs text-red-600">
                {{ errors.category }}
              </div>
            </div>

            <!-- Изображение -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Изображение</label>
              
              <!-- Превью изображения -->
              <div v-if="imagePreview" class="mb-4">
                <div class="relative inline-block">
                  <img
                    :src="imagePreview"
                    alt="Preview"
                    class="w-full max-w-md h-48 object-cover rounded-md border border-gray-200"
                  />
                  <button
                    type="button"
                    @click="removeImage"
                    class="absolute top-2 right-2 p-1 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors"
                  >
                    <XMarkIcon class="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <!-- Загрузка изображения -->
              <div class="flex items-center justify-center w-full">
                <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-md cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                  <div class="flex flex-col items-center justify-center pt-5 pb-6">
                    <PhotoIcon class="w-8 h-8 mb-2 text-gray-400" />
                    <p class="mb-2 text-sm text-gray-500">
                      <span class="font-medium">Нажмите для загрузки</span> или перетащите файл
                    </p>
                    <p class="text-xs text-gray-500">PNG, JPG, WEBP до 10MB</p>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleImageChange"
                  />
                </label>
              </div>
              <div v-if="errors.image" class="mt-1 text-xs text-red-600">
                {{ errors.image }}
              </div>
            </div>
          </div>
        </div>

        <!-- Содержимое -->
        <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Содержимое статьи</h2>
          
          <!-- Редактор -->
          <div>
            <label class="block text-sm font-medium text-gray-700">
              Текст статьи <span class="text-red-500">*</span>
            </label>
            
            <!-- Панель инструментов -->
            <div class="border border-gray-300 rounded-t-md bg-gray-50 p-2 flex items-center space-x-2">
              <button
                type="button"
                @click="formatText('bold')"
                class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors"
                title="Жирный"
              >
                <BoldIcon class="w-4 h-4" />
              </button>
              <button
                type="button"
                @click="formatText('italic')"
                class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors"
                title="Курсив"
              >
                <ItalicIcon class="w-4 h-4" />
              </button>
              <div class="border-l border-gray-300 h-6"></div>
              <button
                type="button"
                @click="formatText('h2')"
                class="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors"
                title="Заголовок"
              >
                H2
              </button>
              <button
                type="button"
                @click="formatText('quote')"
                class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors"
                title="Цитата"
              >
                <ChatBubbleLeftIcon class="w-4 h-4" />
              </button>
              <div class="border-l border-gray-300 h-6"></div>
              <button
                type="button"
                @click="formatText('link')"
                class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors"
                title="Ссылка"
              >
                <LinkIcon class="w-4 h-4" />
              </button>
            </div>
            
            <!-- Текстовая область -->
            <textarea
              ref="contentTextarea"
              v-model="form.content"
              required
              rows="15"
              class="block w-full px-3 py-2 border border-gray-300 rounded-b-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
              :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.content }"
              placeholder="Напишите содержимое статьи...&#10;&#10;Вы можете использовать простую разметку:&#10;**жирный текст**&#10;*курсив*&#10;## Заголовок&#10;> Цитата&#10;[ссылка](URL)"
              @keydown="handleKeydown"
            ></textarea>
            
            <div v-if="errors.content" class="mt-1 text-xs text-red-600">
              {{ errors.content }}
            </div>
            <div class="mt-1 text-xs text-gray-500 flex justify-between">
              <span>{{ form.content.length }} символов</span>
              <span class="text-gray-400">Минимум 100 символов</span>
            </div>
          </div>
        </div>

        <!-- Настройки публикации -->
        <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Настройки публикации</h2>
          
          <div class="space-y-4">
            <!-- Статус -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Статус публикации</label>
              <div class="space-y-3">
                <label class="flex items-start">
                  <input
                    v-model="form.status"
                    type="radio"
                    value="published"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 mt-1"
                  />
                  <span class="ml-3 text-sm">
                    <span class="font-medium text-gray-900">Опубликовать</span>
                    <span class="text-gray-500 block">Статья будет доступна всем пользователям</span>
                  </span>
                </label>
                <label class="flex items-start">
                  <input
                    v-model="form.status"
                    type="radio"
                    value="draft"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 mt-1"
                  />
                  <span class="ml-3 text-sm">
                    <span class="font-medium text-gray-900">Сохранить как черновик</span>
                    <span class="text-gray-500 block">Статья будет сохранена, но не опубликована</span>
                  </span>
                </label>
              </div>
            </div>

            <!-- Дополнительные настройки -->
            <div class="pt-4 border-t border-gray-200">
              <div class="flex items-center">
                <input
                  id="allow-comments"
                  v-model="form.allowComments"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="allow-comments" class="ml-3 text-sm text-gray-700">
                  Разрешить комментарии к статье
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Общие ошибки -->
        <div v-if="errors.general" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          <div class="flex">
            <ExclamationTriangleIcon class="h-5 w-5 text-red-400 mr-2" />
            <span>{{ errors.general }}</span>
          </div>
        </div>

        <!-- Кнопки действий -->
        <div class="flex items-center justify-between sticky bottom-0 bg-gray-50 p-4 rounded-md border border-gray-200">
          <router-link
            to="/posts"
            class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
          >
            <ArrowLeftIcon class="w-4 h-4 mr-2" />
            Отмена
          </router-link>
          
          <div class="flex items-center space-x-3">
            <!-- Предварительный просмотр -->
            <button
              type="button"
              @click="showPreview = true"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
              :disabled="!form.title || !form.content"
              :class="{ 'opacity-50 cursor-not-allowed': !form.title || !form.content }"
            >
              <EyeIcon class="w-4 h-4 mr-2" />
              Предпросмотр
            </button>
            
            <!-- Автосохранение статус -->
            <div v-if="isAutoSaving" class="flex items-center text-sm text-gray-500">
              <div class="inline-block w-4 h-4 border-2 border-gray-500 border-t-transparent rounded-full animate-spin mr-2"></div>
              Автосохранение...
            </div>
            <div v-else-if="lastSaved" class="text-sm text-gray-500">
              Сохранено {{ formatTime(lastSaved) }}
            </div>
            
            <!-- Сохранить -->
            <button
              type="submit"
              :disabled="postsStore.isSubmitting || !form.title.trim() || !form.content.trim()"
              class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
              :class="{ 'opacity-50 cursor-not-allowed': postsStore.isSubmitting || !form.title.trim() || !form.content.trim() }"
            >
              <div v-if="postsStore.isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              <DocumentPlusIcon v-else class="w-4 h-4 mr-2" />
              {{ form.status === 'published' ? 'Опубликовать' : 'Сохранить черновик' }}
            </button>
          </div>
        </div>
      </form>

      <!-- Модальное окно предпросмотра -->
      <teleport to="body">
        <div
          v-if="showPreview"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          @click.self="showPreview = false"
        >
          <div class="bg-white rounded-md max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6 border-b border-gray-200 flex items-center justify-between sticky top-0 bg-white">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Предварительный просмотр</h3>
                <p class="text-sm text-gray-500">Так будет выглядеть ваша статья</p>
              </div>
              <button
                @click="showPreview = false"
                class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-50 transition-colors"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>
            
            <div class="p-6">
              <!-- Превью поста -->
              <article class="prose prose-sm md:prose-lg max-w-none text-gray-700">
                <div v-if="imagePreview" class="mb-6">
                  <img :src="imagePreview" alt="Preview" class="w-full h-64 object-cover rounded-md" />
                </div>
                
                <h1 class="text-2xl md:text-3xl font-semibold text-gray-900 mb-4">
                  {{ form.title || 'Заголовок статьи' }}
                </h1>
                
                <div class="flex items-center space-x-4 text-gray-600 text-sm mb-6 pb-6 border-b border-gray-200">
                  <div class="flex items-center space-x-2">
                    <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                      {{ authStore.userInitials }}
                    </div>
                    <span>{{ authStore.userFullName || 'Автор' }}</span>
                  </div>
                  <span>•</span>
                  <span>{{ new Date().toLocaleDateString('ru-RU') }}</span>
                  <span v-if="selectedCategoryName">•</span>
                  <span v-if="selectedCategoryName" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600">
                    {{ selectedCategoryName }}
                  </span>
                </div>
                
                <div v-html="formattedPreviewContent"></div>
              </article>
            </div>
            
            <div class="p-6 border-t border-gray-200 bg-gray-50">
              <div class="flex justify-end space-x-3">
                <button
                  @click="showPreview = false"
                  class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
                >
                  Закрыть
                </button>
                <button
                  @click="showPreview = false"
                  class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
                >
                  Продолжить редактирование
                </button>
              </div>
            </div>
          </div>
        </div>
      </teleport>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import { useToast } from 'vue-toastification'
import api from '@/services/api'
import {
  XMarkIcon,
  PhotoIcon,
  EyeIcon,
  ChatBubbleLeftIcon,
  ArrowLeftIcon,
  DocumentPlusIcon,
  LinkIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

// Компоненты иконок для форматирования
const BoldIcon = {
  template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M6 4v12c0 .55.45 1 1 1h4.5c2.49 0 4.5-2.01 4.5-4.5 0-1.4-.65-2.64-1.67-3.45.39-.82.67-1.69.67-2.55C15 4.01 12.99 2 10.5 2H7c-.55 0-1 .45-1 1v1zm2 2h2.5c.83 0 1.5.67 1.5 1.5S11.33 9 10.5 9H8V6zm0 5h3c.83 0 1.5.67 1.5 1.5S11.83 14 11 14H8v-3z"/></svg>'
}

const ItalicIcon = {
  template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M8 2h6v2h-2l-2 8h2v2H6v-2h2l2-8H8V2z"/></svg>'
}

export default {
  name: 'PostCreateView',
  components: {
    XMarkIcon,
    PhotoIcon,
    EyeIcon,
    ChatBubbleLeftIcon,
    ArrowLeftIcon,
    DocumentPlusIcon,
    LinkIcon,
    ExclamationTriangleIcon,
    BoldIcon,
    ItalicIcon
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const postsStore = usePostsStore()
    const toast = useToast()
    
    const contentTextarea = ref(null)
    const showPreview = ref(false)
    const imagePreview = ref(null)
    const imageFile = ref(null)
    const isAutoSaving = ref(false)
    const lastSaved = ref(null)
    const autoSaveTimer = ref(null)
    
    const form = reactive({
      title: '',
      content: '',
      category: '',
      status: 'published',
      allowComments: true
    })
    
    const errors = ref({})
    
    const categories = computed(() => postsStore.categories)
    
    const selectedCategoryName = computed(() => {
      if (!form.category) return null
      const category = categories.value.find(cat => cat.id == form.category)
      return category?.name || null
    })
    
    const formattedPreviewContent = computed(() => {
      if (!form.content) return '<p class="text-gray-500 italic">Содержимое статьи будет отображено здесь...</p>'
      
      return form.content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^## (.*$)/gm, '<h2 class="text-2xl font-semibold text-gray-900 mt-8 mb-4">$1</h2>')
        .replace(/^### (.*$)/gm, '<h3 class="text-xl font-semibold text-gray-900 mt-6 mb-3">$1</h3>')
        .replace(/^> (.*$)/gm, '<blockquote class="border-l-4 border-gray-200 pl-4 italic text-gray-600 my-4">$1</blockquote>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 hover:text-blue-700 underline" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\n\n/g, '</p><p class="mb-4">')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p class="mb-4">')
        .replace(/$/, '</p>')
    })
    
    // Автосохранение
    const startAutoSave = () => {
      if (autoSaveTimer.value) {
        clearInterval(autoSaveTimer.value)
      }
      
      autoSaveTimer.value = setInterval(() => {
        if (form.title.trim() && form.content.trim()) {
          saveAsDraft(true)
        }
      }, 30000) // Автосохранение каждые 30 секунд
    }
    
    const saveAsDraft = async (isAutoSave = false) => {
      if (!form.title.trim() || !form.content.trim()) return
      
      if (isAutoSave) {
        isAutoSaving.value = true
      }
      
      try {
        const formData = new FormData()
        formData.append('title', form.title.trim())
        formData.append('content', form.content.trim())
        formData.append('status', 'draft')
        
        if (form.category) {
          formData.append('category', form.category)
        }
        
        if (imageFile.value) {
          formData.append('image', imageFile.value)
        }
        
        // Сохраняем как черновик
        await api.post('/api/v1/posts/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (isAutoSave) {
          lastSaved.value = new Date()
        }
      } catch (error) {
        console.error('Ошибка автосохранения:', error)
      } finally {
        if (isAutoSave) {
          isAutoSaving.value = false
        }
      }
    }
    
    const handleImageChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        // Проверяем размер файла (10MB)
        if (file.size > 10 * 1024 * 1024) {
          toast.error('Размер файла не должен превышать 10MB')
          return
        }
        
        // Проверяем тип файла
        if (!file.type.startsWith('image/')) {
          toast.error('Можно загружать только изображения')
          return
        }
        
        imageFile.value = file
        
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const removeImage = () => {
      imagePreview.value = null
      imageFile.value = null
    }
    
    const formatText = (format) => {
      const textarea = contentTextarea.value
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selectedText = form.content.substring(start, end)
      
      let formattedText = ''
      let cursorOffset = 0
      
      switch (format) {
        case 'bold':
          formattedText = `**${selectedText}**`
          cursorOffset = selectedText ? 0 : 2
          break
        case 'italic':
          formattedText = `*${selectedText}*`
          cursorOffset = selectedText ? 0 : 1
          break
        case 'h2':
          formattedText = `## ${selectedText}`
          cursorOffset = selectedText ? 0 : 3
          break
        case 'quote':
          formattedText = `> ${selectedText}`
          cursorOffset = selectedText ? 0 : 2
          break
        case 'link':
          const url = selectedText.startsWith('http') ? selectedText : 'https://'
          const linkText = selectedText.startsWith('http') ? 'Текст ссылки' : selectedText || 'Текст ссылки'
          formattedText = `[${linkText}](${url})`
          cursorOffset = selectedText ? 0 : 1
          break
        default:
          formattedText = selectedText
      }
      
      form.content = form.content.substring(0, start) + formattedText + form.content.substring(end)
      
      // Восстанавливаем фокус
      setTimeout(() => {
        textarea.focus()
        const newPosition = start + formattedText.length - cursorOffset
        textarea.setSelectionRange(newPosition, newPosition)
      }, 0)
    }
    
    const handleKeydown = (event) => {
      // Горячие клавиши
      if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
          case 'b':
            event.preventDefault()
            formatText('bold')
            break
          case 'i':
            event.preventDefault()
            formatText('italic')
            break
          case 's':
            event.preventDefault()
            if (event.shiftKey) {
              form.status = 'published'
              handleSubmit()
            } else {
              saveAsDraft()
            }
            break
        }
      }
      
      // Tab для отступов
      if (event.key === 'Tab') {
        event.preventDefault()
        const start = event.target.selectionStart
        const end = event.target.selectionEnd
        form.content = form.content.substring(0, start) + '  ' + form.content.substring(end)
        setTimeout(() => {
          event.target.setSelectionRange(start + 2, start + 2)
        }, 0)
      }
    }
    
    const validateForm = () => {
      const newErrors = {}
      
      if (!form.title.trim()) {
        newErrors.title = 'Заголовок обязателен'
      } else if (form.title.length > 200) {
        newErrors.title = 'Заголовок не должен превышать 200 символов'
      }
      
      if (!form.content.trim()) {
        newErrors.content = 'Содержимое статьи обязательно'
      } else if (form.content.length < 100) {
        newErrors.content = 'Статья должна содержать минимум 100 символов'
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    const handleSubmit = async () => {
      errors.value = {}
      
      if (!validateForm()) {
        toast.error('Пожалуйста, исправьте ошибки в форме')
        return
      }
      
      try {
        // Создаем объект с данными для API
        const postData = {
          title: form.title.trim(),
          content: form.content.trim(),
          status: form.status
        }
        
        // Добавляем категорию, если выбрана
        if (form.category) {
          postData.category = form.category
        }
        
        // Если есть изображение, создаем FormData
        let requestData
        if (imageFile.value) {
          requestData = new FormData()
          Object.keys(postData).forEach(key => {
            requestData.append(key, postData[key])
          })
          requestData.append('image', imageFile.value)
        } else {
          requestData = postData
        }
        
        // Используем store метод вместо прямого API вызова
        const newPost = await postsStore.createPost(requestData)
        
        // Очищаем автосохранение
        if (autoSaveTimer.value) {
          clearInterval(autoSaveTimer.value)
        }
        
        toast.success(
          form.status === 'published' 
            ? 'Статья успешно опубликована!' 
            : 'Черновик сохранен!'
        )
        
        router.push({ name: 'PostDetail', params: { slug: newPost.slug } })
        
      } catch (error) {
        console.error('Ошибка создания поста:', error)
        
        if (error.response?.status === 400) {
          const data = error.response.data
          Object.keys(data).forEach(key => {
            if (Array.isArray(data[key])) {
              errors.value[key] = data[key][0]
            }
          })
        } else {
          errors.value.general = 'Произошла ошибка при создании статьи. Попробуйте еще раз.'
        }
      }
    }
    
    const formatTime = (date) => {
      const now = new Date()
      const diff = Math.floor((now - date) / 1000)
      
      if (diff < 60) return 'только что'
      if (diff < 3600) return `${Math.floor(diff / 60)} мин. назад`
      if (diff < 86400) return `${Math.floor(diff / 3600)} ч. назад`
      
      return date.toLocaleDateString('ru-RU')
    }
    
    // Отслеживаем изменения для автосохранения
    watch([() => form.title, () => form.content], () => {
      if (form.title.trim() && form.content.trim()) {
        startAutoSave()
      }
    })
    
    onMounted(async () => {
      // Загружаем категории, если их нет
      if (categories.value.length === 0) {
        await postsStore.fetchCategories()
      }
      
      // Фокусируемся на заголовке
      document.querySelector('input[type="text"]')?.focus()
    })
    
    onUnmounted(() => {
      if (autoSaveTimer.value) {
        clearInterval(autoSaveTimer.value)
      }
    })
    
    return {
      authStore,
      postsStore,
      form,
      errors,
      categories,
      selectedCategoryName,
      contentTextarea,
      showPreview,
      imagePreview,
      isAutoSaving,
      lastSaved,
      handleImageChange,
      removeImage,
      formatText,
      handleKeydown,
      handleSubmit,
      formatTime,
      saveAsDraft
    }
  }
}
</script>
