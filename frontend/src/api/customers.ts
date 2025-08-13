import api from './index'
import type { Customer } from '@/types'

export const customersApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<Customer[]> => {
    return await api.get('/customers', { params })
  },

  getById: async (id: number): Promise<Customer> => {
    return await api.get(`/customers/${id}`)
  },

  create: async (data: Omit<Customer, 'id' | 'created_at'>): Promise<Customer> => {
    return await api.post('/customers', data)
  },

  update: async (id: number, data: Partial<Customer>): Promise<Customer> => {
    return await api.put(`/customers/${id}`, data)
  },

  delete: async (id: number): Promise<void> => {
    return await api.delete(`/customers/${id}`)
  },
}