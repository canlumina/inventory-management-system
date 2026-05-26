import unittest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import schemas
from app.api import deps
from app.api.api_v1.endpoints import users
from app.core.database import Base
from app.models.user import User, UserRole


class UserPermissionTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()
        self.admin = self._create_user("admin", "admin@example.com", UserRole.admin)
        self.staff = self._create_user("staff", "staff@example.com", UserRole.staff)

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def _create_user(self, username, email, role):
        user = User(
            username=username,
            email=email,
            password_hash="hashed",
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def test_role_requirement_rejects_staff_for_admin_action(self):
        require_admin = deps.require_roles(UserRole.admin)

        with self.assertRaises(HTTPException) as raised:
            require_admin(self.staff)

        self.assertEqual(raised.exception.status_code, 403)

    def test_role_requirement_allows_admin_for_admin_action(self):
        require_admin = deps.require_roles(UserRole.admin)

        self.assertEqual(require_admin(self.admin), self.admin)

    def test_admin_can_create_user(self):
        credential = "warehouse123"
        created = users.create_user(
            db=self.db,
            user_in=schemas.UserCreate(
                username="warehouse",
                email="warehouse@example.com",
                password=credential,
                role=UserRole.manager,
            ),
            current_user=self.admin,
        )

        self.assertEqual(created.username, "warehouse")
        self.assertEqual(created.role, UserRole.manager)

    def test_duplicate_username_is_rejected(self):
        credential = "warehouse123"
        with self.assertRaises(HTTPException) as raised:
            users.create_user(
                db=self.db,
                user_in=schemas.UserCreate(
                    username="staff",
                    email="other@example.com",
                    password=credential,
                    role=UserRole.staff,
                ),
                current_user=self.admin,
            )

        self.assertEqual(raised.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
