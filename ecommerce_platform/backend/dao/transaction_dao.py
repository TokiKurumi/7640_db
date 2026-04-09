"""
Transaction Data Access Object (TransactionDAO)
"""

from . import BaseDAO, DatabaseConfig
from typing import List, Dict, Any, Optional, Tuple


class TransactionDAO(BaseDAO):
    """Transaction data access class"""

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """Get all transactions"""
        query = """
            SELECT transaction_id, order_id, vendor_id, customer_id, product_id, 
                   quantity, transaction_amount, transaction_date, status 
            FROM transactions 
            ORDER BY transaction_date DESC
        """
        return self.execute_query(query)

    def get_transactions_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:
        """Get transactions by vendor ID"""
        query = """
            SELECT transaction_id, order_id, vendor_id, customer_id, product_id, 
                   quantity, transaction_amount, transaction_date, status 
            FROM transactions 
            WHERE vendor_id = %s 
            ORDER BY transaction_date DESC
        """
        return self.execute_query(query, (vendor_id,))

    def get_transactions_by_order(self, order_id: int) -> List[Dict[str, Any]]:
        """Get transactions by order ID"""
        query = """
            SELECT transaction_id, order_id, vendor_id, customer_id, product_id, 
                   quantity, transaction_amount, transaction_date, status 
            FROM transactions 
            WHERE order_id = %s
        """
        return self.execute_query(query, (order_id,))

    def create_transaction(self, order_id: int, vendor_id: int, customer_id: int,
                          product_id: int, quantity: int, transaction_amount: float,
                          status: str = 'completed') -> Tuple[int, int]:
        """Create a new transaction"""
        query = """
            INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, 
                                     transaction_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_update(query, (order_id, vendor_id, customer_id, product_id,
                                           quantity, transaction_amount, status))

    def update_transaction_status(self, transaction_id: int, status: str) -> int:
        """Update transaction status"""
        query = "UPDATE transactions SET status = %s WHERE transaction_id = %s"
        affected_rows, _ = self.execute_update(query, (status, transaction_id))
        return affected_rows