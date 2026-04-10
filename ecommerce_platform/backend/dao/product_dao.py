
from . import BaseDAO, DatabaseConfig
from typing import List, Dict, Any, Optional, Tuple


class ProductDAO(BaseDAO):


    def get_all_products(self) -> List[Dict[str, Any]]:

        query = """
            SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, 
                   tag1, tag2, tag3, created_date 
            FROM products 
            ORDER BY product_id
        """
        return self.execute_query(query)

    def get_products_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:

        query = """
            SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, 
                   tag1, tag2, tag3, created_date 
            FROM products 
            WHERE vendor_id = %s 
            ORDER BY product_id
        """
        return self.execute_query(query, (vendor_id,))

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:

        query = """
            SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, 
                   tag1, tag2, tag3, created_date 
            FROM products 
            WHERE product_id = %s
        """
        return self.execute_query(query, (product_id,), fetch_one=True)

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        # step by step to select tags
        search_term = f"%{tag}%"
        query = """
            SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, 
                   tag1, tag2, tag3, created_date 
            FROM products 
            WHERE product_name LIKE %s OR tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
            ORDER BY product_name
        """
        return self.execute_query(query, (search_term, search_term, search_term, search_term))

    def create_product(self, vendor_id: int, product_name: str, listed_price: float,
                      stock_quantity: int, tag1: Optional[str] = None,
                      tag2: Optional[str] = None, tag3: Optional[str] = None) -> Tuple[int, int]:
        query = """
            INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_update(query, (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3))

    def update_stock(self, product_id: int, quantity_change: int) -> int:
        query = """
            UPDATE products 
            SET stock_quantity = stock_quantity + %s 
            WHERE product_id = %s
        """
        affected_rows, _ = self.execute_update(query, (quantity_change, product_id))
        return affected_rows

    def get_stock_quantity(self, product_id: int) -> Optional[int]:
        query = "SELECT stock_quantity FROM products WHERE product_id = %s"
        result = self.execute_query(query, (product_id,), fetch_one=True)
        return result['stock_quantity'] if result else None