import test from 'node:test'
import assert from 'node:assert/strict'

import {
  buildCustomerAmountRanking,
  buildProductStockRanking,
  buildSupplierAmountRanking,
} from './reportRankings.mjs'

test('buildProductStockRanking sorts inventory items by current stock and limits results', () => {
  const ranking = buildProductStockRanking(
    {
      items: [
        { product_name: '键盘', current_stock: 18 },
        { product_name: '显示器', current_stock: 42 },
        { product_name: '鼠标', current_stock: 30 },
      ],
    },
    2,
  )

  assert.deepEqual(ranking, [
    { name: '显示器', stock: 42 },
    { name: '鼠标', stock: 30 },
  ])
})

test('buildSupplierAmountRanking aggregates purchase amount by supplier', () => {
  const ranking = buildSupplierAmountRanking({
    orders: [
      { supplier_name: '华东供应商', total_amount: '120.50' },
      { supplier_name: '华北供应商', total_amount: '80' },
      { supplier_name: '华东供应商', total_amount: '29.50' },
    ],
  })

  assert.deepEqual(ranking, [
    { name: '华东供应商', amount: 150 },
    { name: '华北供应商', amount: 80 },
  ])
})

test('buildCustomerAmountRanking aggregates sales amount by customer and ignores empty names', () => {
  const ranking = buildCustomerAmountRanking({
    orders: [
      { customer_name: '客户A', total_amount: '200' },
      { customer_name: ' ', total_amount: '999' },
      { customer_name: '客户B', total_amount: '340' },
      { customer_name: '客户A', total_amount: '50' },
    ],
  })

  assert.deepEqual(ranking, [
    { name: '客户B', amount: 340 },
    { name: '客户A', amount: 250 },
  ])
})
