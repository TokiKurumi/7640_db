"""
异步 API 客户端 - 避免 GUI 阻塞
"""

import threading
from typing import Callable, Any, Optional, Dict, Tuple
from services.api_client import APIClient
from ui.base_components import DialogHelper


class AsyncAPIClient:
    """异步包装的 API 客户端"""
    
    @staticmethod
    def call_async(func: Callable, args: Tuple = (), kwargs: Optional[Dict[str, Any]] = None, 
                   on_success: Optional[Callable] = None, 
                   on_error: Optional[Callable] = None):
        """
        异步执行 API 调用
        
        :param func: 要执行的函数（来自 APIClient）
        :param args: 位置参数
        :param kwargs: 关键字参数
        :param on_success: 成功回调 - 接收返回值作为参数
        :param on_error: 失败回调 - 接收异常作为参数
        """
        if kwargs is None:
            kwargs = {}
        
        def worker():
            try:
                result = func(*args, **kwargs)
                if on_success:
                    on_success(result)
            except Exception as e:
                if on_error:
                    on_error(e)
                else:
                    print(f"API 调用失败: {str(e)}")
        
        # 在后台线程中执行
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    # 常用 API 包装
    @staticmethod
    def get_vendors_async(on_success, on_error=None):
        """异步获取供应商"""
        AsyncAPIClient.call_async(APIClient.get_vendors, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_products_async(on_success, on_error=None):
        """异步获取产品"""
        AsyncAPIClient.call_async(APIClient.get_products, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_customers_async(on_success, on_error=None):
        """异步获取客户"""
        AsyncAPIClient.call_async(APIClient.get_customers, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_orders_async(on_success, on_error=None):
        """异步获取订单"""
        AsyncAPIClient.call_async(APIClient.get_orders, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_transactions_async(on_success, on_error=None):
        """异步获取交易"""
        AsyncAPIClient.call_async(APIClient.get_transactions, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def search_products_async(tag, on_success, on_error=None):
        """异步搜索产品"""
        AsyncAPIClient.call_async(APIClient.search_products, args=(tag,), on_success=on_success, on_error=on_error)
    
    @staticmethod
    def create_order_async(customer_id, items, on_success, on_error=None):
        """异步创建订单"""
        AsyncAPIClient.call_async(APIClient.create_order, args=(customer_id, items), 
                                 on_success=on_success, on_error=on_error)
    
    @staticmethod
    def create_product_async(vendor_id, product_name, price, stock, tag1, tag2, tag3, 
                            on_success, on_error=None):
        """异步创建产品"""
        AsyncAPIClient.call_async(
            APIClient.create_product, 
            args=(vendor_id, product_name, price, stock, tag1, tag2, tag3),
            on_success=on_success, 
            on_error=on_error
        )
