from pydantic import BaseModel, ConfigDict, EmailStr, Field


PHONE_PATTERN = r"^\+?[0-9 ()-]{7,25}$"


class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    phone_number: str = Field(..., min_length=7, max_length=25, pattern=PHONE_PATTERN)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, min_length=7, max_length=25, pattern=PHONE_PATTERN)


class CustomerRead(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
