from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from app.models.sales_order import SalesOrderStatus
from app.schemas.product import Product
from app.schemas.customer import Customer
from app.schemas.user import User


class SalesOrderItemBase(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None


class SalesOrderItemCreate(SalesOrderItemBase):
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class SalesOrderItemUpdate(SalesOrderItemBase):
    pass


class SalesOrderItemInDBBase(SalesOrderItemBase):
    id: Optional[int] = None
    sales_order_id: Optional[int] = None

    class Config:
        from_attributes = True


class SalesOrderItem(SalesOrderItemInDBBase):
    product: Optional[Product] = None


class SalesOrderBase(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[SalesOrderStatus] = SalesOrderStatus.pending
    order_date: Optional[datetime] = None
    total_amount: Optional[Decimal] = None


class SalesOrderCreate(SalesOrderBase):
    customer_id: int
    items: List[SalesOrderItemCreate]


class SalesOrderUpdate(SalesOrderBase):
    pass


class SalesOrderInDBBase(SalesOrderBase):
    id: Optional[int] = None
    order_number: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SalesOrder(SalesOrderInDBBase):
    items: List[SalesOrderItem] = []
    customer: Optional[Customer] = None
    creator: Optional[User] = None


class SalesOrderInDB(SalesOrderInDBBase):
    pass