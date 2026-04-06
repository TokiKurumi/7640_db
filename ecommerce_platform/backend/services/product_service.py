"""
产品服务层 (ProductService)
"""

from dao.product_dao import ProductDAO
from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class ProductService:
    """产品业务逻辑类"""

    def __init__(self, config: DatabaseConfig):
        self.product_dao = ProductDAO(config)
        self.vendor_dao = VendorDAO(config)

    def get_all_products(self) -> List[Dict[str, Any]]:
        """获取所有产品"""
        try:
            return self.product_dao.get_all_products()
        except Exception as e:
            raise Exception(f"获取产品列表失败: {str(e)}")

    def get_products_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:
        """
        根据供应商ID获取产品
        :param vendor_id: 供应商ID
        :return: 产品列表
        """
        # 验证供应商是否存在
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"供应商ID {vendor_id} 不存在")

        try:
            return self.product_dao.get_products_by_vendor(vendor_id)
        except Exception as e:
            raise Exception(f"获取产品列表失败: {str(e)}")

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取产品"""
        if not product_id or product_id <= 0:
            raise ValueError("产品ID无效")

        product = self.product_dao.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"产品ID {product_id} 不存在")
        return product

    def search_products_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        根据标签搜索产品
        :param tag: 搜索标签
        :return: 匹配的产品列表
        """
        if not tag or len(tag.strip()) == 0:
            raise ValueError("搜索标签不能为空")

        try:
            return self.product_dao.search_by_tag(tag.strip())
        except Exception as e:
            raise Exception(f"搜索产品失败: {str(e)}")

    def create_product(self, vendor_id: int, product_name: str, listed_price: float,
                      stock_quantity: int, tag1: Optional[str] = None,
                      tag2: Optional[str] = None, tag3: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新产品
        :param vendor_id: 供应商ID
        :param product_name: 产品名称
        :param listed_price: 列表价格
        :param stock_quantity: 库存数量
        :param tag1, tag2, tag3: 标签
        :return: 新创建的产品信息
        """
        # 验证供应商
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"供应商ID {vendor_id} 不存在")

        # 验证输入
        if not product_name or len(product_name.strip()) == 0:
            raise ValueError("产品名称不能为空")

        if listed_price <= 0:
            raise ValueError("产品价格必须大于0")

        if stock_quantity < 0:
            raise ValueError("库存数量不能为负数")

        try:
            affected_rows, product_id = self.product_dao.create_product(
                vendor_id, product_name.strip(), listed_price, stock_quantity, tag1, tag2, tag3
            )

            if affected_rows > 0:
                return self.get_product_by_id(product_id)
            else:
                raise Exception("创建产品失败")
        except Exception as e:
            raise Exception(f"创建产品失败: {str(e)}")

    def get_product_stock(self, product_id: int) -> int:
        """获取产品库存"""
        stock = self.product_dao.get_stock_quantity(product_id)
        if stock is None:
            raise ValueError(f"产品ID {product_id} 不存在")
        return stock

    def check_stock_availability(self, product_id: int, required_quantity: int) -> bool:
        """检查产品是否有足够库存"""
        stock = self.get_product_stock(product_id)
        return stock >= required_quantity
