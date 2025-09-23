from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class CategoryBase(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Category(CategoryInDBBase):
    children: List['Category'] = []


class CategoryInDB(CategoryInDBBase):
    pass


# 用于递归引用
Category.model_rebuild()