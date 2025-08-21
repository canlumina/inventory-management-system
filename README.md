<div align="center">

# 🏪 进销存管理系统

**现代化的企业级库存管理解决方案**

<p align="center">
  <img src="https://img.shields.io/badge/Vue.js-3.4+-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/TypeScript-5.2+-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-24.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/yangcan/webload?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red?style=flat-square" alt="Made with Love">
</p>

**一个功能全面、技术先进的进销存管理系统，专为中小企业设计。支持商品管理、库存控制、采购流程、销售管理、财务报表等核心业务功能。**

[快速开始](#-快速开始) • [功能特性](#-核心功能) • [技术栈](#-技术栈) • [部署指南](#-docker-部署) • [开发文档](#-开发文档)

</div>

---

## ✨ 核心功能

<table>
  <tr>
    <td width="50%">
      
### 🛒 **采购管理**
- 📝 采购单创建与编辑
- 🏢 供应商信息管理
- 🔄 采购流程控制（待确认→已确认→已入库）
- 📦 自动库存入库更新
- 💰 采购成本统计分析

### 💼 **销售管理**  
- 🎯 销售单创建与管理
- 👥 客户信息维护
- 🚚 销售流程控制（待确认→已确认→已发货→已完成）
- 📤 自动库存出库更新
- 📊 销售业绩统计

### 📦 **库存管理**
- 🔍 实时库存查询
- ⚠️ 智能库存预警
- 📝 库存调整操作
- 📋 库存变动记录
- 🏷️ 商品信息维护

    </td>
    <td width="50%">
      
### 📈 **报表统计**
- 📊 实时仪表板数据展示
- 📋 库存报表（状态分析、价值统计）
- 🛒 采购报表（订单统计、供应商分析）  
- 💰 销售报表（业绩分析、客户统计）
- 💹 财务报表（成本收入、利润分析）

### 👤 **用户管理**
- 🔐 JWT 令牌认证
- 🛡️ 角色权限控制
- 👨‍💼 多用户管理
- 🔄 会话状态管理

### 🎨 **用户体验**
- 📱 响应式设计
- 🎭 页面切换动画
- 🔍 智能搜索过滤
- 💫 加载状态优化
- 🎯 错误处理机制

    </td>
  </tr>
</table>

## 🛠 技术栈

### 前端技术
| 技术 | 版本 | 描述 |
|-----|-----|-----|
| **Vue.js** | 3.4+ | 渐进式 JavaScript 框架 |
| **TypeScript** | 5.2+ | JavaScript 超集，提供类型安全 |
| **Element Plus** | 2.4+ | Vue 3 组件库 |
| **Pinia** | 2.1+ | Vue 状态管理库 |
| **Vue Router** | 4.2+ | Vue.js 官方路由管理器 |
| **Axios** | 1.6+ | HTTP 客户端 |
| **Vite** | 5.0+ | 现代化构建工具 |

### 后端技术
| 技术 | 版本 | 描述 |
|-----|-----|-----|
| **Python** | 3.8+ | 后端开发语言 |
| **FastAPI** | 0.104+ | 现代、高性能的 Python Web 框架 |
| **SQLAlchemy** | 2.0+ | Python ORM 框架 |
| **Alembic** | 1.13+ | 数据库迁移工具 |
| **PostgreSQL** | 15+ | 关系型数据库 |
| **Pydantic** | 2.5+ | 数据验证库 |
| **JWT** | - | JSON Web Tokens 认证 |

### 开发运维
| 技术 | 版本 | 描述 |
|-----|-----|-----|
| **Docker** | 24.0+ | 容器化部署 |
| **Docker Compose** | 2.20+ | 多容器应用管理 |
| **Nginx** | 1.24+ | Web 服务器和反向代理 |
| **Git** | - | 版本控制系统 |

## 📁 项目结构

```
webload/
├── 📁 backend/                    # 🐍 Python FastAPI 后端
│   ├── 📁 app/
│   │   ├── 📁 api/               # 🔗 API 路由和端点
│   │   │   └── 📁 api_v1/        # API v1 版本
│   │   ├── 📁 core/              # ⚙️ 核心配置和工具
│   │   ├── 📁 crud/              # 🔄 数据库 CRUD 操作
│   │   ├── 📁 models/            # 📊 SQLAlchemy 数据模型
│   │   ├── 📁 schemas/           # 📋 Pydantic 数据模型
│   │   └── 📄 main.py            # 🚀 FastAPI 应用入口
│   ├── 📁 alembic/               # 🗃️ 数据库迁移文件
│   ├── 📄 requirements.txt       # 📦 Python 依赖包
│   └── 📄 run.py                 # 🏃‍♂️ 开发服务器启动脚本
├── 📁 frontend/                   # 🎨 Vue 3 前端
│   ├── 📁 src/
│   │   ├── 📁 api/               # 🌐 API 请求封装
│   │   ├── 📁 components/        # 🧩 可复用 Vue 组件
│   │   ├── 📁 stores/            # 🗂️ Pinia 状态管理
│   │   ├── 📁 types/             # 🏷️ TypeScript 类型定义
│   │   ├── 📁 utils/             # 🔧 工具函数
│   │   ├── 📁 views/             # 📄 页面组件
│   │   └── 📄 main.ts            # 🎯 Vue 应用入口
│   ├── 📄 package.json           # 📦 Node.js 依赖包
│   ├── 📄 vite.config.ts         # ⚡ Vite 配置文件
│   └── 📄 tsconfig.json          # 📐 TypeScript 配置
├── 📄 docker-compose.yml         # 🐳 Docker 容器编排
├── 📄 DEVELOPMENT.md             # 📚 开发文档
└── 📄 README.md                  # 📖 项目说明文档
```

## 🚀 快速开始

### 📋 环境要求

| 软件 | 版本要求 | 用途 |
|-----|---------|------|
| 🐍 **Python** | 3.8+ | 后端开发语言 |
| 🟢 **Node.js** | 18+ | 前端构建工具 |
| 🐘 **PostgreSQL** | 15+ | 数据库 |
| 🐳 **Docker** | 24.0+ | 容器化部署（推荐） |

### ⚡ 一键启动（推荐）

使用 Docker Compose 一键启动完整系统：

```bash
# 克隆项目
git clone <repository-url>
cd webload

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

**🎉 启动完成后访问：**
- **前端应用**: http://localhost:3000
- **后端 API**: http://localhost:8000  
- **API 文档**: http://localhost:8000/docs

### 🛠 本地开发模式

<details>
<summary><b>点击展开本地开发步骤</b></summary>

#### 1️⃣ 后端启动

```bash
# 进入后端目录
cd backend

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接

# 数据库迁移
alembic upgrade head

# 启动开发服务器
python run.py
# 或 uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2️⃣ 前端启动

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

#### 3️⃣ 数据库设置

```bash
# PostgreSQL 安装和配置
createdb inventory_db
psql inventory_db < initial_data.sql  # 可选：导入初始数据
```

</details>

## 📚 API 文档

启动后端服务后，可以访问自动生成的 API 文档：

<table>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger UI">
      <br>
      <a href="http://localhost:8000/docs"><b>交互式 API 文档</b></a>
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/ReDoc-8CA1AF?style=for-the-badge&logo=readthedocs&logoColor=white" alt="ReDoc">
      <br>
      <a href="http://localhost:8000/redoc"><b>美观的 API 文档</b></a>
    </td>
  </tr>
</table>

### 🔗 主要 API 端点

| 模块 | 端点 | 描述 |
|-----|------|-----|
| 🔐 **认证** | `/api/v1/auth/*` | 用户登录、令牌管理 |
| 📦 **商品** | `/api/v1/products/*` | 商品 CRUD 操作 |
| 🏢 **供应商** | `/api/v1/suppliers/*` | 供应商管理 |
| 👥 **客户** | `/api/v1/customers/*` | 客户管理 |
| 🛒 **采购** | `/api/v1/purchases/*` | 采购订单管理 |
| 💼 **销售** | `/api/v1/sales/*` | 销售订单管理 |
| 📊 **库存** | `/api/v1/inventory/*` | 库存查询和调整 |
| 📈 **报表** | `/api/v1/reports/*` | 统计报表数据 |

## 🐳 Docker 部署

### 生产环境部署

```bash
# 克隆代码
git clone <repository-url>
cd webload

# 构建和启动服务
docker-compose -f docker-compose.prod.yml up -d

# 初始化数据库
docker-compose exec backend alembic upgrade head

# 查看日志
docker-compose logs -f
```

### 开发环境调试

```bash
# 启动开发环境
docker-compose up -d

# 查看服务状态
docker-compose ps

# 进入容器调试
docker-compose exec backend bash
docker-compose exec frontend sh

# 查看实时日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🗄️ 数据库设计

<details>
<summary><b>点击展开数据库表结构</b></summary>

### 核心数据表

| 表名 | 描述 | 关键字段 |
|-----|-----|----------|
| 👤 **users** | 用户表 | `id`, `username`, `email`, `role` |
| 🏷️ **categories** | 商品分类表 | `id`, `name`, `parent_id` |
| 📦 **products** | 商品表 | `id`, `name`, `code`, `category_id` |
| 🏢 **suppliers** | 供应商表 | `id`, `name`, `contact`, `address` |
| 👥 **customers** | 客户表 | `id`, `name`, `contact`, `address` |
| 📊 **inventory** | 库存表 | `product_id`, `quantity`, `reserved_quantity` |
| 🛒 **purchase_orders** | 采购单表 | `id`, `supplier_id`, `status`, `total_amount` |
| 💼 **sales_orders** | 销售单表 | `id`, `customer_id`, `status`, `total_amount` |
| 📋 **inventory_transactions** | 库存变动记录 | `id`, `product_id`, `type`, `quantity` |

### ER 关系图
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Products  │────│  Inventory  │────│ Transactions│
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │
       │            ┌─────────────┐
       └────────────│  Categories │
                    │             │
                    └─────────────┘
```

</details>

## 🎨 功能特性

### 💻 现代化界面设计

- **🎭 动画效果**: 页面切换动画、加载动画、悬停效果
- **📱 响应式布局**: 支持桌面、平板、手机多端适配  
- **🎨 主题定制**: Element Plus 组件主题定制
- **🔍 智能搜索**: 实时搜索过滤、高级筛选条件
- **📊 数据可视化**: 图表展示、统计面板

### ⚡ 性能优化

- **🚀 快速加载**: Vite 构建工具，极速热重载
- **💾 智能缓存**: Keep-Alive 页面缓存，减少重复渲染
- **📦 按需加载**: 路由懒加载，组件按需导入
- **🔄 状态管理**: Pinia 轻量级状态管理

### 🛡️ 安全特性

- **🔐 JWT 认证**: 无状态身份验证
- **🛡️ 权限控制**: 基于角色的访问控制（RBAC）
- **🔒 数据验证**: Pydantic 模型验证，防止注入攻击
- **🚨 错误处理**: 统一错误处理，用户友好提示

## 👨‍💻 开发指南

### 🔧 本地开发环境配置

<details>
<summary><b>详细开发配置指南</b></summary>

#### 环境变量配置

**后端环境变量** (`.env`):
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/inventory_db
SECRET_KEY=your-super-secret-key-here
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**前端环境变量** (`.env.development`):
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=进销存管理系统
```

#### 代码规范

```bash
# 后端代码检查
cd backend
pip install black flake8 isort
black . && flake8 . && isort .

# 前端代码检查  
cd frontend
npm run lint      # ESLint 检查
npm run type-check # TypeScript 类型检查
```

</details>

### 🆕 添加新功能

1. **后端开发流程**:
   ```bash
   # 1. 创建数据模型
   backend/app/models/new_model.py
   
   # 2. 定义 Pydantic 模式
   backend/app/schemas/new_schema.py
   
   # 3. 实现 CRUD 操作
   backend/app/crud/new_crud.py
   
   # 4. 创建 API 端点
   backend/app/api/api_v1/endpoints/new_endpoint.py
   
   # 5. 生成数据库迁移
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```

2. **前端开发流程**:
   ```bash
   # 1. 定义 TypeScript 类型
   frontend/src/types/index.ts
   
   # 2. 创建 API 请求函数
   frontend/src/api/new-api.ts
   
   # 3. 开发页面组件
   frontend/src/views/NewView.vue
   
   # 4. 配置路由
   frontend/src/router/index.ts
   ```

### 📊 数据库操作

```bash
# 创建新迁移
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请按照以下步骤进行：

### 📝 提交代码

1. **Fork 项目** 到你的 GitHub 账户
2. **克隆到本地**:
   ```bash
   git clone https://github.com/your-username/webload.git
   cd webload
   ```
3. **创建功能分支**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **提交更改**:
   ```bash
   git commit -m "Add some amazing feature"
   ```
5. **推送到分支**:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **创建 Pull Request**

### 📋 代码规范

- **Python**: 遵循 [PEP 8](https://pep8.org/) 规范
- **TypeScript/Vue**: 遵循 [Vue Style Guide](https://vuejs.org/style-guide/)
- **提交信息**: 使用 [Conventional Commits](https://conventionalcommits.org/)

### 🐛 报告问题

在 [Issues](../../issues) 页面报告 Bug 时，请提供：
- **详细描述**: 问题的具体表现
- **复现步骤**: 如何重现该问题
- **环境信息**: 操作系统、浏览器版本等
- **截图**: 如果适用的话

## 📄 开发文档

- 📚 [开发文档](./DEVELOPMENT.md) - 详细的技术文档和开发历程
- 🏗️ [系统设计](./system_design.md) - 系统架构和设计思路
- 🔗 [API 文档](http://localhost:8000/docs) - 交互式 API 文档

## 🚀 部署与运维

<details>
<summary><b>生产环境部署指南</b></summary>

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### PM2 配置

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'webload-backend',
    script: 'uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    cwd: './backend',
    instances: 1,
    exec_mode: 'fork'
  }]
}
```

</details>

## 📜 许可证

本项目基于 **MIT License** 开源协议，详情请查看 [LICENSE](./LICENSE) 文件。

```
MIT License - 意味着您可以自由使用、修改、分发本软件 🎉
```

## 💬 联系方式

<div align="center">

**有问题或建议？我们很乐意听到您的声音！**

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=for-the-badge&logo=github)](../../issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue?style=for-the-badge&logo=github)](../../discussions)

**或者通过以下方式联系开发团队：**

📧 Email: [developer@example.com](mailto:developer@example.com)  
💬 QQ群: 123456789  
🐧 微信群: 扫码加入

</div>

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给它一个星标！**

Made with ❤️ by [开发团队](../../contributors)

</div>