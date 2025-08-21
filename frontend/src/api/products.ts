import api from './index'
import type { Product } from '@/types'

export const productsApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<Product[]> => {
    return await api.get('/products/', { params })
  },

  getById: async (id: number): Promise<Product> => {
    return await api.get(`/products/${id}`)
  },

  create: async (data: Omit<Product, 'id' | 'created_at' | 'updated_at'>): Promise<Product> => {
    return await api.post('/products', data)
  },

  update: async (id: number, data: Partial<Product>): Promise<Product> => {
    return await api.put(`/products/${id}`, data)
  },

  delete: async (id: number): Promise<void> => {
    return await api.delete(`/products/${id}`)
  },
}