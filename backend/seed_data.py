#!/usr/bin/env python3
"""
数据种子脚本 - 创建示例数据用于测试
"""
import os
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import *
from app.core.security import get_password_hash

# 使用环境变量中的数据库URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/inventory_db")

def create_sample_data():
    """创建示例数据"""
    print(f"连接数据库: {DATABASE_URL}")

    # 创建数据库引擎
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        print("开始创建示例数据...")

        # 检查是否已经有测试数据
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("检测到已存在数据，清空现有测试数据...")
            # 删除现有数据（注意顺序，避免外键约束）
            db.query(InventoryTransaction).delete()
            db.query(SalesOrderItem).delete()
            db.query(PurchaseOrderItem).delete()
            db.query(SalesOrder).delete()
            db.query(PurchaseOrder).delete()
            db.query(Inventory).delete()
            db.query(Product).delete()
            db.query(Customer).delete()
            db.query(Supplier).delete()
            db.query(Category).delete()
            db.commit()

        # 1. 创建商品分类
        print("创建商品分类...")
        categories = [
            Category(name="电子产品", description="各类电子设备和配件"),
            Category(name="办公用品", description="办公室日常用品"),
            Category(name="家居用品", description="家庭生活用品"),
            Category(name="服装配饰", description="服装、鞋帽、配饰"),
            Category(name="食品饮料", description="食品和饮料类商品")
        ]
        db.add_all(categories)
        db.commit()

        # 刷新获取ID
        for cat in categories:
            db.refresh(cat)

        # 2. 创建供应商
        print("创建供应商...")
        suppliers = [
            Supplier(
                name="深圳科技有限公司",
                contact_person="张经理",
                phone="13800138001",
                email="zhang@tech.com",
                address="深圳市南山区科技园"
            ),
            Supplier(
                name="上海办公用品批发中心",
                contact_person="李总",
                phone="13800138002",
                email="li@office.com",
                address="上海市浦东新区商贸区"
            ),
            Supplier(
                name="广州家居制造厂",
                contact_person="王厂长",
                phone="13800138003",
                email="wang@home.com",
                address="广州市白云区工业园"
            ),
            Supplier(
                name="杭州服装贸易公司",
                contact_person="赵总监",
                phone="13800138004",
                email="zhao@fashion.com",
                address="杭州市江干区服装城"
            ),
            Supplier(
                name="成都食品供应商",
                contact_person="刘主管",
                phone="13800138005",
                email="liu@food.com",
                address="成都市高新区食品园"
            )
        ]
        db.add_all(suppliers)
        db.commit()

        for supplier in suppliers:
            db.refresh(supplier)

        # 3. 创建客户
        print("创建客户...")
        customers = [
            Customer(
                name="北京商贸有限公司",
                contact_person="陈经理",
                phone="13900139001",
                email="chen@trade.com",
                address="北京市朝阳区商务区"
            ),
            Customer(
                name="天津零售连锁店",
                contact_person="孙店长",
                phone="13900139002",
                email="sun@retail.com",
                address="天津市河西区商业街"
            ),
            Customer(
                name="西安电子市场",
                contact_person="马总",
                phone="13900139003",
                email="ma@electronics.com",
                address="西安市高新区电子城"
            ),
            Customer(
                name="重庆超市连锁",
                contact_person="周经理",
                phone="13900139004",
                email="zhou@supermarket.com",
                address="重庆市渝中区商圈"
            ),
            Customer(
                name="南京办公设备公司",
                contact_person="吴总",
                phone="13900139005",
                email="wu@office-eq.com",
                address="南京市建邺区写字楼"
            )
        ]
        db.add_all(customers)
        db.commit()

        for customer in customers:
            db.refresh(customer)

        # 4. 创建商品
        print("创建商品...")
        products = [
            # 电子产品
            Product(
                name="苹果iPhone 15",
                code="PHONE001",
                category_id=categories[0].id,
                description="最新款苹果手机",
                unit="台",
                purchase_price=Decimal("6000.00"),
                sale_price=Decimal("7500.00"),
                min_stock=10
            ),
            Product(
                name="戴尔笔记本电脑",
                code="LAPTOP001",
                category_id=categories[0].id,
                description="商务办公笔记本",
                unit="台",
                purchase_price=Decimal("4000.00"),
                sale_price=Decimal("5200.00"),
                min_stock=5
            ),
            Product(
                name="无线蓝牙耳机",
                code="EARPHONE001",
                category_id=categories[0].id,
                description="高品质无线耳机",
                unit="副",
                purchase_price=Decimal("200.00"),
                sale_price=Decimal("299.00"),
                min_stock=20
            ),

            # 办公用品
            Product(
                name="A4复印纸",
                code="PAPER001",
                category_id=categories[1].id,
                description="70g A4白色复印纸",
                unit="包",
                purchase_price=Decimal("15.00"),
                sale_price=Decimal("25.00"),
                min_stock=100
            ),
            Product(
                name="办公椅",
                code="CHAIR001",
                category_id=categories[1].id,
                description="人体工学办公椅",
                unit="把",
                purchase_price=Decimal("300.00"),
                sale_price=Decimal("450.00"),
                min_stock=15
            ),
            Product(
                name="打印机",
                code="PRINTER001",
                category_id=categories[1].id,
                description="激光打印机",
                unit="台",
                purchase_price=Decimal("800.00"),
                sale_price=Decimal("1200.00"),
                min_stock=8
            ),

            # 家居用品
            Product(
                name="LED台灯",
                code="LAMP001",
                category_id=categories[2].id,
                description="护眼LED学习台灯",
                unit="个",
                purchase_price=Decimal("80.00"),
                sale_price=Decimal("128.00"),
                min_stock=30
            ),
            Product(
                name="保温杯",
                code="CUP001",
                category_id=categories[2].id,
                description="不锈钢保温杯",
                unit="个",
                purchase_price=Decimal("35.00"),
                sale_price=Decimal("58.00"),
                min_stock=50
            ),

            # 服装配饰
            Product(
                name="商务衬衫",
                code="SHIRT001",
                category_id=categories[3].id,
                description="纯棉商务白衬衫",
                unit="件",
                purchase_price=Decimal("60.00"),
                sale_price=Decimal("120.00"),
                min_stock=40
            ),
            Product(
                name="真皮公文包",
                code="BAG001",
                category_id=categories[3].id,
                description="牛皮商务公文包",
                unit="个",
                purchase_price=Decimal("200.00"),
                sale_price=Decimal("350.00"),
                min_stock=12
            )
        ]
        db.add_all(products)
        db.commit()

        for product in products:
            db.refresh(product)

        # 5. 创建初始库存
        print("创建初始库存...")
        inventories = []
        for product in products:
            initial_qty = product.min_stock * 3  # 初始库存为最低库存的3倍
            inventory = Inventory(
                product_id=product.id,
                quantity=initial_qty,
                reserved_quantity=0
            )
            inventories.append(inventory)

        db.add_all(inventories)
        db.commit()

        # 6. 创建一些采购单
        print("创建采购单...")
        admin_user = db.query(User).filter(User.username == "admin").first()

        # 采购单1 - 已完成
        purchase1_items = [
            {"product": products[0], "quantity": 20, "unit_price": products[0].purchase_price},
            {"product": products[1], "quantity": 10, "unit_price": products[1].purchase_price},
            {"product": products[2], "quantity": 50, "unit_price": products[2].purchase_price},
        ]
        total1 = sum(item["quantity"] * item["unit_price"] for item in purchase1_items)

        purchase1 = PurchaseOrder(
            order_number="PO001",
            supplier_id=suppliers[0].id,
            status=PurchaseOrderStatus.received,
            order_date=datetime.now() - timedelta(days=15),
            total_amount=total1,
            created_by=admin_user.id
        )
        db.add(purchase1)
        db.commit()
        db.refresh(purchase1)

        for item_data in purchase1_items:
            item = PurchaseOrderItem(
                purchase_order_id=purchase1.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["quantity"] * item_data["unit_price"]
            )
            db.add(item)

        # 采购单2 - 进行中
        purchase2_items = [
            {"product": products[3], "quantity": 200, "unit_price": products[3].purchase_price},
            {"product": products[4], "quantity": 25, "unit_price": products[4].purchase_price},
        ]
        total2 = sum(item["quantity"] * item["unit_price"] for item in purchase2_items)

        purchase2 = PurchaseOrder(
            order_number="PO002",
            supplier_id=suppliers[1].id,
            status=PurchaseOrderStatus.confirmed,
            order_date=datetime.now() - timedelta(days=5),
            total_amount=total2,
            created_by=admin_user.id
        )
        db.add(purchase2)
        db.commit()
        db.refresh(purchase2)

        for item_data in purchase2_items:
            item = PurchaseOrderItem(
                purchase_order_id=purchase2.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["quantity"] * item_data["unit_price"]
            )
            db.add(item)

        # 7. 创建一些销售单
        print("创建销售单...")

        # 销售单1 - 已完成
        sales1_items = [
            {"product": products[0], "quantity": 5, "unit_price": products[0].sale_price},
            {"product": products[2], "quantity": 15, "unit_price": products[2].sale_price},
        ]
        total_sales1 = sum(item["quantity"] * item["unit_price"] for item in sales1_items)

        sales1 = SalesOrder(
            order_number="SO001",
            customer_id=customers[0].id,
            status=SalesOrderStatus.delivered,
            order_date=datetime.now() - timedelta(days=10),
            total_amount=total_sales1,
            created_by=admin_user.id
        )
        db.add(sales1)
        db.commit()
        db.refresh(sales1)

        for item_data in sales1_items:
            item = SalesOrderItem(
                sales_order_id=sales1.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["quantity"] * item_data["unit_price"]
            )
            db.add(item)

        # 销售单2 - 进行中
        sales2_items = [
            {"product": products[1], "quantity": 3, "unit_price": products[1].sale_price},
            {"product": products[6], "quantity": 10, "unit_price": products[6].sale_price},
        ]
        total_sales2 = sum(item["quantity"] * item["unit_price"] for item in sales2_items)

        sales2 = SalesOrder(
            order_number="SO002",
            customer_id=customers[1].id,
            status=SalesOrderStatus.confirmed,
            order_date=datetime.now() - timedelta(days=3),
            total_amount=total_sales2,
            created_by=admin_user.id
        )
        db.add(sales2)
        db.commit()
        db.refresh(sales2)

        for item_data in sales2_items:
            item = SalesOrderItem(
                sales_order_id=sales2.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["quantity"] * item_data["unit_price"]
            )
            db.add(item)

        # 8. 创建库存变动记录
        print("创建库存变动记录...")
        transactions = [
            # 采购入库记录
            InventoryTransaction(
                product_id=products[0].id,
                transaction_type=TransactionType.purchase,
                quantity=20,
                reference_type=ReferenceType.purchase_order,
                reference_id=purchase1.id,
                created_at=purchase1.order_date
            ),
            InventoryTransaction(
                product_id=products[1].id,
                transaction_type=TransactionType.purchase,
                quantity=10,
                reference_type=ReferenceType.purchase_order,
                reference_id=purchase1.id,
                created_at=purchase1.order_date
            ),
            InventoryTransaction(
                product_id=products[2].id,
                transaction_type=TransactionType.purchase,
                quantity=50,
                reference_type=ReferenceType.purchase_order,
                reference_id=purchase1.id,
                created_at=purchase1.order_date
            ),

            # 销售出库记录
            InventoryTransaction(
                product_id=products[0].id,
                transaction_type=TransactionType.sale,
                quantity=-5,
                reference_type=ReferenceType.sales_order,
                reference_id=sales1.id,
                created_at=sales1.order_date
            ),
            InventoryTransaction(
                product_id=products[2].id,
                transaction_type=TransactionType.sale,
                quantity=-15,
                reference_type=ReferenceType.sales_order,
                reference_id=sales1.id,
                created_at=sales1.order_date
            ),
        ]
        db.add_all(transactions)

        db.commit()

        print("示例数据创建成功！")
        print("\n创建的数据摘要:")
        print(f"- 商品分类: {len(categories)} 个")
        print(f"- 供应商: {len(suppliers)} 个")
        print(f"- 客户: {len(customers)} 个")
        print(f"- 商品: {len(products)} 个")
        print(f"- 采购单: 2 个")
        print(f"- 销售单: 2 个")
        print(f"- 库存记录: {len(inventories)} 个")
        print(f"- 库存变动记录: {len(transactions)} 个")
        print("\n现在可以在系统中查看这些测试数据了！")

    except Exception as e:
        print(f"创建数据失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()