"""
Order Data Model
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    """Base model for order items"""
    product_id: int
    quantity: int = Field(gt=0, description="Quantity must be > 0")


class OrderItemResponse(OrderItemBase):
    """Order item response model"""
    order_item_id: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base model for an order - used for creation requests"""
    customer_id: int
    items: List[OrderItemBase] = Field(min_items=1, description="At least one item is required")


class OrderResponse(BaseModel):
    """Order response model - used for API returns"""
    order_id: int
    customer_id: int
    total_price: float
    status: str
    order_date: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True