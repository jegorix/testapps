// Lazy loading компонентов постов
const Posts = () => import('@/views/posts/PostsView.vue')
const PostDetail = () => import('@/views/posts/PostDetailView.vue')
const PostCreate = () => import('@/views/posts/PostCreateView.vue')
const PostEdit = () => import('@/views/posts/PostEditView.vue')
const MyPosts = () => import('@/views/posts/MyPostsView.vue')

// Валидатор для slug параметров
const validateSlug = (to, from, next) => {
  if (!to.params.slug || to.params.slug.trim() === '') {
    next({ name: 'NotFound' })
  } else {
    next()
  }
}

const postRoutes = [
  {
    path: '/posts',
    name: 'Posts',
    component: Posts,
    meta: {
      title: 'Все посты'
    }
  },
  {
    path: '/posts/create',
    name: 'PostCreate',
    component: PostCreate,
    meta: {
      title: 'Создать пост',
      requiresAuth: true
    }
  },
  {
    path: '/posts/my',
    name: 'MyPosts',
    component: MyPosts,
    meta: {
      title: 'Мои посты',
      requiresAuth: true
    }
  },
  {
    path: '/posts/:slug',
    name: 'PostDetail',
    component: PostDetail,
    meta: {
      title: 'Пост'
    },
    props: true,
    beforeEnter: validateSlug
  },
  {
    path: '/posts/:slug/edit',
    name: 'PostEdit',
    component: PostEdit,
    meta: {
      title: 'Редактировать пост',
      requiresAuth: true
    },
    props: true,
    beforeEnter: validateSlug
  }
]

export default postRoutes