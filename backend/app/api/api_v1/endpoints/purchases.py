from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db
from app.models.purchase_order import PurchaseOrderStatus

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


class StatusUpdateRequest(BaseModel):
    status: PurchaseOrderStatus


def _validate_purchase_status_update(
    current_status: PurchaseOrderStatus,
    next_status: PurchaseOrderStatus,
) -> None:
    if current_status == next_status:
        return

    if next_status == PurchaseOrderStatus.received:
        raise ValueError("Use the receive endpoint to receive purchase orders")

    allowed_transitions = {
        PurchaseOrderStatus.pending: {
            PurchaseOrderStatus.confirmed,
            PurchaseOrderStatus.cancelled,
        },
        PurchaseOrderStatus.confirmed: {
            PurchaseOrderStatus.cancelled,
        },
        PurchaseOrderStatus.received: set(),
        PurchaseOrderStatus.cancelled: set(),
    }

    if next_status not in allowed_transitions.get(current_status, set()):
        raise ValueError(
            f"Cannot change purchase order status from {current_status.value} to {next_status.value}"
        )


@router.put("/{id}/status", response_model=schemas.PurchaseOrder)
def update_purchase_status(
    *,
    db: Session = Depends(get_db),
    id: int,
    status_request: StatusUpdateRequest,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update purchase order status.
    """
    purchase = crud.purchase_order.get(db=db, id=id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    try:
        _validate_purchase_status_update(purchase.status, status_request.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    purchase_data = schemas.PurchaseOrderUpdate(status=status_request.status)
    purchase = crud.purchase_order.update(db=db, db_obj=purchase, obj_in=purchase_data)
    return purchase


@router.post("/{id}/receive", response_model=schemas.PurchaseOrder)
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
    
    try:
        return crud.purchase_order.receive(db=db, purchase_order=purchase)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
