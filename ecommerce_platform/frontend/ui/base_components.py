"""
UI 基础组件 - 可复用的 UI 元素
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config.app_config import FONT_SIZE_NORMAL, FONT_SIZE_TITLE, COLOR_ERROR, COLOR_INFO
from typing import Callable, Optional, List, Dict, Any
import math


class BaseFrame(ttk.Frame):
    """基础 Frame 类"""
    
    def __init__(self, parent, title: Optional[str] = None, padding: int = 10, **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        
        if title:
            label = ttk.Label(self, text=title, font=("Arial", FONT_SIZE_TITLE, "bold"))
            label.pack(anchor=tk.W, padx=padding, pady=(padding, 5))
            
            separator = ttk.Separator(self, orient=tk.HORIZONTAL)
            separator.pack(fill=tk.X, padx=padding, pady=5)


class InputFrame(BaseFrame):
    """输入表单 Frame"""
    
    def __init__(self, parent, fields: List[Dict[str, Any]], layout: str = "vertical", **kwargs):
        """
        :param fields: [{'label': '标签', 'key': 'field_name', 'type': 'text/textarea/select'}, ...]
        :param layout: 'vertical' 或 'horizontal'
        """
        super().__init__(parent, **kwargs)
        self.fields = {}
        self.layout = layout
        
        for field in fields:
            label_text = field.get('label', '')
            key = field.get('key', '')
            field_type = field.get('type', 'text')
            
            if layout == "vertical":
                # 竖直布局：每个字段占一行
                row_frame = ttk.Frame(self)
                row_frame.pack(fill=tk.X, padx=5, pady=5)
                
                # 创建标签
                label = ttk.Label(row_frame, text=f"{label_text}:", width=15)
                label.pack(side=tk.LEFT, padx=5)
                
                # 根据类型创建输入框
                if field_type == 'textarea':
                    widget = tk.Text(row_frame, width=40, height=3)
                elif field_type == 'select':
                    widget = ttk.Combobox(row_frame, width=37, values=field.get('values', []))
                else:  # text
                    widget = ttk.Entry(row_frame, width=40)
                
                widget.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            else:
                # 水平布局：标签和输入框在同一行
                label = ttk.Label(self, text=f"{label_text}:", width=12)
                label.pack(side=tk.LEFT, padx=5, pady=5)
                
                if field_type == 'textarea':
                    widget = tk.Text(self, width=25, height=2)
                elif field_type == 'select':
                    widget = ttk.Combobox(self, width=23, values=field.get('values', []))
                else:
                    widget = ttk.Entry(self, width=25)
                
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
    """数据表格（非分页版本，保持向后兼容）"""
    
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
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_row(self, values: List[Any]):
        """添加行"""
        self.tree.insert("", "end", values=values)

    def get_selected(self) -> Optional[List[Any]]:
        """获取选中行"""
        selected = self.tree.selection()
        if selected:
            return list(self.tree.item(selected[0])['values'])
        return None

    def clear_all(self):
        """清空所有行"""
        for item in self.tree.get_children():
            self.tree.delete(item)


class PaginatedDataTable(BaseFrame):
    """分页数据表格"""
    
    def __init__(self, parent, columns: List[str], page_size: int = 10, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.columns = columns
        self.page_size = page_size
        self.all_data = []
        self.current_page = 0
        self.total_pages = 0
        
        # 顶部：分页控制
        pagination_frame = ttk.Frame(self)
        pagination_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(pagination_frame, text="< 上一页", command=self.prev_page).pack(side=tk.LEFT, padx=2)
        ttk.Button(pagination_frame, text="下一页 >", command=self.next_page).pack(side=tk.LEFT, padx=2)
        
        self.page_label = ttk.Label(pagination_frame, text="第 1 页")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        # 中间：表格
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
        
        # 底部：行数信息
        self.info_label = ttk.Label(self, text="总计: 0 行")
        self.info_label.pack(fill=tk.X, padx=5, pady=5)

    def add_row(self, values: List[Any]):
        """添加行到数据缓存"""
        self.all_data.append(values)
        self._refresh_display()

    def clear_all(self):
        """清空所有数据"""
        self.all_data = []
        self.current_page = 0
        self.total_pages = 0
        self._refresh_display()

    def load_data(self, data: List[List[Any]]):
        """加载完整数据集"""
        self.all_data = data
        self.current_page = 0
        self.total_pages = max(1, math.ceil(len(data) / self.page_size))
        self._refresh_display()

    def _refresh_display(self):
        """刷新当前页显示"""
        # 清空树形表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 计算页数
        if len(self.all_data) == 0:
            self.total_pages = 1
            self.current_page = 0
        else:
            self.total_pages = math.ceil(len(self.all_data) / self.page_size)
            self.current_page = min(self.current_page, self.total_pages - 1)
        
        # 获取当前页数据
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_data = self.all_data[start_idx:end_idx]
        
        # 填充数据
        for values in page_data:
            self.tree.insert("", "end", values=values)
        
        # 更新标签
        if self.total_pages > 0:
            self.page_label.config(text=f"第 {self.current_page + 1} / {self.total_pages} 页")
        self.info_label.config(text=f"总计: {len(self.all_data)} 行 (每页 {self.page_size} 行)")

    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._refresh_display()

    def prev_page(self):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_display()

    def get_selected(self) -> Optional[List[Any]]:
        """获取选中行"""
        selected = self.tree.selection()
        if selected:
            return list(self.tree.item(selected[0])['values'])
        return None


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
