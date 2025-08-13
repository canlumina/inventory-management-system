<template>
  <div class="products">
    <div class="header">
      <h1>商品管理</h1>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        新增商品
      </el-button>
    </div>

    <el-card>
      <el-table :data="products" style="width: 100%" v-loading="loading">
        <el-table-column prop="code" label="商品编码" width="120" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="purchase_price" label="进价" width="100">
          <template #default="scope">
            ¥{{ scope.row.purchase_price || 0 }}
          </template>
        </el-table-column>
        <el-table-column prop="sale_price" label="售价" width="100">
          <template #default="scope">
            ¥{{ scope.row.sale_price || 0 }}
          </template>
        </el-table-column>
        <el-table-column prop="min_stock" label="最低库存" width="100" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="editProduct(scope.row)"
            >
              编辑
            </el-button>
            <el-popconfirm
              title="确定要删除这个商品吗？"
              @confirm="deleteProduct(scope.row.id)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  size="small"
                >
                  删除
                </el-button>
              </template>
            </el-popconfirm>
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

    <!-- Create/Edit Dialog -->
    <el-dialog
      :title="dialogMode === 'create' ? '新增商品' : '编辑商品'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        
        <el-form-item label="商品编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>

        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="进价" prop="purchase_price">
              <el-input-number
                v-model="form.purchase_price"
                :precision="2"
                :min="0"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="售价" prop="sale_price">
              <el-input-number
                v-model="form.sale_price"
                :precision="2"
                :min="0"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="最低库存" prop="min_stock">
          <el-input-number
            v-model="form.min_stock"
            :min="0"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { productsApi } from '@/api/products'
import type { Product } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()

const products = ref<Product[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const form = reactive<Partial<Product>>({
  name: '',
  code: '',
  unit: '件',
  purchase_price: undefined,
  sale_price: undefined,
  min_stock: 0,
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入商品编码', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
}

const loadProducts = async () => {
  try {
    loading.value = true
    const data = await productsApi.getList({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    products.value = data
    total.value = data.length // In real app, this should come from API
  } catch (error) {
    ElMessage.error('加载商品列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

const editProduct = (product: Product) => {
  dialogMode.value = 'edit'
  Object.assign(form, product)
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    name: '',
    code: '',
    unit: '件',
    purchase_price: undefined,
    sale_price: undefined,
    min_stock: 0,
    description: '',
  })
  formRef.value?.clearValidate()
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    if (dialogMode.value === 'create') {
      await productsApi.create(form as Omit<Product, 'id' | 'created_at' | 'updated_at'>)
      ElMessage.success('商品创建成功')
    } else {
      await productsApi.update(form.id!, form)
      ElMessage.success('商品更新成功')
    }

    dialogVisible.value = false
    loadProducts()
  } catch (error) {
    console.error('Submit failed:', error)
  } finally {
    submitting.value = false
  }
}

const deleteProduct = async (id: number) => {
  try {
    await productsApi.delete(id)
    ElMessage.success('商品删除成功')
    loadProducts()
  } catch (error) {
    ElMessage.error('删除商品失败')
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadProducts()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadProducts()
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.products .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.products h1 {
  margin: 0;
  color: #303133;
}
</style>