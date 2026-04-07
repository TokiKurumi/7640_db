"""
客户、订单和交易标签页控制器
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List, Dict, Any
from controllers.tab_controller import TabController
from ui.base_components import BaseFrame, InputFrame, PaginatedDataTable, DataTable, DialogHelper
from services.api_client import APIClient


class CustomerTabController(TabController):
    """客户标签页"""
    
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook, "客户")
    
    def setup_ui(self):
        """设置 UI"""
        # 操作按钮
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="新建客户", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_customers).pack(side=tk.LEFT, padx=5)
        
        # 客户表格（分页）
        self.customer_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "名称", "电话", "地址"],
            page_size=10,
            title="客户列表"
        )
        self.customer_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_customers(self):
        """刷新客户列表"""
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
            DialogHelper.show_error("错误", f"加载客户失败: {str(e)}")

    def show_create_dialog(self):
        """显示创建客户对话框"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("新建客户")
        dialog.geometry("400x200")
        
        fields_frame = InputFrame(dialog, [
            {'label': '客户名称', 'key': 'name', 'type': 'text'},
            {'label': '电话号码', 'key': 'phone', 'type': 'text'},
            {'label': '收货地址', 'key': 'address', 'type': 'textarea'},
        ], padding=10)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create():
            values = fields_frame.get_values()
            try:
                APIClient.create_customer(values['name'], values['phone'], values['address'])
                DialogHelper.show_success("成功", "客户创建成功")
                dialog.destroy()
                self.refresh_customers()
            except Exception as e:
                DialogHelper.show_error("错误", str(e))
        
        ttk.Button(button_frame, text="创建", command=create).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)


class OrderTabController(TabController):
    """订单标签页"""
    
    def __init__(self, notebook: ttk.Notebook, customers: Optional[List[Dict[str, Any]]] = None, products: Optional[List[Dict[str, Any]]] = None):
        self.customers = customers if customers is not None else []
        self.products = products if products is not None else []
        self.order_items = []
        super().__init__(notebook, "订单")

    def setup_ui(self):
        """设置 UI"""
        # 操作按钮
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="新建订单", command=self.show_create_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消订单", command=self.cancel_selected_order).pack(side=tk.LEFT, padx=5)
        
        # 订单表格（分页）
        self.order_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "客户", "日期", "总额", "状态"],
            page_size=10,
            title="订单列表"
        )
        self.order_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 将表格的选择事件与详情显示关联
        self.order_table.tree.bind("<Double-1>", lambda e: self.show_order_details())

    def refresh_orders(self):
        """刷新订单列表"""
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
            DialogHelper.show_error("错误", f"加载订单失败: {str(e)}")

    def show_create_dialog(self):
        """显示创建订单对话框"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("新建订单")
        dialog.geometry("600x400")
        
        # 顾客选择
        customer_options = [f"(ID:{c['customer_id']}) {c['customer_name']}" for c in self.customers]
        product_options = [f"(ID:{p['product_id']}) {p['product_name']} - ¥{p['listed_price']}" for p in self.products]
        
        fields_frame = InputFrame(dialog, [
            {'label': '客户', 'key': 'customer', 'type': 'select', 'values': customer_options},
            {'label': '产品', 'key': 'product', 'type': 'select', 'values': product_options},
            {'label': '数量', 'key': 'quantity', 'type': 'text'},
        ], padding=10)
        fields_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 按钮框架
        action_frame = ttk.Frame(dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(action_frame, text="添加项", command=lambda: self._add_order_item(fields_frame, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="创建订单", command=lambda: self._create_order(fields_frame, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # 订单项列表
        self.order_items = []
        items_table = DataTable(
            dialog,
            columns=["产品ID", "数量"],
            title="订单项"
        )

    def _add_order_item(self, fields_frame, dialog):
        """添加订单项"""
        values = fields_frame.get_values()
        try:
            product_str = values['product']
            product_id = int(product_str.split("(ID:")[1].rstrip(")"))
            quantity = int(values['quantity'])
            
            self.order_items.append({'product_id': product_id, 'quantity': quantity})
            DialogHelper.show_success("成功", f"已添加产品 ID {product_id}")
            fields_frame.clear_values()
        except Exception as e:
            DialogHelper.show_error("错误", f"添加失败: {str(e)}")

    def _create_order(self, fields_frame, dialog):
        """创建订单"""
        if not self.order_items:
            DialogHelper.show_error("错误", "订单至少需要一个商品")
            return
        
        values = fields_frame.get_values()
        try:
            customer_str = values['customer']
            customer_id = int(customer_str.split("(ID:")[1].rstrip(")"))
            
            APIClient.create_order(customer_id, self.order_items)
            DialogHelper.show_success("成功", "订单创建成功")
            self.order_items = []
            dialog.destroy()
            self.refresh_orders()
        except Exception as e:
            DialogHelper.show_error("错误", str(e))

    def show_order_details(self):
        """显示订单详情"""
        row = self.order_table.get_selected()
        if not row:
            return
        
        order_id = row[0]
        try:
            order = APIClient.get_order_details(order_id)
            
            # 创建详情窗口
            details_dialog = tk.Toplevel(self.frame)
            details_dialog.title(f"订单 {order_id} 详情")
            details_dialog.geometry("400x300")
            
            # 订单信息
            info_text = f"""
订单ID: {order['order_id']}
客户ID: {order['customer_id']}
总额: ¥{order['total_price']:.2f}
状态: {order['status']}
日期: {order['order_date']}
            """
            
            ttk.Label(details_dialog, text=info_text, justify=tk.LEFT).pack(padx=10, pady=10)
            
            # 订单项
            items_table = DataTable(
                details_dialog,
                columns=["产品ID", "数量", "单价", "小计"],
                title="订单项"
            )
            
            for item in order['items']:
                items_table.add_row([
                    item['product_id'],
                    item['quantity'],
                    f"¥{item['unit_price']:.2f}",
                    f"¥{item['subtotal']:.2f}"
                ])
            
            # 操作按钮
            if order['status'] == 'pending':
                button_frame = ttk.Frame(details_dialog)
                button_frame.pack(fill=tk.X, padx=10, pady=10)
                
                def remove_item():
                    selected = items_table.get_selected()
                    if selected:
                        product_id = selected[0]
                        try:
                            APIClient.remove_order_item(order_id, product_id)
                            DialogHelper.show_success("成功", "商品已删除")
                            details_dialog.destroy()
                            self.refresh_orders()
                        except Exception as e:
                            DialogHelper.show_error("错误", str(e))
                
                ttk.Button(button_frame, text="删除选中商品", command=remove_item).pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            DialogHelper.show_error("错误", f"加载订单详情失败: {str(e)}")

    def cancel_selected_order(self):
        """取消选中的订单"""
        row = self.order_table.get_selected()
        if not row:
            DialogHelper.show_error("提示", "请选择一个订单")
            return
        
        order_id = row[0]
        if DialogHelper.confirm("确认", f"确定取消订单 {order_id} 吗?"):
            try:
                APIClient.cancel_order(order_id)
                DialogHelper.show_success("成功", "订单已取消")
                self.refresh_orders()
            except Exception as e:
                DialogHelper.show_error("错误", str(e))


class TransactionTabController(TabController):
    """交易标签页"""
    
    def __init__(self, notebook: ttk.Notebook, vendors: Optional[List[Dict[str, Any]]] = None):
        self.vendors = vendors if vendors is not None else []
        super().__init__(notebook, "交易")

    def setup_ui(self):
        """设置 UI"""
        # 操作按钮
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="刷新", command=self.refresh_transactions).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="按供应商筛选", command=self.show_filter_dialog).pack(side=tk.LEFT, padx=5)
        
        # 交易表格（分页）
        self.transaction_table = PaginatedDataTable(
            self.frame,
            columns=["ID", "订单ID", "供应商", "客户", "产品", "数量", "金额", "日期"],
            page_size=10,
            title="交易历史"
        )
        self.transaction_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def refresh_transactions(self):
        """刷新交易列表"""
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
            DialogHelper.show_error("错误", f"加载交易失败: {str(e)}")

    def show_filter_dialog(self):
        """显示筛选对话框"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("筛选交易")
        dialog.geometry("300x100")
        
        vendor_options = [f"(ID:{v['vendor_id']}) {v['business_name']}" for v in self.vendors]
        
        ttk.Label(dialog, text="选择供应商:").pack(padx=10, pady=5)
        vendor_combo = ttk.Combobox(dialog, values=vendor_options, width=28)
        vendor_combo.pack(padx=10, pady=5)
        
        def filter_by_vendor():
            vendor_str = vendor_combo.get()
            if not vendor_str:
                DialogHelper.show_error("错误", "请选择供应商")
                return
                        
            vendor_id = int(vendor_str.split("(ID:")[1].split(")")[0])
            
            try:
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
            except Exception as e:
                DialogHelper.show_error("错误", str(e))
        
        ttk.Button(dialog, text="筛选", command=filter_by_vendor).pack(pady=5)
