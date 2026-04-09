"""
Customer Data Model
"""

from pydantic import BaseModel, Field
from datetime import datetime


class CustomerBase(BaseModel):
    """Base model for customer - used for creation requests"""
    customer_name: str
    contact_number: str = Field(max_length=20)
    shipping_address: str


class CustomerResponse(CustomerBase):
    """Customer response model - used for API returns"""
    customer_id: int
    created_date: datetime

    class Config:
        from_attributes = True