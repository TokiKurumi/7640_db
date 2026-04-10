

from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class VendorService:

    def __init__(self, config: DatabaseConfig):
        self.vendor_dao = VendorDAO(config)

    def get_all_vendors(self) -> List[Dict[str, Any]]:
        return self.vendor_dao.get_all_vendors()


    def get_vendor_by_id(self, vendor_id: int) -> Optional[Dict[str, Any]]:

        if not vendor_id or vendor_id <= 0:
            raise ValueError("Invalid vendor ID")

        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)

        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")
        return vendor

    def create_vendor(self, business_name: str, geographical_presence: Optional[str] = None) -> Dict[str, Any]:

        # Validate input
        if not business_name or len(business_name.strip()) == 0:
            raise ValueError("Business name cannot be empty")

        business_name = business_name.strip()

        # Check if business name already exists
        if self.vendor_dao.vendor_exists(business_name):
            raise ValueError(f"Business name '{business_name}' already exists")


        affected_rows, vendor_id = self.vendor_dao.create_vendor(business_name, geographical_presence)

        if affected_rows > 0:
            # Return the newly created vendor
            return self.get_vendor_by_id(vendor_id)
        else:
            raise Exception("Failed to create vendor")
