// Lazy loading компонентов комментариев
const MyComments = () => import('@/views/comments/MyCommentsView.vue')

const commentRoutes = [
  {
    path: '/comments/my',
    name: 'MyComments',
    component: MyComments,
    meta: {
      title: 'Мои комментарии',
      requiresAuth: true
    }
  }
]

export default commentRoutes