<template>
  <div class="dashboard">
    <h1>仪表盘</h1>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon products">
              <el-icon><Goods /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.products }}</div>
              <div class="stat-label">商品总数</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon inventory">
              <el-icon><Box /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.lowStock }}</div>
              <div class="stat-label">低库存商品</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon purchases">
              <el-icon><ShoppingCart /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.pendingPurchases }}</div>
              <div class="stat-label">待处理采购单</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon sales">
              <el-icon><Sell /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.pendingSales }}</div>
              <div class="stat-label">待处理销售单</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近操作</span>
            </div>
          </template>
          
          <el-timeline>
            <el-timeline-item
              v-for="activity in activities"
              :key="activity.id"
              :timestamp="activity.timestamp"
              :color="activity.color"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>库存预警</span>
            </div>
          </template>
          
          <el-table :data="lowStockProducts" style="width: 100%">
            <el-table-column prop="name" label="商品名称" />
            <el-table-column prop="current_stock" label="当前库存" width="100" />
            <el-table-column prop="min_stock" label="最低库存" width="100" />
            <el-table-column label="状态" width="80">
              <template #default="scope">
                <el-tag
                  :type="scope.row.current_stock === 0 ? 'danger' : 'warning'"
                  size="small"
                >
                  {{ scope.row.current_stock === 0 ? '缺货' : '预警' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const stats = ref({
  products: 156,
  lowStock: 8,
  pendingPurchases: 12,
  pendingSales: 5
})

const activities = ref([
  {
    id: 1,
    content: '新增商品：iPhone 14 Pro',
    timestamp: '2025-01-20 14:30',
    color: '#409EFF'
  },
  {
    id: 2,
    content: '采购单 PO20250120001 已确认',
    timestamp: '2025-01-20 11:20',
    color: '#67C23A'
  },
  {
    id: 3,
    content: '销售单 SO20250120002 已发货',
    timestamp: '2025-01-20 09:15',
    color: '#E6A23C'
  },
  {
    id: 4,
    content: '库存调整：小米13 +50件',
    timestamp: '2025-01-19 16:40',
    color: '#F56C6C'
  }
])

const lowStockProducts = ref([
  {
    name: 'iPhone 13',
    current_stock: 0,
    min_stock: 10
  },
  {
    name: '小米12',
    current_stock: 3,
    min_stock: 20
  },
  {
    name: 'iPad Air',
    current_stock: 5,
    min_stock: 15
  },
  {
    name: 'MacBook Pro',
    current_stock: 2,
    min_stock: 8
  }
])

onMounted(() => {
  // Load dashboard data
  console.log('Dashboard mounted')
})
</script>

<style scoped>
.dashboard h1 {
  margin-bottom: 30px;
  color: #303133;
}

.stats-row {
  margin-bottom: 30px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 10px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.stat-icon.products {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-icon.inventory {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.stat-icon.purchases {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.stat-icon.sales {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.content-row {
  margin-bottom: 30px;
}

.card-header {
  font-weight: bold;
  color: #303133;
}
</style>