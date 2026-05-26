from pathlib import Path
import ast
import unittest


class InitialSchemaMigrationTest(unittest.TestCase):
    def test_initial_schema_migration_exists(self):
        versions_dir = Path(__file__).resolve().parents[1] / "alembic" / "versions"
        migrations = sorted(versions_dir.glob("*initial_schema.py"))

        self.assertEqual(len(migrations), 1)

    def test_initial_schema_migration_creates_core_tables(self):
        versions_dir = Path(__file__).resolve().parents[1] / "alembic" / "versions"
        migration = next(versions_dir.glob("*initial_schema.py"))
        contents = migration.read_text()
        tree = ast.parse(contents)

        created_tables = {
            node.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "create_table"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        }

        expected_tables = {
            "users",
            "categories",
            "products",
            "suppliers",
            "customers",
            "inventory",
            "purchase_orders",
            "purchase_order_items",
            "sales_orders",
            "sales_order_items",
            "inventory_transactions",
        }

        for table_name in expected_tables:
            with self.subTest(table_name=table_name):
                self.assertIn(table_name, created_tables)


if __name__ == "__main__":
    unittest.main()
