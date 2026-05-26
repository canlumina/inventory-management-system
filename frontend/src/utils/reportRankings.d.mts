export interface ProductStockRankingItem {
  name: string
  stock: number
}

export interface AmountRankingItem {
  name: string
  amount: number
}

export interface InventoryReportLike {
  items?: Array<{
    product_name?: string
    current_stock?: number | string
  }>
}

export interface OrderReportLike<NameKey extends string> {
  orders?: Array<Record<NameKey, string | undefined> & {
    total_amount?: number | string
  }>
}

export declare function buildProductStockRanking(
  report: InventoryReportLike | null | undefined,
  limit?: number,
): ProductStockRankingItem[]

export declare function buildSupplierAmountRanking(
  report: OrderReportLike<'supplier_name'> | null | undefined,
  limit?: number,
): AmountRankingItem[]

export declare function buildCustomerAmountRanking(
  report: OrderReportLike<'customer_name'> | null | undefined,
  limit?: number,
): AmountRankingItem[]
