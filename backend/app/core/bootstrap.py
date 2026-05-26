from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.core.config import settings
from app.models.user import User, UserRole


def ensure_default_admin(
    db: Session,
    *,
    username: str,
    email: str,
    password: str,
) -> User:
    existing_user = (
        db.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )
    if existing_user:
        return existing_user

    user = User(
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        role=UserRole.admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def bootstrap_default_admin() -> None:
    if not settings.create_default_admin:
        print("Default admin bootstrap disabled.")
        return

    if not settings.default_admin_password:
        raise RuntimeError("DEFAULT_ADMIN_PASSWORD must be set when CREATE_DEFAULT_ADMIN=true")

    db = SessionLocal()
    try:
        user = ensure_default_admin(
            db,
            username=settings.default_admin_username,
            email=settings.default_admin_email,
            password=settings.default_admin_password,
        )
        print(f"Default admin ready: {user.username}")
    finally:
        db.close()


if __name__ == "__main__":
    bootstrap_default_admin()
