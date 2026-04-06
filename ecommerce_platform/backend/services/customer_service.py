"""
客户服务层 (CustomerService)
"""

from dao.customer_dao import CustomerDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class CustomerService:
    """客户业务逻辑类"""

    def __init__(self, config: DatabaseConfig):
        self.customer_dao = CustomerDAO(config)

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """获取所有客户"""
        try:
            return self.customer_dao.get_all_customers()
        except Exception as e:
            raise Exception(f"获取客户列表失败: {str(e)}")

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取客户"""
        if not customer_id or customer_id <= 0:
            raise ValueError("客户ID无效")

        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"客户ID {customer_id} 不存在")
        return customer

    def create_customer(self, customer_name: str, contact_number: str,
                       shipping_address: str) -> Dict[str, Any]:
        """
        创建新客户
        :param customer_name: 客户名称
        :param contact_number: 联系电话 (唯一)
        :param shipping_address: 收货地址
        :return: 新创建的客户信息
        """
        # 验证输入
        if not customer_name or len(customer_name.strip()) == 0:
            raise ValueError("客户名称不能为空")

        if not contact_number or len(contact_number.strip()) == 0:
            raise ValueError("联系电话不能为空")

        if not shipping_address or len(shipping_address.strip()) == 0:
            raise ValueError("收货地址不能为空")

        # 检查电话号码是否已存在
        if self.customer_dao.customer_exists(contact_number.strip()):
            raise ValueError(f"联系电话 '{contact_number}' 已被使用")

        try:
            affected_rows, customer_id = self.customer_dao.create_customer(
                customer_name.strip(), contact_number.strip(), shipping_address.strip()
            )

            if affected_rows > 0:
                return self.get_customer_by_id(customer_id)
            else:
                raise Exception("创建客户失败")
        except Exception as e:
            raise Exception(f"创建客户失败: {str(e)}")

    def customer_exists(self, customer_id: int) -> bool:
        """检查客户是否存在"""
        customer = self.customer_dao.get_customer_by_id(customer_id)
        return customer is not None
