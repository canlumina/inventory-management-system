from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.sales_order import SalesOrder, SalesOrderItem, SalesOrderStatus
from app.models.inventory_transaction import TransactionType, ReferenceType
from app.schemas.sales_order import SalesOrderCreate, SalesOrderUpdate
from app.crud.crud_inventory import inventory


class CRUDSalesOrder(CRUDBase[SalesOrder, SalesOrderCreate, SalesOrderUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return (
            db.query(self.model)
            .options(
                joinedload(SalesOrder.customer),
                joinedload(SalesOrder.creator),
                joinedload(SalesOrder.items).joinedload(SalesOrderItem.product)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get(self, db: Session, id: int):
        return (
            db.query(self.model)
            .options(
                joinedload(SalesOrder.customer),
                joinedload(SalesOrder.creator),
                joinedload(SalesOrder.items).joinedload(SalesOrderItem.product)
            )
            .filter(self.model.id == id)
            .first()
        )
    def create_with_items(
        self, db: Session, *, obj_in: SalesOrderCreate, created_by: int
    ) -> SalesOrder:
        # Generate order number
        order_number = f"SO{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate total amount
        total_amount = sum(item.total_price for item in obj_in.items)
        
        # Create sales order
        db_obj = SalesOrder(
            order_number=order_number,
            customer_id=obj_in.customer_id,
            total_amount=total_amount,
            created_by=created_by
        )
        db.add(db_obj)
        db.flush()  # Get the ID before committing
        
        # Create items
        for item_data in obj_in.items:
            item = SalesOrderItem(
                sales_order_id=db_obj.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.total_price
            )
            db.add(item)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def ship(self, db: Session, *, sales_order: SalesOrder) -> SalesOrder:
        if sales_order.status != SalesOrderStatus.confirmed:
            raise ValueError("Sales order must be confirmed to ship")
        
        # Check and reserve inventory for each item
        for item in sales_order.items:
            available = inventory.get_by_product(db, product_id=item.product_id)
            if not available or available.available_quantity < item.quantity:
                raise ValueError(f"Insufficient inventory for product {item.product_id}")
        
        # Update inventory for each item
        for item in sales_order.items:
            inventory.adjust_quantity(
                db,
                product_id=item.product_id,
                quantity=-item.quantity,  # Negative for outbound
                reference_type=ReferenceType.sales_order,
                reference_id=sales_order.id
            )
        
        # Update sales order status
        sales_order.status = SalesOrderStatus.shipped
        db.add(sales_order)
        db.commit()
        db.refresh(sales_order)
        return sales_order


sales_order = CRUDSalesOrder(SalesOrder)