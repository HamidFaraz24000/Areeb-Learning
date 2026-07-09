from collections import Counter
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from inventory_management.models.customer import Customer
from inventory_management.models.order import Order, OrderItem
from inventory_management.models.product import Product
from inventory_management.schemas.order import OrderCreate


def _get_order_query():
    return (
        select(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.items).joinedload(OrderItem.product),
        )
        .order_by(Order.id)
    )


def create_order(db: Session, payload: OrderCreate) -> Order:
    customer = db.get(Customer, payload.customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    requested_quantities = Counter()
    for item in payload.items:
        requested_quantities[item.product_id] += item.quantity

    products = {
        product.id: product
        for product in db.scalars(select(Product).where(Product.id.in_(requested_quantities.keys()))).all()
    }

    missing_ids = [product_id for product_id in requested_quantities if product_id not in products]
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found: {missing_ids[0]}",
        )

    for product_id, quantity in requested_quantities.items():
        product = products[product_id]
        if quantity > product.available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product_id}",
            )

    order = Order(customer_id=payload.customer_id, status="CREATED", total_amount=Decimal("0.00"))
    db.add(order)
    db.flush()

    total = Decimal("0.00")
    for product_id, quantity in requested_quantities.items():
        product = products[product_id]
        line_total = product.unit_price * quantity
        product.available_quantity -= quantity
        total += line_total
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.unit_price,
                line_total=line_total,
            )
        )

    order.total_amount = total
    db.commit()
    return get_order(db, order.id)


def get_order(db: Session, order_id: int) -> Order:
    order = db.execute(_get_order_query().where(Order.id == order_id)).unique().scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


def list_orders(db: Session) -> list[Order]:
    return list(db.scalars(_get_order_query()).unique().all())


def cancel_order(db: Session, order_id: int) -> Order:
    order = get_order(db, order_id)
    if order.status == "CANCELLED":
        return order

    for item in order.items:
        item.product.available_quantity += item.quantity
    order.status = "CANCELLED"
    db.commit()
    return get_order(db, order.id)
