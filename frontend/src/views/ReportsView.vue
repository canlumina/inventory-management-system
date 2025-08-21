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

              <div style="margin-bottom: 20px" v-if="salesReport">
                <el-row :gutter="16">
                  <el-col :span="4">
                    <el-statistic title="销售单总数" :value="salesReport.summary.total_orders" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="销售总额" :value="`¥${salesReport.summary.total_amount}`" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="实际收入" :value="`¥${salesReport.summary.total_revenue}`" />
                  </el-col>
                  <el-col :span="3">
                    <el-statistic title="待确认" :value="salesReport.summary.pending_orders" />
                  </el-col>
                  <el-col :span="3">
                    <el-statistic title="已确认" :value="salesReport.summary.confirmed_orders" />
                  </el-col>
                  <el-col :span="3">
                    <el-statistic title="已发货" :value="salesReport.summary.shipped_orders" />
                  </el-col>
                  <el-col :span="3">
                    <el-statistic title="已完成" :value="salesReport.summary.delivered_orders" />
                  </el-col>
                </el-row>
              </div>

              <el-table :data="salesReport?.orders" style="width: 100%" v-loading="salesReportLoading">
                <el-table-column prop="order_number" label="销售单号" width="160" />
                <el-table-column prop="customer_name" label="客户" />
                <el-table-column prop="order_date" label="销售日期" width="120">
                  <template #default="scope">
                    {{ formatDateTime(scope.row.order_date) }}
                  </template>
                </el-table-column>
                <el-table-column prop="total_amount" label="销售金额" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.total_amount }}
                  </template>
                </el-table-column>
                <el-table-column prop="items_count" label="商品数量" width="100" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="scope">
                    <el-tag :type="getSalesStatusType(scope.row.status)" size="small">
                      {{ getSalesStatusText(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="库存报表" name="inventory">
              <div style="margin-bottom: 20px" v-if="inventoryReport">
                <el-row :gutter="16">
                  <el-col :span="6">
                    <el-statistic title="商品总数" :value="inventoryReport.total_products" />
                  </el-col>
                  <el-col :span="6">
                    <el-statistic title="库存总价值" :value="`¥${inventoryReport.total_stock_value}`" />
                  </el-col>
                  <el-col :span="6">
                    <el-statistic title="低库存商品" :value="inventoryReport.low_stock_products" />
                  </el-col>
                  <el-col :span="6">
                    <el-statistic title="缺货商品" :value="inventoryReport.out_of_stock_products" />
                  </el-col>
                </el-row>
              </div>
              
              <el-table :data="inventoryReport?.items" style="width: 100%" v-loading="inventoryReportLoading">
                <el-table-column prop="product_name" label="商品名称" />
                <el-table-column prop="product_code" label="商品编码" width="120" />
                <el-table-column prop="current_stock" label="当前库存" width="100" />
                <el-table-column prop="available_stock" label="可用库存" width="100" />
                <el-table-column prop="stock_value" label="库存价值" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.stock_value }}
                  </template>
                </el-table-column>
                <el-table-column prop="stock_status" label="库存状态" width="100">
                  <template #default="scope">
                    <el-tag
                      :type="scope.row.stock_status === 'out_of_stock' ? 'danger' : scope.row.stock_status === 'warning' ? 'warning' : 'success'"
                      size="small"
                    >
                      {{ scope.row.stock_status === 'out_of_stock' ? '缺货' : scope.row.stock_status === 'warning' ? '预警' : '正常' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="采购报表" name="purchase">
              <div style="margin-bottom: 20px" v-if="purchaseReport">
                <el-row :gutter="16">
                  <el-col :span="4">
                    <el-statistic title="采购单总数" :value="purchaseReport.summary.total_orders" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="采购总金额" :value="`¥${purchaseReport.summary.total_amount}`" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="待确认" :value="purchaseReport.summary.pending_orders" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="已确认" :value="purchaseReport.summary.confirmed_orders" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="已入库" :value="purchaseReport.summary.received_orders" />
                  </el-col>
                  <el-col :span="4">
                    <el-statistic title="已取消" :value="purchaseReport.summary.cancelled_orders" />
                  </el-col>
                </el-row>
              </div>
              
              <el-table :data="purchaseReport?.orders" style="width: 100%" v-loading="purchaseReportLoading">
                <el-table-column prop="order_number" label="采购单号" width="160" />
                <el-table-column prop="supplier_name" label="供应商" />
                <el-table-column prop="order_date" label="采购日期" width="120">
                  <template #default="scope">
                    {{ formatDateTime(scope.row.order_date) }}
                  </template>
                </el-table-column>
                <el-table-column prop="total_amount" label="采购金额" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.total_amount }}
                  </template>
                </el-table-column>
                <el-table-column prop="items_count" label="商品数量" width="100" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="scope">
                    <el-tag :type="getStatusType(scope.row.status)" size="small">
                      {{ getStatusText(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>
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
import { reportsApi } from '@/api/reports'
import type { InventoryReport, SalesReport, PurchaseReport, FinancialSummary } from '@/api/reports'

const salesDateRange = ref([])
const activeTab = ref('sales')
const salesReportLoading = ref(false)
const inventoryReportLoading = ref(false)
const purchaseReportLoading = ref(false)

// Report data
const inventoryReport = ref<InventoryReport | null>(null)
const salesReport = ref<SalesReport | null>(null)
const purchaseReport = ref<PurchaseReport | null>(null)
const financialReport = ref<FinancialSummary | null>(null)

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

// API loading functions
const loadInventoryReport = async () => {
  try {
    inventoryReportLoading.value = true
    inventoryReport.value = await reportsApi.getInventoryReport()
  } catch (error) {
    ElMessage.error('加载库存报表失败')
  } finally {
    inventoryReportLoading.value = false
  }
}

const loadSalesReport = async () => {
  try {
    salesReportLoading.value = true
    const params: any = {}
    if (salesReportForm.dateRange && salesReportForm.dateRange.length === 2) {
      params.start_date = salesReportForm.dateRange[0]
      params.end_date = salesReportForm.dateRange[1]
    }
    salesReport.value = await reportsApi.getSalesReport(params)
  } catch (error) {
    ElMessage.error('加载销售报表失败')
  } finally {
    salesReportLoading.value = false
  }
}

const loadPurchaseReport = async () => {
  try {
    purchaseReportLoading.value = true
    purchaseReport.value = await reportsApi.getPurchaseReport()
  } catch (error) {
    ElMessage.error('加载采购报表失败')
  } finally {
    purchaseReportLoading.value = false
  }
}

const loadFinancialReport = async () => {
  try {
    financialReport.value = await reportsApi.getFinancialReport()
  } catch (error) {
    ElMessage.error('加载财务报表失败')
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

// Helper functions for status formatting
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: '',
    confirmed: 'warning',
    received: 'success',
    cancelled: 'danger'
  }
  return types[status] || ''
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待确认',
    confirmed: '已确认',
    received: '已入库',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const getSalesStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: '',
    confirmed: 'warning',
    shipped: 'info',
    delivered: 'success',
    cancelled: 'danger'
  }
  return types[status] || ''
}

const getSalesStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待确认',
    confirmed: '已确认',
    shipped: '已发货',
    delivered: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(() => {
  // 初始化加载所有报表数据
  loadInventoryReport()
  loadSalesReport()
  loadPurchaseReport()
  loadFinancialReport()
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