#!/usr/bin/env python3
"""
数据库初始化脚本 - 创建表和默认用户
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash
# 导入所有模型以确保表被创建
from app import models

# 使用环境变量中的数据库URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/inventory_db")

def init_database():
    """初始化数据库表结构和默认数据"""
    print(f"连接数据库: {DATABASE_URL}")
    
    # 创建数据库引擎
    engine = create_engine(DATABASE_URL)
    
    # 创建所有表
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 检查是否已存在管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            print("管理员用户已存在")
            return
        
        # 创建默认管理员用户
        print("创建默认管理员用户...")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.admin
        )
        db.add(admin_user)
        
        # 创建默认经理用户
        print("创建默认经理用户...")
        manager_user = User(
            username="manager",
            email="manager@example.com", 
            password_hash=get_password_hash("manager123"),
            role=UserRole.manager
        )
        db.add(manager_user)
        
        # 创建默认员工用户
        print("创建默认员工用户...")
        staff_user = User(
            username="staff",
            email="staff@example.com",
            password_hash=get_password_hash("staff123"),
            role=UserRole.staff
        )
        db.add(staff_user)
        
        db.commit()
        print("默认用户创建成功！")
        print("管理员: admin / admin123")
        print("经理: manager / manager123")
        print("员工: staff / staff123")
        
    except Exception as e:
        print(f"创建用户失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()