"""
订单 (Order) 数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    """订单项基础模型"""
    product_id: int
    quantity: int = Field(gt=0, description="数量必须>0")


class OrderItemResponse(OrderItemBase):
    """订单项响应模型"""
    order_item_id: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """订单基础模型 - 用于创建请求"""
    customer_id: int
    items: List[OrderItemBase] = Field(min_items=1, description="至少需要一个商品")


class OrderResponse(BaseModel):
    """订单响应模型 - 用于API返回"""
    order_id: int
    customer_id: int
    total_price: float
    status: str
    order_date: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
