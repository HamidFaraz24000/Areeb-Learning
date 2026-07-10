from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from inventory_management.database import get_db
from inventory_management.schemas.product import ProductCreate, ProductRead, ProductUpdate
from inventory_management.services import products as product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def add_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, payload)


@router.get("", response_model=list[ProductRead])
def view_products(
    search: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    return product_service.list_products(db, search=search, category=category)


@router.get("/{product_id}", response_model=ProductRead)
def view_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update_product(db, product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
