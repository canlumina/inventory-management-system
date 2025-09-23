import api from './index'
import type { Category } from '@/types'

export const categoriesApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<Category[]> => {
    return await api.get('/categories/', { params })
  },

  getById: async (id: number): Promise<Category> => {
    return await api.get(`/categories/${id}`)
  },

  create: async (data: Omit<Category, 'id' | 'created_at' | 'children'>): Promise<Category> => {
    return await api.post('/categories/', data)
  },

  update: async (id: number, data: Partial<Category>): Promise<Category> => {
    return await api.put(`/categories/${id}`, data)
  },

  delete: async (id: number): Promise<void> => {
    return await api.delete(`/categories/${id}`)
  },
}