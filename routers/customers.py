from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from inventory_management.database import get_db
from inventory_management.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from inventory_management.services import customers as customer_service

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def add_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db, payload)


@router.get("", response_model=list[CustomerRead])
def view_customers(db: Session = Depends(get_db)):
    return customer_service.list_customers(db)


@router.get("/{customer_id}", response_model=CustomerRead)
def view_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_service.get_customer(db, customer_id)


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    return customer_service.update_customer(db, customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer_service.delete_customer(db, customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
