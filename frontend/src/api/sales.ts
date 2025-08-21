import api from './index'
import type { SalesOrder, SalesOrderItem } from '@/types'

export const salesApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<SalesOrder[]> => {
    return await api.get('/sales', { params })
  },

  getById: async (id: number): Promise<SalesOrder> => {
    return await api.get(`/sales/${id}`)
  },

  create: async (data: { 
    customer_id: number
    items: SalesOrderItem[]
  }): Promise<SalesOrder> => {
    return await api.post('/sales', data)
  },

  update: async (id: number, data: Partial<SalesOrder>): Promise<SalesOrder> => {
    return await api.put(`/sales/${id}`, data)
  },

  updateStatus: async (id: number, status: string): Promise<SalesOrder> => {
    return await api.put(`/sales/${id}/status`, { status })
  },

  ship: async (id: number): Promise<SalesOrder> => {
    return await api.post(`/sales/${id}/ship`)
  },
}