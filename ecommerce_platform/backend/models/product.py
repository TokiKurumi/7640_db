"""
Product Data Model
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Base model for a product - used for creation requests"""
    product_name: str
    listed_price: float = Field(gt=0, description="Price must be greater than 0")
    stock_quantity: int = Field(ge=0, description="Stock must be ≥ 0")
    tag1: Optional[str] = None
    tag2: Optional[str] = None
    tag3: Optional[str] = None


class ProductResponse(ProductBase):
    """Product response model - used for API returns"""
    product_id: int
    vendor_id: int
    created_date: datetime

    class Config:
        from_attributes = True