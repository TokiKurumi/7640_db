
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendorBase(BaseModel):
    business_name: str
    geographical_presence: Optional[str] = None


class VendorResponse(VendorBase):
    vendor_id: int
    average_rating: float
    created_date: datetime

    class Config:
        from_attributes = True