"""
UI Base Components - Reusable UI Elements
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config.app_config import FONT_SIZE_NORMAL, FONT_SIZE_TITLE, COLOR_ERROR, COLOR_INFO
from typing import Callable, Optional, List, Dict, Any
import math


class BaseFrame(ttk.Frame):
    """Base Frame Class"""
    
    def __init__(self, parent, title: Optional[str] = None, padding: int = 10, **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        
        if title:
            label = ttk.Label(self, text=title, font=("Arial", FONT_SIZE_TITLE, "bold"))
            label.pack(anchor=tk.W, padx=padding, pady=(padding, 5))
            
            separator = ttk.Separator(self, orient=tk.HORIZONTAL)
            separator.pack(fill=tk.X, padx=padding, pady=5)


class InputFrame(BaseFrame):
    """Input Form Frame"""
    
    def __init__(self, parent, fields: List[Dict[str, Any]], layout: str = "vertical", **kwargs):
        """
        :param fields: [{'label': 'Label', 'key': 'field_name', 'type': 'text/textarea/select'}, ...]
        :param layout: 'vertical' or 'horizontal'
        """
        super().__init__(parent, **kwargs)
        self.fields = {}
        self.layout = layout
        
        for field in fields:
            label_text = field.get('label', '')
            key = field.get('key', '')
            field_type = field.get('type', 'text')
            
            if layout == "vertical":
                # Vertical layout: each field takes one row
                row_frame = ttk.Frame(self)
                row_frame.pack(fill=tk.X, padx=5, pady=5)
                
                # Create label
                label = ttk.Label(row_frame, text=f"{label_text}:", width=15)
                label.pack(side=tk.LEFT, padx=5)
                
                # Create input widget based on type
                if field_type == 'textarea':
                    widget = tk.Text(row_frame, width=40, height=3)
                elif field_type == 'select':
                    widget = ttk.Combobox(row_frame, width=37, values=field.get('values', []), state='readonly')
                else:  # text
                    widget = ttk.Entry(row_frame, width=40)
                
                widget.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            else:
                # Horizontal layout: label and input are on the same line
                label = ttk.Label(self, text=f"{label_text}:", width=12)
                label.pack(side=tk.LEFT, padx=5, pady=5)
                
                if field_type == 'textarea':
                    widget = tk.Text(self, width=25, height=2)
                elif field_type == 'select':
                    widget = ttk.Combobox(self, width=23, values=field.get('values', []), state='readonly')
                else:
                    widget = ttk.Entry(self, width=25)
                
                widget.pack(side=tk.LEFT, padx=5, pady=5)
            
            self.fields[key] = widget

    def get_values(self) -> Dict[str, str]:
        """Get all input values"""
        values = {}
        for key, widget in self.fields.items():
            if isinstance(widget, tk.Text):
                values[key] = widget.get("1.0", tk.END).strip()
            elif isinstance(widget, ttk.Combobox):
                values[key] = widget.get()
            else:
                values[key] = widget.get()
        return values

    def clear_values(self):
        """Clear all inputs"""
        for widget in self.fields.values():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)


class DataTable(BaseFrame):
    """Data Table (non-paginated version for backward compatibility)"""
    
    def __init__(self, parent, columns: List[str], **kwargs):
        super().__init__(parent, **kwargs)
        
        # Create Treeview
        self.tree = ttk.Treeview(self, columns=columns, height=15, show='headings')
        
        # Set columns
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col, anchor=tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_row(self, values: List[Any]):
        """Add a row"""
        self.tree.insert("", "end", values=values)

    def get_selected(self) -> Optional[List[Any]]:
        """Get the selected row"""
        selected = self.tree.selection()
        if selected:
            return list(self.tree.item(selected[0])['values'])
        return None

    def clear_all(self):
        """Clear all rows"""
        for item in self.tree.get_children():
            self.tree.delete(item)


class PaginatedDataTable(BaseFrame):
    """Paginated Data Table"""
    
    def __init__(self, parent, columns: List[str], page_size: int = 10, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.columns = columns
        self.page_size = page_size
        self.all_data = []
        self.current_page = 0
        self.total_pages = 0
        
        # Top: Pagination controls
        pagination_frame = ttk.Frame(self)
        pagination_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(pagination_frame, text="< Prev", command=self.prev_page).pack(side=tk.LEFT, padx=2)
        ttk.Button(pagination_frame, text="Next >", command=self.next_page).pack(side=tk.LEFT, padx=2)
        
        self.page_label = ttk.Label(pagination_frame, text="Page 1")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        # Middle: Table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')
        
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bottom: Row count information
        self.info_label = ttk.Label(self, text="Total: 0 rows")
        self.info_label.pack(fill=tk.X, padx=5, pady=5)

    def add_row(self, values: List[Any]):
        """Add a row to the data cache"""
        self.all_data.append(values)
        self._refresh_display()

    def clear_all(self):
        """Clear all data"""
        self.all_data = []
        self.current_page = 0
        self.total_pages = 0
        self._refresh_display()

    def load_data(self, data: List[List[Any]]):
        """Load the full dataset"""
        self.all_data = data
        self.current_page = 0
        self.total_pages = max(1, math.ceil(len(data) / self.page_size))
        self._refresh_display()

    def _refresh_display(self):
        """Refresh the current page display"""
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Calculate page count
        if len(self.all_data) == 0:
            self.total_pages = 1
            self.current_page = 0
        else:
            self.total_pages = math.ceil(len(self.all_data) / self.page_size)
            self.current_page = min(self.current_page, self.total_pages - 1)
        
        # Get current page data
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_data = self.all_data[start_idx:end_idx]
        
        # Populate data
        for values in page_data:
            self.tree.insert("", "end", values=values)
        
        # Update labels
        if self.total_pages > 0:
            self.page_label.config(text=f"Page {self.current_page + 1} / {self.total_pages}")
        self.info_label.config(text=f"Total: {len(self.all_data)} rows ({self.page_size} per page)")

    def next_page(self):
        """Next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._refresh_display()

    def prev_page(self):
        """Previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_display()

    def get_selected(self) -> Optional[List[Any]]:
        """Get the selected row"""
        selected = self.tree.selection()
        if selected:
            return list(self.tree.item(selected[0])['values'])
        return None


class StatusBar(ttk.Frame):
    """Status Bar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, padx=5, pady=5)

    def set_status(self, message: str, status_type: str = "info"):
        """Set status"""
        self.status_var.set(message)
        self.update()


class DialogHelper:
    """Dialog Helper Functions"""
    
    @staticmethod
    def show_success(title: str, message: str):
        """Show success dialog"""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title: str, message: str):
        """Show warning dialog"""
        messagebox.showwarning(title, message)

    @staticmethod
    def confirm(title: str, message: str) -> bool:
        """Show confirmation dialog"""
        return messagebox.askyesno(title, message)