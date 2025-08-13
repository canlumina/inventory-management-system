<template>
  <div class="purchases">
    <div class="header">
      <h1>采购管理</h1>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        新增采购单
      </el-button>
    </div>

    <el-card>
      <el-table :data="purchases" style="width: 100%" v-loading="loading">
        <el-table-column prop="order_number" label="采购单号" width="160" />
        <el-table-column prop="supplier.name" label="供应商" />
        <el-table-column prop="total_amount" label="采购金额" width="120">
          <template #default="scope">
            ¥{{ scope.row.total_amount }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order_date" label="采购日期" width="160">
          <template #default="scope">
            {{ formatDateTime(scope.row.order_date) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="viewPurchase(scope.row)"
            >
              查看
            </el-button>
            <el-button
              v-if="scope.row.status === 'confirmed'"
              type="success"
              size="small"
              @click="receivePurchase(scope.row)"
            >
              入库
            </el-button>
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

    <!-- Create Purchase Order Dialog -->
    <el-dialog
      title="新增采购单"
      v-model="createDialogVisible"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="供应商" prop="supplier_id">
          <el-select
            v-model="form.supplier_id"
            placeholder="请选择供应商"
            style="width: 100%"
          >
            <el-option
              v-for="supplier in suppliers"
              :key="supplier.id"
              :label="supplier.name"
              :value="supplier.id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <div class="items-section">
        <div class="section-header">
          <h3>采购明细</h3>
          <el-button type="primary" @click="addItem">
            <el-icon><Plus /></el-icon>
            添加商品
          </el-button>
        </div>

        <el-table :data="form.items" style="width: 100%">
          <el-table-column label="商品" width="200">
            <template #default="scope">
              <el-select
                v-model="scope.row.product_id"
                placeholder="选择商品"
                @change="updateItemPrice(scope.$index)"
                style="width: 100%"
              >
                <el-option
                  v-for="product in products"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="数量" width="120">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.quantity"
                :min="1"
                @change="updateItemTotal(scope.$index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="单价" width="120">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.unit_price"
                :precision="2"
                :min="0"
                @change="updateItemTotal(scope.$index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="小计" width="120">
            <template #default="scope">
              ¥{{ scope.row.total_price || 0 }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button
                type="danger"
                size="small"
                @click="removeItem(scope.$index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="total-amount">
          <strong>总金额：¥{{ totalAmount }}</strong>
        </div>
      </div>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          创建采购单
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { purchasesApi } from '@/api/purchases'
import { suppliersApi } from '@/api/suppliers'
import { productsApi } from '@/api/products'
import type { PurchaseOrder, PurchaseOrderItem, Supplier, Product } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const createDialogVisible = ref(false)
const formRef = ref<FormInstance>()

const purchases = ref<PurchaseOrder[]>([])
const suppliers = ref<Supplier[]>([])
const products = ref<Product[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const form = reactive<{
  supplier_id: number | undefined
  items: PurchaseOrderItem[]
}>({
  supplier_id: undefined,
  items: []
})

const rules = {
  supplier_id: [{ required: true, message: '请选择供应商', trigger: 'change' }]
}

const totalAmount = computed(() => {
  return form.items.reduce((sum, item) => sum + (item.total_price || 0), 0)
})

const loadPurchases = async () => {
  try {
    loading.value = true
    const data = await purchasesApi.getList({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    purchases.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('加载采购单列表失败')
  } finally {
    loading.value = false
  }
}

const loadSuppliers = async () => {
  try {
    const data = await suppliersApi.getList()
    suppliers.value = data
  } catch (error) {
    ElMessage.error('加载供应商列表失败')
  }
}

const loadProducts = async () => {
  try {
    const data = await productsApi.getList()
    products.value = data
  } catch (error) {
    ElMessage.error('加载商品列表失败')
  }
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: '',
    confirmed: 'warning',
    received: 'success',
    cancelled: 'danger'
  }
  return types[status] || ''
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待确认',
    confirmed: '已确认',
    received: '已入库',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const showCreateDialog = () => {
  resetForm()
  createDialogVisible.value = true
}

const resetForm = () => {
  form.supplier_id = undefined
  form.items = []
  addItem()
}

const addItem = () => {
  form.items.push({
    product_id: 0,
    quantity: 1,
    unit_price: 0,
    total_price: 0
  })
}

const removeItem = (index: number) => {
  form.items.splice(index, 1)
}

const updateItemPrice = (index: number) => {
  const item = form.items[index]
  const product = products.value.find(p => p.id === item.product_id)
  if (product && product.purchase_price) {
    item.unit_price = product.purchase_price
    updateItemTotal(index)
  }
}

const updateItemTotal = (index: number) => {
  const item = form.items[index]
  item.total_price = item.quantity * item.unit_price
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    if (form.items.length === 0) {
      ElMessage.error('请添加采购商品')
      return
    }

    submitting.value = true
    await purchasesApi.create({
      supplier_id: form.supplier_id!,
      items: form.items
    })
    
    ElMessage.success('采购单创建成功')
    createDialogVisible.value = false
    loadPurchases()
  } catch (error) {
    console.error('Submit failed:', error)
  } finally {
    submitting.value = false
  }
}

const viewPurchase = (purchase: PurchaseOrder) => {
  console.log('View purchase:', purchase)
}

const receivePurchase = async (purchase: PurchaseOrder) => {
  try {
    await ElMessageBox.confirm(
      `确定要对采购单 ${purchase.order_number} 进行入库操作吗？`,
      '确认入库',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await purchasesApi.receive(purchase.id)
    ElMessage.success('采购单入库成功')
    loadPurchases()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('入库操作失败')
    }
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadPurchases()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadPurchases()
}

onMounted(() => {
  loadPurchases()
  loadSuppliers()
  loadProducts()
})
</script>

<style scoped>
.purchases .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.purchases h1 {
  margin: 0;
  color: #303133;
}

.items-section {
  margin-top: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.section-header h3 {
  margin: 0;
  color: #303133;
}

.total-amount {
  text-align: right;
  margin-top: 10px;
  font-size: 16px;
}
</style>