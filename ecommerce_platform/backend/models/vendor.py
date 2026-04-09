"""
Vendor Data Model
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendorBase(BaseModel):
    """Base model for a vendor - used for creation requests"""
    business_name: str
    geographical_presence: Optional[str] = None


class VendorResponse(VendorBase):
    """Vendor response model - used for API returns"""
    vendor_id: int
    average_rating: float
    created_date: datetime

    class Config:
        from_attributes = True