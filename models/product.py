from decimal import Decimal

from sqlalchemy import CheckConstraint, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory_management.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    available_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    order_items = relationship("OrderItem", back_populates="product")

    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="ck_products_unit_price_non_negative"),
        CheckConstraint("available_quantity >= 0", name="ck_products_quantity_non_negative"),
    )
