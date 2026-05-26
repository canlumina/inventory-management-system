import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.security import verify_password
from app.core.bootstrap import ensure_default_admin
from app.models.user import User, UserRole


class DefaultAdminBootstrapTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_creates_default_admin_user(self):
        credential = "admin123"
        user = ensure_default_admin(
            self.db,
            username="admin",
            email="admin@example.com",
            password=credential,
        )

        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.role, UserRole.admin)
        self.assertTrue(verify_password(credential, user.password_hash))

    def test_does_not_duplicate_existing_default_admin(self):
        credential = "admin123"
        changed_credential = "changed-password"
        first = ensure_default_admin(
            self.db,
            username="admin",
            email="admin@example.com",
            password=credential,
        )
        second = ensure_default_admin(
            self.db,
            username="admin",
            email="admin@example.com",
            password=changed_credential,
        )

        self.assertEqual(first.id, second.id)
        self.assertEqual(self.db.query(User).count(), 1)
        self.assertTrue(verify_password(credential, second.password_hash))


if __name__ == "__main__":
    unittest.main()
