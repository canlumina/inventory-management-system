<template>
  <div id="app">
    <el-container>
      <!-- Header -->
      <el-header>
        <div class="header-content">
          <div class="logo">
            <h2>进销存管理系统</h2>
          </div>
          <div class="user-info">
            <el-dropdown v-if="userStore.user">
              <span class="el-dropdown-link">
                {{ userStore.user.username }}
                <el-icon class="el-icon--right">
                  <arrow-down />
                </el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-button v-else @click="$router.push('/login')" type="primary">登录</el-button>
          </div>
        </div>
      </el-header>

      <el-container>
        <!-- Sidebar -->
        <el-aside width="200px" v-if="userStore.user">
          <el-menu
            :default-active="$route.path"
            class="el-menu-vertical"
            router
          >
            <el-menu-item index="/dashboard">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            
            <el-sub-menu index="products">
              <template #title>
                <el-icon><Goods /></el-icon>
                <span>商品管理</span>
              </template>
              <el-menu-item index="/products">商品列表</el-menu-item>
              <el-menu-item index="/categories">商品分类</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="inventory">
              <template #title>
                <el-icon><Box /></el-icon>
                <span>库存管理</span>
              </template>
              <el-menu-item index="/inventory">库存查询</el-menu-item>
              <el-menu-item index="/inventory-adjustment">库存调整</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="purchase">
              <template #title>
                <el-icon><ShoppingCart /></el-icon>
                <span>采购管理</span>
              </template>
              <el-menu-item index="/purchases">采购单</el-menu-item>
              <el-menu-item index="/suppliers">供应商</el-menu-item>
            </el-sub-menu>

            <el-sub-menu index="sales">
              <template #title>
                <el-icon><Sell /></el-icon>
                <span>销售管理</span>
              </template>
              <el-menu-item index="/sales">销售单</el-menu-item>
              <el-menu-item index="/customers">客户管理</el-menu-item>
            </el-sub-menu>

            <el-menu-item index="/reports">
              <el-icon><DataAnalysis /></el-icon>
              <span>报表统计</span>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- Main Content -->
        <el-main>
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <keep-alive>
                <component :is="Component" />
              </keep-alive>
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('退出登录成功')
}
</script>

<style scoped>
#app {
  height: 100vh;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  background-color: #409eff;
  color: white;
}

.logo h2 {
  margin: 0;
  color: white;
}

.el-dropdown-link {
  cursor: pointer;
  color: white;
}

.el-aside {
  background-color: #f5f5f5;
}

.el-menu-vertical {
  border-right: none;
}

.el-main {
  padding: 20px;
  background-color: #f0f2f5;
  position: relative;
}

/* Page transition effects */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Hover effects for menu items */
.el-menu-item:hover {
  background-color: #ecf5ff !important;
}

.el-sub-menu__title:hover {
  background-color: #ecf5ff !important;
}

/* Active menu item styling */
.el-menu-item.is-active {
  background-color: #409eff !important;
  color: white !important;
}

/* Scrollbar styling for better UX */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>