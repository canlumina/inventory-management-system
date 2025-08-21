<template>
  <el-card class="search-filter" shadow="never">
    <el-form :model="filters" :inline="true" @submit.prevent="handleSearch">
      <slot name="filters" :filters="filters" :search="handleSearch" :reset="handleReset">
        <!-- Default search input -->
        <el-form-item label="搜索">
          <el-input
            v-model="filters.search"
            placeholder="请输入搜索关键词"
            clearable
            @keyup.enter="handleSearch"
            style="width: 250px"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
      </slot>
      
      <el-form-item>
        <el-button type="primary" @click="handleSearch" :loading="loading">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="handleReset">
          <el-icon><Refresh /></el-icon>
          重置
        </el-button>
        <slot name="actions" :filters="filters" :search="handleSearch" :reset="handleReset" />
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

interface Props {
  loading?: boolean
  initialFilters?: Record<string, any>
}

interface Emits {
  (e: 'search', filters: Record<string, any>): void
  (e: 'reset'): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  initialFilters: () => ({})
})

const emit = defineEmits<Emits>()

const filters = reactive({ 
  search: '', 
  ...props.initialFilters 
})

const handleSearch = () => {
  emit('search', { ...filters })
}

const handleReset = () => {
  Object.keys(filters).forEach((key: string) => {
    if (key in props.initialFilters) {
      ;(filters as any)[key] = props.initialFilters[key]
    } else {
      ;(filters as any)[key] = ''
    }
  })
  emit('reset')
}

// Watch for changes in initialFilters prop
watch(
  () => props.initialFilters,
  (newFilters) => {
    Object.assign(filters, newFilters)
  },
  { deep: true }
)

defineExpose({
  filters,
  search: handleSearch,
  reset: handleReset
})
</script>

<style scoped>
.search-filter {
  margin-bottom: 16px;
}

.search-filter :deep(.el-card__body) {
  padding: 16px;
}

.search-filter :deep(.el-form--inline .el-form-item) {
  margin-bottom: 0;
}
</style>