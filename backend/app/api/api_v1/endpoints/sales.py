from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db
from app.models.sales_order import SalesOrderStatus

router = APIRouter()


@router.get("/", response_model=List[schemas.SalesOrder])
def read_sales(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve sales orders.
    """
    sales = crud.sales_order.get_multi(db, skip=skip, limit=limit)
    return sales


@router.post("/", response_model=schemas.SalesOrder)
def create_sales(
    *,
    db: Session = Depends(get_db),
    sales_in: schemas.SalesOrderCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new sales order.
    """
    sales = crud.sales_order.create_with_items(
        db=db, obj_in=sales_in, created_by=current_user.id
    )
    return sales


@router.get("/{id}", response_model=schemas.SalesOrder)
def read_sales_order(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get sales order by ID.
    """
    sales = crud.sales_order.get(db=db, id=id)
    if not sales:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return sales


class StatusUpdateRequest(BaseModel):
    status: SalesOrderStatus


def _validate_sales_status_update(
    current_status: SalesOrderStatus,
    next_status: SalesOrderStatus,
) -> None:
    if current_status == next_status:
        return

    if next_status == SalesOrderStatus.shipped:
        raise ValueError("Use the ship endpoint to ship sales orders")

    allowed_transitions = {
        SalesOrderStatus.pending: {
            SalesOrderStatus.confirmed,
            SalesOrderStatus.cancelled,
        },
        SalesOrderStatus.confirmed: {
            SalesOrderStatus.cancelled,
        },
        SalesOrderStatus.shipped: {
            SalesOrderStatus.delivered,
        },
        SalesOrderStatus.delivered: set(),
        SalesOrderStatus.cancelled: set(),
    }

    if next_status not in allowed_transitions.get(current_status, set()):
        raise ValueError(
            f"Cannot change sales order status from {current_status.value} to {next_status.value}"
        )


@router.put("/{id}/status", response_model=schemas.SalesOrder)
def update_sales_status(
    *,
    db: Session = Depends(get_db),
    id: int,
    status_request: StatusUpdateRequest,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update sales order status.
    """
    sales = crud.sales_order.get(db=db, id=id)
    if not sales:
        raise HTTPException(status_code=404, detail="Sales order not found")
    
    try:
        _validate_sales_status_update(sales.status, status_request.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    sales_data = schemas.SalesOrderUpdate(status=status_request.status)
    sales = crud.sales_order.update(db=db, db_obj=sales, obj_in=sales_data)
    return sales


@router.post("/{id}/ship", response_model=schemas.SalesOrder)
def ship_sales_order(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Ship sales order (update inventory).
    """
    sales = crud.sales_order.get(db=db, id=id)
    if not sales:
        raise HTTPException(status_code=404, detail="Sales order not found")
    
    try:
        return crud.sales_order.ship(db=db, sales_order=sales)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
