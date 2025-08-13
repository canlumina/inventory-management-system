# 进销存系统设计文档

## 系统架构

### 前端架构（Vue 3）
- **框架**: Vue 3 + TypeScript
- **状态管理**: Pinia
- **路由**: Vue Router
- **UI组件**: Element Plus
- **构建工具**: Vite

### 后端架构（Python）
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **认证**: JWT
- **API文档**: 自动生成的OpenAPI

### 系统模块

1. **用户管理模块**
   - 用户登录/注册
   - 角色权限管理
   - 用户信息管理

2. **商品管理模块**
   - 商品信息维护
   - 商品分类管理
   - 商品规格管理

3. **供应商管理模块**
   - 供应商信息管理
   - 供应商联系人管理

4. **客户管理模块**
   - 客户信息管理
   - 客户联系记录

5. **采购管理模块**
   - 采购计划
   - 采购订单管理
   - 采购入库

6. **销售管理模块**
   - 销售订单管理
   - 销售出库
   - 客户管理

7. **库存管理模块**
   - 实时库存查询
   - 库存预警
   - 库存盘点

8. **报表统计模块**
   - 采购报表
   - 销售报表
   - 库存报表
   - 财务报表

## 数据库设计

### 核心表结构

#### 用户表 (users)
```sql
- id: 主键
- username: 用户名
- email: 邮箱
- password_hash: 密码哈希
- role: 角色（admin/manager/staff）
- created_at: 创建时间
- updated_at: 更新时间
```

#### 商品分类表 (categories)
```sql
- id: 主键
- name: 分类名称
- parent_id: 父分类ID
- description: 描述
- created_at: 创建时间
```

#### 商品表 (products)
```sql
- id: 主键
- name: 商品名称
- code: 商品编码
- category_id: 分类ID
- description: 描述
- unit: 单位
- purchase_price: 进价
- sale_price: 售价
- min_stock: 最低库存
- created_at: 创建时间
- updated_at: 更新时间
```

#### 供应商表 (suppliers)
```sql
- id: 主键
- name: 供应商名称
- contact_person: 联系人
- phone: 电话
- email: 邮箱
- address: 地址
- created_at: 创建时间
```

#### 客户表 (customers)
```sql
- id: 主键
- name: 客户名称
- contact_person: 联系人
- phone: 电话
- email: 邮箱
- address: 地址
- created_at: 创建时间
```

#### 库存表 (inventory)
```sql
- id: 主键
- product_id: 商品ID
- quantity: 当前库存数量
- reserved_quantity: 预留数量
- updated_at: 更新时间
```

#### 采购单表 (purchase_orders)
```sql
- id: 主键
- order_number: 采购单号
- supplier_id: 供应商ID
- status: 状态（pending/confirmed/received/cancelled）
- order_date: 采购日期
- total_amount: 总金额
- created_by: 创建人
- created_at: 创建时间
```

#### 采购单明细表 (purchase_order_items)
```sql
- id: 主键
- purchase_order_id: 采购单ID
- product_id: 商品ID
- quantity: 数量
- unit_price: 单价
- total_price: 总价
```

#### 销售单表 (sales_orders)
```sql
- id: 主键
- order_number: 销售单号
- customer_id: 客户ID
- status: 状态（pending/confirmed/shipped/delivered/cancelled）
- order_date: 销售日期
- total_amount: 总金额
- created_by: 创建人
- created_at: 创建时间
```

#### 销售单明细表 (sales_order_items)
```sql
- id: 主键
- sales_order_id: 销售单ID
- product_id: 商品ID
- quantity: 数量
- unit_price: 单价
- total_price: 总价
```

#### 库存变动记录表 (inventory_transactions)
```sql
- id: 主键
- product_id: 商品ID
- transaction_type: 变动类型（purchase/sale/adjustment）
- quantity: 变动数量（正负数）
- reference_type: 关联类型（purchase_order/sales_order）
- reference_id: 关联ID
- created_at: 创建时间
```

## API设计

### 认证接口
- POST /api/auth/login - 用户登录
- POST /api/auth/register - 用户注册
- POST /api/auth/logout - 用户登出
- GET /api/auth/me - 获取当前用户信息

### 商品管理接口
- GET /api/products - 获取商品列表
- POST /api/products - 创建商品
- GET /api/products/{id} - 获取商品详情
- PUT /api/products/{id} - 更新商品
- DELETE /api/products/{id} - 删除商品

### 库存管理接口
- GET /api/inventory - 获取库存列表
- GET /api/inventory/{product_id} - 获取商品库存
- POST /api/inventory/adjustment - 库存调整

### 采购管理接口
- GET /api/purchases - 获取采购单列表
- POST /api/purchases - 创建采购单
- GET /api/purchases/{id} - 获取采购单详情
- PUT /api/purchases/{id} - 更新采购单
- POST /api/purchases/{id}/receive - 采购入库

### 销售管理接口
- GET /api/sales - 获取销售单列表
- POST /api/sales - 创建销售单
- GET /api/sales/{id} - 获取销售单详情
- PUT /api/sales/{id} - 更新销售单
- POST /api/sales/{id}/ship - 销售出库

## 技术栈选择理由

### 后端选择 FastAPI
- 高性能，基于异步编程
- 自动生成API文档
- 类型检查支持
- 易于测试和部署

### 前端选择 Vue 3
- 响应式系统优化
- Composition API灵活性
- TypeScript支持
- 丰富的生态系统

### 数据库选择 PostgreSQL
- 支持复杂查询
- 事务完整性
- 扩展性好
- 开源免费