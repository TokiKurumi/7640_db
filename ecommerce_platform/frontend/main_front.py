"""
E-Commerce Platform - A clean frontend GUI (v2.0 Modular)

Architecture:
  - config/: Configuration files
  - services/: API clients
  - ui/: UI base components
  - controllers/: Tab controllers
  - main.py: Main application
"""

import tkinter as tk
from tkinter import ttk
from config.app_config import *
from services.api_client import APIClient
from services.async_api_client import AsyncAPIClient
from ui.base_components import StatusBar, DialogHelper
from controllers.vendor_tab import VendorTabController
from controllers.product_tab import ProductTabController
from controllers.other_tabs import CustomerTabController, OrderTabController, TransactionTabController


class EcommercePlatformApp:
    """E-commerce Platform GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.resizable(True, True)
        
        # Initialize data
        self.vendors = []
        self.products = []
        self.customers = []
        
        # Set style
        style = ttk.Style()
        style.theme_use(THEME_NAME)
        
        # Create UI
        self.setup_ui()
        
        # Load initial data
        self.load_initial_data()

    def setup_ui(self):
        """Set up the UI"""
        # Create the main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create the Notebook (tab container)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
         # Create tab controllers
        # Note: vendors, products, customers are still empty and will be loaded and updated in load_initial_data
        self.vendor_tab = VendorTabController(self.notebook, self.on_vendors_updated)
        self.product_tab = ProductTabController(self.notebook, [])
        self.customer_tab = CustomerTabController(self.notebook)
        self.order_tab = OrderTabController(self.notebook, [], [])
        self.transaction_tab = TransactionTabController(self.notebook, [])
        
        # Create the status bar
        self.status_bar = StatusBar(self.root)

    def load_initial_data(self):
        """Load initial data (asynchronously)"""
        self.update_status("Loading data...")
        
        # Counter to track completed loading tasks
        self.load_count = 0
        self.load_total = 3  # Need to load 3 types of data: vendors, products, customers
        
        def on_vendors_loaded(data):
            self.vendors = data
            self._on_data_loaded()
        
        def on_products_loaded(data):
            self.products = data
            self._on_data_loaded()
        
        def on_customers_loaded(data):
            self.customers = data
            self._on_data_loaded()
        
        def on_error(error):
            DialogHelper.show_error("Error", f"Failed to load data: {str(error)}")
            self.update_status("Error")
        
        # Load three types of data in parallel (asynchronously)
        AsyncAPIClient.get_vendors_async(on_vendors_loaded, on_error)
        AsyncAPIClient.get_products_async(on_products_loaded, on_error)
        AsyncAPIClient.get_customers_async(on_customers_loaded, on_error)
    
    def _on_data_loaded(self):
        """Data loading callback"""
        self.load_count += 1
        
        # When all data has finished loading
        if self.load_count == self.load_total:
            # Update tab references
            self.product_tab.vendors = self.vendors
            self.order_tab.customers = self.customers
            self.order_tab.products = self.products
            self.transaction_tab.vendors = self.vendors
            
            # Refresh all tabs (synchronously)
            self.vendor_tab.refresh_vendors()
            self.product_tab.refresh_products()
            self.customer_tab.refresh_customers()
            self.order_tab.refresh_orders()
            self.transaction_tab.refresh_transactions()
            
            self.update_status("Ready")

    def on_vendors_updated(self):
        """Vendor update callback (asynchronous)"""
        def on_success(data):
            self.vendors = data
            self.product_tab.vendors = self.vendors
            self.transaction_tab.vendors = self.vendors
        
        def on_error(error):
            DialogHelper.show_error("Error", f"Failed to update data: {str(error)}")
        
        AsyncAPIClient.get_vendors_async(on_success, on_error)

    def update_status(self, message: str):
        """Update the status bar"""
        self.status_bar.set_status(message)


def main():
    """Main function"""
    root = tk.Tk()
    app = EcommercePlatformApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()