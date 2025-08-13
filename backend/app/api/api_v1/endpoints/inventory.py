from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Inventory])
def read_inventory(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve inventory.
    """
    inventory = crud.inventory.get_multi(db, skip=skip, limit=limit)
    return inventory


@router.get("/{product_id}", response_model=schemas.Inventory)
def read_product_inventory(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get inventory by product ID.
    """
    inventory = crud.inventory.get_by_product(db=db, product_id=product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.post("/adjustment")
def adjust_inventory(
    *,
    db: Session = Depends(get_db),
    adjustment_in: schemas.InventoryAdjustment,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Adjust inventory quantity.
    """
    return crud.inventory.adjust_quantity(
        db=db, product_id=adjustment_in.product_id, quantity=adjustment_in.quantity
    )