from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from enum import Enum


class OrderStatusEnum(str, Enum):
    new = "new"
    paid = "paid"
    completed = "completed"
    cancelled = "cancelled"


class OrderProductsBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)


class OrderProductsCreate(OrderProductsBase):
    pass


class OrderProductsUpdate(OrderProductsBase):
    pass


class OrderProductsRead(OrderProductsBase):
    id: int



class OrderBase(BaseModel):
    address: str = Field(max_length=255)
    phone_number: str = Field(max_length=20)
    comment: str = Field(max_length=255)
    status: OrderStatusEnum = OrderStatusEnum.new


class OrderCreate(OrderBase):
    products: list[OrderProductsCreate]


class OrderUpdate(OrderBase):
    products: list[OrderProductsUpdate]


class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum = OrderStatusEnum.new


class OrderRead(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    products: list[OrderProductsRead]
    total_sum: float

