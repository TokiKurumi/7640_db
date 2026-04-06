"""
API 服务客户端
"""

import requests
from config.app_config import API_BASE_URL, API_TIMEOUT
from typing import Optional, Dict, Any, List


class APIClient:
    """API 客户端 - 所有 HTTP 请求"""

    @staticmethod
    def request(method: str, endpoint: str, data: Optional[dict] = None, 
                params: Optional[dict] = None) -> Any:
        """
        发起 API 请求
        :param method: HTTP 方法 (GET, POST, PUT, DELETE)
        :param endpoint: API 端点路径
        :param data: 请求数据 (JSON)
        :param params: 查询参数
        :return: 响应数据
        :raises: Exception 当请求失败
        """
        try:
            url = f"{API_BASE_URL}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, params=params, timeout=API_TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=API_TIMEOUT)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=API_TIMEOUT)
            elif method == "DELETE":
                response = requests.delete(url, timeout=API_TIMEOUT)
            else:
                raise ValueError(f"不支持的方法: {method}")
            
            response.raise_for_status()
            return response.json() if response.text else {}
        
        except requests.exceptions.Timeout:
            raise Exception(f"请求超时 (>{API_TIMEOUT}秒)")
        except requests.exceptions.ConnectionError:
            raise Exception("连接失败 - 请确保后端服务运行在 localhost:8000")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP 错误 {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求错误: {str(e)}")

    # ========================================================================
    # Vendor API
    # ========================================================================

    @staticmethod
    def get_vendors() -> List[Dict[str, Any]]:
        """获取所有供应商"""
        return APIClient.request("GET", "/vendors")

    @staticmethod
    def create_vendor(business_name: str, location: Optional[str] = None) -> Dict[str, Any]:
        """创建供应商"""
        data = {"business_name": business_name, "geographical_presence": location}
        return APIClient.request("POST", "/vendors", data=data)

    # ========================================================================
    # Product API
    # ========================================================================

    @staticmethod
    def get_products(vendor_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取产品"""
        params = {"vendor_id": vendor_id} if vendor_id else None
        return APIClient.request("GET", "/products", params=params)

    @staticmethod
    def create_product(vendor_id: int, product_name: str, price: float,
                      stock: int, tag1: str = None, tag2: str = None,
                      tag3: str = None) -> Dict[str, Any]:
        """创建产品"""
        data = {
            "product_name": product_name,
            "listed_price": price,
            "stock_quantity": stock,
            "tag1": tag1,
            "tag2": tag2,
            "tag3": tag3
        }
        return APIClient.request("POST", f"/products?vendor_id={vendor_id}", data=data)

    @staticmethod
    def search_products(tag: str) -> List[Dict[str, Any]]:
        """搜索产品"""
        return APIClient.request("GET", "/products/search", params={"tag": tag})

    # ========================================================================
    # Customer API
    # ========================================================================

    @staticmethod
    def get_customers() -> List[Dict[str, Any]]:
        """获取所有客户"""
        return APIClient.request("GET", "/customers")

    @staticmethod
    def create_customer(name: str, phone: str, address: str) -> Dict[str, Any]:
        """创建客户"""
        data = {
            "customer_name": name,
            "contact_number": phone,
            "shipping_address": address
        }
        return APIClient.request("POST", "/customers", data=data)

    # ========================================================================
    # Order API
    # ========================================================================

    @staticmethod
    def get_orders(customer_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取订单"""
        params = {"customer_id": customer_id} if customer_id else None
        return APIClient.request("GET", "/orders", params=params)

    @staticmethod
    def get_order_details(order_id: int) -> Dict[str, Any]:
        """获取订单详情"""
        return APIClient.request("GET", f"/orders/{order_id}")

    @staticmethod
    def create_order(customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单"""
        data = {"customer_id": customer_id, "items": items}
        return APIClient.request("POST", "/orders", data=data)

    @staticmethod
    def cancel_order(order_id: int) -> Dict[str, str]:
        """取消订单"""
        return APIClient.request("DELETE", f"/orders/{order_id}")

    @staticmethod
    def remove_order_item(order_id: int, product_id: int) -> Dict[str, str]:
        """删除订单项"""
        return APIClient.request("DELETE", f"/orders/{order_id}/items/{product_id}")

    # ========================================================================
    # Transaction API
    # ========================================================================

    @staticmethod
    def get_transactions(vendor_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取交易"""
        params = {"vendor_id": vendor_id} if vendor_id else None
        return APIClient.request("GET", "/transactions", params=params)
