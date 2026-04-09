"""
Order Data Access Object (OrderDAO)
"""

from . import BaseDAO, DatabaseConfig
from typing import List, Dict, Any, Optional, Tuple


class OrderDAO(BaseDAO):
    """Order data access class"""

    def get_all_orders(self) -> List[Dict[str, Any]]:
        """Get all orders"""
        query = """
            SELECT order_id, customer_id, total_price, status, order_date 
            FROM orders 
            ORDER BY order_date DESC
        """
        return self.execute_query(query)

    def get_orders_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get orders by customer ID"""
        query = """
            SELECT order_id, customer_id, total_price, status, order_date 
            FROM orders 
            WHERE customer_id = %s 
            ORDER BY order_date DESC
        """
        return self.execute_query(query, (customer_id,))

    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        query = """
            SELECT order_id, customer_id, total_price, status, order_date 
            FROM orders 
            WHERE order_id = %s
        """
        return self.execute_query(query, (order_id,), fetch_one=True)

    def get_order_items(self, order_id: int) -> List[Dict[str, Any]]:
        """Get all items for an order"""
        query = """
            SELECT order_item_id, product_id, quantity, unit_price, subtotal 
            FROM order_items 
            WHERE order_id = %s
        """
        return self.execute_query(query, (order_id,))

    def create_order(self, customer_id: int, total_price: float, status: str = 'pending') -> Tuple[int, int]:
        """Create a new order"""
        query = """
            INSERT INTO orders (customer_id, total_price, status)
            VALUES (%s, %s, %s)
        """
        return self.execute_update(query, (customer_id, total_price, status))

    def add_order_item(self, order_id: int, product_id: int, quantity: int,
                      unit_price: float, subtotal: float) -> Tuple[int, int]:
        """Add an order item"""
        query = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_update(query, (order_id, product_id, quantity, unit_price, subtotal))

    def update_order_status(self, order_id: int, status: str) -> int:
        """Update order status"""
        query = "UPDATE orders SET status = %s WHERE order_id = %s"
        affected_rows, _ = self.execute_update(query, (status, order_id))
        return affected_rows

    def update_order_total(self, order_id: int, new_total: float) -> int:
        """Update order total"""
        query = "UPDATE orders SET total_price = %s WHERE order_id = %s"
        affected_rows, _ = self.execute_update(query, (new_total, order_id))
        return affected_rows

    def remove_order_item(self, order_id: int, product_id: int) -> int:
        """Remove an order item"""
        query = "DELETE FROM order_items WHERE order_id = %s AND product_id = %s"
        affected_rows, _ = self.execute_update(query, (order_id, product_id))
        return affected_rows

    def get_order_status(self, order_id: int) -> Optional[str]:
        """Get order status"""
        query = "SELECT status FROM orders WHERE order_id = %s"
        result = self.execute_query(query, (order_id,), fetch_one=True)
        return result['status'] if result else None