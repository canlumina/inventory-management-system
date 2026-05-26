<template>
  <div class="categories">
    <div class="header">
      <h1>商品分类管理</h1>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        新增分类
      </el-button>
    </div>

    <el-card>
      <el-table
        :data="categories"
        style="width: 100%"
        v-loading="loading"
        row-key="id"
        default-expand-all
      >
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
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
              @click="editCategory(scope.row)"
            >
              编辑
            </el-button>
            <el-popconfirm
              title="确定要删除这个分类吗？"
              @confirm="deleteCategory(scope.row.id)"
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
    </el-card>

    <!-- Create/Edit Dialog -->
    <el-dialog
      :title="dialogMode === 'create' ? '新增分类' : '编辑分类'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>

        <el-form-item label="上级分类" prop="parent_id">
          <el-select
            v-model="form.parent_id"
            placeholder="请选择上级分类（可选）"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="category in availableParents"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { categoriesApi } from '@/api/categories'
import type { Category } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()

const categories = ref<Category[]>([])

const form = reactive<Partial<Category>>({
  name: '',
  parent_id: undefined,
  description: '',
})

const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

// 计算可用的父分类（不包括当前编辑的分类及其子分类）
const availableParents = computed(() => {
  if (dialogMode.value === 'create') {
    return flattenCategories(categories.value)
  }
  // 编辑模式下排除自己和子分类
  return flattenCategories(categories.value).filter(cat =>
    cat.id !== form.id && !isDescendant(cat.id!, form.id!)
  )
})

// 扁平化分类树
const flattenCategories = (cats: Category[], level = 0): Category[] => {
  const result: Category[] = []
  for (const cat of cats) {
    result.push({
      ...cat,
      name: '　'.repeat(level) + cat.name // 用全角空格表示层级
    })
    if (cat.children && cat.children.length > 0) {
      result.push(...flattenCategories(cat.children, level + 1))
    }
  }
  return result
}

// 判断是否为子分类
const isDescendant = (categoryId: number, parentId: number): boolean => {
  const findChildren = (cats: Category[]): boolean => {
    for (const cat of cats) {
      if (cat.parent_id === parentId) {
        if (cat.id === categoryId) return true
        if (cat.children && findChildren(cat.children)) return true
      }
    }
    return false
  }
  return findChildren(categories.value)
}

const loadCategories = async () => {
  try {
    loading.value = true
    const data = await categoriesApi.getList()
    categories.value = buildCategoryTree(data)
  } catch (error) {
    ElMessage.error('加载分类列表失败')
  } finally {
    loading.value = false
  }
}

// 构建分类树
const buildCategoryTree = (cats: Category[]): Category[] => {
  const categoryMap = new Map<number, Category>()
  const rootCategories: Category[] = []

  // 创建映射
  cats.forEach(cat => {
    categoryMap.set(cat.id, { ...cat, children: [] })
  })

  // 构建树结构
  cats.forEach(cat => {
    const category = categoryMap.get(cat.id)!
    if (cat.parent_id) {
      const parent = categoryMap.get(cat.parent_id)
      if (parent) {
        parent.children!.push(category)
      }
    } else {
      rootCategories.push(category)
    }
  })

  return rootCategories
}

const showCreateDialog = () => {
  dialogMode.value = 'create'
  resetForm()
  dialogVisible.value = true
}

const editCategory = (category: Category) => {
  dialogMode.value = 'edit'
  Object.assign(form, category)
  dialogVisible.value = true
}

const resetForm = () => {
  Object.assign(form, {
    id: undefined,
    name: '',
    parent_id: undefined,
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
      await categoriesApi.create(form as Omit<Category, 'id' | 'created_at' | 'children'>)
      ElMessage.success('分类创建成功')
    } else {
      await categoriesApi.update(form.id!, form)
      ElMessage.success('分类更新成功')
    }

    dialogVisible.value = false
    loadCategories()
  } catch {
    if (submitting.value) {
      ElMessage.error(dialogMode.value === 'create' ? '分类创建失败' : '分类更新失败')
    }
  } finally {
    submitting.value = false
  }
}

const deleteCategory = async (id: number) => {
  try {
    await categoriesApi.delete(id)
    ElMessage.success('分类删除成功')
    loadCategories()
  } catch (error: any) {
    const message = error?.response?.data?.detail || '删除分类失败'
    ElMessage.error(message)
  }
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.categories .header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.categories h1 {
  margin: 0;
  color: #303133;
}
</style>
