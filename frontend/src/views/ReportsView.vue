<template>
  <div class="reports">
    <h1>报表统计</h1>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>销售趋势</span>
              <el-date-picker
                v-model="salesDateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                size="small"
              />
            </div>
          </template>
          
          <div class="chart-container">
            <!-- 这里可以集成 ECharts 或其他图表库 -->
            <div class="chart-placeholder">
              <el-icon size="48" color="#ccc"><TrendCharts /></el-icon>
              <p>销售趋势图表</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>库存分布</span>
            </div>
          </template>
          
          <div class="chart-container">
            <div class="chart-placeholder">
              <el-icon size="48" color="#ccc"><PieChart /></el-icon>
              <p>库存分布图表</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>销售排行榜</span>
            </div>
          </template>
          
          <el-table :data="topProducts" style="width: 100%">
            <el-table-column prop="name" label="商品名称" />
            <el-table-column prop="sales" label="销量" width="80" />
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>供应商排行</span>
            </div>
          </template>
          
          <el-table :data="topSuppliers" style="width: 100%">
            <el-table-column prop="name" label="供应商名称" />
            <el-table-column prop="amount" label="采购金额" width="100">
              <template #default="scope">
                ¥{{ scope.row.amount }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>客户排行</span>
            </div>
          </template>
          
          <el-table :data="topCustomers" style="width: 100%">
            <el-table-column prop="name" label="客户名称" />
            <el-table-column prop="amount" label="销售金额" width="100">
              <template #default="scope">
                ¥{{ scope.row.amount }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>详细报表</span>
              <div>
                <el-button type="primary" @click="exportSalesReport">
                  <el-icon><Download /></el-icon>
                  导出销售报表
                </el-button>
                <el-button @click="exportInventoryReport">
                  <el-icon><Download /></el-icon>
                  导出库存报表
                </el-button>
              </div>
            </div>
          </template>

          <el-tabs v-model="activeTab">
            <el-tab-pane label="销售报表" name="sales">
              <el-form :model="salesReportForm" :inline="true">
                <el-form-item label="日期范围">
                  <el-date-picker
                    v-model="salesReportForm.dateRange"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="loadSalesReport">查询</el-button>
                </el-form-item>
              </el-form>

              <el-table :data="salesReportData" style="width: 100%" v-loading="salesReportLoading">
                <el-table-column prop="date" label="日期" width="120" />
                <el-table-column prop="orders" label="订单数" width="100" />
                <el-table-column prop="amount" label="销售金额" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.amount }}
                  </template>
                </el-table-column>
                <el-table-column prop="profit" label="利润" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.profit }}
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="库存报表" name="inventory">
              <el-table :data="inventoryReportData" style="width: 100%" v-loading="inventoryReportLoading">
                <el-table-column prop="product_name" label="商品名称" />
                <el-table-column prop="current_stock" label="当前库存" width="100" />
                <el-table-column prop="stock_value" label="库存价值" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.stock_value }}
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="库存状态" width="100">
                  <template #default="scope">
                    <el-tag
                      :type="scope.row.current_stock === 0 ? 'danger' : scope.row.current_stock <= scope.row.min_stock ? 'warning' : 'success'"
                      size="small"
                    >
                      {{ scope.row.current_stock === 0 ? '缺货' : scope.row.current_stock <= scope.row.min_stock ? '预警' : '正常' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="采购报表" name="purchase">
              <el-table :data="purchaseReportData" style="width: 100%" v-loading="purchaseReportLoading">
                <el-table-column prop="date" label="日期" width="120" />
                <el-table-column prop="orders" label="采购单数" width="100" />
                <el-table-column prop="amount" label="采购金额" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.amount }}
                  </template>
                </el-table-column>
                <el-table-column prop="supplier_name" label="主要供应商" />
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const salesDateRange = ref([])
const activeTab = ref('sales')
const salesReportLoading = ref(false)
const inventoryReportLoading = ref(false)
const purchaseReportLoading = ref(false)

// 模拟数据
const topProducts = ref([
  { name: 'iPhone 14 Pro', sales: 150 },
  { name: '小米 13', sales: 120 },
  { name: 'iPad Air', sales: 95 },
  { name: 'MacBook Pro', sales: 88 },
  { name: '华为 P50', sales: 76 }
])

const topSuppliers = ref([
  { name: '苹果供应商', amount: 1250000 },
  { name: '小米供应商', amount: 980000 },
  { name: '华为供应商', amount: 750000 },
  { name: '三星供应商', amount: 650000 }
])

const topCustomers = ref([
  { name: '大客户A', amount: 580000 },
  { name: '企业客户B', amount: 450000 },
  { name: '零售客户C', amount: 320000 },
  { name: '经销商D', amount: 280000 }
])

const salesReportForm = reactive({
  dateRange: []
})

const salesReportData = ref([
  { date: '2025-01-15', orders: 25, amount: 125000, profit: 25000 },
  { date: '2025-01-16', orders: 32, amount: 156000, profit: 31200 },
  { date: '2025-01-17', orders: 28, amount: 140000, profit: 28000 },
  { date: '2025-01-18', orders: 35, amount: 175000, profit: 35000 },
  { date: '2025-01-19', orders: 30, amount: 150000, profit: 30000 }
])

const inventoryReportData = ref([
  { product_name: 'iPhone 14 Pro', current_stock: 45, min_stock: 10, stock_value: 450000 },
  { product_name: '小米 13', current_stock: 0, min_stock: 20, stock_value: 0 },
  { product_name: 'iPad Air', current_stock: 8, min_stock: 15, stock_value: 40000 },
  { product_name: 'MacBook Pro', current_stock: 25, min_stock: 8, stock_value: 375000 }
])

const purchaseReportData = ref([
  { date: '2025-01-15', orders: 8, amount: 80000, supplier_name: '苹果供应商' },
  { date: '2025-01-16', orders: 12, amount: 120000, supplier_name: '小米供应商' },
  { date: '2025-01-17', orders: 6, amount: 60000, supplier_name: '华为供应商' },
  { date: '2025-01-18', orders: 10, amount: 100000, supplier_name: '三星供应商' }
])

const loadSalesReport = async () => {
  try {
    salesReportLoading.value = true
    // 这里调用 API 加载销售报表数据
    // const data = await reportsApi.getSalesReport(salesReportForm.dateRange)
    // salesReportData.value = data
  } catch (error) {
    ElMessage.error('加载销售报表失败')
  } finally {
    salesReportLoading.value = false
  }
}

const exportSalesReport = () => {
  ElMessage.success('销售报表导出成功')
  // 这里实现导出逻辑
}

const exportInventoryReport = () => {
  ElMessage.success('库存报表导出成功')
  // 这里实现导出逻辑
}

onMounted(() => {
  // 初始化加载报表数据
  console.log('Reports page mounted')
})
</script>

<style scoped>
.reports h1 {
  margin-bottom: 30px;
  color: #303133;
}

.chart-card {
  height: 300px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #303133;
}

.chart-container {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #ccc;
}

.chart-placeholder p {
  margin-top: 10px;
  font-size: 14px;
}
</style>