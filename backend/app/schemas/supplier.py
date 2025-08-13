from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class SupplierBase(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class SupplierCreate(SupplierBase):
    name: str


class SupplierUpdate(SupplierBase):
    pass


class SupplierInDBBase(SupplierBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Supplier(SupplierInDBBase):
    pass


class SupplierInDB(SupplierInDBBase):
    pass