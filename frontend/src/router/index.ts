import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import ParkingLots from '../views/admin/ParkingLots.vue'
import RegisteredUsers from '../views/admin/RegisteredUsers.vue'
import Analytics from '../views/admin/Analytics.vue'
import BookingHistory from '../views/user/BookingHistory.vue'
import BookSpot from '../views/user/BookSpot.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage
    },
    {
      path: '/signup',
      name: 'Signup', 
      component: SignupPage
    },
    {
      path: '/admin',
      name: 'AdminDashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          redirect: '/admin/parking-lots'
        },
        {
          path: 'parking-lots',
          name: 'ParkingLots',
          component: ParkingLots
        },
        {
          path: 'users',
          name: 'RegisteredUsers', 
          component: RegisteredUsers
        },
        {
          path: 'analytics',
          name: 'Analytics',
          component: Analytics
        }
      ]
    },
    {
      path: '/user',
      name: 'UserDashboard',
      component: UserDashboard,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/user/book-spot'
        },
        {
          path: 'book-spot',
          name: 'BookSpot',
          component: BookSpot
        },
        {
          path: 'history',
          name: 'BookingHistory',
          component: BookingHistory
        }
      ]
    }
  ]
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/user')
  } else if ((to.name === 'Login' || to.name === 'Signup') && authStore.isAuthenticated) {
    if (authStore.isAdmin) {
      next('/admin')
    } else {
      next('/user')
    }
  } else {
    next()
  }
})

export default router