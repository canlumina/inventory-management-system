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
    # Convert ORM objects to schema with calculated available_quantity and product info
    result = []
    for item in inventory:
        product_data = None
        if item.product:
            product_data = schemas.Product.model_validate(item.product)
        
        result.append(schemas.Inventory(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            reserved_quantity=item.reserved_quantity,
            updated_at=item.updated_at,
            available_quantity=item.available_quantity,
            product=product_data
        ))
    return result


@router.get("/alerts", response_model=List[schemas.Inventory])
def get_inventory_alerts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get inventory items that are below minimum stock level.
    """
    # Get all inventory records with products
    inventory = crud.inventory.get_multi(db, skip=0, limit=1000)
    
    # Filter for low stock items
    alerts = []
    for item in inventory:
        if item.product and item.available_quantity <= (item.product.min_stock or 0):
            product_data = schemas.Product.model_validate(item.product)
            alerts.append(schemas.Inventory(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                reserved_quantity=item.reserved_quantity,
                updated_at=item.updated_at,
                available_quantity=item.available_quantity,
                product=product_data
            ))
    
    return alerts


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
    
    product_data = None
    if inventory.product:
        product_data = schemas.Product.model_validate(inventory.product)
    
    return schemas.Inventory(
        id=inventory.id,
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        reserved_quantity=inventory.reserved_quantity,
        updated_at=inventory.updated_at,
        available_quantity=inventory.available_quantity,
        product=product_data
    )


@router.post("/adjustment", response_model=schemas.Inventory)
def adjust_inventory(
    *,
    db: Session = Depends(get_db),
    adjustment_in: schemas.InventoryAdjustment,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Adjust inventory quantity.
    """
    inventory = crud.inventory.adjust_quantity(
        db=db, product_id=adjustment_in.product_id, quantity=adjustment_in.quantity
    )
    
    product_data = None
    if inventory.product:
        product_data = schemas.Product.model_validate(inventory.product)
    
    return schemas.Inventory(
        id=inventory.id,
        product_id=inventory.product_id,
        quantity=inventory.quantity,
        reserved_quantity=inventory.reserved_quantity,
        updated_at=inventory.updated_at,
        available_quantity=inventory.available_quantity,
        product=product_data
    )