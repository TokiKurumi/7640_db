"""
UI 基础组件 - 可复用的 UI 元素
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config.app_config import FONT_SIZE_NORMAL, FONT_SIZE_TITLE, COLOR_ERROR, COLOR_INFO
from typing import Callable, Optional, List, Dict, Any


class BaseFrame(ttk.Frame):
    """基础 Frame 类"""
    
    def __init__(self, parent, title: str = None, padding: int = 10, **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        
        if title:
            label = ttk.Label(self, text=title, font=("Arial", FONT_SIZE_TITLE, "bold"))
            label.pack(anchor=tk.W, padx=padding, pady=(padding, 5))
            
            separator = ttk.Separator(self, orient=tk.HORIZONTAL)
            separator.pack(fill=tk.X, padx=padding, pady=5)


class InputFrame(BaseFrame):
    """输入表单 Frame"""
    
    def __init__(self, parent, fields: List[Dict[str, Any]], **kwargs):
        """
        :param fields: [{'label': '标签', 'key': 'field_name', 'type': 'text/textarea/select'}, ...]
        """
        super().__init__(parent, **kwargs)
        self.fields = {}
        
        for field in fields:
            label_text = field.get('label', '')
            key = field.get('key', '')
            field_type = field.get('type', 'text')
            
            # 创建标签
            label = ttk.Label(self, text=f"{label_text}:", width=15)
            label.pack(side=tk.LEFT, padx=5, pady=5)
            
            # 根据类型创建输入框
            if field_type == 'textarea':
                widget = tk.Text(self, width=30, height=3)
            elif field_type == 'select':
                widget = ttk.Combobox(self, width=28, values=field.get('values', []))
            else:  # text
                widget = ttk.Entry(self, width=30)
            
            widget.pack(side=tk.LEFT, padx=5, pady=5)
            self.fields[key] = widget

    def get_values(self) -> Dict[str, str]:
        """获取所有输入值"""
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
        """清空所有输入"""
        for widget in self.fields.values():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)


class DataTable(BaseFrame):
    """数据表格"""
    
    def __init__(self, parent, columns: List[str], **kwargs):
        super().__init__(parent, **kwargs)
        
        # 创建 Treeview
        self.tree = ttk.Treeview(self, columns=columns, height=15, show='headings')
        
        # 设置列
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col, anchor=tk.W)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_row(self, values: List[Any]):
        """添加行"""
        self.tree.insert("", "end", values=values)

    def get_selected(self) -> Optional[List[Any]]:
        """获取选中行"""
        selected = self.tree.selection()
        if selected:
            return self.tree.item(selected[0])['values']
        return None

    def clear_all(self):
        """清空所有行"""
        for item in self.tree.get_children():
            self.tree.delete(item)


class StatusBar(ttk.Frame):
    """状态栏"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, padx=5, pady=5)

    def set_status(self, message: str, status_type: str = "info"):
        """设置状态"""
        self.status_var.set(message)
        self.update()


class DialogHelper:
    """对话框辅助函数"""
    
    @staticmethod
    def show_success(title: str, message: str):
        """显示成功对话框"""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_error(title: str, message: str):
        """显示错误对话框"""
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title: str, message: str):
        """显示警告对话框"""
        messagebox.showwarning(title, message)

    @staticmethod
    def confirm(title: str, message: str) -> bool:
        """显示确认对话框"""
        return messagebox.askyesno(title, message)
