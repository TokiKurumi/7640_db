"""
订单服务层 (OrderService)
"""

from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO
from dao.customer_dao import CustomerDAO
from dao.transaction_dao import TransactionDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class OrderService:
    """订单业务逻辑类"""

    def __init__(self, config: DatabaseConfig):
        self.order_dao = OrderDAO(config)
        self.product_dao = ProductDAO(config)
        self.customer_dao = CustomerDAO(config)
        self.transaction_dao = TransactionDAO(config)

    def get_all_orders(self) -> List[Dict[str, Any]]:
        """获取所有订单"""
        try:
            return self.order_dao.get_all_orders()
        except Exception as e:
            raise Exception(f"获取订单列表失败: {str(e)}")

    def get_orders_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """根据客户ID获取订单"""
        # 验证客户
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"客户ID {customer_id} 不存在")

        try:
            return self.order_dao.get_orders_by_customer(customer_id)
        except Exception as e:
            raise Exception(f"获取订单列表失败: {str(e)}")

    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """获取订单详情(包括所有项)"""
        if not order_id or order_id <= 0:
            raise ValueError("订单ID无效")

        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"订单ID {order_id} 不存在")

        # 获取订单项
        items = self.order_dao.get_order_items(order_id)
        order['items'] = items
        return order

    def create_order(self, customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        创建新订单
        :param customer_id: 客户ID
        :param items: 订单项列表 [{'product_id': id, 'quantity': qty}, ...]
        :return: 新创建的订单信息
        """
        # 验证客户
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"客户ID {customer_id} 不存在")

        # 验证items
        if not items or len(items) == 0:
            raise ValueError("订单至少需要一个商品")

        # 计算总价并验证库存
        total_price = 0
        items_data = []

        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            # 获取产品信息
            product = self.product_dao.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"产品ID {product_id} 不存在")

            # 检查库存
            if product['stock_quantity'] < quantity:
                raise ValueError(f"产品 '{product['product_name']}' 库存不足 (需要{quantity}, 现有{product['stock_quantity']})")

            subtotal = product['listed_price'] * quantity
            total_price += subtotal

            items_data.append({
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': product['listed_price'],
                'subtotal': subtotal,
                'vendor_id': product['vendor_id']
            })

        # 创建订单
        try:
            affected_rows, order_id = self.order_dao.create_order(customer_id, total_price, 'pending')

            if affected_rows > 0:
                # 添加订单项和扣减库存
                for item_data in items_data:
                    # 添加订单项
                    self.order_dao.add_order_item(
                        order_id,
                        item_data['product_id'],
                        item_data['quantity'],
                        item_data['unit_price'],
                        item_data['subtotal']
                    )

                    # 扣减库存
                    self.product_dao.update_stock(item_data['product_id'], -item_data['quantity'])

                    # 创建交易记录
                    self.transaction_dao.create_transaction(
                        order_id,
                        item_data['vendor_id'],
                        customer_id,
                        item_data['product_id'],
                        item_data['quantity'],
                        item_data['subtotal'],
                        'completed'
                    )

                return self.get_order_by_id(order_id)
            else:
                raise Exception("创建订单失败")
        except Exception as e:
            raise Exception(f"创建订单失败: {str(e)}")

    def cancel_order(self, order_id: int) -> bool:
        """
        取消订单 (只能取消未发货的订单)
        :param order_id: 订单ID
        :return: 是否成功
        """
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"订单ID {order_id} 不存在")

        # 检查订单状态
        if order['status'] in ['shipped', 'delivered']:
            raise ValueError(f"不能取消已发货的订单 (当前状态: {order['status']})")

        try:
            # 恢复库存
            items = self.order_dao.get_order_items(order_id)
            for item in items:
                self.product_dao.update_stock(item['product_id'], item['quantity'])

            # 更新订单状态
            self.order_dao.update_order_status(order_id, 'cancelled')
            return True
        except Exception as e:
            raise Exception(f"取消订单失败: {str(e)}")

    def remove_order_item(self, order_id: int, product_id: int) -> bool:
        """
        从订单中删除一个商品
        :param order_id: 订单ID
        :param product_id: 产品ID
        :return: 是否成功
        """
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"订单ID {order_id} 不存在")

        # 检查订单状态
        if order['status'] in ['shipped', 'delivered']:
            raise ValueError(f"不能修改已发货的订单 (当前状态: {order['status']})")

        try:
            # 获取订单项
            items = self.order_dao.get_order_items(order_id)
            item_to_remove = None

            for item in items:
                if item['product_id'] == product_id:
                    item_to_remove = item
                    break

            if not item_to_remove:
                raise ValueError(f"该订单中不存在产品ID {product_id}")

            # 恢复库存
            self.product_dao.update_stock(product_id, item_to_remove['quantity'])

            # 删除订单项
            self.order_dao.remove_order_item(order_id, product_id)

            # 更新订单总额
            new_total = order['total_price'] - item_to_remove['subtotal']
            self.order_dao.update_order_total(order_id, new_total)

            return True
        except Exception as e:
            raise Exception(f"删除订单项失败: {str(e)}")

    def update_order_status(self, order_id: int, status: str) -> bool:
        """更新订单状态"""
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

        if status not in valid_statuses:
            raise ValueError(f"无效的订单状态。允许的状态: {', '.join(valid_statuses)}")

        try:
            affected_rows = self.order_dao.update_order_status(order_id, status)
            return affected_rows > 0
        except Exception as e:
            raise Exception(f"更新订单状态失败: {str(e)}")
