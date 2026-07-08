from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=80)
    unit_price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    available_quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    unit_price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    available_quantity: int | None = Field(default=None, ge=0)


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
