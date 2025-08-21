from typing import Any, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, case

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db
from app.models.purchase_order import PurchaseOrderStatus
from app.models.sales_order import SalesOrderStatus
from app.models.inventory_transaction import TransactionType, ReferenceType

router = APIRouter()


class InventoryReportItem(BaseModel):
    product_id: int
    product_name: str
    product_code: str
    current_stock: int
    reserved_stock: int
    available_stock: int
    min_stock: int
    stock_status: str  # normal, warning, out_of_stock
    stock_value: Decimal  # current_stock * purchase_price


class InventoryReport(BaseModel):
    total_products: int
    total_stock_value: Decimal
    low_stock_products: int
    out_of_stock_products: int
    items: List[InventoryReportItem]


@router.get("/inventory", response_model=InventoryReport)
def get_inventory_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get inventory statistics report.
    """
    # Get inventory with product info
    inventory_query = (
        db.query(models.Inventory, models.Product)
        .join(models.Product)
        .all()
    )
    
    items = []
    total_stock_value = Decimal('0')
    low_stock_count = 0
    out_of_stock_count = 0
    
    for inventory, product in inventory_query:
        # Calculate stock status
        if inventory.available_quantity == 0:
            stock_status = "out_of_stock"
            out_of_stock_count += 1
        elif inventory.available_quantity <= (product.min_stock or 0):
            stock_status = "warning"
            low_stock_count += 1
        else:
            stock_status = "normal"
        
        # Calculate stock value
        stock_value = Decimal(str(inventory.quantity)) * (product.purchase_price or Decimal('0'))
        total_stock_value += stock_value
        
        items.append(InventoryReportItem(
            product_id=product.id,
            product_name=product.name,
            product_code=product.code,
            current_stock=inventory.quantity,
            reserved_stock=inventory.reserved_quantity,
            available_stock=inventory.available_quantity,
            min_stock=product.min_stock or 0,
            stock_status=stock_status,
            stock_value=stock_value
        ))
    
    return InventoryReport(
        total_products=len(items),
        total_stock_value=total_stock_value,
        low_stock_products=low_stock_count,
        out_of_stock_products=out_of_stock_count,
        items=items
    )


class PurchaseReportSummary(BaseModel):
    total_orders: int
    total_amount: Decimal
    pending_orders: int
    confirmed_orders: int
    received_orders: int
    cancelled_orders: int


class PurchaseReportItem(BaseModel):
    order_id: int
    order_number: str
    supplier_name: str
    status: str
    order_date: datetime
    total_amount: Decimal
    items_count: int


class PurchaseReport(BaseModel):
    summary: PurchaseReportSummary
    orders: List[PurchaseReportItem]


@router.get("/purchases", response_model=PurchaseReport)
def get_purchase_report(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get purchase statistics report.
    """
    # Build query with date filters
    query = db.query(models.PurchaseOrder).join(models.Supplier)
    
    if start_date:
        query = query.filter(models.PurchaseOrder.order_date >= start_date)
    if end_date:
        query = query.filter(models.PurchaseOrder.order_date <= end_date)
    
    orders = query.all()
    
    # Calculate summary statistics
    total_amount = sum(order.total_amount or Decimal('0') for order in orders)
    status_counts = {
        'pending': sum(1 for order in orders if order.status == PurchaseOrderStatus.pending),
        'confirmed': sum(1 for order in orders if order.status == PurchaseOrderStatus.confirmed),
        'received': sum(1 for order in orders if order.status == PurchaseOrderStatus.received),
        'cancelled': sum(1 for order in orders if order.status == PurchaseOrderStatus.cancelled),
    }
    
    # Build report items
    order_items = []
    for order in orders:
        items_count = len(order.items) if order.items else 0
        order_items.append(PurchaseReportItem(
            order_id=order.id,
            order_number=order.order_number,
            supplier_name=order.supplier.name if order.supplier else "",
            status=order.status.value,
            order_date=order.order_date,
            total_amount=order.total_amount or Decimal('0'),
            items_count=items_count
        ))
    
    summary = PurchaseReportSummary(
        total_orders=len(orders),
        total_amount=total_amount,
        pending_orders=status_counts['pending'],
        confirmed_orders=status_counts['confirmed'],
        received_orders=status_counts['received'],
        cancelled_orders=status_counts['cancelled']
    )
    
    return PurchaseReport(summary=summary, orders=order_items)


class SalesReportSummary(BaseModel):
    total_orders: int
    total_amount: Decimal
    total_revenue: Decimal
    pending_orders: int
    confirmed_orders: int
    shipped_orders: int
    delivered_orders: int
    cancelled_orders: int


class SalesReportItem(BaseModel):
    order_id: int
    order_number: str
    customer_name: str
    status: str
    order_date: datetime
    total_amount: Decimal
    items_count: int


class SalesReport(BaseModel):
    summary: SalesReportSummary
    orders: List[SalesReportItem]


@router.get("/sales", response_model=SalesReport)
def get_sales_report(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get sales statistics report.
    """
    # Build query with date filters
    query = db.query(models.SalesOrder).join(models.Customer)
    
    if start_date:
        query = query.filter(models.SalesOrder.order_date >= start_date)
    if end_date:
        query = query.filter(models.SalesOrder.order_date <= end_date)
    
    orders = query.all()
    
    # Calculate summary statistics
    total_amount = sum(order.total_amount or Decimal('0') for order in orders)
    # Revenue only from completed orders (shipped/delivered)
    completed_orders = [o for o in orders if o.status in [SalesOrderStatus.shipped, SalesOrderStatus.delivered]]
    total_revenue = sum(order.total_amount or Decimal('0') for order in completed_orders)
    
    status_counts = {
        'pending': sum(1 for order in orders if order.status == SalesOrderStatus.pending),
        'confirmed': sum(1 for order in orders if order.status == SalesOrderStatus.confirmed),
        'shipped': sum(1 for order in orders if order.status == SalesOrderStatus.shipped),
        'delivered': sum(1 for order in orders if order.status == SalesOrderStatus.delivered),
        'cancelled': sum(1 for order in orders if order.status == SalesOrderStatus.cancelled),
    }
    
    # Build report items
    order_items = []
    for order in orders:
        items_count = len(order.items) if order.items else 0
        order_items.append(SalesReportItem(
            order_id=order.id,
            order_number=order.order_number,
            customer_name=order.customer.name if order.customer else "",
            status=order.status.value,
            order_date=order.order_date,
            total_amount=order.total_amount or Decimal('0'),
            items_count=items_count
        ))
    
    summary = SalesReportSummary(
        total_orders=len(orders),
        total_amount=total_amount,
        total_revenue=total_revenue,
        pending_orders=status_counts['pending'],
        confirmed_orders=status_counts['confirmed'],
        shipped_orders=status_counts['shipped'],
        delivered_orders=status_counts['delivered'],
        cancelled_orders=status_counts['cancelled']
    )
    
    return SalesReport(summary=summary, orders=order_items)


class FinancialSummary(BaseModel):
    total_purchase_cost: Decimal
    total_sales_revenue: Decimal
    gross_profit: Decimal
    gross_profit_margin: float  # percentage


@router.get("/financial", response_model=FinancialSummary)
def get_financial_report(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get financial statistics report (cost and profit analysis).
    """
    # Get purchase costs (received orders only)
    purchase_query = db.query(models.PurchaseOrder).filter(
        models.PurchaseOrder.status == PurchaseOrderStatus.received
    )
    if start_date:
        purchase_query = purchase_query.filter(models.PurchaseOrder.order_date >= start_date)
    if end_date:
        purchase_query = purchase_query.filter(models.PurchaseOrder.order_date <= end_date)
    
    purchases = purchase_query.all()
    total_purchase_cost = sum(order.total_amount or Decimal('0') for order in purchases)
    
    # Get sales revenue (shipped/delivered orders only)
    sales_query = db.query(models.SalesOrder).filter(
        models.SalesOrder.status.in_([SalesOrderStatus.shipped, SalesOrderStatus.delivered])
    )
    if start_date:
        sales_query = sales_query.filter(models.SalesOrder.order_date >= start_date)
    if end_date:
        sales_query = sales_query.filter(models.SalesOrder.order_date <= end_date)
    
    sales = sales_query.all()
    total_sales_revenue = sum(order.total_amount or Decimal('0') for order in sales)
    
    # Calculate profit
    gross_profit = total_sales_revenue - total_purchase_cost
    gross_profit_margin = float(gross_profit / total_sales_revenue * 100) if total_sales_revenue > 0 else 0.0
    
    return FinancialSummary(
        total_purchase_cost=total_purchase_cost,
        total_sales_revenue=total_sales_revenue,
        gross_profit=gross_profit,
        gross_profit_margin=round(gross_profit_margin, 2)
    )


class DashboardSummary(BaseModel):
    total_products: int
    low_stock_alerts: int
    total_inventory_value: Decimal
    pending_purchase_orders: int
    pending_sales_orders: int
    monthly_revenue: Decimal
    monthly_orders: int
    top_selling_product: Optional[str]


@router.get("/dashboard", response_model=DashboardSummary)
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get dashboard summary data.
    """
    # Product and inventory stats
    total_products = db.query(models.Product).count()
    
    # Low stock alerts - need to handle available_quantity as property
    inventory_items = (
        db.query(models.Inventory, models.Product)
        .join(models.Product)
        .all()
    )
    low_stock_alerts = sum(
        1 for inv, prod in inventory_items 
        if inv.available_quantity <= (prod.min_stock or 0)
    )
    
    # Total inventory value
    inventory_query = (
        db.query(models.Inventory, models.Product)
        .join(models.Product)
        .all()
    )
    total_inventory_value = sum(
        Decimal(str(inv.quantity)) * (prod.purchase_price or Decimal('0'))
        for inv, prod in inventory_query
    )
    
    # Pending orders
    pending_purchases = db.query(models.PurchaseOrder).filter(
        models.PurchaseOrder.status == PurchaseOrderStatus.pending
    ).count()
    
    pending_sales = db.query(models.SalesOrder).filter(
        models.SalesOrder.status == SalesOrderStatus.pending
    ).count()
    
    # Monthly stats (current month)
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
    
    monthly_sales = db.query(models.SalesOrder).filter(
        and_(
            models.SalesOrder.order_date >= current_month_start,
            models.SalesOrder.order_date < next_month_start,
            models.SalesOrder.status.in_([SalesOrderStatus.shipped, SalesOrderStatus.delivered])
        )
    ).all()
    
    monthly_revenue = sum(order.total_amount or Decimal('0') for order in monthly_sales)
    monthly_orders = len(monthly_sales)
    
    # Top selling product (simplified - just get first product for demo)
    top_product = db.query(models.Product).first()
    top_selling_product = top_product.name if top_product else None
    
    return DashboardSummary(
        total_products=total_products,
        low_stock_alerts=low_stock_alerts,
        total_inventory_value=total_inventory_value,
        pending_purchase_orders=pending_purchases,
        pending_sales_orders=pending_sales,
        monthly_revenue=monthly_revenue,
        monthly_orders=monthly_orders,
        top_selling_product=top_selling_product
    )