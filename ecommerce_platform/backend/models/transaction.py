"""
交易 (Transaction) 数据模型
"""

from pydantic import BaseModel
from datetime import datetime


class TransactionResponse(BaseModel):
    """交易响应模型 - 用于API返回"""
    transaction_id: int
    order_id: int
    vendor_id: int
    customer_id: int
    product_id: int
    quantity: int
    transaction_amount: float
    transaction_date: datetime
    status: str

    class Config:
        from_attributes = True
