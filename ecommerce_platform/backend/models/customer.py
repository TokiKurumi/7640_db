

from pydantic import BaseModel, Field
from datetime import datetime


class CustomerBase(BaseModel):
    customer_name: str
    contact_number: str = Field(max_length=20)
    shipping_address: str


class CustomerResponse(CustomerBase):
    customer_id: int
    created_date: datetime

    # Pydantic to build the models with dict
    class Config:
        from_attributes = True