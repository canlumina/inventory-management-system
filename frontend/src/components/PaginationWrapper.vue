<template>
  <el-pagination
    v-model:current-page="currentPageModel"
    v-model:page-size="pageSizeModel"
    :total="total"
    :page-sizes="pageSizes"
    :layout="layout"
    :background="background"
    :small="small"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    class="pagination-wrapper"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  currentPage: number
  pageSize: number
  total: number
  pageSizes?: number[]
  layout?: string
  background?: boolean
  small?: boolean
}

interface Emits {
  (e: 'update:currentPage', value: number): void
  (e: 'update:pageSize', value: number): void
  (e: 'change', currentPage: number, pageSize: number): void
}

const props = withDefaults(defineProps<Props>(), {
  pageSizes: () => [10, 20, 50, 100],
  layout: 'total, sizes, prev, pager, next, jumper',
  background: true,
  small: false
})

const emit = defineEmits<Emits>()

const currentPageModel = computed({
  get: () => props.currentPage,
  set: (value: number) => emit('update:currentPage', value)
})

const pageSizeModel = computed({
  get: () => props.pageSize,
  set: (value: number) => emit('update:pageSize', value)
})

const handleSizeChange = (size: number) => {
  emit('change', 1, size) // Reset to first page when changing page size
}

const handleCurrentChange = (page: number) => {
  emit('change', page, props.pageSize)
}
</script>

<style scoped>
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>