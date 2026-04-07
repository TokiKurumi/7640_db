"""
供应商标签页控制器
"""

import tkinter as tk
from tkinter import ttk
from controllers.tab_controller import TabController
from ui.base_components import BaseFrame, InputFrame, PaginatedDataTable, DialogHelper
from services.api_client import APIClient


class VendorTabController(TabController):
    """供应商标签页"""
    
    def __init__(self, notebook: ttk.Notebook, on_refresh_callback=None):
        self.on_refresh_callback = on_refresh_callback
        super().__init__(notebook, "供应商")

    def setup_ui(self):
        """设置 UI"""
        # 创建按钮框架
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="新建供应商", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_vendors).pack(side=tk.LEFT, padx=5)
        
        # 创建数据表格（分页）
        self.vendor_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "业务名称", "评分", "位置"],
            page_size=10,
            title="供应商列表"
        )
        self.vendor_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_vendors(self):
        """刷新供应商列表"""
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
            DialogHelper.show_error("错误", f"加载供应商失败: {str(e)}")

    def show_create_dialog(self):
        """显示创建对话框"""
        # 创建对话框窗口
        dialog = tk.Toplevel(self.frame)
        dialog.title("新建供应商")
        dialog.geometry("450x150")
        dialog.resizable(False, False)
        
        # 输入框
        fields_frame = InputFrame(dialog, [
            {'label': '业务名称', 'key': 'name', 'type': 'text'},
            {'label': '地理位置', 'key': 'location', 'type': 'text'}
        ], layout="vertical", padding=10)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create():
            values = fields_frame.get_values()
            try:
                APIClient.create_vendor(values['name'], values['location'])
                DialogHelper.show_success("成功", "供应商创建成功")
                dialog.destroy()
                self.refresh_vendors()
            except Exception as e:
                DialogHelper.show_error("错误", str(e))
        
        ttk.Button(button_frame, text="创建", command=create).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
