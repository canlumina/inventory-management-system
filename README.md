# 进销存管理系统

一个基于 Vue 3 + FastAPI 的现代化进销存管理系统。

## 系统特性

### 🚀 核心功能
- **用户管理**: 支持多角色用户管理（管理员、经理、员工）
- **商品管理**: 商品信息维护、分类管理、规格管理
- **供应商管理**: 供应商信息管理、联系人管理
- **客户管理**: 客户信息管理、联系记录
- **采购管理**: 采购计划、订单管理、采购入库
- **销售管理**: 销售订单管理、销售出库、客户管理
- **库存管理**: 实时库存查询、库存预警、库存盘点
- **报表统计**: 采购报表、销售报表、库存报表、财务报表

### 💻 技术栈
- **前端**: Vue 3 + TypeScript + Element Plus + Pinia + Vue Router
- **后端**: FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **认证**: JWT Token
- **构建工具**: Vite

## 项目结构

```
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── crud/           # 数据库操作
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   └── main.py         # 应用入口
│   ├── alembic/            # 数据库迁移
│   └── requirements.txt    # 依赖包
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/            # API请求
│   │   ├── components/     # 组件
│   │   ├── stores/         # 状态管理
│   │   ├── types/          # TypeScript类型
│   │   ├── views/          # 页面
│   │   └── main.ts         # 应用入口
│   └── package.json        # 依赖包
└── system_design.md        # 系统设计文档
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 后端启动

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\\Scripts\\activate   # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

5. 初始化数据库
```bash
alembic upgrade head
```

6. 启动后端服务
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端启动

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

4. 打开浏览器访问 `http://localhost:3000`

### 构建生产版本

**后端:**
```bash
# 使用 Docker 或直接部署
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**前端:**
```bash
npm run build
```

## API文档

启动后端服务后，可以访问自动生成的API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 数据库设计

系统包含以下核心数据表：
- `users` - 用户表
- `categories` - 商品分类表
- `products` - 商品表
- `suppliers` - 供应商表
- `customers` - 客户表
- `inventory` - 库存表
- `purchase_orders` - 采购单表
- `sales_orders` - 销售单表
- `inventory_transactions` - 库存变动记录表

详细设计请参考 [系统设计文档](system_design.md)

## 功能截图

### 仪表盘
- 实时统计数据显示
- 库存预警提醒
- 最近操作记录

### 商品管理
- 商品信息CRUD
- 商品分类管理
- 库存关联显示

### 采购管理
- 采购单创建和管理
- 供应商信息维护
- 采购入库操作

### 销售管理
- 销售单创建和管理
- 客户信息维护
- 销售出库操作

### 库存管理
- 实时库存查询
- 库存调整功能
- 库存预警设置

### 报表统计
- 销售趋势分析
- 库存分布图表
- 导出功能

## 开发指南

### 添加新功能
1. 后端：在对应的models、schemas、crud、api中添加相关代码
2. 前端：在types、api、views中添加相应的页面和接口

### 数据库迁移
```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head
```

## 部署指南

### Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 传统部署
1. 配置Nginx反向代理
2. 使用PM2或Supervisor管理后端进程
3. 构建前端静态文件并部署到Web服务器

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。