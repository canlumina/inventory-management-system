from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve customers.
    """
    customers = crud.customer.get_multi(db, skip=skip, limit=limit)
    return customers


@router.post("/", response_model=schemas.Customer)
def create_customer(
    *,
    db: Session = Depends(get_db),
    customer_in: schemas.CustomerCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new customer.
    """
    customer = crud.customer.create(db=db, obj_in=customer_in)
    return customer


@router.get("/{id}", response_model=schemas.Customer)
def read_customer(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get customer by ID.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{id}", response_model=schemas.Customer)
def update_customer(
    *,
    db: Session = Depends(get_db),
    id: int,
    customer_in: schemas.CustomerUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a customer.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = crud.customer.update(db=db, db_obj=customer, obj_in=customer_in)
    return customer