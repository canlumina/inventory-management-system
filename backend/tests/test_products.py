import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import deps
from app.core.database import Base, get_db
from app.main import app
from app.models.category import Category
from app.models.product import Product
from app.models.user import User, UserRole


class ProductEndpointTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()
        self.user = self._create_user()

        def override_get_db():
            yield self.db

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[deps.get_current_user] = lambda: self.user
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def _create_user(self):
        user = User(
            username="admin",
            email="admin@example.com",
            password_hash="hashed",
            role=UserRole.admin,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def _create_category(self, name):
        category = Category(name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def _create_product(self, name, code, category_id=None):
        product = Product(
            name=name,
            code=code,
            category_id=category_id,
            unit="pcs",
            min_stock=0,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def test_read_products_filters_by_category_id(self):
        target_category = self._create_category("Hardware")
        other_category = self._create_category("Software")
        target_product = self._create_product("Keyboard", "KEYBOARD", target_category.id)
        self._create_product("License", "LICENSE", other_category.id)

        response = self.client.get("/api/v1/products/", params={"category_id": target_category.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [target_product.id])

    def test_read_products_filters_parent_category_with_descendants(self):
        parent_category = self._create_category("Hardware")
        child_category = Category(name="Keyboards", parent_id=parent_category.id)
        other_category = self._create_category("Software")
        self.db.add(child_category)
        self.db.commit()
        self.db.refresh(child_category)
        target_product = self._create_product("Mechanical Keyboard", "MECH-KEYBOARD", child_category.id)
        self._create_product("License", "LICENSE", other_category.id)

        response = self.client.get("/api/v1/products/", params={"category_id": parent_category.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [target_product.id])

    def test_read_products_filters_by_search_keyword(self):
        target_product = self._create_product("Industrial Keyboard", "IND-KEYBOARD")
        self._create_product("Office Mouse", "OFFICE-MOUSE")

        response = self.client.get("/api/v1/products/", params={"search": "keyboard"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [target_product.id])

    def test_delete_product_returns_serializable_deleted_product(self):
        product = self._create_product("Delete Me", "DELETE-ME")

        response = self.client.delete(f"/api/v1/products/{product.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], product.id)
        self.assertEqual(self.client.get(f"/api/v1/products/{product.id}").status_code, 404)


if __name__ == "__main__":
    unittest.main()
