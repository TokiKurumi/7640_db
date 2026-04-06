"""
客户 (Customer) 数据模型
"""

from pydantic import BaseModel, Field
from datetime import datetime


class CustomerBase(BaseModel):
    """客户基础模型 - 用于创建请求"""
    customer_name: str
    contact_number: str = Field(max_length=20)
    shipping_address: str


class CustomerResponse(CustomerBase):
    """客户响应模型 - 用于API返回"""
    customer_id: int
    created_date: datetime

    class Config:
        from_attributes = True
