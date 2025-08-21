from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.product import Product


class InventoryBase(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = 0
    reserved_quantity: Optional[int] = 0


class InventoryCreate(InventoryBase):
    product_id: int


class InventoryUpdate(InventoryBase):
    pass


class InventoryInDBBase(InventoryBase):
    id: Optional[int] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Inventory(InventoryInDBBase):
    available_quantity: Optional[int] = None
    product: Optional[Product] = None


class InventoryInDB(InventoryInDBBase):
    pass


class InventoryAdjustment(BaseModel):
    product_id: int
    quantity: int  # Positive for increase, negative for decrease
    reason: Optional[str] = None