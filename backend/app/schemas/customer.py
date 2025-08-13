from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class CustomerBase(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    name: str


class CustomerUpdate(CustomerBase):
    pass


class CustomerInDBBase(CustomerBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Customer(CustomerInDBBase):
    pass


class CustomerInDB(CustomerInDBBase):
    pass