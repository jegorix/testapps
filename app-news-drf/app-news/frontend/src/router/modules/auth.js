// Lazy loading компонентов аутентификации
const Login = () => import('@/views/auth/LoginView.vue')
const Register = () => import('@/views/auth/RegisterView.vue')
const Profile = () => import('@/views/auth/ProfileView.vue')
const ChangePassword = () => import('@/views/auth/ChangePasswordView.vue')

const authRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Вход',
      requiresGuest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: 'Регистрация',
      requiresGuest: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      title: 'Профиль',
      requiresAuth: true
    }
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: {
      title: 'Смена пароля',
      requiresAuth: true
    }
  }
]

export default authRoutes