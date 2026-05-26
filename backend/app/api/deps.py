from typing import Callable, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import UserRole

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_str}/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        token_data = schemas.TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=int(token_data.sub)) if token_data.sub else None
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_roles(*allowed_roles: UserRole) -> Callable[[models.User], models.User]:
    def role_checker(
        current_user: models.User = Depends(get_current_user),
    ) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker


get_current_admin_user = require_roles(UserRole.admin)
