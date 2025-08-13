from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TransactionType(str, enum.Enum):
    purchase = "purchase"
    sale = "sale"
    adjustment = "adjustment"


class ReferenceType(str, enum.Enum):
    purchase_order = "purchase_order"
    sales_order = "sales_order"
    manual_adjustment = "manual_adjustment"


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Integer, nullable=False)  # Positive for inbound, negative for outbound
    reference_type = Column(Enum(ReferenceType), nullable=False)
    reference_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="inventory_transactions")