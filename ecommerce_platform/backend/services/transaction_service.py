"""
交易服务层 (TransactionService)
"""

from dao.transaction_dao import TransactionDAO
from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any


class TransactionService:
    """交易业务逻辑类"""

    def __init__(self, config: DatabaseConfig):
        self.transaction_dao = TransactionDAO(config)
        self.vendor_dao = VendorDAO(config)

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """获取所有交易"""
        try:
            return self.transaction_dao.get_all_transactions()
        except Exception as e:
            raise Exception(f"获取交易列表失败: {str(e)}")

    def get_transactions_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:
        """
        根据供应商ID获取交易
        :param vendor_id: 供应商ID
        :return: 交易列表
        """
        # 验证供应商
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"供应商ID {vendor_id} 不存在")

        try:
            return self.transaction_dao.get_transactions_by_vendor(vendor_id)
        except Exception as e:
            raise Exception(f"获取交易列表失败: {str(e)}")

    def get_transactions_by_order(self, order_id: int) -> List[Dict[str, Any]]:
        """根据订单ID获取交易"""
        try:
            transactions = self.transaction_dao.get_transactions_by_order(order_id)
            if not transactions:
                raise ValueError(f"订单ID {order_id} 没有对应的交易")
            return transactions
        except Exception as e:
            raise Exception(f"获取交易失败: {str(e)}")

    def get_vendor_revenue(self, vendor_id: int) -> float:
        """获取供应商总收入"""
        # 验证供应商
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"供应商ID {vendor_id} 不存在")

        try:
            transactions = self.get_transactions_by_vendor(vendor_id)
            total_revenue = sum(tx['transaction_amount'] for tx in transactions if tx['status'] == 'completed')
            return total_revenue
        except Exception as e:
            raise Exception(f"计算收入失败: {str(e)}")
