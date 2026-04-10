
from dao.customer_dao import CustomerDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class CustomerService:

    def __init__(self, config: DatabaseConfig):
        self.customer_dao = CustomerDAO(config)

    def get_all_customers(self) -> List[Dict[str, Any]]:
        # try:
        #     return self.customer_dao.get_all_customers()
        # except Exception as e:
        #     raise Exception(f"Failed to get customer list: {str(e)}")

        return self.customer_dao.get_all_customers()

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        if not customer_id or customer_id <= 0:
            raise ValueError("Invalid customer ID")

        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")
        return customer

    # def customer_count(self, customer_id: int) -> int:
    #     customer = self.customer_dao.get_customer_by_id(customer_id)
    #     return customer is not None

    def create_customer(self, customer_name: str, contact_number: str,
                       shipping_address: str) -> Dict[str, Any]:
        """
        Create a new customer
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

        affected_rows, customer_id = self.customer_dao.create_customer(
            customer_name.strip(), contact_number.strip(), shipping_address.strip()
        )

        if affected_rows > 0:
            return self.get_customer_by_id(customer_id)
        else:
            raise Exception("Failed to create customer")



    def customer_exists(self, customer_id: int) -> bool:
        customer = self.customer_dao.get_customer_by_id(customer_id)
        return customer is not None