<template>
  <div class="loading-container" v-if="show">
    <div class="loading-spinner">
      <el-icon class="is-loading" :size="size">
        <Loading />
      </el-icon>
      <p v-if="text" class="loading-text">{{ text }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  show: boolean
  text?: string
  size?: number
}

withDefaults(defineProps<Props>(), {
  text: '加载中...',
  size: 40
})
</script>

<style scoped>
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-spinner {
  text-align: center;
}

.loading-text {
  margin-top: 16px;
  color: #666;
  font-size: 14px;
}

.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>