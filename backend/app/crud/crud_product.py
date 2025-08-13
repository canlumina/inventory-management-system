from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Product]:
        return db.query(Product).filter(Product.code == code).first()

    def get_by_category(self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        return (
            db.query(Product)
            .filter(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_name(self, db: Session, *, name: str, skip: int = 0, limit: int = 100) -> List[Product]:
        return (
            db.query(Product)
            .filter(Product.name.contains(name))
            .offset(skip)
            .limit(limit)
            .all()
        )


product = CRUDProduct(Product)