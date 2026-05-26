import unittest

from pydantic import ValidationError

from app.core.config import Settings


class ProductionConfigSecurityTest(unittest.TestCase):
    def test_development_allows_default_secret_for_local_startup(self):
        settings = Settings(
            environment="development",
            secret_key="your-secret-key-here",
            database_url="postgresql://postgres:password@localhost:5432/inventory_db",
        )

        self.assertEqual(settings.environment, "development")

    def test_production_rejects_default_secret_key(self):
        with self.assertRaises(ValidationError) as raised:
            Settings(
                environment="production",
                secret_key="your-secret-key-here",
                database_url="postgresql://postgres:prod-db-password@localhost:5432/inventory_db",
            )

        self.assertIn("SECRET_KEY", str(raised.exception))

    def test_production_rejects_default_database_password(self):
        with self.assertRaises(ValidationError) as raised:
            Settings(
                environment="production",
                secret_key="prod-secret-key-with-at-least-32-characters",
                database_url="postgresql://postgres:password@localhost:5432/inventory_db",
            )

        self.assertIn("DATABASE_URL", str(raised.exception))

    def test_production_rejects_default_admin_password(self):
        credential = "admin123"
        with self.assertRaises(ValidationError) as raised:
            Settings(
                environment="production",
                secret_key="prod-secret-key-with-at-least-32-characters",
                database_url="postgresql://postgres:prod-db-password@localhost:5432/inventory_db",
                create_default_admin=True,
                default_admin_password=credential,
            )

        self.assertIn("DEFAULT_ADMIN_PASSWORD", str(raised.exception))

    def test_production_allows_strong_runtime_settings(self):
        settings = Settings(
            environment="production",
            secret_key="prod-secret-key-with-at-least-32-characters",
            database_url="postgresql://postgres:prod-db-password@localhost:5432/inventory_db",
            create_default_admin=False,
        )

        self.assertEqual(settings.environment, "production")


if __name__ == "__main__":
    unittest.main()
