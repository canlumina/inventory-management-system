from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from app.models.inventory_transaction import TransactionType, ReferenceType
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.crud.crud_inventory import inventory


class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]):
    def create_with_items(
        self, db: Session, *, obj_in: PurchaseOrderCreate, created_by: int
    ) -> PurchaseOrder:
        # Generate order number
        order_number = f"PO{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate total amount
        total_amount = sum(item.total_price for item in obj_in.items)
        
        # Create purchase order
        db_obj = PurchaseOrder(
            order_number=order_number,
            supplier_id=obj_in.supplier_id,
            total_amount=total_amount,
            created_by=created_by
        )
        db.add(db_obj)
        db.flush()  # Get the ID before committing
        
        # Create items
        for item_data in obj_in.items:
            item = PurchaseOrderItem(
                purchase_order_id=db_obj.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.total_price
            )
            db.add(item)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def receive(self, db: Session, *, purchase_order: PurchaseOrder) -> PurchaseOrder:
        if purchase_order.status != PurchaseOrderStatus.confirmed:
            raise ValueError("Purchase order must be confirmed to receive")
        
        # Update inventory for each item
        for item in purchase_order.items:
            inventory.adjust_quantity(
                db,
                product_id=item.product_id,
                quantity=item.quantity,
                reference_type=ReferenceType.purchase_order,
                reference_id=purchase_order.id
            )
        
        # Update purchase order status
        purchase_order.status = PurchaseOrderStatus.received
        db.add(purchase_order)
        db.commit()
        db.refresh(purchase_order)
        return purchase_order


purchase_order = CRUDPurchaseOrder(PurchaseOrder)