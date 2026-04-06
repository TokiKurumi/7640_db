"""
供应商 (Vendor) 数据模型
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendorBase(BaseModel):
    """供应商基础模型 - 用于创建请求"""
    business_name: str
    geographical_presence: Optional[str] = None


class VendorResponse(VendorBase):
    """供应商响应模型 - 用于API返回"""
    vendor_id: int
    average_rating: float
    created_date: datetime

    class Config:
        from_attributes = True
