

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Quantity must be > 0")


class OrderItemResponse(OrderItemBase):
    order_item_id: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_id: int
    items: List[OrderItemBase] = Field(min_items=1, description="At least one item is required")


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    total_price: float
    status: str
    order_date: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True