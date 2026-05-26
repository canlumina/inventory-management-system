"""initial schema

Revision ID: 202605260001
Revises:
Create Date: 2026-05-26 00:00:01.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202605260001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role = sa.Enum("admin", "manager", "staff", name="userrole")
purchase_order_status = sa.Enum(
    "pending", "confirmed", "received", "cancelled", name="purchaseorderstatus"
)
sales_order_status = sa.Enum(
    "pending", "confirmed", "shipped", "delivered", "cancelled", name="salesorderstatus"
)
transaction_type = sa.Enum("purchase", "sale", "adjustment", name="transactiontype")
reference_type = sa.Enum(
    "purchase_order", "sales_order", "manual_adjustment", name="referencetype"
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", user_role, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=False)

    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("contact_person", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_suppliers_id"), "suppliers", ["id"], unique=False)
    op.create_index(op.f("ix_suppliers_name"), "suppliers", ["name"], unique=False)

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("contact_person", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_id"), "customers", ["id"], unique=False)
    op.create_index(op.f("ix_customers_name"), "customers", ["name"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit", sa.String(), nullable=False),
        sa.Column("purchase_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("sale_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("min_stock", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)
    op.create_index(op.f("ix_products_code"), "products", ["code"], unique=True)

    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("reserved_quantity", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id"),
    )
    op.create_index(op.f("ix_inventory_id"), "inventory", ["id"], unique=False)

    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_number", sa.String(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("status", purchase_order_status, nullable=True),
        sa.Column("order_date", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchase_orders_id"), "purchase_orders", ["id"], unique=False)
    op.create_index(op.f("ix_purchase_orders_order_number"), "purchase_orders", ["order_number"], unique=True)

    op.create_table(
        "sales_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_number", sa.String(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("status", sales_order_status, nullable=True),
        sa.Column("order_date", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_orders_id"), "sales_orders", ["id"], unique=False)
    op.create_index(op.f("ix_sales_orders_order_number"), "sales_orders", ["order_number"], unique=True)

    op.create_table(
        "inventory_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("transaction_type", transaction_type, nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("reference_type", reference_type, nullable=False),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_inventory_transactions_id"), "inventory_transactions", ["id"], unique=False
    )

    op.create_table(
        "purchase_order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("purchase_order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["purchase_order_id"], ["purchase_orders.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchase_order_items_id"), "purchase_order_items", ["id"], unique=False)

    op.create_table(
        "sales_order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sales_order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["sales_order_id"], ["sales_orders.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_order_items_id"), "sales_order_items", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_sales_order_items_id"), table_name="sales_order_items")
    op.drop_table("sales_order_items")

    op.drop_index(op.f("ix_purchase_order_items_id"), table_name="purchase_order_items")
    op.drop_table("purchase_order_items")

    op.drop_index(op.f("ix_inventory_transactions_id"), table_name="inventory_transactions")
    op.drop_table("inventory_transactions")

    op.drop_index(op.f("ix_sales_orders_order_number"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_id"), table_name="sales_orders")
    op.drop_table("sales_orders")

    op.drop_index(op.f("ix_purchase_orders_order_number"), table_name="purchase_orders")
    op.drop_index(op.f("ix_purchase_orders_id"), table_name="purchase_orders")
    op.drop_table("purchase_orders")

    op.drop_index(op.f("ix_inventory_id"), table_name="inventory")
    op.drop_table("inventory")

    op.drop_index(op.f("ix_products_code"), table_name="products")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")

    op.drop_index(op.f("ix_customers_name"), table_name="customers")
    op.drop_index(op.f("ix_customers_id"), table_name="customers")
    op.drop_table("customers")

    op.drop_index(op.f("ix_suppliers_name"), table_name="suppliers")
    op.drop_index(op.f("ix_suppliers_id"), table_name="suppliers")
    op.drop_table("suppliers")

    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    reference_type.drop(bind, checkfirst=True)
    transaction_type.drop(bind, checkfirst=True)
    sales_order_status.drop(bind, checkfirst=True)
    purchase_order_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
