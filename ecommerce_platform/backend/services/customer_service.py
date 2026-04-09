"""
Customer Service Layer (CustomerService)
"""

from dao.customer_dao import CustomerDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class CustomerService:
    """Customer business logic class"""

    def __init__(self, config: DatabaseConfig):
        self.customer_dao = CustomerDAO(config)

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers"""
        try:
            return self.customer_dao.get_all_customers()
        except Exception as e:
            raise Exception(f"Failed to get customer list: {str(e)}")

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Get customer by ID"""
        if not customer_id or customer_id <= 0:
            raise ValueError("Invalid customer ID")

        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")
        return customer

    def create_customer(self, customer_name: str, contact_number: str,
                       shipping_address: str) -> Dict[str, Any]:
        """
        Create a new customer
        :param customer_name: Customer name
        :param contact_number: Contact number (unique)
        :param shipping_address: Shipping address
        :return: Newly created customer information
        """
        # Validate input
        if not customer_name or len(customer_name.strip()) == 0:
            raise ValueError("Customer name cannot be empty")

        if not contact_number or len(contact_number.strip()) == 0:
            raise ValueError("Contact number cannot be empty")

        if not shipping_address or len(shipping_address.strip()) == 0:
            raise ValueError("Shipping address cannot be empty")

        # Check if contact number already exists
        if self.customer_dao.customer_exists(contact_number.strip()):
            raise ValueError(f"Contact number '{contact_number}' is already in use")

        try:
            affected_rows, customer_id = self.customer_dao.create_customer(
                customer_name.strip(), contact_number.strip(), shipping_address.strip()
            )

            if affected_rows > 0:
                return self.get_customer_by_id(customer_id)
            else:
                raise Exception("Failed to create customer")
        except Exception as e:
            raise Exception(f"Failed to create customer: {str(e)}")

    def customer_exists(self, customer_id: int) -> bool:
        """Check if a customer exists"""
        customer = self.customer_dao.get_customer_by_id(customer_id)
        return customer is not None