import api from './index'
import type { User, LoginForm } from '@/types'

export const authApi = {
  login: async (data: LoginForm): Promise<{ access_token: string; token_type: string }> => {
    const formData = new FormData()
    formData.append('username', data.username)
    formData.append('password', data.password)
    
    return await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  getMe: async (): Promise<User> => {
    return await api.post('/auth/test-token')
  },
}