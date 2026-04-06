"""
数据库访问层 - DAO (Data Access Object)
提供与数据库的直接交互
"""

import pymysql
from pymysql.cursors import DictCursor
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """数据库配置"""
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
    """基础DAO类 - 提供通用的数据库操作"""

    def __init__(self, config: DatabaseConfig):
        self.config = config

    def get_connection(self):
        """获取数据库连接"""
        try:
            return pymysql.connect(**self.config.to_dict())
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False) -> Any:
        """执行查询语句"""
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
            logger.error(f"查询执行失败: {str(e)}")
            raise

    def execute_update(self, query: str, params: tuple = ()) -> Tuple[int, int]:
        """执行更新/插入/删除语句"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            conn.close()
            return affected_rows, last_id
        except Exception as e:
            conn.rollback()
            logger.error(f"更新执行失败: {str(e)}")
            raise

    def execute_transaction(self, operations: List[Tuple[str, tuple]]) -> bool:
        """执行事务操作"""
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
            logger.error(f"事务执行失败: {str(e)}")
            raise
