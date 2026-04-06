"""
COMP7640 E-Commerce Platform - Frontend GUI
Tkinter-based GUI Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from typing import Optional, List, Dict
import json
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================
API_BASE_URL = "http://localhost:8000/api"

# ============================================================================
# API Client
# ============================================================================
class APIClient:
    """API Client for backend communication"""
    
    @staticmethod
    def request(method: str, endpoint: str, data: Optional[dict] = None, params: Optional[dict] = None):
        """Make API request"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, params=params, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")

# ============================================================================
# Main Application
# ============================================================================
class EcommercePlatformGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("COMP7640 E-Commerce Platform")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_vendor_tab()
        self.create_product_tab()
        self.create_customer_tab()
        self.create_order_tab()
        self.create_transaction_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Load initial data
        self.refresh_all()
    
    def set_status(self, message: str):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update()
    
    # ========================================================================
    # VENDOR TAB
    # ========================================================================
    def create_vendor_tab(self):
        """Create vendor management tab"""
        vendor_frame = ttk.Frame(self.notebook)
        self.notebook.add(vendor_frame, text="Vendors")
        
        # Title
        title = ttk.Label(vendor_frame, text="Vendor Management", font=("Arial", 14, "bold"))
        title.pack(padx=10, pady=10)
        
        # Create vendor section
        create_frame = ttk.LabelFrame(vendor_frame, text="Create New Vendor", padding=10)
        create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(create_frame, text="Business Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.vendor_name_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.vendor_name_var, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(create_frame, text="Geographical Presence:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.vendor_location_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.vendor_location_var, width=30).grid(row=1, column=1, padx=5)
        
        ttk.Button(create_frame, text="Create Vendor", command=self.create_vendor).grid(row=2, column=1, sticky=tk.E, pady=10)
        
        # Vendors list section
        list_frame = ttk.LabelFrame(vendor_frame, text="All Vendors", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("ID", "Business Name", "Rating", "Location")
        self.vendor_tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.vendor_tree.column("#0", width=0, stretch=tk.NO)
        self.vendor_tree.column("ID", anchor=tk.W, width=50)
        self.vendor_tree.column("Business Name", anchor=tk.W, width=250)
        self.vendor_tree.column("Rating", anchor=tk.CENTER, width=100)
        self.vendor_tree.column("Location", anchor=tk.W, width=300)
        
        self.vendor_tree.heading("#0", text="", anchor=tk.W)
        self.vendor_tree.heading("ID", text="ID", anchor=tk.W)
        self.vendor_tree.heading("Business Name", text="Business Name", anchor=tk.W)
        self.vendor_tree.heading("Rating", text="Rating", anchor=tk.CENTER)
        self.vendor_tree.heading("Location", text="Location", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.vendor_tree.yview)
        self.vendor_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vendor_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_vendor(self):
        """Create new vendor"""
        name = self.vendor_name_var.get().strip()
        location = self.vendor_location_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Business name is required")
            return
        
        try:
            self.set_status("Creating vendor...")
            data = {
                "business_name": name,
                "geographical_presence": location
            }
            APIClient.request("POST", "/vendors", data=data)
            messagebox.showinfo("Success", "Vendor created successfully")
            self.vendor_name_var.set("")
            self.vendor_location_var.set("")
            self.refresh_vendor_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.set_status("Ready")
    
    def refresh_vendor_list(self):
        """Refresh vendor list"""
        try:
            self.set_status("Loading vendors...")
            # Clear existing items
            for item in self.vendor_tree.get_children():
                self.vendor_tree.delete(item)
            
            # Fetch vendors
            vendors = APIClient.request("GET", "/vendors")
            for vendor in vendors:
                self.vendor_tree.insert("", "end", values=(
                    vendor['vendor_id'],
                    vendor['business_name'],
                    f"{vendor['average_rating']:.1f}",
                    vendor.get('geographical_presence', 'N/A')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vendors: {str(e)}")
        finally:
            self.set_status("Ready")
    
    # ========================================================================
    # PRODUCT TAB
    # ========================================================================
    def create_product_tab(self):
        """Create product management tab"""
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="Products")
        
        # Title
        title = ttk.Label(product_frame, text="Product Management", font=("Arial", 14, "bold"))
        title.pack(padx=10, pady=10)
        
        # Create product section
        create_frame = ttk.LabelFrame(product_frame, text="Create New Product", padding=10)
        create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(create_frame, text="Vendor:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.product_vendor_var = tk.StringVar()
        self.vendor_combo = ttk.Combobox(create_frame, textvariable=self.product_vendor_var, width=28)
        self.vendor_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(create_frame, text="Product Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.product_name_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.product_name_var, width=30).grid(row=1, column=1, padx=5)
        
        ttk.Label(create_frame, text="Price:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.product_price_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.product_price_var, width=30).grid(row=2, column=1, padx=5)
        
        ttk.Label(create_frame, text="Stock Quantity:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.product_stock_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.product_stock_var, width=30).grid(row=3, column=1, padx=5)
        
        ttk.Label(create_frame, text="Tag 1:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.product_tag1_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.product_tag1_var, width=30).grid(row=4, column=1, padx=5)
        
        ttk.Label(create_frame, text="Tag 2:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.product_tag2_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.product_tag2_var, width=30).grid(row=5, column=1, padx=5)
        
        ttk.Label(create_frame, text="Tag 3:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.product_tag3_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.product_tag3_var, width=30).grid(row=6, column=1, padx=5)
        
        ttk.Button(create_frame, text="Create Product", command=self.create_product).grid(row=7, column=1, sticky=tk.E, pady=10)
        
        # Search section
        search_frame = ttk.LabelFrame(product_frame, text="Search Products", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search by Tag:").pack(side=tk.LEFT, padx=5)
        self.search_tag_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_tag_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Show All", command=self.refresh_product_list).pack(side=tk.LEFT, padx=5)
        
        # Products list section
        list_frame = ttk.LabelFrame(product_frame, text="All Products", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("ID", "Vendor", "Name", "Price", "Stock", "Tags")
        self.product_tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.product_tree.column("#0", width=0, stretch=tk.NO)
        self.product_tree.column("ID", anchor=tk.W, width=50)
        self.product_tree.column("Vendor", anchor=tk.W, width=120)
        self.product_tree.column("Name", anchor=tk.W, width=200)
        self.product_tree.column("Price", anchor=tk.CENTER, width=80)
        self.product_tree.column("Stock", anchor=tk.CENTER, width=80)
        self.product_tree.column("Tags", anchor=tk.W, width=250)
        
        self.product_tree.heading("#0", text="", anchor=tk.W)
        self.product_tree.heading("ID", text="ID", anchor=tk.W)
        self.product_tree.heading("Vendor", text="Vendor", anchor=tk.W)
        self.product_tree.heading("Name", text="Product Name", anchor=tk.W)
        self.product_tree.heading("Price", text="Price", anchor=tk.CENTER)
        self.product_tree.heading("Stock", text="Stock", anchor=tk.CENTER)
        self.product_tree.heading("Tags", text="Tags", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_product(self):
        """Create new product"""
        vendor_id = self.vendor_combo.current()
        if vendor_id == -1:
            messagebox.showerror("Error", "Please select a vendor")
            return
        
        name = self.product_name_var.get().strip()
        price_str = self.product_price_var.get().strip()
        stock_str = self.product_stock_var.get().strip()
        
        if not name or not price_str or not stock_str:
            messagebox.showerror("Error", "Name, price, and stock are required")
            return
        
        try:
            price = float(price_str)
            stock = int(stock_str)
            vendor_id_value = int(self.vendor_combo.get().split("(ID:")[1].rstrip(")"))
            
            self.set_status("Creating product...")
            data = {
                "product_name": name,
                "listed_price": price,
                "stock_quantity": stock,
                "tag1": self.product_tag1_var.get().strip() or None,
                "tag2": self.product_tag2_var.get().strip() or None,
                "tag3": self.product_tag3_var.get().strip() or None
            }
            APIClient.request("POST", f"/products?vendor_id={vendor_id_value}", data=data)
            messagebox.showinfo("Success", "Product created successfully")
            
            # Clear inputs
            self.product_name_var.set("")
            self.product_price_var.set("")
            self.product_stock_var.set("")
            self.product_tag1_var.set("")
            self.product_tag2_var.set("")
            self.product_tag3_var.set("")
            
            self.refresh_product_list()
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and stock must be an integer")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.set_status("Ready")
    
    def refresh_product_list(self):
        """Refresh product list"""
        try:
            self.set_status("Loading products...")
            # Clear existing items
            for item in self.product_tree.get_children():
                self.product_tree.delete(item)
            
            # Fetch products
            products = APIClient.request("GET", "/products")
            vendors_map = {v['vendor_id']: v['business_name'] for v in APIClient.request("GET", "/vendors")}
            
            for product in products:
                tags = ", ".join([t for t in [product.get('tag1'), product.get('tag2'), product.get('tag3')] if t])
                vendor_name = vendors_map.get(product['vendor_id'], 'Unknown')
                
                self.product_tree.insert("", "end", values=(
                    product['product_id'],
                    vendor_name,
                    product['product_name'],
                    f"${product['listed_price']:.2f}",
                    product['stock_quantity'],
                    tags
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")
        finally:
            self.set_status("Ready")
    
    def search_products(self):
        """Search products by tag"""
        tag = self.search_tag_var.get().strip()
        if not tag:
            messagebox.showerror("Error", "Please enter a search tag")
            return
        
        try:
            self.set_status("Searching products...")
            # Clear existing items
            for item in self.product_tree.get_children():
                self.product_tree.delete(item)
            
            # Fetch products
            products = APIClient.request("GET", f"/products/search?tag={tag}")
            vendors_map = {v['vendor_id']: v['business_name'] for v in APIClient.request("GET", "/vendors")}
            
            for product in products:
                tags = ", ".join([t for t in [product.get('tag1'), product.get('tag2'), product.get('tag3')] if t])
                vendor_name = vendors_map.get(product['vendor_id'], 'Unknown')
                
                self.product_tree.insert("", "end", values=(
                    product['product_id'],
                    vendor_name,
                    product['product_name'],
                    f"${product['listed_price']:.2f}",
                    product['stock_quantity'],
                    tags
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
        finally:
            self.set_status("Ready")
    
    # ========================================================================
    # CUSTOMER TAB
    # ========================================================================
    def create_customer_tab(self):
        """Create customer management tab"""
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="Customers")
        
        # Title
        title = ttk.Label(customer_frame, text="Customer Management", font=("Arial", 14, "bold"))
        title.pack(padx=10, pady=10)
        
        # Create customer section
        create_frame = ttk.LabelFrame(customer_frame, text="Create New Customer", padding=10)
        create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(create_frame, text="Customer Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.customer_name_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.customer_name_var, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(create_frame, text="Contact Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.customer_phone_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.customer_phone_var, width=30).grid(row=1, column=1, padx=5)
        
        ttk.Label(create_frame, text="Shipping Address:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.customer_address_var = tk.StringVar()
        address_text = tk.Text(create_frame, width=30, height=3)
        address_text.grid(row=2, column=1, padx=5)
        self.customer_address_text = address_text
        
        ttk.Button(create_frame, text="Create Customer", command=self.create_customer).grid(row=3, column=1, sticky=tk.E, pady=10)
        
        # Customers list section
        list_frame = ttk.LabelFrame(customer_frame, text="All Customers", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("ID", "Name", "Contact", "Address")
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.customer_tree.column("#0", width=0, stretch=tk.NO)
        self.customer_tree.column("ID", anchor=tk.W, width=50)
        self.customer_tree.column("Name", anchor=tk.W, width=200)
        self.customer_tree.column("Contact", anchor=tk.W, width=150)
        self.customer_tree.column("Address", anchor=tk.W, width=400)
        
        self.customer_tree.heading("#0", text="", anchor=tk.W)
        self.customer_tree.heading("ID", text="ID", anchor=tk.W)
        self.customer_tree.heading("Name", text="Name", anchor=tk.W)
        self.customer_tree.heading("Contact", text="Contact Number", anchor=tk.W)
        self.customer_tree.heading("Address", text="Shipping Address", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.customer_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_customer(self):
        """Create new customer"""
        name = self.customer_name_var.get().strip()
        phone = self.customer_phone_var.get().strip()
        address = self.customer_address_text.get("1.0", tk.END).strip()
        
        if not name or not phone or not address:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            self.set_status("Creating customer...")
            data = {
                "customer_name": name,
                "contact_number": phone,
                "shipping_address": address
            }
            APIClient.request("POST", "/customers", data=data)
            messagebox.showinfo("Success", "Customer created successfully")
            
            self.customer_name_var.set("")
            self.customer_phone_var.set("")
            self.customer_address_text.delete("1.0", tk.END)
            
            self.refresh_customer_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.set_status("Ready")
    
    def refresh_customer_list(self):
        """Refresh customer list"""
        try:
            self.set_status("Loading customers...")
            # Clear existing items
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
            
            # Fetch customers
            customers = APIClient.request("GET", "/customers")
            for customer in customers:
                self.customer_tree.insert("", "end", values=(
                    customer['customer_id'],
                    customer['customer_name'],
                    customer['contact_number'],
                    customer['shipping_address']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {str(e)}")
        finally:
            self.set_status("Ready")
    
    # ========================================================================
    # ORDER TAB
    # ========================================================================
    def create_order_tab(self):
        """Create order management tab"""
        order_frame = ttk.Frame(self.notebook)
        self.notebook.add(order_frame, text="Orders")
        
        # Title
        title = ttk.Label(order_frame, text="Order Management", font=("Arial", 14, "bold"))
        title.pack(padx=10, pady=10)
        
        # Create order section
        create_frame = ttk.LabelFrame(order_frame, text="Create New Order", padding=10)
        create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(create_frame, text="Customer:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.order_customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(create_frame, textvariable=self.order_customer_var, width=28)
        self.customer_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(create_frame, text="Product:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.order_product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(create_frame, textvariable=self.order_product_var, width=28)
        self.product_combo.grid(row=1, column=1, padx=5)
        
        ttk.Label(create_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.order_quantity_var = tk.StringVar(value="1")
        ttk.Spinbox(create_frame, from_=1, to=1000, textvariable=self.order_quantity_var, width=28).grid(row=2, column=1, padx=5)
        
        button_frame = ttk.Frame(create_frame)
        button_frame.grid(row=3, column=1, sticky=tk.E, pady=10)
        ttk.Button(button_frame, text="Add Item", command=self.add_order_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create Order", command=self.create_order).pack(side=tk.LEFT, padx=5)
        
        # Order items section
        items_frame = ttk.LabelFrame(order_frame, text="Order Items", padding=10)
        items_frame.pack(fill=tk.X, padx=10, pady=5)
        
        columns = ("Product ID", "Product Name", "Quantity", "Unit Price", "Subtotal")
        self.order_items_tree = ttk.Treeview(items_frame, columns=columns, height=5)
        self.order_items_tree.column("#0", width=0, stretch=tk.NO)
        self.order_items_tree.column("Product ID", anchor=tk.W, width=80)
        self.order_items_tree.column("Product Name", anchor=tk.W, width=250)
        self.order_items_tree.column("Quantity", anchor=tk.CENTER, width=80)
        self.order_items_tree.column("Unit Price", anchor=tk.CENTER, width=100)
        self.order_items_tree.column("Subtotal", anchor=tk.CENTER, width=100)
        
        self.order_items_tree.heading("#0", text="", anchor=tk.W)
        self.order_items_tree.heading("Product ID", text="Product ID", anchor=tk.W)
        self.order_items_tree.heading("Product Name", text="Product Name", anchor=tk.W)
        self.order_items_tree.heading("Quantity", text="Qty", anchor=tk.CENTER)
        self.order_items_tree.heading("Unit Price", text="Unit Price", anchor=tk.CENTER)
        self.order_items_tree.heading("Subtotal", text="Subtotal", anchor=tk.CENTER)
        
        self.order_items_tree.pack(fill=tk.BOTH, expand=True)
        self.order_items = []
        
        # Orders list section
        list_frame = ttk.LabelFrame(order_frame, text="All Orders", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("ID", "Customer", "Date", "Total", "Status")
        self.order_tree = ttk.Treeview(list_frame, columns=columns, height=10)
        self.order_tree.column("#0", width=0, stretch=tk.NO)
        self.order_tree.column("ID", anchor=tk.W, width=50)
        self.order_tree.column("Customer", anchor=tk.W, width=200)
        self.order_tree.column("Date", anchor=tk.W, width=180)
        self.order_tree.column("Total", anchor=tk.CENTER, width=100)
        self.order_tree.column("Status", anchor=tk.W, width=150)
        
        self.order_tree.heading("#0", text="", anchor=tk.W)
        self.order_tree.heading("ID", text="Order ID", anchor=tk.W)
        self.order_tree.heading("Customer", text="Customer Name", anchor=tk.W)
        self.order_tree.heading("Date", text="Order Date", anchor=tk.W)
        self.order_tree.heading("Total", text="Total", anchor=tk.CENTER)
        self.order_tree.heading("Status", text="Status", anchor=tk.W)
        
        self.order_tree.bind("<Double-1>", self.show_order_details)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.order_tree.yview)
        self.order_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.order_tree.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(order_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(action_frame, text="Cancel Selected Order", command=self.cancel_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="View Details", command=self.show_selected_order_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Refresh", command=self.refresh_order_list).pack(side=tk.LEFT, padx=5)
    
    def add_order_item(self):
        """Add product to order items"""
        product_id = self.product_combo.current()
        if product_id == -1:
            messagebox.showerror("Error", "Please select a product")
            return
        
        quantity_str = self.order_quantity_var.get().strip()
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return
        
        # Parse product info
        try:
            product_data = self.product_combo.get()
            parts = product_data.split(" - ")
            product_id_value = int(parts[0].split("(ID:")[1].rstrip(")"))
            product_name = parts[1].split(" - ")[0]
            unit_price = float(parts[1].split("$")[1])
            
            # Check if product already in order
            for item in self.order_items:
                if item['product_id'] == product_id_value:
                    messagebox.showerror("Error", "Product already in order")
                    return
            
            subtotal = unit_price * quantity
            self.order_items.append({
                'product_id': product_id_value,
                'product_name': product_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal
            })
            
            # Add to treeview
            self.order_items_tree.insert("", "end", values=(
                product_id_value,
                product_name,
                quantity,
                f"${unit_price:.2f}",
                f"${subtotal:.2f}"
            ))
            
            self.order_quantity_var.set("1")
            self.product_combo.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
    
    def create_order(self):
        """Create new order"""
        if not self.order_items:
            messagebox.showerror("Error", "Please add at least one item to the order")
            return
        
        customer_id = self.customer_combo.current()
        if customer_id == -1:
            messagebox.showerror("Error", "Please select a customer")
            return
        
        try:
            # Parse customer ID
            customer_data = self.customer_combo.get()
            customer_id_value = int(customer_data.split("(ID:")[1].rstrip(")"))
            
            self.set_status("Creating order...")
            data = {
                "customer_id": customer_id_value,
                "items": [
                    {"product_id": item['product_id'], "quantity": item['quantity']}
                    for item in self.order_items
                ]
            }
            
            result = APIClient.request("POST", "/orders", data=data)
            messagebox.showinfo("Success", f"Order created successfully (Order ID: {result['order_id']})")
            
            # Clear order items
            self.order_items = []
            for item in self.order_items_tree.get_children():
                self.order_items_tree.delete(item)
            
            self.customer_combo.set("")
            self.refresh_order_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.set_status("Ready")
    
    def cancel_order(self):
        """Cancel selected order"""
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order")
            return
        
        item = self.order_tree.item(selected[0])
        order_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Cancel order {order_id}?"):
            try:
                self.set_status("Cancelling order...")
                APIClient.request("DELETE", f"/orders/{order_id}")
                messagebox.showinfo("Success", "Order cancelled successfully")
                self.refresh_order_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.set_status("Ready")
    
    def show_order_details(self, event):
        """Show order details on double-click"""
        self.show_selected_order_details()
    
    def show_selected_order_details(self):
        """Show details of selected order"""
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order")
            return
        
        item = self.order_tree.item(selected[0])
        order_id = item['values'][0]
        
        try:
            order_data = APIClient.request("GET", f"/orders/{order_id}")
            
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Order {order_id} Details")
            details_window.geometry("600x400")
            
            # Order info
            info_frame = ttk.LabelFrame(details_window, text="Order Information", padding=10)
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(info_frame, text=f"Order ID: {order_data['order_id']}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Customer ID: {order_data['customer_id']}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Total: ${order_data['total_price']:.2f}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Status: {order_data['status'].upper()}").pack(anchor=tk.W)
            ttk.Label(info_frame, text=f"Order Date: {order_data['order_date']}").pack(anchor=tk.W)
            
            # Items
            items_frame = ttk.LabelFrame(details_window, text="Items", padding=10)
            items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            columns = ("Product ID", "Quantity", "Unit Price", "Subtotal")
            items_tree = ttk.Treeview(items_frame, columns=columns, height=10)
            items_tree.column("#0", width=0, stretch=tk.NO)
            items_tree.column("Product ID", anchor=tk.W, width=80)
            items_tree.column("Quantity", anchor=tk.CENTER, width=100)
            items_tree.column("Unit Price", anchor=tk.CENTER, width=100)
            items_tree.column("Subtotal", anchor=tk.CENTER, width=100)
            
            items_tree.heading("#0", text="", anchor=tk.W)
            items_tree.heading("Product ID", text="Product ID", anchor=tk.W)
            items_tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
            items_tree.heading("Unit Price", text="Unit Price", anchor=tk.CENTER)
            items_tree.heading("Subtotal", text="Subtotal", anchor=tk.CENTER)
            
            for item in order_data['items']:
                items_tree.insert("", "end", values=(
                    item['product_id'],
                    item['quantity'],
                    f"${item['unit_price']:.2f}",
                    f"${item['subtotal']:.2f}"
                ))
            
            items_tree.pack(fill=tk.BOTH, expand=True)
            
            # Action buttons
            action_frame = ttk.Frame(details_window)
            action_frame.pack(fill=tk.X, padx=10, pady=5)
            
            def remove_item():
                selected_item = items_tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select an item")
                    return
                
                item_data = items_tree.item(selected_item[0])
                product_id = item_data['values'][0]
                
                try:
                    APIClient.request("DELETE", f"/orders/{order_id}/items/{product_id}")
                    messagebox.showinfo("Success", "Item removed successfully")
                    details_window.destroy()
                    self.refresh_order_list()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            
            if order_data['status'] == 'pending':
                ttk.Button(action_frame, text="Remove Selected Item", command=remove_item).pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_order_list(self):
        """Refresh order list"""
        try:
            self.set_status("Loading orders...")
            # Clear existing items
            for item in self.order_tree.get_children():
                self.order_tree.delete(item)
            
            # Fetch orders
            orders = APIClient.request("GET", "/orders")
            customers_map = {c['customer_id']: c['customer_name'] for c in APIClient.request("GET", "/customers")}
            
            for order in orders:
                customer_name = customers_map.get(order['customer_id'], 'Unknown')
                self.order_tree.insert("", "end", values=(
                    order['order_id'],
                    customer_name,
                    order['order_date'][:19],  # Format datetime
                    f"${order['total_price']:.2f}",
                    order['status'].upper()
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {str(e)}")
        finally:
            self.set_status("Ready")
    
    # ========================================================================
    # TRANSACTION TAB
    # ========================================================================
    def create_transaction_tab(self):
        """Create transaction view tab"""
        transaction_frame = ttk.Frame(self.notebook)
        self.notebook.add(transaction_frame, text="Transactions")
        
        # Title
        title = ttk.Label(transaction_frame, text="Transaction History", font=("Arial", 14, "bold"))
        title.pack(padx=10, pady=10)
        
        # Filter section
        filter_frame = ttk.LabelFrame(transaction_frame, text="Filter Transactions", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Vendor:").pack(side=tk.LEFT, padx=5)
        self.transaction_vendor_var = tk.StringVar()
        vendor_combo = ttk.Combobox(filter_frame, textvariable=self.transaction_vendor_var, width=30)
        vendor_combo.pack(side=tk.LEFT, padx=5)
        self.transaction_vendor_combo = vendor_combo
        
        ttk.Button(filter_frame, text="Filter", command=self.filter_transactions).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Show All", command=self.refresh_transaction_list).pack(side=tk.LEFT, padx=5)
        
        # Transactions list section
        list_frame = ttk.LabelFrame(transaction_frame, text="All Transactions", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("ID", "Order ID", "Vendor", "Customer", "Product", "Qty", "Amount", "Date", "Status")
        self.transaction_tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.transaction_tree.column("#0", width=0, stretch=tk.NO)
        self.transaction_tree.column("ID", anchor=tk.W, width=40)
        self.transaction_tree.column("Order ID", anchor=tk.W, width=60)
        self.transaction_tree.column("Vendor", anchor=tk.W, width=120)
        self.transaction_tree.column("Customer", anchor=tk.W, width=100)
        self.transaction_tree.column("Product", anchor=tk.W, width=100)
        self.transaction_tree.column("Qty", anchor=tk.CENTER, width=40)
        self.transaction_tree.column("Amount", anchor=tk.CENTER, width=80)
        self.transaction_tree.column("Date", anchor=tk.W, width=150)
        self.transaction_tree.column("Status", anchor=tk.W, width=80)
        
        self.transaction_tree.heading("#0", text="", anchor=tk.W)
        self.transaction_tree.heading("ID", text="ID", anchor=tk.W)
        self.transaction_tree.heading("Order ID", text="Order", anchor=tk.W)
        self.transaction_tree.heading("Vendor", text="Vendor", anchor=tk.W)
        self.transaction_tree.heading("Customer", text="Customer", anchor=tk.W)
        self.transaction_tree.heading("Product", text="Product", anchor=tk.W)
        self.transaction_tree.heading("Qty", text="Qty", anchor=tk.CENTER)
        self.transaction_tree.heading("Amount", text="Amount", anchor=tk.CENTER)
        self.transaction_tree.heading("Date", text="Date", anchor=tk.W)
        self.transaction_tree.heading("Status", text="Status", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transaction_tree.pack(fill=tk.BOTH, expand=True)
    
    def refresh_transaction_list(self):
        """Refresh transaction list"""
        try:
            self.set_status("Loading transactions...")
            # Clear existing items
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            # Fetch transactions
            transactions = APIClient.request("GET", "/transactions")
            vendors_map = {v['vendor_id']: v['business_name'] for v in APIClient.request("GET", "/vendors")}
            customers_map = {c['customer_id']: c['customer_name'] for c in APIClient.request("GET", "/customers")}
            products_map = {p['product_id']: p['product_name'] for p in APIClient.request("GET", "/products")}
            
            for tx in transactions:
                vendor_name = vendors_map.get(tx['vendor_id'], 'Unknown')
                customer_name = customers_map.get(tx['customer_id'], 'Unknown')
                product_name = products_map.get(tx['product_id'], 'Unknown')
                
                self.transaction_tree.insert("", "end", values=(
                    tx['transaction_id'],
                    tx['order_id'],
                    vendor_name,
                    customer_name,
                    product_name,
                    tx['quantity'],
                    f"${tx['transaction_amount']:.2f}",
                    tx['transaction_date'][:19],
                    tx['status'].upper()
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
        finally:
            self.set_status("Ready")
    
    def filter_transactions(self):
        """Filter transactions by vendor"""
        vendor_id = self.transaction_vendor_combo.current()
        if vendor_id == -1:
            messagebox.showerror("Error", "Please select a vendor")
            return
        
        try:
            self.set_status("Loading transactions...")
            # Parse vendor ID
            vendor_data = self.transaction_vendor_combo.get()
            vendor_id_value = int(vendor_data.split("(ID:")[1].rstrip(")"))
            
            # Clear existing items
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            # Fetch transactions
            transactions = APIClient.request("GET", f"/transactions?vendor_id={vendor_id_value}")
            vendors_map = {v['vendor_id']: v['business_name'] for v in APIClient.request("GET", "/vendors")}
            customers_map = {c['customer_id']: c['customer_name'] for c in APIClient.request("GET", "/customers")}
            products_map = {p['product_id']: p['product_name'] for p in APIClient.request("GET", "/products")}
            
            for tx in transactions:
                vendor_name = vendors_map.get(tx['vendor_id'], 'Unknown')
                customer_name = customers_map.get(tx['customer_id'], 'Unknown')
                product_name = products_map.get(tx['product_id'], 'Unknown')
                
                self.transaction_tree.insert("", "end", values=(
                    tx['transaction_id'],
                    tx['order_id'],
                    vendor_name,
                    customer_name,
                    product_name,
                    tx['quantity'],
                    f"${tx['transaction_amount']:.2f}",
                    tx['transaction_date'][:19],
                    tx['status'].upper()
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter transactions: {str(e)}")
        finally:
            self.set_status("Ready")
    
    # ========================================================================
    # DATA REFRESH
    # ========================================================================
    def refresh_all(self):
        """Refresh all data"""
        self.refresh_vendor_list()
        self.refresh_product_list()
        self.refresh_customer_list()
        self.refresh_order_list()
        self.refresh_transaction_list()
        self.update_comboboxes()
    
    def update_comboboxes(self):
        """Update all combobox options"""
        try:
            # Vendor combo
            vendors = APIClient.request("GET", "/vendors")
            vendor_options = [f"(ID:{v['vendor_id']}) {v['business_name']}" for v in vendors]
            self.vendor_combo['values'] = vendor_options
            
            # Customer combo
            customers = APIClient.request("GET", "/customers")
            customer_options = [f"(ID:{c['customer_id']}) {c['customer_name']}" for c in customers]
            self.customer_combo['values'] = customer_options
            self.order_customer_var.set("")
            
            # Product combo
            products = APIClient.request("GET", "/products")
            product_options = [f"(ID:{p['product_id']}) - {p['product_name']} - ${p['listed_price']:.2f}" for p in products]
            self.product_combo['values'] = product_options
            self.order_product_var.set("")
            
            # Transaction vendor combo
            self.transaction_vendor_combo['values'] = vendor_options
            self.transaction_vendor_var.set("")
        except Exception as e:
            logger.error(f"Failed to update comboboxes: {str(e)}")

def main():
    root = tk.Tk()
    app = EcommercePlatformGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
