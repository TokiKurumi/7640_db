"""
Customer, Order, and Transaction Tab Controllers
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List, Dict, Any
from controllers.tab_controller import TabController
from ui.base_components import BaseFrame, InputFrame, PaginatedDataTable, DataTable, DialogHelper
from services.api_client import APIClient
from services.async_api_client import AsyncAPIClient


class CustomerTabController(TabController):
    """Customer Tab"""
    
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook, "Customers")
    
    def setup_ui(self):
        """Set up the UI"""
        # Action buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="New Customer", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_customers).pack(side=tk.LEFT, padx=5)
        
        # Customer table (paginated)
        self.customer_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "Name", "Phone", "Address"],
            page_size=10,
            title="Customer List"
        )
        self.customer_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_customers(self):
        """Refresh customer list"""
        try:
            self.customer_table.clear_all()
            customers = APIClient.get_customers()
            
            for customer in customers:
                self.customer_table.add_row([
                    customer['customer_id'],
                    customer['customer_name'],
                    customer['contact_number'],
                    customer['shipping_address']
                ])
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to load customers: {str(e)}")

    def show_create_dialog(self):
        """Show create customer dialog"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("New Customer")
        dialog.geometry("400x200")
        
        fields_frame = InputFrame(dialog, [
            {'label': 'Customer Name', 'key': 'name', 'type': 'text'},
            {'label': 'Phone Number', 'key': 'phone', 'type': 'text'},
            {'label': 'Shipping Address', 'key': 'address', 'type': 'textarea'},
        ], padding=10)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create():
            values = fields_frame.get_values()
            try:
                APIClient.create_customer(values['name'], values['phone'], values['address'])
                DialogHelper.show_success("Success", "Customer created successfully")
                dialog.destroy()
                self.refresh_customers()
            except Exception as e:
                DialogHelper.show_error("Error", str(e))
        
        ttk.Button(button_frame, text="Create", command=create).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)


class OrderTabController(TabController):
    """Order Tab"""
    
    def __init__(self, notebook: ttk.Notebook, customers: Optional[List[Dict[str, Any]]] = None, products: Optional[List[Dict[str, Any]]] = None):
        self.customers = customers if customers is not None else []
        self.products = products if products is not None else []
        self.order_items = []
        super().__init__(notebook, "Orders")

    def setup_ui(self):
        """Set up the UI"""
        # Action buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="New Order", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel Order", command=self.cancel_selected_order).pack(side=tk.LEFT, padx=5)
        
        # Order table (paginated)
        self.order_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "Customer", "Date", "Total", "Status"],
            page_size=10,
            title="Order List"
        )
        self.order_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bind table selection event to show details
        self.order_table.tree.bind("<Double-1>", lambda e: self.show_order_details())

    def refresh_orders(self):
        """Refresh order list"""
        try:
            self.order_table.clear_all()
            orders = APIClient.get_orders()
            customers_map = {c['customer_id']: c['customer_name'] for c in self.customers}
            
            for order in orders:
                customer_name = customers_map.get(order['customer_id'], 'Unknown')
                self.order_table.add_row([
                    order['order_id'],
                    customer_name,
                    str(order['order_date'])[:10],
                    f"¥{order['total_price']:.2f}",
                    order['status']
                ])
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to load orders: {str(e)}")

    def show_create_dialog(self):
        """Show create order dialog"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("New Order")
        dialog.geometry("800x600")
        
        # Explanatory text
        ttk.Label(dialog, text="Please add items line by line. You can select different customers for each line (but all items in the same order must belong to the same customer)", 
                 wraplength=700).pack(padx=10, pady=5)
        
        # Input fields - Product selection
        product_options = [f"{p['product_name']} (ID:{p['product_id']})" for p in self.products]
        
        fields_frame = InputFrame(dialog, [
            {'label': 'Product', 'key': 'product', 'type': 'select', 'values': product_options},
            {'label': 'Quantity', 'key': 'quantity', 'type': 'text'},
        ], padding=10)
        fields_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Button frame
        action_frame = ttk.Frame(dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Order items list
        self.order_items = []
        items_table = DataTable(
            dialog,
            columns=["Product Name", "Product ID", "Quantity"],
            title="Order Items"
        )
        # Important: must be packed to be visible
        items_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bottom: Customer selection (unified for the entire order)
        bottom_frame = ttk.Frame(dialog)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(bottom_frame, text="Select Customer:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        customer_options = [f"{c['customer_name']} (ID:{c['customer_id']})" for c in self.customers]
        customer_combo = ttk.Combobox(bottom_frame, values=customer_options, width=50, state='readonly', font=("Arial", 11))
        customer_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(action_frame, text="Add Item", command=lambda: self._add_order_item(fields_frame, items_table)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Create Order", command=lambda: self._create_order_with_customer(fields_frame, items_table, dialog, customer_combo)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _add_order_item(self, fields_frame, items_table):
        """Add order item"""
        values = fields_frame.get_values()
        try:
            # Check if a product is selected
            product_str = values['product'].strip()
            if not product_str:
                raise ValueError("Product not selected, please select a product from the dropdown menu")
            
            # Format: "Product Name (ID:123)" -> extract 123
            product_id_str = product_str.split("(ID:")[-1].rstrip(")")
            if not product_id_str.isdigit():
                raise ValueError(f"Product ID is not a number: {product_id_str}")
            product_id = int(product_id_str)
            
            # Check quantity
            quantity_str = values['quantity'].strip()
            if not quantity_str:
                raise ValueError("Quantity not entered")
            quantity = int(quantity_str)
            
            if quantity <= 0:
                DialogHelper.show_error("Error", "Quantity must be greater than 0")
                return
            
            # Get product information
            product_name = next((p['product_name'] for p in self.products if p['product_id'] == product_id), "Unknown")
            
            # Add to order item list
            self.order_items.append({
                'product_id': product_id,
                'quantity': quantity
            })
            
            # Display in table
            items_table.add_row([
                product_name,
                product_id,
                quantity
            ])
            
            DialogHelper.show_success("Success", f"Added {product_name} x{quantity}")
            fields_frame.clear_values()
        except ValueError as e:
            DialogHelper.show_error("Error", f"Input format error: {str(e)}")
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to add: {str(e)}")

    def _create_order_with_customer(self, fields_frame, items_table, dialog, customer_combo):
        """Create order (from customer selection at the bottom of the dialog)"""
        # Check if there are order items
        if not self.order_items or len(self.order_items) == 0:
            DialogHelper.show_error("Error", "Please add at least one item to the order first")
            return
        
        try:
            customer_str = customer_combo.get().strip()
            
            # Check if a customer is selected
            if not customer_str:
                raise ValueError("Customer not selected, please select a customer from the dropdown menu")
            
            # Improvement: Safer string parsing with detailed error messages
            if '(ID:' not in customer_str:
                raise ValueError(f"Customer format error, should be '{{name}} (ID:{{id}})', but got: {customer_str}")
            
            customer_id_str = customer_str.split("(ID:")[-1].rstrip(")")
            if not customer_id_str.isdigit():
                raise ValueError(f"Customer ID is not a number: {customer_id_str}")
            
            customer_id = int(customer_id_str)
            
            # Clear temporary variables before creating the order
            items_to_create = self.order_items.copy()
            
            def on_success(result):
                DialogHelper.show_success("Success", f"Order created successfully! Added {len(items_to_create)} items")
                # Clear order items and close the dialog
                self.order_items = []
                dialog.destroy()
                self.refresh_orders()
            
            def on_error(error):
                DialogHelper.show_error("Error", f"Failed to create order: {str(error)}")
            
            # Create order asynchronously to avoid blocking the UI
            AsyncAPIClient.create_order_async(customer_id, items_to_create, on_success, on_error)
        except ValueError as e:
            DialogHelper.show_error("Error", f"Input format error: {str(e)}")
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to create order: {str(e)}")
    
    def _create_order(self, fields_frame, dialog):
        """Create order (async) - old method retained for backward compatibility"""
        # Check if there are order items
        if not self.order_items or len(self.order_items) == 0:
            DialogHelper.show_error("Error", "Please add at least one item to the order first")
            return
        
        values = fields_frame.get_values()
        try:
            customer_str = values['customer'].strip()
            
            # Check if a customer is selected
            if not customer_str:
                raise ValueError("Customer not selected, please select a customer from the dropdown menu")
            
            # Improvement: Safer string parsing with detailed error messages
            if '(ID:' not in customer_str:
                raise ValueError(f"Customer format error, should be '{{name}} (ID:{{id}})', but got: {customer_str}")
            
            customer_id_str = customer_str.split("(ID:")[-1].rstrip(")")
            if not customer_id_str.isdigit():
                raise ValueError(f"Customer ID is not a number: {customer_id_str}")
            
            customer_id = int(customer_id_str)
            
            # Clear temporary variables before creating the order
            items_to_create = self.order_items.copy()
            
            def on_success(result):
                DialogHelper.show_success("Success", f"Order created successfully! Added {len(items_to_create)} items")
                # Clear order items and close the dialog
                self.order_items = []
                dialog.destroy()
                self.refresh_orders()
            
            def on_error(error):
                DialogHelper.show_error("Error", f"Failed to create order: {str(error)}")
            
            # Create order asynchronously to avoid blocking the UI
            AsyncAPIClient.create_order_async(customer_id, items_to_create, on_success, on_error)
        except ValueError as e:
            DialogHelper.show_error("Error", f"Input format error: {str(e)}")
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to create order: {str(e)}")

    def show_order_details(self):
        """Show order details"""
        row = self.order_table.get_selected()
        if not row:
            return
        
        order_id = row[0]
        try:
            order = APIClient.get_order_details(order_id)
            
            # Create details window
            details_dialog = tk.Toplevel(self.frame)
            details_dialog.title(f"Order {order_id} Details")
            details_dialog.geometry("600x400")
            
            # Order information
            info_text = f"""
Order ID: {order['order_id']}
Customer ID: {order['customer_id']}
Total: ¥{order['total_price']:.2f}
Status: {order['status']}
Date: {order['order_date']}
            """
            
            ttk.Label(details_dialog, text=info_text, justify=tk.LEFT).pack(padx=10, pady=10)
            
            # Order Items
            items_table = DataTable(
                details_dialog,
                columns=["Product Name", "Product ID", "Quantity", "Unit Price", "Subtotal"],
                title="Order Items"
            )
            # Important: must be packed to be visible
            items_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Build a map from product ID to name
            products_map = {p['product_id']: p['product_name'] for p in self.products}
            
            for item in order['items']:
                product_name = products_map.get(item['product_id'], "Unknown Product")
                items_table.add_row([
                    product_name,
                    item['product_id'],
                    item['quantity'],
                    f"¥{item['unit_price']:.2f}",
                    f"¥{item['subtotal']:.2f}"
                ])
            
            # Action buttons
            if order['status'] == 'pending':
                button_frame = ttk.Frame(details_dialog)
                button_frame.pack(fill=tk.X, padx=10, pady=10)
                
                def remove_item():
                    selected = items_table.get_selected()
                    if selected:
                        product_id = selected[0]
                        try:
                            APIClient.remove_order_item(order_id, product_id)
                            DialogHelper.show_success("Success", "Item removed")
                            details_dialog.destroy()
                            self.refresh_orders()
                        except Exception as e:
                            DialogHelper.show_error("Error", str(e))
                
                ttk.Button(button_frame, text="Remove Selected Item", command=remove_item).pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to load order details: {str(e)}")

    def cancel_selected_order(self):
        """Cancel selected order"""
        row = self.order_table.get_selected()
        if not row:
            DialogHelper.show_error("Info", "Please select an order")
            return
        
        order_id = row[0]
        if DialogHelper.confirm("Confirm", f"Are you sure you want to cancel order {order_id}?"):
            try:
                APIClient.cancel_order(order_id)
                DialogHelper.show_success("Success", "Order has been cancelled")
                
                # Asynchronous refresh (to avoid data not being updated due to network latency)
                def on_success(result):
                    # Reload order list
                    self.refresh_orders()
                
                def on_error(error):
                    DialogHelper.show_error("Error", f"Failed to refresh order list: {str(error)}")
                    # Force refresh
                    self.refresh_orders()
                
                # Use async to get the latest order list
                AsyncAPIClient.get_orders_async(on_success, on_error)
            except Exception as e:
                DialogHelper.show_error("Error", str(e))


class TransactionTabController(TabController):
    """Transaction Tab"""
    
    def __init__(self, notebook: ttk.Notebook, vendors: Optional[List[Dict[str, Any]]] = None):
        self.vendors = vendors if vendors is not None else []
        super().__init__(notebook, "Transactions")

    def setup_ui(self):
        """Set up the UI"""
        # Action buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_transactions).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Filter by Vendor", command=self.show_filter_dialog).pack(side=tk.LEFT, padx=5)
        
        # Transaction table (paginated)
        self.transaction_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "Order ID", "Vendor", "Customer", "Product", "Quantity", "Amount", "Date"],
            page_size=10,
            title="Transaction History"
        )
        self.transaction_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_transactions(self):
        """Refresh transaction list"""
        try:
            self.transaction_table.clear_all()
            transactions = APIClient.get_transactions()
            
            for tx in transactions:
                self.transaction_table.add_row([
                    tx['transaction_id'],
                    tx['order_id'],
                    tx['vendor_id'],
                    tx['customer_id'],
                    tx['product_id'],
                    tx['quantity'],
                    f"¥{tx['transaction_amount']:.2f}",
                    str(tx['transaction_date'])[:10]
                ])
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to load transactions: {str(e)}")

    def show_filter_dialog(self):
        """Show filter dialog"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("Filter Transactions")
        dialog.geometry("300x100")
        
        # Unified format: {name} (ID:{id})
        vendor_options = [f"{v['business_name']} (ID:{v['vendor_id']})" for v in self.vendors]
        
        ttk.Label(dialog, text="Select Vendor:").pack(padx=10, pady=5)
        vendor_combo = ttk.Combobox(dialog, values=vendor_options, width=28)
        vendor_combo.pack(padx=10, pady=5)
        
        def filter_by_vendor():
            vendor_str = vendor_combo.get()
            if not vendor_str:
                DialogHelper.show_error("Error", "Please select a vendor")
                return
            
            try:
                # Unified parsing algorithm
                vendor_id_str = vendor_str.split("(ID:")[-1].rstrip(")")
                if not vendor_id_str.isdigit():
                    raise ValueError(f"Vendor ID is not a number: {vendor_id_str}")
                vendor_id = int(vendor_id_str)
                
                self.transaction_table.clear_all()
                transactions = APIClient.get_transactions(vendor_id)
                
                for tx in transactions:
                    self.transaction_table.add_row([
                        tx['transaction_id'],
                        tx['order_id'],
                        tx['vendor_id'],
                        tx['customer_id'],
                        tx['product_id'],
                        tx['quantity'],
                        f"¥{tx['transaction_amount']:.2f}",
                        str(tx['transaction_date'])[:10]
                    ])
                
                dialog.destroy()
            except ValueError as e:
                DialogHelper.show_error("Error", f"Filter failed: {str(e)}")
            except Exception as e:
                DialogHelper.show_error("Error", f"Filter failed: {str(e)}")
        
        ttk.Button(dialog, text="Filter", command=filter_by_vendor).pack(pady=5)