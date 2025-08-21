import api from './index'

export interface InventoryReportItem {
  product_id: number
  product_name: string
  product_code: string
  current_stock: number
  reserved_stock: number
  available_stock: number
  min_stock: number
  stock_status: string
  stock_value: string
}

export interface InventoryReport {
  total_products: number
  total_stock_value: string
  low_stock_products: number
  out_of_stock_products: number
  items: InventoryReportItem[]
}

export interface PurchaseReportSummary {
  total_orders: number
  total_amount: string
  pending_orders: number
  confirmed_orders: number
  received_orders: number
  cancelled_orders: number
}

export interface PurchaseReportItem {
  order_id: number
  order_number: string
  supplier_name: string
  status: string
  order_date: string
  total_amount: string
  items_count: number
}

export interface PurchaseReport {
  summary: PurchaseReportSummary
  orders: PurchaseReportItem[]
}

export interface SalesReportSummary {
  total_orders: number
  total_amount: string
  total_revenue: string
  pending_orders: number
  confirmed_orders: number
  shipped_orders: number
  delivered_orders: number
  cancelled_orders: number
}

export interface SalesReportItem {
  order_id: number
  order_number: string
  customer_name: string
  status: string
  order_date: string
  total_amount: string
  items_count: number
}

export interface SalesReport {
  summary: SalesReportSummary
  orders: SalesReportItem[]
}

export interface FinancialSummary {
  total_purchase_cost: string
  total_sales_revenue: string
  gross_profit: string
  gross_profit_margin: number
}

export interface DashboardSummary {
  total_products: number
  low_stock_alerts: number
  total_inventory_value: string
  pending_purchase_orders: number
  pending_sales_orders: number
  monthly_revenue: string
  monthly_orders: number
  top_selling_product: string | null
}

export const reportsApi = {
  getInventoryReport: async (): Promise<InventoryReport> => {
    return await api.get('/reports/inventory')
  },

  getPurchaseReport: async (params?: { 
    start_date?: string
    end_date?: string 
  }): Promise<PurchaseReport> => {
    return await api.get('/reports/purchases', { params })
  },

  getSalesReport: async (params?: { 
    start_date?: string
    end_date?: string 
  }): Promise<SalesReport> => {
    return await api.get('/reports/sales', { params })
  },

  getFinancialReport: async (params?: { 
    start_date?: string
    end_date?: string 
  }): Promise<FinancialSummary> => {
    return await api.get('/reports/financial', { params })
  },

  getDashboardData: async (): Promise<DashboardSummary> => {
    return await api.get('/reports/dashboard')
  },
}