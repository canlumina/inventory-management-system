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
              <div class="stat-number">{{ dashboardData?.total_products || 0 }}</div>
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
              <div class="stat-number">{{ dashboardData?.low_stock_alerts || 0 }}</div>
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
              <div class="stat-number">{{ dashboardData?.pending_purchase_orders || 0 }}</div>
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
              <div class="stat-number">{{ dashboardData?.pending_sales_orders || 0 }}</div>
              <div class="stat-label">待处理销售单</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Additional stats row -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon revenue">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">¥{{ dashboardData?.monthly_revenue || 0 }}</div>
              <div class="stat-label">本月收入</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon orders">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ dashboardData?.monthly_orders || 0 }}</div>
              <div class="stat-label">本月订单</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon value">
              <el-icon><Shop /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">¥{{ dashboardData?.total_inventory_value || 0 }}</div>
              <div class="stat-label">库存总值</div>
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
          
          <el-table :data="lowStockProducts" style="width: 100%" v-loading="loading">
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="current_stock" label="当前库存" width="100" />
            <el-table-column prop="min_stock" label="最低库存" width="100" />
            <el-table-column prop="stock_status" label="状态" width="80">
              <template #default="scope">
                <el-tag
                  :type="scope.row.stock_status === 'out_of_stock' ? 'danger' : 'warning'"
                  size="small"
                >
                  {{ scope.row.stock_status === 'out_of_stock' ? '缺货' : '预警' }}
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
import { ElMessage } from 'element-plus'
import { reportsApi } from '@/api/reports'
import type { DashboardSummary, InventoryReport } from '@/api/reports'

const loading = ref(false)
const dashboardData = ref<DashboardSummary | null>(null)
const lowStockProducts = ref<any[]>([])

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

const loadDashboardData = async () => {
  try {
    loading.value = true
    dashboardData.value = await reportsApi.getDashboardData()
  } catch (error) {
    ElMessage.error('加载仪表盘数据失败')
  } finally {
    loading.value = false
  }
}

const loadLowStockProducts = async () => {
  try {
    const inventoryReport: InventoryReport = await reportsApi.getInventoryReport()
    // Filter products with low stock or out of stock
    lowStockProducts.value = inventoryReport.items.filter(item => 
      item.stock_status === 'warning' || item.stock_status === 'out_of_stock'
    ).slice(0, 10) // Show top 10 low stock items
  } catch (error) {
    ElMessage.error('加载库存预警数据失败')
  }
}

onMounted(() => {
  loadDashboardData()
  loadLowStockProducts()
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

.stat-icon.revenue {
  background: linear-gradient(135deg, #fa709a, #fee140);
}

.stat-icon.orders {
  background: linear-gradient(135deg, #a8edea, #fed6e3);
  color: #333 !important;
}

.stat-icon.value {
  background: linear-gradient(135deg, #ffecd2, #fcb69f);
  color: #333 !important;
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