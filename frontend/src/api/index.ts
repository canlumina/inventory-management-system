import axios from 'axios'
import { ElMessage, ElNotification } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { handleApiError } from '@/utils/errorHandler'

// 在开发环境中使用代理，生产环境中使用环境变量
const baseURL = '/api/v1'
console.log('API Base URL:', baseURL)
console.log('VITE_API_URL:', import.meta.env.VITE_API_URL)

const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Retry configuration
const MAX_RETRIES = 3
let retryCount = 0

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Reset retry count on successful response
    retryCount = 0
    return response.data
  },
  async (error) => {
    const { response, config } = error
    
    // Handle 401 specifically
    if (response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      ElNotification({
        title: '认证失败',
        message: '登录已过期，请重新登录',
        type: 'warning',
        duration: 3000
      })
      setTimeout(() => {
        window.location.href = '/login'
      }, 1000)
      return Promise.reject(error)
    }
    
    // Retry logic for network errors or 5xx errors
    if (
      (!response || response.status >= 500) &&
      config &&
      retryCount < MAX_RETRIES
    ) {
      retryCount++
      ElMessage({
        message: `网络错误，正在重试... (${retryCount}/${MAX_RETRIES})`,
        type: 'warning',
        duration: 2000
      })
      
      // Exponential backoff delay
      const delay = Math.pow(2, retryCount) * 1000
      await new Promise(resolve => setTimeout(resolve, delay))
      
      return api.request(config)
    }
    
    // Reset retry count for non-retryable errors
    retryCount = 0
    
    // Handle other errors using our error handler
    handleApiError(error)
    
    return Promise.reject(error)
  }
)

export default api