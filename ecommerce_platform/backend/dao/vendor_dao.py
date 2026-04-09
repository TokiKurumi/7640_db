"""
Vendor Data Access Object (VendorDAO)
"""

from . import BaseDAO, DatabaseConfig
from typing import List, Dict, Any, Optional


class VendorDAO(BaseDAO):
    """Vendor data access class"""

    def get_all_vendors(self) -> List[Dict[str, Any]]:
        """Get all vendors"""
        query = """
            SELECT vendor_id, business_name, average_rating, geographical_presence, created_date 
            FROM vendors 
            ORDER BY vendor_id
        """
        return self.execute_query(query)

    def get_vendor_by_id(self, vendor_id: int) -> Optional[Dict[str, Any]]:
        """Get vendor by ID"""
        query = """
            SELECT vendor_id, business_name, average_rating, geographical_presence, created_date 
            FROM vendors 
            WHERE vendor_id = %s
        """
        return self.execute_query(query, (vendor_id,), fetch_one=True)

    def create_vendor(self, business_name: str, geographical_presence: Optional[str] = None) -> tuple[int, int]:
        """Create a new vendor"""
        query = """
            INSERT INTO vendors (business_name, geographical_presence, average_rating)
            VALUES (%s, %s, 0.0)
        """
        return self.execute_update(query, (business_name, geographical_presence))

    def vendor_exists(self, business_name: str) -> bool:
        """Check if a vendor exists"""
        query = "SELECT vendor_id FROM vendors WHERE business_name = %s"
        result = self.execute_query(query, (business_name,), fetch_one=True)
        return result is not None


# Import Tuple
from typing import Tuple