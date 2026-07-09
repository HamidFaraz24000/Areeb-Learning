from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from inventory_management.models.customer import Customer
from inventory_management.schemas.customer import CustomerCreate, CustomerUpdate


def _ensure_email_is_available(db: Session, email: str, customer_id: int | None = None) -> None:
    query = select(Customer).where(Customer.email == email)
    existing = db.scalar(query)
    if existing and existing.id != customer_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customer email already exists")


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    _ensure_email_is_available(db, payload.email)
    customer = Customer(**payload.model_dump())
    db.add(customer)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customer email already exists") from exc
    db.refresh(customer)
    return customer


def list_customers(db: Session) -> list[Customer]:
    return list(db.scalars(select(Customer).order_by(Customer.id)).all())


def get_customer(db: Session, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


def update_customer(db: Session, customer_id: int, payload: CustomerUpdate) -> Customer:
    customer = get_customer(db, customer_id)
    data = payload.model_dump(exclude_unset=True)
    if "email" in data:
        _ensure_email_is_available(db, data["email"], customer_id=customer_id)
    for key, value in data.items():
        setattr(customer, key, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customer email already exists") from exc
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    customer = get_customer(db, customer_id)
    db.delete(customer)
    db.commit()
