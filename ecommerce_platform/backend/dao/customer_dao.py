"""
客户数据访问对象 (CustomerDAO)
"""

from . import BaseDAO, DatabaseConfig
from typing import List, Dict, Any, Optional, Tuple


class CustomerDAO(BaseDAO):
    """客户数据访问类"""

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """获取所有客户"""
        query = """
            SELECT customer_id, customer_name, contact_number, shipping_address, created_date 
            FROM customers 
            ORDER BY customer_id
        """
        return self.execute_query(query)

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取客户"""
        query = """
            SELECT customer_id, customer_name, contact_number, shipping_address, created_date 
            FROM customers 
            WHERE customer_id = %s
        """
        return self.execute_query(query, (customer_id,), fetch_one=True)

    def create_customer(self, customer_name: str, contact_number: str,
                       shipping_address: str) -> Tuple[int, int]:
        """创建新客户"""
        query = """
            INSERT INTO customers (customer_name, contact_number, shipping_address)
            VALUES (%s, %s, %s)
        """
        return self.execute_update(query, (customer_name, contact_number, shipping_address))

    def customer_exists(self, contact_number: str) -> bool:
        """检查客户是否存在 (根据联系电话)"""
        query = "SELECT customer_id FROM customers WHERE contact_number = %s"
        result = self.execute_query(query, (contact_number,), fetch_one=True)
        return result is not None
