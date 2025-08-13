<template>
  <div class="inventory">
    <div class="header">
      <h1>库存管理</h1>
      <el-button type="warning" @click="$router.push('/inventory-adjustment')">
        <el-icon><EditPen /></el-icon>
        库存调整
      </el-button>
    </div>

    <el-card>
      <el-table :data="inventory" style="width: 100%" v-loading="loading">
        <el-table-column prop="product.code" label="商品编码" width="120" />
        <el-table-column prop="product.name" label="商品名称" />
        <el-table-column prop="product.unit" label="单位" width="80" />
        <el-table-column prop="quantity" label="当前库存" width="100">
          <template #default="scope">
            <span :class="{ 'low-stock': scope.row.quantity <= (scope.row.product?.min_stock || 0) }">
              {{ scope.row.quantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="reserved_quantity" label="预留库存" width="100" />
        <el-table-column prop="available_quantity" label="可用库存" width="100">
          <template #default="scope">
            <span :class="{ 'low-stock': scope.row.available_quantity <= (scope.row.product?.min_stock || 0) }">
              {{ scope.row.available_quantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="库存状态" width="100">
          <template #default="scope">
            <el-tag
              :type="getStockStatusType(scope.row)"
              size="small"
            >
              {{ getStockStatusText(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="更新时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.updated_at) }}
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { inventoryApi } from '@/api/inventory'
import type { Inventory } from '@/types'

const loading = ref(false)
const inventory = ref<Inventory[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadInventory = async () => {
  try {
    loading.value = true
    const data = await inventoryApi.getList({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    inventory.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('加载库存数据失败')
  } finally {
    loading.value = false
  }
}

const getStockStatusType = (row: Inventory) => {
  const minStock = row.product?.min_stock || 0
  if (row.available_quantity === 0) return 'danger'
  if (row.available_quantity <= minStock) return 'warning'
  return 'success'
}

const getStockStatusText = (row: Inventory) => {
  const minStock = row.product?.min_stock || 0
  if (row.available_quantity === 0) return '缺货'
  if (row.available_quantity <= minStock) return '预警'
  return '正常'
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadInventory()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadInventory()
}

onMounted(() => {
  loadInventory()
})
</script>

<style scoped>
.inventory .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.inventory h1 {
  margin: 0;
  color: #303133;
}

.low-stock {
  color: #f56c6c;
  font-weight: bold;
}
</style>