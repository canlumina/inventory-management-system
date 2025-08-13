import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const setUser = (userData: User, userToken: string) => {
    user.value = userData
    token.value = userToken
    localStorage.setItem('token', userToken)
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const checkAuth = async () => {
    if (token.value) {
      try {
        const userData = await authApi.getMe()
        user.value = userData
        return true
      } catch {
        logout()
        return false
      }
    }
    return false
  }

  return {
    user,
    token,
    setUser,
    logout,
    checkAuth
  }
})