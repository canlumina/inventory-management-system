<template>
  <div class="products">
    <div class="header">
      <h1>商品管理</h1>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        新增商品
      </el-button>
    </div>

    <!-- Search Filter -->
    <SearchFilter
      :loading="loading"
      :initial-filters="{ search: '', category: '' }"
      @search="handleSearch"
      @reset="handleReset"
    >
      <template #filters="{ filters }">
        <el-form-item label="搜索">
          <el-input
            v-model="(filters as any).search"
            placeholder="商品名称/编码"
            clearable
            @keyup.enter="handleSearch(filters)"
            style="width: 250px"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="(filters as any).category"
            placeholder="请选择分类"
            clearable
            style="width: 150px"
          >
            <el-option label="电子产品" value="electronics" />
            <el-option label="服装" value="clothing" />
            <el-option label="食品" value="food" />
          </el-select>
        </el-form-item>
      </template>
    </SearchFilter>

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

      <PaginationWrapper
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        @change="handlePageChange"
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
import { type FormInstance } from 'element-plus'
import { productsApi } from '@/api/products'
import type { Product } from '@/types'
import SearchFilter from '@/components/SearchFilter.vue'
import PaginationWrapper from '@/components/PaginationWrapper.vue'
import { commonRules } from '@/utils/validation'
import { handleApiError, handleSuccess } from '@/utils/errorHandler'

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

// Search filters
const searchFilters = ref<{
  search: string
  category: string
}>({
  search: '',
  category: ''
})

const rules = {
  name: commonRules.name,
  code: commonRules.code,
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  purchase_price: commonRules.price,
  sale_price: commonRules.price,
  min_stock: [{ required: true, message: '请输入最低库存', trigger: 'blur' }],
  description: commonRules.description
}

const loadProducts = async () => {
  try {
    loading.value = true
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    // Add search filters
    if (searchFilters.value.search) {
      params.search = searchFilters.value.search
    }
    if (searchFilters.value.category) {
      params.category = searchFilters.value.category
    }
    
    const data = await productsApi.getList(params)
    products.value = data
    total.value = data.length // In real app, this should come from API
  } catch (error) {
    handleApiError(error, '加载商品列表失败')
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
      handleSuccess('商品创建成功')
    } else {
      await productsApi.update(form.id!, form)
      handleSuccess('商品更新成功')
    }

    dialogVisible.value = false
    loadProducts()
  } catch (error) {
    handleApiError(error, dialogMode.value === 'create' ? '创建商品失败' : '更新商品失败')
  } finally {
    submitting.value = false
  }
}

const deleteProduct = async (id: number) => {
  try {
    await productsApi.delete(id)
    handleSuccess('商品删除成功')
    loadProducts()
  } catch (error) {
    handleApiError(error, '删除商品失败')
  }
}

// Search functionality
const handleSearch = (filters: any) => {
  searchFilters.value = filters
  currentPage.value = 1
  loadProducts()
}

const handleReset = () => {
  searchFilters.value = {
    search: '',
    category: ''
  }
  currentPage.value = 1
  loadProducts()
}

// Pagination
const handlePageChange = (page: number, size: number) => {
  currentPage.value = page
  pageSize.value = size
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