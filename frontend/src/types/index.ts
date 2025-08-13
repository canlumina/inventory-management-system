export interface User {
  id: number
  username: string
  email: string
  role: 'admin' | 'manager' | 'staff'
  created_at: string
}

export interface Product {
  id: number
  name: string
  code: string
  category_id?: number
  description?: string
  unit: string
  purchase_price?: number
  sale_price?: number
  min_stock: number
  created_at: string
  updated_at?: string
}

export interface Inventory {
  id: number
  product_id: number
  quantity: number
  reserved_quantity: number
  available_quantity: number
  updated_at: string
  product?: Product
}

export interface Supplier {
  id: number
  name: string
  contact_person?: string
  phone?: string
  email?: string
  address?: string
  created_at: string
}

export interface Customer {
  id: number
  name: string
  contact_person?: string
  phone?: string
  email?: string
  address?: string
  created_at: string
}

export interface PurchaseOrderItem {
  id?: number
  product_id: number
  quantity: number
  unit_price: number
  total_price: number
  product?: Product
}

export interface PurchaseOrder {
  id: number
  order_number: string
  supplier_id: number
  status: 'pending' | 'confirmed' | 'received' | 'cancelled'
  order_date: string
  total_amount: number
  created_by: number
  created_at: string
  supplier?: Supplier
  items: PurchaseOrderItem[]
}

export interface SalesOrderItem {
  id?: number
  product_id: number
  quantity: number
  unit_price: number
  total_price: number
  product?: Product
}

export interface SalesOrder {
  id: number
  order_number: string
  customer_id: number
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'
  order_date: string
  total_amount: number
  created_by: number
  created_at: string
  customer?: Customer
  items: SalesOrderItem[]
}

export interface LoginForm {
  username: string
  password: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
}