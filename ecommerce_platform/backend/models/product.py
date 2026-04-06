"""
产品 (Product) 数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """产品基础模型 - 用于创建请求"""
    product_name: str
    listed_price: float = Field(gt=0, description="价格必须大于0")
    stock_quantity: int = Field(ge=0, description="库存必须≥0")
    tag1: Optional[str] = None
    tag2: Optional[str] = None
    tag3: Optional[str] = None


class ProductResponse(ProductBase):
    """产品响应模型 - 用于API返回"""
    product_id: int
    vendor_id: int
    created_date: datetime

    class Config:
        from_attributes = True
