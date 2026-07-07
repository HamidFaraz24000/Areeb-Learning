from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory_management.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(191), nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(25), nullable=False)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
