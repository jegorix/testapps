// Lazy loading компонентов подписки
const SubscriptionView = () => import('@/views/subscription/SubscriptionView.vue')
const PaymentSuccessView = () => import('@/views/subscription/PaymentSuccessView.vue')
const PaymentCancelView = () => import('@/views/subscription/PaymentCancelView.vue')

const subscriptionRoutes = [
  {
    path: '/subscription',
    name: 'Subscription',
    component: SubscriptionView,
    meta: {
      title: 'Подписка',
      requiresAuth: true
    }
  },
  {
    path: '/subscription/success',
    name: 'PaymentSuccess',
    component: PaymentSuccessView,
    meta: {
      title: 'Оплата успешна'
    }
  },
  {
    path: '/subscription/cancel',
    name: 'PaymentCancel',
    component: PaymentCancelView,
    meta: {
      title: 'Оплата отменена'
    }
  }
]

export default subscriptionRoutes