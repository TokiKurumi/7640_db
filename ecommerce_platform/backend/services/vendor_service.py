"""
Vendor Service Layer (VendorService)
"""

from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class VendorService:
    """Vendor business logic class"""

    def __init__(self, config: DatabaseConfig):
        self.vendor_dao = VendorDAO(config)

    def get_all_vendors(self) -> List[Dict[str, Any]]:
        """
        Get all vendors
        :return: List of vendors
        """
        try:
            return self.vendor_dao.get_all_vendors()
        except Exception as e:
            raise Exception(f"Failed to get vendor list: {str(e)}")

    def get_vendor_by_id(self, vendor_id: int) -> Optional[Dict[str, Any]]:
        """
        Get vendor by ID
        :param vendor_id: Vendor ID
        :return: Vendor information or None
        """
        if not vendor_id or vendor_id <= 0:
            raise ValueError("Invalid vendor ID")

        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")
        return vendor

    def create_vendor(self, business_name: str, geographical_presence: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new vendor
        :param business_name: Business name (unique)
        :param geographical_presence: Geographical location
        :return: Newly created vendor information
        """
        # Validate input
        if not business_name or len(business_name.strip()) == 0:
            raise ValueError("Business name cannot be empty")

        business_name = business_name.strip()

        # Check if business name already exists
        if self.vendor_dao.vendor_exists(business_name):
            raise ValueError(f"Business name '{business_name}' already exists")

        try:
            affected_rows, vendor_id = self.vendor_dao.create_vendor(business_name, geographical_presence)

            if affected_rows > 0:
                # Return the newly created vendor
                return self.get_vendor_by_id(vendor_id)
            else:
                raise Exception("Failed to create vendor")
        except Exception as e:
            raise Exception(f"Failed to create vendor: {str(e)}")