from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Supplier])
def read_suppliers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve suppliers.
    """
    suppliers = crud.supplier.get_multi(db, skip=skip, limit=limit)
    return suppliers


@router.post("/", response_model=schemas.Supplier)
def create_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_in: schemas.SupplierCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new supplier.
    """
    supplier = crud.supplier.create(db=db, obj_in=supplier_in)
    return supplier


@router.get("/{id}", response_model=schemas.Supplier)
def read_supplier(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get supplier by ID.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.put("/{id}", response_model=schemas.Supplier)
def update_supplier(
    *,
    db: Session = Depends(get_db),
    id: int,
    supplier_in: schemas.SupplierUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a supplier.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.supplier.update(db=db, db_obj=supplier, obj_in=supplier_in)
    return supplier