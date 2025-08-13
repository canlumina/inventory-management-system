import api from './index'
import type { Supplier } from '@/types'

export const suppliersApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<Supplier[]> => {
    return await api.get('/suppliers', { params })
  },

  getById: async (id: number): Promise<Supplier> => {
    return await api.get(`/suppliers/${id}`)
  },

  create: async (data: Omit<Supplier, 'id' | 'created_at'>): Promise<Supplier> => {
    return await api.post('/suppliers', data)
  },

  update: async (id: number, data: Partial<Supplier>): Promise<Supplier> => {
    return await api.put(`/suppliers/${id}`, data)
  },

  delete: async (id: number): Promise<void> => {
    return await api.delete(`/suppliers/${id}`)
  },
}