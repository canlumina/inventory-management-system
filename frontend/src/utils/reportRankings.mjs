const DEFAULT_LIMIT = 5

function toFiniteNumber(value) {
  const numberValue = Number(value)
  return Number.isFinite(numberValue) ? numberValue : 0
}

function toAmount(value) {
  return Math.round(toFiniteNumber(value) * 100) / 100
}

function normalizeName(value) {
  return typeof value === 'string' ? value.trim() : ''
}

function sortRankingItems(left, right, valueKey) {
  return right[valueKey] - left[valueKey] || left.name.localeCompare(right.name, 'zh-CN')
}

function aggregateAmountByName(items, nameKey, amountKey, limit = DEFAULT_LIMIT) {
  const totals = new Map()

  for (const item of items || []) {
    const name = normalizeName(item?.[nameKey])

    if (!name) {
      continue
    }

    totals.set(name, (totals.get(name) || 0) + toFiniteNumber(item?.[amountKey]))
  }

  return Array.from(totals, ([name, amount]) => ({ name, amount: toAmount(amount) }))
    .sort((left, right) => sortRankingItems(left, right, 'amount'))
    .slice(0, limit)
}

export function buildProductStockRanking(report, limit = DEFAULT_LIMIT) {
  return (report?.items || [])
    .map((item) => ({
      name: normalizeName(item?.product_name),
      stock: toFiniteNumber(item?.current_stock),
    }))
    .filter((item) => item.name)
    .sort((left, right) => sortRankingItems(left, right, 'stock'))
    .slice(0, limit)
}

export function buildSupplierAmountRanking(report, limit = DEFAULT_LIMIT) {
  return aggregateAmountByName(report?.orders, 'supplier_name', 'total_amount', limit)
}

export function buildCustomerAmountRanking(report, limit = DEFAULT_LIMIT) {
  return aggregateAmountByName(report?.orders, 'customer_name', 'total_amount', limit)
}
