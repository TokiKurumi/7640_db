"""
Transaction Service Layer (TransactionService)
"""

from dao.transaction_dao import TransactionDAO
from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any


class TransactionService:
    """Transaction business logic class"""

    def __init__(self, config: DatabaseConfig):
        self.transaction_dao = TransactionDAO(config)
        self.vendor_dao = VendorDAO(config)

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """Get all transactions"""
        try:
            return self.transaction_dao.get_all_transactions()
        except Exception as e:
            raise Exception(f"Failed to get transaction list: {str(e)}")

    def get_transactions_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:
        """
        Get transactions by vendor ID
        :param vendor_id: Vendor ID
        :return: List of transactions
        """
        # Validate vendor
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")

        try:
            return self.transaction_dao.get_transactions_by_vendor(vendor_id)
        except Exception as e:
            raise Exception(f"Failed to get transaction list: {str(e)}")

    def get_transactions_by_order(self, order_id: int) -> List[Dict[str, Any]]:
        """Get transactions by order ID"""
        try:
            transactions = self.transaction_dao.get_transactions_by_order(order_id)
            if not transactions:
                raise ValueError(f"No transactions found for order ID {order_id}")
            return transactions
        except Exception as e:
            raise Exception(f"Failed to get transactions: {str(e)}")

    def get_vendor_revenue(self, vendor_id: int) -> float:
        """Get total revenue for a vendor"""
        # Validate vendor
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")

        try:
            transactions = self.get_transactions_by_vendor(vendor_id)
            total_revenue = sum(tx['transaction_amount'] for tx in transactions if tx['status'] == 'completed')
            return total_revenue
        except Exception as e:
            raise Exception(f"Failed to calculate revenue: {str(e)}")