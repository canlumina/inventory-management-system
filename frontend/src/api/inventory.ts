import api from './index'
import type { Inventory } from '@/types'

export const inventoryApi = {
  getList: async (params?: { skip?: number; limit?: number }): Promise<Inventory[]> => {
    return await api.get('/inventory', { params })
  },

  getByProductId: async (productId: number): Promise<Inventory> => {
    return await api.get(`/inventory/${productId}`)
  },

  adjust: async (data: { product_id: number; quantity: number; reason?: string }): Promise<void> => {
    return await api.post('/inventory/adjustment', data)
  },

  getAlerts: async (): Promise<Inventory[]> => {
    return await api.get('/inventory/alerts')
  },
}