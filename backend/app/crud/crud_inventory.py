from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction, TransactionType, ReferenceType
from app.schemas.inventory import InventoryCreate, InventoryUpdate


class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def get_by_product(self, db: Session, *, product_id: int) -> Optional[Inventory]:
        return db.query(Inventory).filter(Inventory.product_id == product_id).first()

    def create_or_get(self, db: Session, *, product_id: int) -> Inventory:
        inventory = self.get_by_product(db, product_id=product_id)
        if not inventory:
            inventory = Inventory(product_id=product_id, quantity=0, reserved_quantity=0)
            db.add(inventory)
            db.commit()
            db.refresh(inventory)
        return inventory

    def adjust_quantity(
        self, 
        db: Session, 
        *, 
        product_id: int, 
        quantity: int,
        reference_type: ReferenceType = ReferenceType.manual_adjustment,
        reference_id: Optional[int] = None
    ) -> Inventory:
        inventory = self.create_or_get(db, product_id=product_id)
        
        # Update inventory
        inventory.quantity += quantity
        db.add(inventory)
        
        # Create transaction record
        transaction = InventoryTransaction(
            product_id=product_id,
            transaction_type=TransactionType.adjustment if quantity != 0 else TransactionType.adjustment,
            quantity=quantity,
            reference_type=reference_type,
            reference_id=reference_id
        )
        db.add(transaction)
        
        db.commit()
        db.refresh(inventory)
        return inventory

    def reserve_quantity(self, db: Session, *, product_id: int, quantity: int) -> bool:
        inventory = self.get_by_product(db, product_id=product_id)
        if not inventory or inventory.available_quantity < quantity:
            return False
        
        inventory.reserved_quantity += quantity
        db.add(inventory)
        db.commit()
        return True

    def release_reserved(self, db: Session, *, product_id: int, quantity: int) -> None:
        inventory = self.get_by_product(db, product_id=product_id)
        if inventory:
            inventory.reserved_quantity = max(0, inventory.reserved_quantity - quantity)
            db.add(inventory)
            db.commit()


inventory = CRUDInventory(Inventory)