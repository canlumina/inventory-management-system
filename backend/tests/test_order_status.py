from decimal import Decimal
import unittest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.api_v1.endpoints.purchases import (
    StatusUpdateRequest as PurchaseStatusUpdateRequest,
    receive_purchase,
    update_purchase_status,
)
from app.api.api_v1.endpoints.sales import (
    StatusUpdateRequest as SalesStatusUpdateRequest,
    ship_sales_order,
    update_sales_status,
)
from app.core.database import Base
from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from app.models.sales_order import SalesOrder, SalesOrderItem, SalesOrderStatus
from app.models.supplier import Supplier
from app.models.user import User, UserRole


class OrderStatusEndpointTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()
        self.user = self._create_user()
        self.supplier = self._create_supplier()
        self.customer = self._create_customer()
        self.product = self._create_product()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def _create_user(self):
        user = User(
            username="admin",
            email="admin@example.com",
            password_hash="hashed",
            role=UserRole.admin,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def _create_supplier(self):
        supplier = Supplier(name="Test Supplier")
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def _create_customer(self):
        customer = Customer(name="Test Customer")
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def _create_product(self):
        product = Product(name="Widget", code="WIDGET", unit="pcs", min_stock=0)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def _create_purchase_order(self, status=PurchaseOrderStatus.pending):
        order = PurchaseOrder(
            order_number="PO-TEST",
            supplier_id=self.supplier.id,
            status=status,
            total_amount=Decimal("10.00"),
            created_by=self.user.id,
        )
        self.db.add(order)
        self.db.flush()
        self.db.add(
            PurchaseOrderItem(
                purchase_order_id=order.id,
                product_id=self.product.id,
                quantity=2,
                unit_price=Decimal("5.00"),
                total_price=Decimal("10.00"),
            )
        )
        self.db.commit()
        self.db.refresh(order)
        return order

    def _create_sales_order(self, status=SalesOrderStatus.confirmed, inventory_quantity=1):
        self.db.add(
            Inventory(
                product_id=self.product.id,
                quantity=inventory_quantity,
                reserved_quantity=0,
            )
        )
        order = SalesOrder(
            order_number="SO-TEST",
            customer_id=self.customer.id,
            status=status,
            total_amount=Decimal("10.00"),
            created_by=self.user.id,
        )
        self.db.add(order)
        self.db.flush()
        self.db.add(
            SalesOrderItem(
                sales_order_id=order.id,
                product_id=self.product.id,
                quantity=2,
                unit_price=Decimal("5.00"),
                total_price=Decimal("10.00"),
            )
        )
        self.db.commit()
        self.db.refresh(order)
        return order

    def test_purchase_status_update_rejects_received_bypass(self):
        order = self._create_purchase_order(status=PurchaseOrderStatus.confirmed)

        with self.assertRaises(HTTPException) as raised:
            update_purchase_status(
                db=self.db,
                id=order.id,
                status_request=PurchaseStatusUpdateRequest(status=PurchaseOrderStatus.received),
                current_user=self.user,
            )

        self.assertEqual(raised.exception.status_code, 400)

    def test_receive_purchase_returns_400_when_order_is_not_confirmed(self):
        order = self._create_purchase_order(status=PurchaseOrderStatus.pending)

        with self.assertRaises(HTTPException) as raised:
            receive_purchase(db=self.db, id=order.id, current_user=self.user)

        self.assertEqual(raised.exception.status_code, 400)

    def test_sales_status_update_rejects_shipped_bypass(self):
        order = self._create_sales_order(status=SalesOrderStatus.confirmed, inventory_quantity=10)

        with self.assertRaises(HTTPException) as raised:
            update_sales_status(
                db=self.db,
                id=order.id,
                status_request=SalesStatusUpdateRequest(status=SalesOrderStatus.shipped),
                current_user=self.user,
            )

        self.assertEqual(raised.exception.status_code, 400)

    def test_ship_sales_order_returns_400_when_inventory_is_insufficient(self):
        order = self._create_sales_order(status=SalesOrderStatus.confirmed, inventory_quantity=1)

        with self.assertRaises(HTTPException) as raised:
            ship_sales_order(db=self.db, id=order.id, current_user=self.user)

        self.assertEqual(raised.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
