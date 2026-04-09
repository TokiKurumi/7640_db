"""
Vendor Tab Controller
"""

import tkinter as tk
from tkinter import ttk
from controllers.tab_controller import TabController
from ui.base_components import BaseFrame, InputFrame, PaginatedDataTable, DialogHelper
from services.api_client import APIClient


class VendorTabController(TabController):
    """Vendor Tab"""
    
    def __init__(self, notebook: ttk.Notebook, on_refresh_callback=None):
        self.on_refresh_callback = on_refresh_callback
        super().__init__(notebook, "Vendors")

    def setup_ui(self):
        """Set up the UI"""
        # Create button frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="New Vendor", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_vendors).pack(side=tk.LEFT, padx=5)
        
        # Create data table (paginated)
        self.vendor_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "Business Name", "Rating", "Location"],
            page_size=10,
            title="Vendor List"
        )
        self.vendor_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_vendors(self):
        """Refresh vendor list"""
        try:
            self.vendor_table.clear_all()
            vendors = APIClient.get_vendors()
            
            for vendor in vendors:
                self.vendor_table.add_row([
                    vendor['vendor_id'],
                    vendor['business_name'],
                    f"{vendor['average_rating']:.1f}",
                    vendor.get('geographical_presence', 'N/A')
                ])
            
            if self.on_refresh_callback:
                self.on_refresh_callback()
        except Exception as e:
            DialogHelper.show_error("Error", f"Failed to load vendors: {str(e)}")

    def show_create_dialog(self):
        """Show create dialog"""
        # Create dialog window
        dialog = tk.Toplevel(self.frame)
        dialog.title("New Vendor")
        dialog.geometry("450x150")
        dialog.resizable(False, False)
        
        # Input fields
        fields_frame = InputFrame(dialog, [
            {'label': 'Business Name', 'key': 'name', 'type': 'text'},
            {'label': 'Geographical Location', 'key': 'location', 'type': 'text'}
        ], layout="vertical", padding=10)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create():
            values = fields_frame.get_values()
            try:
                APIClient.create_vendor(values['name'], values['location'])
                DialogHelper.show_success("Success", "Vendor created successfully")
                dialog.destroy()
                self.refresh_vendors()
            except Exception as e:
                DialogHelper.show_error("Error", str(e))
        
        ttk.Button(button_frame, text="Create", command=create).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)