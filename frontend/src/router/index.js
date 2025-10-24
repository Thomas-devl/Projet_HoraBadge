import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import EmployeeDashboard from '../views/EmployeeDashboard.vue'
import ManagerDashboard from '../views/ManagerDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import authService from '../services/authService'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard/employee',
    name: 'EmployeeDashboard',
    component: EmployeeDashboard,
    meta: { requiresAuth: true, roles: ['employee', 'manager', 'admin'] }
  },
  {
    path: '/dashboard/manager',
    name: 'ManagerDashboard',
    component: ManagerDashboard,
    meta: { requiresAuth: true, roles: ['manager', 'admin'] }
  },
  {
    path: '/dashboard/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  // Redirection par défaut vers le bon dashboard
  {
    path: '/dashboard',
    redirect: () => {
      const user = authService.getCurrentUser()
      if (!user) return '/login'
      
      // Admin peut accéder à tous les dashboards
      if (user.role === 'admin') return '/dashboard/admin'
      if (user.role === 'manager') return '/dashboard/manager'
      return '/dashboard/employee'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guards pour la protection des routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()
  const user = authService.getCurrentUser()
  
  // Si la route nécessite une authentification et l'utilisateur n'est pas connecté
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // Si la route est réservée aux invités et l'utilisateur est connecté
  if (to.meta.requiresGuest && isAuthenticated) {
    next('/dashboard')
    return
  }
  
  // Vérifier les rôles requis
  if (to.meta.roles && user) {
    const hasRequiredRole = to.meta.roles.includes(user.role)
    if (!hasRequiredRole) {
      // Rediriger vers le dashboard approprié au rôle
      if (user.role === 'admin') {
        next('/dashboard/admin')
      } else if (user.role === 'manager') {
        next('/dashboard/manager')
      } else {
        next('/dashboard/employee')
      }
      return
    }
  }
  
  // Sinon, continuer normalement
  next()
})

export default router
