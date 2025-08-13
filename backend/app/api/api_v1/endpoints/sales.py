from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

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


@router.post("/{id}/ship")
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
    
    return crud.sales_order.ship(db=db, sales_order=sales)