"""
Database Access Layer - DAO (Data Access Object)
Provides direct interaction with the database
"""

import pymysql
from pymysql.cursors import DictCursor
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DatabaseConfig:
    def __init__(self, host='localhost', port=3306, user='root', password='',
                 database='ecommerce_platform', charset='utf8mb4'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def to_dict(self):
        return {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': self.charset,
            'cursorclass': DictCursor
        }


class BaseDAO:

    def __init__(self, config: DatabaseConfig):
        self.config = config

    def get_connection(self):
        try:
            return pymysql.connect(**self.config.to_dict())
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False) -> Any:
        """Execute a query statement"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise

    def execute_update(self, query: str, params: tuple = ()) -> Tuple[int, int]:
        """return affected rows: to dynamic update the table"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            # rowcount
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            conn.close()
            return affected_rows, last_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Update execution failed: {str(e)}")
            raise

    def execute_transaction(self, operations: List[Tuple[str, tuple]]) -> bool:
        # Transaction need to rollback
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            for query, params in operations:
                cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction execution failed: {str(e)}")
            raise