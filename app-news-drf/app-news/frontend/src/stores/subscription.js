// frontend/src/stores/subscription.js - исправленная версия
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { subscriptionAPI, paymentAPI } from '@/services/api'

export const useSubscriptionStore = defineStore('subscription', () => {
  // Состояние
  const subscription = ref(null)
  const plans = ref([])
  const pinnedPost = ref(null)
  const isLoading = ref(false)
  const isSubmitting = ref(false)

  // Вычисляемые свойства
  const hasSubscription = computed(() => !!subscription.value)
  const isActive = computed(() => {
    if (!subscription.value) return false
    return subscription.value.is_active || false
  })
  const canPinPosts = computed(() => isActive.value)

  // Действия
  const fetchPlans = async () => {
    isLoading.value = true
    try {
      const response = await subscriptionAPI.getPlans()
      // Исправляем: берем results из пагинированного ответа
      plans.value = response.data.results || response.data || []
      console.log('Fetched plans:', plans.value) // Для отладки
      return response.data
    } catch (error) {
      console.error('Error fetching plans:', error)
      plans.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchSubscriptionStatus = async () => {
    isLoading.value = true
    try {
      const response = await subscriptionAPI.getStatus()
      const data = response.data || {}
      
      subscription.value = data.subscription || null
      pinnedPost.value = data.pinned_post || null
      
      return data
    } catch (error) {
      console.error('Error fetching subscription status:', error)
      subscription.value = null
      pinnedPost.value = null
      
      // Не пробрасываем ошибку дальше, если это 404 или похожее
      if (error.response?.status === 404) {
        return { subscription: null, pinned_post: null }
      }
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const createCheckoutSession = async (planId) => {
    if (!planId) {
      throw new Error('Plan ID is required')
    }

    isSubmitting.value = true
    try {
      const response = await paymentAPI.createCheckoutSession({
        subscription_plan_id: planId,
        success_url: `${window.location.origin}/subscription/success`,
        cancel_url: `${window.location.origin}/subscription/cancel`
      })
      return response.data
    } catch (error) {
      console.error('Error creating checkout session:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const pinPost = async (postId) => {
    if (!postId) {
      throw new Error('Post ID is required')
    }

    isSubmitting.value = true
    try {
      const response = await subscriptionAPI.pinPost({
        post_id: postId
      })
      pinnedPost.value = response.data
      return response.data
    } catch (error) {
      console.error('Error pinning post:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const unpinPost = async () => {
    isSubmitting.value = true
    try {
      await subscriptionAPI.unpinPost()
      pinnedPost.value = null
    } catch (error) {
      console.error('Error unpinning post:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const cancelSubscription = async () => {
    isSubmitting.value = true
    try {
      await subscriptionAPI.cancelSubscription()
      subscription.value = null
      pinnedPost.value = null
    } catch (error) {
      console.error('Error cancelling subscription:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  // Утилиты для безопасного доступа к данным
  const getSubscriptionPlan = () => {
    if (!subscription.value?.plan_info) return null
    return subscription.value.plan_info
  }

  const getPinnedPostInfo = () => {
    if (!pinnedPost.value?.post_info) return null
    return pinnedPost.value.post_info
  }

  const getSubscriptionDaysRemaining = () => {
    if (!subscription.value?.days_remaining) return 0
    return subscription.value.days_remaining
  }

  // Сброс состояния
  const resetState = () => {
    subscription.value = null
    plans.value = []
    pinnedPost.value = null
    isLoading.value = false
    isSubmitting.value = false
  }

  return {
    // Состояние
    subscription,
    plans,
    pinnedPost,
    isLoading,
    isSubmitting,
    
    // Вычисляемые свойства
    hasSubscription,
    isActive,
    canPinPosts,
    
    // Действия
    fetchPlans,
    fetchSubscriptionStatus,
    createCheckoutSession,
    pinPost,
    unpinPost,
    cancelSubscription,
    
    // Утилиты
    getSubscriptionPlan,
    getPinnedPostInfo,
    getSubscriptionDaysRemaining,
    resetState
  }
})