from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class ProductBase(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    unit: Optional[str] = "件"
    purchase_price: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    min_stock: Optional[int] = 0


class ProductCreate(ProductBase):
    name: str
    code: str
    unit: str = "件"


class ProductUpdate(ProductBase):
    pass


class ProductInDBBase(ProductBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass