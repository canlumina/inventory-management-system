from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.PurchaseOrder])
def read_purchases(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve purchase orders.
    """
    purchases = crud.purchase_order.get_multi(db, skip=skip, limit=limit)
    return purchases


@router.post("/", response_model=schemas.PurchaseOrder)
def create_purchase(
    *,
    db: Session = Depends(get_db),
    purchase_in: schemas.PurchaseOrderCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new purchase order.
    """
    purchase = crud.purchase_order.create_with_items(
        db=db, obj_in=purchase_in, created_by=current_user.id
    )
    return purchase


@router.get("/{id}", response_model=schemas.PurchaseOrder)
def read_purchase(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get purchase order by ID.
    """
    purchase = crud.purchase_order.get(db=db, id=id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return purchase


@router.post("/{id}/receive")
def receive_purchase(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Receive purchase order (update inventory).
    """
    purchase = crud.purchase_order.get(db=db, id=id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    return crud.purchase_order.receive(db=db, purchase_order=purchase)