import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/products',
      name: 'Products',
      component: () => import('@/views/ProductsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/inventory',
      name: 'Inventory',
      component: () => import('@/views/InventoryView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/inventory-adjustment',
      name: 'InventoryAdjustment',
      component: () => import('@/views/InventoryAdjustmentView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/purchases',
      name: 'Purchases',
      component: () => import('@/views/PurchasesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/suppliers',
      name: 'Suppliers',
      component: () => import('@/views/SuppliersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sales',
      name: 'Sales',
      component: () => import('@/views/SalesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/customers',
      name: 'Customers',
      component: () => import('@/views/CustomersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reports',
      name: 'Reports',
      component: () => import('@/views/ReportsView.vue'),
      meta: { requiresAuth: true }
    },
  ]
})

router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth) {
    if (!userStore.user && userStore.token) {
      // 尝试使用存储的token恢复用户信息
      const isAuthenticated = await userStore.checkAuth()
      if (!isAuthenticated) {
        next('/login')
        return
      }
    } else if (!userStore.user) {
      next('/login')
      return
    }
  }
  
  if (to.meta.requiresGuest && userStore.user) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router