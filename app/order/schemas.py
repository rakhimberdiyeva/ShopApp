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
    order_id: int
    product_id: int
    quantity: int
    price: Decimal = Field(max_digits=20, decimal_places=2)


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


class OrderCreate(OrderBase):
    user_id: int
    status: OrderStatusEnum = OrderStatusEnum.new

class OrderUpdate(OrderBase):
    pass


class OrderStatusUpdate(BaseModel):
    status: str = Field(max_length=30)


class OrderRead(OrderBase):
    id: int
    user_id: int
    status: OrderStatusEnum = OrderStatusEnum.new
    created_at: datetime
    products: list[OrderProductsRead]

