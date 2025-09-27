// Lazy loading компонентов категорий
const Categories = () => import('@/views/categories/CategoriesView.vue')
const CategoryPosts = () => import('@/views/categories/CategoryPostsView.vue')

// Валидатор для slug параметров
const validateSlug = (to, from, next) => {
  if (!to.params.slug || to.params.slug.trim() === '') {
    next({ name: 'NotFound' })
  } else {
    next()
  }
}

const categoryRoutes = [
  {
    path: '/categories',
    name: 'Categories',
    component: Categories,
    meta: {
      title: 'Категории'
    }
  },
  {
    path: '/categories/:slug',
    name: 'CategoryPosts',
    component: CategoryPosts,
    meta: {
      title: 'Посты категории'
    },
    props: true,
    beforeEnter: validateSlug
  }
]

export default categoryRoutes