"""
Transaction Data Model
"""

from pydantic import BaseModel
from datetime import datetime


class TransactionResponse(BaseModel):
    """Transaction response model - used for API returns"""
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