"""
产品标签页控制器
"""

import tkinter as tk
from tkinter import ttk
from controllers.tab_controller import TabController
from ui.base_components import BaseFrame, InputFrame, DataTable, DialogHelper
from services.api_client import APIClient


class ProductTabController(TabController):
    """产品标签页"""
    
    def __init__(self, notebook: ttk.Notebook, vendors: list = None):
        self.vendors = vendors or []
        self.products = []
        super().__init__(notebook, "产品")

    def setup_ui(self):
        """设置 UI"""
        # 操作框架
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(action_frame, text="新建产品", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="搜索", command=self.show_search_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="刷新", command=self.refresh_products).pack(side=tk.LEFT, padx=5)
        
        # 产品表格
        self.product_table = DataTable(
            self.frame,
            columns=["ID", "供应商", "名称", "价格", "库存", "标签"],
            title="产品列表"
        )

    def refresh_products(self):
        """刷新产品列表"""
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
                    f"¥{product['listed_price']:.2f}",
                    product['stock_quantity'],
                    tags
                ])
        except Exception as e:
            DialogHelper.show_error("错误", f"加载产品失败: {str(e)}")

    def show_create_dialog(self):
        """显示创建产品对话框"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("新建产品")
        dialog.geometry("500x400")
        
        # 输入框
        vendor_options = [f"(ID:{v['vendor_id']}) {v['business_name']}" for v in self.vendors]
        
        fields_frame = InputFrame(dialog, [
            {'label': '供应商', 'key': 'vendor', 'type': 'select', 'values': vendor_options},
            {'label': '产品名称', 'key': 'name', 'type': 'text'},
            {'label': '价格', 'key': 'price', 'type': 'text'},
            {'label': '库存', 'key': 'stock', 'type': 'text'},
            {'label': '标签1', 'key': 'tag1', 'type': 'text'},
            {'label': '标签2', 'key': 'tag2', 'type': 'text'},
            {'label': '标签3', 'key': 'tag3', 'type': 'text'},
        ], padding=10)
        fields_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create():
            values = fields_frame.get_values()
            try:
                vendor_str = values['vendor']
                vendor_id = int(vendor_str.split("(ID:")[1].rstrip(")"))
                
                APIClient.create_product(
                    vendor_id, values['name'], float(values['price']),
                    int(values['stock']), values['tag1'], values['tag2'], values['tag3']
                )
                DialogHelper.show_success("成功", "产品创建成功")
                dialog.destroy()
                self.refresh_products()
            except Exception as e:
                DialogHelper.show_error("错误", str(e))
        
        ttk.Button(button_frame, text="创建", command=create).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def show_search_dialog(self):
        """显示搜索对话框"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("搜索产品")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="搜索标签:").pack(padx=10, pady=5)
        search_entry = ttk.Entry(dialog, width=30)
        search_entry.pack(padx=10, pady=5)
        
        def search():
            tag = search_entry.get().strip()
            if not tag:
                DialogHelper.show_error("错误", "请输入搜索标签")
                return
            
            try:
                self.product_table.clear_all()
                results = APIClient.search_products(tag)
                vendors_map = {v['vendor_id']: v['business_name'] for v in self.vendors}
                
                for product in results:
                    vendor_name = vendors_map.get(product['vendor_id'], 'Unknown')
                    tags = ", ".join([t for t in [product.get('tag1'), product.get('tag2'), product.get('tag3')] if t])
                    
                    self.product_table.add_row([
                        product['product_id'],
                        vendor_name,
                        product['product_name'],
                        f"¥{product['listed_price']:.2f}",
                        product['stock_quantity'],
                        tags
                    ])
                
                dialog.destroy()
            except Exception as e:
                DialogHelper.show_error("错误", str(e))
        
        ttk.Button(dialog, text="搜索", command=search).pack(pady=5)
