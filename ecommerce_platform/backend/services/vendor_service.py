"""
供应商服务层 (VendorService)
"""

from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class VendorService:
    """供应商业务逻辑类"""

    def __init__(self, config: DatabaseConfig):
        self.vendor_dao = VendorDAO(config)

    def get_all_vendors(self) -> List[Dict[str, Any]]:
        """
        获取所有供应商
        :return: 供应商列表
        """
        try:
            return self.vendor_dao.get_all_vendors()
        except Exception as e:
            raise Exception(f"获取供应商列表失败: {str(e)}")

    def get_vendor_by_id(self, vendor_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取供应商
        :param vendor_id: 供应商ID
        :return: 供应商信息或None
        """
        if not vendor_id or vendor_id <= 0:
            raise ValueError("供应商ID无效")

        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"供应商ID {vendor_id} 不存在")
        return vendor

    def create_vendor(self, business_name: str, geographical_presence: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新供应商
        :param business_name: 业务名称 (唯一)
        :param geographical_presence: 地理位置
        :return: 新创建的供应商信息
        """
        # 验证输入
        if not business_name or len(business_name.strip()) == 0:
            raise ValueError("业务名称不能为空")

        business_name = business_name.strip()

        # 检查业务名称是否已存在
        if self.vendor_dao.vendor_exists(business_name):
            raise ValueError(f"业务名称 '{business_name}' 已存在")

        try:
            affected_rows, vendor_id = self.vendor_dao.create_vendor(business_name, geographical_presence)

            if affected_rows > 0:
                # 返回新创建的供应商
                return self.get_vendor_by_id(vendor_id)
            else:
                raise Exception("创建供应商失败")
        except Exception as e:
            raise Exception(f"创建供应商失败: {str(e)}")
