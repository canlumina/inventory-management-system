# GitHub 上传指南

## 1. 初始化Git仓库

```bash
# 进入项目目录
cd /home/yangcan/Workspaces/webload

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: 进销存管理系统

- 实现了完整的前后端分离架构
- 后端: FastAPI + SQLAlchemy + PostgreSQL
- 前端: Vue 3 + TypeScript + Element Plus
- 功能: 用户管理、商品管理、库存管理、采购销售、报表统计
- 支持Docker部署"
```

## 2. 在GitHub上创建仓库

1. 打开 GitHub.com
2. 点击右上角的 "+" 按钮
3. 选择 "New repository"
4. 填写仓库信息：
   - Repository name: `inventory-management-system`
   - Description: `基于Vue3+FastAPI的现代化进销存管理系统`
   - 选择 Public 或 Private
   - **不要**勾选 "Add a README file"
   - **不要**勾选 "Add .gitignore"
   - **不要**勾选 "Choose a license"
5. 点击 "Create repository"

## 3. 关联远程仓库并推送

```bash
# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/inventory-management-system.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 4. 后续提交流程

```bash
# 查看文件状态
git status

# 添加修改的文件
git add .
# 或添加特定文件
git add filename

# 提交更改
git commit -m "描述你的更改"

# 推送到GitHub
git push origin main
```

## 5. 常用Git命令

```bash
# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull origin main

# 创建新分支
git checkout -b feature-branch-name

# 切换分支
git checkout main

# 合并分支
git merge feature-branch-name
```

## 6. 建议的提交信息格式

```bash
# 功能相关
git commit -m "feat: 添加用户角色管理功能"
git commit -m "feat: 实现库存预警功能"

# 修复相关
git commit -m "fix: 修复登录状态丢失问题"
git commit -m "fix: 解决库存数量计算错误"

# 文档相关
git commit -m "docs: 更新API文档"
git commit -m "docs: 添加部署指南"

# 样式相关
git commit -m "style: 优化商品管理页面UI"

# 重构相关
git commit -m "refactor: 重构库存计算逻辑"

# 测试相关
git commit -m "test: 添加用户认证单元测试"
```

## 7. 如果需要忽略已经追踪的文件

```bash
# 停止追踪某个文件但保留本地文件
git rm --cached filename

# 停止追踪某个目录
git rm -r --cached directory/

# 提交更改
git commit -m "Remove tracked files that should be ignored"
```

## 8. 克隆仓库到其他地方

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/inventory-management-system.git

# 进入项目目录
cd inventory-management-system

# 后端设置
cd backend
pip install -r requirements.txt
cp .env.example .env  # 配置环境变量

# 前端设置
cd ../frontend
npm install
```

## 9. 协作开发

```bash
# Fork别人的仓库后，添加上游仓库
git remote add upstream https://github.com/ORIGINAL_OWNER/inventory-management-system.git

# 同步上游更新
git fetch upstream
git checkout main
git merge upstream/main
```

## 注意事项

1. **.env 文件已被忽略**，记得在部署时配置环境变量
2. **node_modules 和 __pycache__ 已被忽略**，其他开发者需要重新安装依赖
3. **数据库文件已被忽略**，需要重新创建数据库
4. 推送前请确保代码测试通过
5. 敏感信息（如API密钥、数据库密码）不要提交到仓库