"""
Product Tab Controller
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List, Dict, Any
from controllers.tab_controller import TabController
from ui.base_components import BaseFrame, InputFrame, PaginatedDataTable, DialogHelper
from services.api_client import APIClient
from services.async_api_client import AsyncAPIClient


class ProductTabController(TabController):
    """Product Tab"""
    
    def __init__(self, notebook: ttk.Notebook, vendors: Optional[List[Dict[str, Any]]] = None):
        self.vendors = vendors if vendors is not None else []
        self.products = []
        super().__init__(notebook, "Products")

    def setup_ui(self):
        """Set up the UI"""
        # Action frame
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(action_frame, text="New Product", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Search", command=self.show_search_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_products).pack(side=tk.LEFT, padx=5)
        
        # Product table (paginated)
        self.product_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "Vendor", "Name", "Price", "Stock", "Tags"],
            page_size=10,
            title="Product List"
        )
        self.product_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_products(self):
        """Refresh the product list"""
        try:
            self.product_table.clear_all()
            self.products = APIClient.get_products()
            vendors_map = {v['vendor_id']: v['business_name'] for v in self.vendors}
            
            for product in self.products:
                vendor_name = vendors_map.get(product['vendor_id'], 'Unknown')
                tags = ", ".join([t for t in [product.get('tag1'), product.get('tag2'), product.get('tag3')] if t])
                
                self.product_table.add_row([
                    product['product_id'],
                    vendor_name,
                    product['product_name'],
                    f"${product['listed_price']:.2f}",
                    product['stock_quantity'],
                    tags
                ])
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to load products: {str(e)}")

    def show_create_dialog(self):
        """Show create product dialog"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("New Product")
        dialog.geometry("500x350")
        
        # Input fields - Vendor format is standardized as: {name} (ID:{id})
        vendor_options = [f"{v['business_name']} (ID:{v['vendor_id']})" for v in self.vendors]
        
        fields_frame = InputFrame(dialog, [
            {'label': 'Vendor', 'key': 'vendor', 'type': 'select', 'values': vendor_options},
            {'label': 'Product Name', 'key': 'name', 'type': 'text'},
            {'label': 'Price', 'key': 'price', 'type': 'text'},
            {'label': 'Stock', 'key': 'stock', 'type': 'text'},
            {'label': 'Tag 1', 'key': 'tag1', 'type': 'text'},
            {'label': 'Tag 2', 'key': 'tag2', 'type': 'text'},
            {'label': 'Tag 3', 'key': 'tag3', 'type': 'text'},
        ], layout="vertical", padding=10)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create():
            values = fields_frame.get_values()
            try:
                vendor_str = values['vendor']
                # Improvement: use a consistent parsing algorithm
                vendor_id_str = vendor_str.split("(ID:")[-1].rstrip(")")
                if not vendor_id_str.isdigit():
                    raise ValueError(f"Vendor ID is not a number: {vendor_id_str}")
                vendor_id = int(vendor_id_str)
                
                APIClient.create_product(
                    vendor_id, values['name'], float(values['price']),
                    int(values['stock']), values['tag1'], values['tag2'], values['tag3']
                )
                DialogHelper.show_success("Success", "Product created successfully")
                dialog.destroy()
                self.refresh_products()
            except ValueError as e:
                DialogHelper.show_error("Error", f"Invalid input format: {str(e)}")
            except Exception as e:
                DialogHelper.show_error("Error", str(e))
        
        ttk.Button(button_frame, text="Create", command=create).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def show_search_dialog(self):
        """Show search dialog"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("Search Products")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="Search Tag:").pack(padx=10, pady=5)
        search_entry = ttk.Entry(dialog, width=30)
        search_entry.pack(padx=10, pady=5)
        
        def search():
            tag = search_entry.get().strip()
            if not tag:
                DialogHelper.show_error("Error", "Please enter a search tag")
                return
            
            # Clear the table and show loading status
            self.product_table.clear_all()
            ttk.Button(dialog, text="Searching...", state=tk.DISABLED).pack()
            
            def on_search_success(results):
                self.product_table.clear_all()
                vendors_map = {v['vendor_id']: v['business_name'] for v in self.vendors}
                
                if not results:
                    DialogHelper.show_error("Info", f"No products found with tag '{tag}'")
                    return
                
                for product in results:
                    vendor_name = vendors_map.get(product['vendor_id'], 'Unknown')
                    tags = ", ".join([t for t in [product.get('tag1'), product.get('tag2'), product.get('tag3')] if t])
                    
                    self.product_table.add_row([
                        product['product_id'],
                        vendor_name,
                        product['product_name'],
                        f"${product['listed_price']:.2f}",
                        product['stock_quantity'],
                        tags
                    ])
                
                DialogHelper.show_success("Success", f"Found {len(results)} matching products")
                dialog.destroy()
            
            def on_search_error(error):
                DialogHelper.show_error("Error", f"Search failed: {str(error)}")
            
            # Search asynchronously to avoid blocking the UI
            AsyncAPIClient.search_products_async(tag, on_search_success, on_search_error)
        
        ttk.Button(dialog, text="Search", command=search).pack(pady=5)