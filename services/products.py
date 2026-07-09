from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from inventory_management.models.product import Product
from inventory_management.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, payload: ProductCreate) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session, search: str | None = None, category: str | None = None) -> list[Product]:
    query = select(Product)
    if search:
        like_term = f"%{search}%"
        query = query.where(or_(Product.name.like(like_term), Product.description.like(like_term)))
    if category:
        query = query.where(Product.category == category)
    return list(db.scalars(query.order_by(Product.id)).all())


def get_product(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_product(db, product_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
