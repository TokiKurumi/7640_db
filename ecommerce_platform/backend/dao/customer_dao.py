"""
Customer Data Access Object (CustomerDAO)
"""

from . import BaseDAO, DatabaseConfig
from typing import List, Dict, Any, Optional, Tuple


class CustomerDAO(BaseDAO):
    """Customer data access class"""

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers"""
        query = """
            SELECT customer_id, customer_name, contact_number, shipping_address, created_date 
            FROM customers 
            ORDER BY customer_id
        """
        return self.execute_query(query)

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Get customer by ID"""
        query = """
            SELECT customer_id, customer_name, contact_number, shipping_address, created_date 
            FROM customers 
            WHERE customer_id = %s
        """
        return self.execute_query(query, (customer_id,), fetch_one=True)

    def create_customer(self, customer_name: str, contact_number: str,
                       shipping_address: str) -> Tuple[int, int]:
        """Create a new customer"""
        query = """
            INSERT INTO customers (customer_name, contact_number, shipping_address)
            VALUES (%s, %s, %s)
        """
        return self.execute_update(query, (customer_name, contact_number, shipping_address))

    def customer_exists(self, contact_number: str) -> bool:
        """Check if a customer exists (by contact number)"""
        query = "SELECT customer_id FROM customers WHERE contact_number = %s"
        result = self.execute_query(query, (contact_number,), fetch_one=True)
        return result is not None