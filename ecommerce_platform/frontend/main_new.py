"""
E-Commerce Platform - 简洁的前端 GUI (v2.0 模块化)

架构:
  - config/: 配置文件
  - services/: API 客户端
  - ui/: UI 基础组件
  - controllers/: 标签页控制器
  - main.py: 主应用
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
    """电商平台 GUI 应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.resizable(True, True)
        
        # 初始化数据
        self.vendors = []
        self.products = []
        self.customers = []
        
        # 设置样式
        style = ttk.Style()
        style.theme_use(THEME_NAME)
        
        # 创建 UI
        self.setup_ui()
        
        # 加载初始数据
        self.load_initial_data()

    def setup_ui(self):
        """设置 UI"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 创建 Notebook (标签页容器)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
         # 创建标签页控制器
        # 注意：vendors, products, customers 还是空的，会在 load_initial_data 中加载和更新
        self.vendor_tab = VendorTabController(self.notebook, self.on_vendors_updated)
        self.product_tab = ProductTabController(self.notebook, [])
        self.customer_tab = CustomerTabController(self.notebook)
        self.order_tab = OrderTabController(self.notebook, [], [])
        self.transaction_tab = TransactionTabController(self.notebook, [])
        
        # 创建状态栏
        self.status_bar = StatusBar(self.root)

    def load_initial_data(self):
        """加载初始数据（异步）"""
        self.update_status("加载数据中...")
        
        # 计数器：用于跟踪完成的加载任务
        self.load_count = 0
        self.load_total = 3  # 需要加载 3 种数据：vendors, products, customers
        
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
            DialogHelper.show_error("错误", f"加载数据失败: {str(error)}")
            self.update_status("错误")
        
        # 并行加载三种数据（异步）
        AsyncAPIClient.get_vendors_async(on_vendors_loaded, on_error)
        AsyncAPIClient.get_products_async(on_products_loaded, on_error)
        AsyncAPIClient.get_customers_async(on_customers_loaded, on_error)
    
    def _on_data_loaded(self):
        """数据加载回调"""
        self.load_count += 1
        
        # 当所有数据都加载完成时
        if self.load_count == self.load_total:
            # 更新标签页引用
            self.product_tab.vendors = self.vendors
            self.order_tab.customers = self.customers
            self.order_tab.products = self.products
            self.transaction_tab.vendors = self.vendors
            
            # 刷新所有标签页（同步）
            self.vendor_tab.refresh_vendors()
            self.product_tab.refresh_products()
            self.customer_tab.refresh_customers()
            self.order_tab.refresh_orders()
            self.transaction_tab.refresh_transactions()
            
            self.update_status("就绪")

    def on_vendors_updated(self):
        """供应商更新回调（异步）"""
        def on_success(data):
            self.vendors = data
            self.product_tab.vendors = self.vendors
            self.transaction_tab.vendors = self.vendors
        
        def on_error(error):
            DialogHelper.show_error("错误", f"更新数据失败: {str(error)}")
        
        AsyncAPIClient.get_vendors_async(on_success, on_error)

    def update_status(self, message: str):
        """更新状态栏"""
        self.status_bar.set_status(message)


def main():
    """主函数"""
    root = tk.Tk()
    app = EcommercePlatformApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
