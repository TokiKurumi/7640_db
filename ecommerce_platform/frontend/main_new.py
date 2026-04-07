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
        """加载初始数据"""
        self.update_status("加载数据中...")
        
        try:
            # 加载供应商
            self.vendors = APIClient.get_vendors()
            print(self.vendors)
            
            # 加载产品
            self.products = APIClient.get_products()
            
            # 加载客户
            self.customers = APIClient.get_customers()
            
            # 更新标签页引用
            self.product_tab.vendors = self.vendors
            self.order_tab.customers = self.customers
            self.order_tab.products = self.products
            self.transaction_tab.vendors = self.vendors
            
            # 刷新所有标签页
            self.vendor_tab.refresh_vendors()
            self.product_tab.refresh_products()
            self.customer_tab.refresh_customers()
            self.order_tab.refresh_orders()
            self.transaction_tab.refresh_transactions()
            
            self.update_status("就绪")
        except Exception as e:
            DialogHelper.show_error("错误", f"加载数据失败: {str(e)}")
            self.update_status("错误")

    def on_vendors_updated(self):
        """供应商更新回调"""
        try:
            self.vendors = APIClient.get_vendors()
            self.product_tab.vendors = self.vendors
            self.order_tab.customers = self.customers
            self.transaction_tab.vendors = self.vendors
        except Exception as e:
            DialogHelper.show_error("错误", f"更新数据失败: {str(e)}")

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
