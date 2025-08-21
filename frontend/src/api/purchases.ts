import api from './index'
import type { PurchaseOrder, PurchaseOrderItem } from '@/types'

export const purchasesApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<PurchaseOrder[]> => {
    return await api.get('/purchases', { params })
  },

  getById: async (id: number): Promise<PurchaseOrder> => {
    return await api.get(`/purchases/${id}`)
  },

  create: async (data: { 
    supplier_id: number
    items: PurchaseOrderItem[]
  }): Promise<PurchaseOrder> => {
    return await api.post('/purchases', data)
  },

  update: async (id: number, data: Partial<PurchaseOrder>): Promise<PurchaseOrder> => {
    return await api.put(`/purchases/${id}`, data)
  },

  updateStatus: async (id: number, status: string): Promise<PurchaseOrder> => {
    return await api.put(`/purchases/${id}/status`, { status })
  },

  receive: async (id: number): Promise<PurchaseOrder> => {
    return await api.post(`/purchases/${id}/receive`)
  },
}