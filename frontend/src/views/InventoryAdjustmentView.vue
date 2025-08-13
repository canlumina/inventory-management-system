<template>
  <div class="inventory-adjustment">
    <div class="header">
      <h1>库存调整</h1>
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        style="max-width: 600px"
      >
        <el-form-item label="商品" prop="product_id">
          <el-select
            v-model="form.product_id"
            placeholder="请选择商品"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="product in products"
              :key="product.id"
              :label="`${product.name} (${product.code})`"
              :value="product.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="调整数量" prop="quantity">
          <el-input-number
            v-model="form.quantity"
            :precision="0"
            style="width: 100%"
            placeholder="正数表示入库，负数表示出库"
          />
          <div class="form-tip">
            正数表示入库，负数表示出库
          </div>
        </el-form-item>

        <el-form-item label="调整原因" prop="reason">
          <el-input
            v-model="form.reason"
            type="textarea"
            :rows="3"
            placeholder="请说明调整原因"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            提交调整
          </el-button>
          <el-button @click="resetForm">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Current Inventory Display -->
    <el-card v-if="selectedProductInventory" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>当前库存信息</span>
        </div>
      </template>
      
      <el-descriptions :column="3">
        <el-descriptions-item label="商品名称">
          {{ selectedProduct?.name }}
        </el-descriptions-item>
        <el-descriptions-item label="当前库存">
          {{ selectedProductInventory.quantity }}
        </el-descriptions-item>
        <el-descriptions-item label="可用库存">
          {{ selectedProductInventory.available_quantity }}
        </el-descriptions-item>
        <el-descriptions-item label="预留库存">
          {{ selectedProductInventory.reserved_quantity }}
        </el-descriptions-item>
        <el-descriptions-item label="最低库存">
          {{ selectedProduct?.min_stock || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="调整后库存">
          <span :class="{ 'adjustment-preview': true, 'negative': adjustedQuantity < 0 }">
            {{ adjustedQuantity }}
          </span>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance } from 'element-plus'
import { inventoryApi } from '@/api/inventory'
import { productsApi } from '@/api/products'
import type { Product, Inventory } from '@/types'

const router = useRouter()
const formRef = ref<FormInstance>()
const submitting = ref(false)

const products = ref<Product[]>([])
const selectedProductInventory = ref<Inventory | null>(null)

const form = reactive({
  product_id: undefined as number | undefined,
  quantity: 0,
  reason: ''
})

const rules = {
  product_id: [{ required: true, message: '请选择商品', trigger: 'change' }],
  quantity: [{ required: true, message: '请输入调整数量', trigger: 'blur' }]
}

const selectedProduct = computed(() => {
  return products.value.find(p => p.id === form.product_id)
})

const adjustedQuantity = computed(() => {
  if (!selectedProductInventory.value || !form.quantity) return selectedProductInventory.value?.quantity || 0
  return selectedProductInventory.value.quantity + form.quantity
})

const loadProducts = async () => {
  try {
    const data = await productsApi.getList()
    products.value = data
  } catch (error) {
    ElMessage.error('加载商品列表失败')
  }
}

const loadProductInventory = async (productId: number) => {
  try {
    const data = await inventoryApi.getByProductId(productId)
    selectedProductInventory.value = data
  } catch (error) {
    selectedProductInventory.value = null
    console.log('获取库存信息失败，可能是新商品')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    await inventoryApi.adjust({
      product_id: form.product_id!,
      quantity: form.quantity,
      reason: form.reason
    })

    ElMessage.success('库存调整成功')
    router.push('/inventory')
  } catch (error) {
    console.error('Adjustment failed:', error)
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.product_id = undefined
  form.quantity = 0
  form.reason = ''
  selectedProductInventory.value = null
  formRef.value?.clearValidate()
}

watch(() => form.product_id, (newProductId) => {
  if (newProductId) {
    loadProductInventory(newProductId)
  } else {
    selectedProductInventory.value = null
  }
})

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.inventory-adjustment .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.inventory-adjustment h1 {
  margin: 0;
  color: #303133;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.card-header {
  font-weight: bold;
  color: #303133;
}

.adjustment-preview {
  font-weight: bold;
  color: #67c23a;
}

.adjustment-preview.negative {
  color: #f56c6c;
}
</style>