

from dao.transaction_dao import TransactionDAO
from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any


class TransactionService:

    def __init__(self, config: DatabaseConfig):
        self.transaction_dao = TransactionDAO(config)
        self.vendor_dao = VendorDAO(config)

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        return self.transaction_dao.get_all_transactions()


    def get_transactions_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:
        # Validate vendor
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")

        return self.transaction_dao.get_transactions_by_vendor(vendor_id)

    #
    # def get_transactions_by_order(self, order_id: int) -> List[Dict[str, Any]]:
    #     transactions = self.transaction_dao.get_transactions_by_order(order_id)
    #
    #     if not transactions:
    #         raise ValueError(f"No transactions found for order ID {order_id}")
    #
    #     return transactions


    # def get_vendor_revenue(self, vendor_id: int) -> float:
    #     # Validate vendor
    #     vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
    #     if not vendor:
    #         raise ValueError(f"Vendor with ID {vendor_id} does not exist")


        # transactions = self.get_transactions_by_vendor(vendor_id)
        #
        # #
        # total_revenue = sum(tx['transaction_amount'] for tx in transactions if tx['status'] == 'completed')
        # return total_revenue
