<template>
  <div class="customers">
    <div class="header">
      <h1>客户管理</h1>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        新增客户
      </el-button>
    </div>

    <el-card>
      <el-table :data="customers" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="客户名称" />
        <el-table-column prop="contact_person" label="联系人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="140" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="address" label="地址" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="editCustomer(scope.row)"
            >
              编辑
            </el-button>
            <el-popconfirm
              title="确定要删除这个客户吗？"
              @confirm="deleteCustomer(scope.row.id)"
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
      :title="dialogMode === 'create' ? '新增客户' : '编辑客户'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="客户名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" />
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>

        <el-form-item label="地址" prop="address">
          <el-input
            v-model="form.address"
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
import { customersApi } from '@/api/customers'
import type { Customer } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()

const customers = ref<Customer[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const form = reactive<Partial<Customer>>({
  name: '',
  contact_person: '',
  phone: '',
  email: '',
  address: '',
})

const rules = {
  name: [{ required: true, message: '请输入客户名称', trigger: 'blur' }],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const loadCustomers = async () => {
  try {
    loading.value = true
    const data = await customersApi.getList({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    customers.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('加载客户列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

const editCustomer = (customer: Customer) => {
  dialogMode.value = 'edit'
  Object.assign(form, customer)
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    name: '',
    contact_person: '',
    phone: '',
    email: '',
    address: '',
  })
  formRef.value?.clearValidate()
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    if (dialogMode.value === 'create') {
      await customersApi.create(form as Omit<Customer, 'id' | 'created_at'>)
      ElMessage.success('客户创建成功')
    } else {
      await customersApi.update(form.id!, form)
      ElMessage.success('客户更新成功')
    }

    dialogVisible.value = false
    loadCustomers()
  } catch (error) {
    console.error('Submit failed:', error)
  } finally {
    submitting.value = false
  }
}

const deleteCustomer = async (id: number) => {
  try {
    await customersApi.delete(id)
    ElMessage.success('客户删除成功')
    loadCustomers()
  } catch (error) {
    ElMessage.error('删除客户失败')
  }
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadCustomers()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadCustomers()
}

onMounted(() => {
  loadCustomers()
})
</script>

<style scoped>
.customers .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.customers h1 {
  margin: 0;
  color: #303133;
}
</style>