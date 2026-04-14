
import threading
from typing import Callable, Any, Optional, Dict, Tuple
from services.api_client import APIClient
from ui.base_components import DialogHelper


class AsyncAPIClient:
    """Only a wrapper, because the tab always


The GUI interface relies on an infinite loop (the main event loop mainloop) to refresh the display and respond to mouse clicks. If you write time-consuming code inside a button click event , the program will become stuck on that task and won't have the opportunity to refresh the interface. As a result, Windows/macOS will label it as "Not Responding."
    """
    
    @staticmethod
    def call_async(func: Callable, args: Tuple = (), kwargs: Optional[Dict[str, Any]] = None, 
                   on_success: Optional[Callable] = None, 
                   on_error: Optional[Callable] = None):
        """
        Execute an API call asynchronously
        
        :param func: The function to execute (from APIClient)
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :param on_success: Success callback - receives the return value as an argument
        :param on_error: Failure callback - receives the exception as an argument
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
                    print(f"API call failed: {str(e)}")
        
        # Execute in a background thread
        # A new thread
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    # Common API wrappers
    @staticmethod
    def get_vendors_async(on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.get_vendors, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_products_async(on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.get_products, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_customers_async(on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.get_customers, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_orders_async(on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.get_orders, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def get_transactions_async(on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.get_transactions, on_success=on_success, on_error=on_error)
    
    @staticmethod
    def search_products_async(tag, on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.search_products, args=(tag,), on_success=on_success, on_error=on_error)
    
    @staticmethod
    def create_order_async(customer_id, items, on_success, on_error=None):
        AsyncAPIClient.call_async(APIClient.create_order, args=(customer_id, items), 
                                 on_success=on_success, on_error=on_error)
    
    @staticmethod
    def create_product_async(vendor_id, product_name, price, stock, tag1, tag2, tag3, 
                            on_success, on_error=None):
        AsyncAPIClient.call_async(
            APIClient.create_product, 
            args=(vendor_id, product_name, price, stock, tag1, tag2, tag3),
            on_success=on_success, 
            on_error=on_error
        )