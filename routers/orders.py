from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from inventory_management.database import get_db
from inventory_management.schemas.order import OrderCreate, OrderRead
from inventory_management.services import orders as order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, payload)


@router.get("", response_model=list[OrderRead])
def view_all_orders(db: Session = Depends(get_db)):
    return order_service.list_orders(db)


@router.get("/{order_id}", response_model=OrderRead)
def view_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(db, order_id)


@router.patch("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.cancel_order(db, order_id)
