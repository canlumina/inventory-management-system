from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Retrieve users. Admin only.
    """
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new user. Admin only.
    """
    if crud.user.get_by_username(db, username=user_in.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if crud.user.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.user.create(db=db, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user profile.
    """
    return current_user


@router.get("/{id}", response_model=schemas.User)
def read_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Get user by ID. Admin only.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update user. Admin only.
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.update(db=db, db_obj=user, obj_in=user_in)


@router.delete("/{id}", response_model=schemas.User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Delete user. Admin only.
    """
    if current_user.id == id:
        raise HTTPException(status_code=400, detail="Cannot delete current user")

    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.remove(db=db, id=id)
