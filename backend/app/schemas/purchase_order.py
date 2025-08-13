from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from app.models.purchase_order import PurchaseOrderStatus


class PurchaseOrderItemBase(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class PurchaseOrderItemUpdate(PurchaseOrderItemBase):
    pass


class PurchaseOrderItemInDBBase(PurchaseOrderItemBase):
    id: Optional[int] = None
    purchase_order_id: Optional[int] = None

    class Config:
        from_attributes = True


class PurchaseOrderItem(PurchaseOrderItemInDBBase):
    pass


class PurchaseOrderBase(BaseModel):
    supplier_id: Optional[int] = None
    status: Optional[PurchaseOrderStatus] = PurchaseOrderStatus.pending
    order_date: Optional[datetime] = None
    total_amount: Optional[Decimal] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    supplier_id: int
    items: List[PurchaseOrderItemCreate]


class PurchaseOrderUpdate(PurchaseOrderBase):
    pass


class PurchaseOrderInDBBase(PurchaseOrderBase):
    id: Optional[int] = None
    order_number: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PurchaseOrder(PurchaseOrderInDBBase):
    items: List[PurchaseOrderItem] = []


class PurchaseOrderInDB(PurchaseOrderInDBBase):
    pass