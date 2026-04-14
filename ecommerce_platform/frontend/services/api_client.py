"""
API Service Client
"""

import requests
from config.app_config import API_BASE_URL, API_TIMEOUT
from typing import Optional, Dict, Any, List


class APIClient:
    """API Client - All HTTP Requests"""

    @staticmethod
    def request(method: str, endpoint: str, data: Optional[dict] = None, 
                params: Optional[dict] = None) -> Any:
        """
        Make an API request
        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param endpoint: API endpoint path
        :param data: Request data (JSON)
        :param params: Query parameters
        :return: Response data
        :raises: Exception when the request fails
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
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.text else {}
        
        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out (>{API_TIMEOUT}s)")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection failed - please ensure the backend service is running at localhost:8000")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")


    @staticmethod
    def get_vendors() -> List[Dict[str, Any]]:
        return APIClient.request("GET", "/vendors")

    @staticmethod
    def create_vendor(business_name: str, location: Optional[str] = None) -> Dict[str, Any]:
        data = {"business_name": business_name, "geographical_presence": location}
        return APIClient.request("POST", "/vendors", data=data)


    # TODO 4/19 接口测试
    @staticmethod
    def get_products(vendor_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params = {"vendor_id": vendor_id} if vendor_id else None
        return APIClient.request("GET", "/products", params=params)

    @staticmethod
    def create_product(vendor_id: int, product_name: str, price: float,
                      stock: int, tag1: str = None, tag2: str = None,
                      tag3: str = None) -> Dict[str, Any]:
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
        return APIClient.request("GET", "/products/search", params={"tag": tag})


    @staticmethod
    def get_customers() -> List[Dict[str, Any]]:
        return APIClient.request("GET", "/customers")

    @staticmethod
    def create_customer(name: str, phone: str, address: str) -> Dict[str, Any]:
        data = {
            "customer_name": name,
            "contact_number": phone,
            "shipping_address": address
        }
        return APIClient.request("POST", "/customers", data=data)


    @staticmethod
    def get_orders(customer_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params = {"customer_id": customer_id} if customer_id else None
        return APIClient.request("GET", "/orders", params=params)

    @staticmethod
    def get_order_details(order_id: int) -> Dict[str, Any]:
        return APIClient.request("GET", f"/orders/{order_id}")

    @staticmethod
    def create_order(customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"customer_id": customer_id, "items": items}
        return APIClient.request("POST", "/orders", data=data)

    @staticmethod
    def cancel_order(order_id: int) -> Dict[str, str]:
        return APIClient.request("DELETE", f"/orders/{order_id}")



    @staticmethod
    def remove_order_item(order_id: int, product_id: int) -> Dict[str, str]:
        return APIClient.request("DELETE", f"/orders/{order_id}/items/{product_id}")



    @staticmethod
    def get_transactions(vendor_id: Optional[int] = None) -> List[Dict[str, Any]]:
        params = {"vendor_id": vendor_id} if vendor_id else None
        return APIClient.request("GET", "/transactions", params=params)