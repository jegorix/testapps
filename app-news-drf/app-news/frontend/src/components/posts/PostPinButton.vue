<!-- frontend/src/components/posts/PostPinButton.vue -->
<template>
    <div v-if="showButton">
      <button
        @click="togglePin"
        :disabled="isLoading"
        class="btn btn-sm"
        :class="isPinned ? 'btn-danger' : 'btn-primary'"
        :title="isPinned ? 'Открепить пост' : 'Закрепить пост'"
      >
        <div v-if="isLoading" class="loading-spinner mr-1"></div>
        <component :is="isPinned ? UnpinIcon : PinIcon" class="w-4 h-4" :class="{ 'mr-1': !isLoading }" />
        {{ isPinned ? 'Открепить' : 'Закрепить' }}
      </button>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useSubscriptionStore } from '@/stores/subscription'
  import { useToast } from 'vue-toastification'
  
  // Простые SVG иконки
  const PinIcon = {
    template: `
      <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
        <path d="M10 2L12 4V8L14 10V12L10 16L6 12V10L8 8V4L10 2Z"/>
      </svg>
    `
  }
  
  const UnpinIcon = {
    template: `
      <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
        <path d="M10 2L12 4V8L14 10V12L10 16L6 12V10L8 8V4L10 2Z" opacity="0.5"/>
        <path d="M15 15L5 5" stroke="currentColor" stroke-width="2"/>
      </svg>
    `
  }
  
  export default {
    name: 'PostPinButton',
    components: { PinIcon, UnpinIcon },
    props: {
      post: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const authStore = useAuthStore()
      const subscriptionStore = useSubscriptionStore()
      const toast = useToast()
      const isLoading = ref(false)
  
      const isPinned = computed(() => {
        return subscriptionStore.pinnedPost?.post === props.post.id
      })
  
      const showButton = computed(() => {
        return (
          authStore.isAuthenticated &&
          props.post.author === authStore.user?.username &&
          props.post.status === 'published'
        )
      })
  
      const togglePin = async () => {
        if (!subscriptionStore.isActive) {
          toast.error('Для закрепления постов нужна активная подписка')
          return
        }
  
        isLoading.value = true
        try {
          if (isPinned.value) {
            await subscriptionStore.unpinPost()
            toast.success('Пост откреплен')
          } else {
            await subscriptionStore.pinPost(props.post.id)
            toast.success('Пост закреплен')
          }
        } catch (error) {
          toast.error('Ошибка при изменении статуса закрепления')
        } finally {
          isLoading.value = false
        }
      }
  
      // Загружаем статус подписки при монтировании
      if (showButton.value) {
        subscriptionStore.fetchSubscriptionStatus()
      }
  
      return {
        isPinned,
        showButton,
        isLoading,
        togglePin,
        PinIcon,
        UnpinIcon
      }
    }
  }
  </script>