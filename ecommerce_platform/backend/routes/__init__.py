"""
API路由层 - 定义所有REST接口
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import (
    VendorBase, VendorResponse, ProductBase, ProductResponse,
    CustomerBase, CustomerResponse, OrderBase, OrderResponse, 
    TransactionResponse
)
from services import VendorService, ProductService, CustomerService, OrderService, TransactionService
from dao import DatabaseConfig

# 创建数据库配置
db_config = DatabaseConfig(
    host='localhost',
    port=3306,
    user='root',
    password='3333',
    database='ecommerce_platform'
)

# 初始化服务
vendor_service = VendorService(db_config)
product_service = ProductService(db_config)
customer_service = CustomerService(db_config)
order_service = OrderService(db_config)
transaction_service = TransactionService(db_config)

# 创建路由器
router = APIRouter(prefix="/api", tags=["ecommerce"])


# ============================================================================
# VENDORS 端点
# ============================================================================

@router.get("/vendors", response_model=List[VendorResponse])
async def get_vendors():
    """获取所有供应商"""
    try:
        return vendor_service.get_all_vendors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vendors", response_model=VendorResponse)
async def create_vendor(vendor: VendorBase):
    """创建新供应商"""
    try:
        return vendor_service.create_vendor(vendor.business_name, vendor.geographical_presence)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vendors/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: int):
    """获取特定供应商"""
    try:
        return vendor_service.get_vendor_by_id(vendor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PRODUCTS 端点
# ============================================================================

@router.get("/products", response_model=List[ProductResponse])
async def get_products(vendor_id: Optional[int] = None):
    """获取所有产品或按供应商筛选"""
    try:
        if vendor_id:
            return product_service.get_products_by_vendor(vendor_id)
        return product_service.get_all_products()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products", response_model=ProductResponse)
async def create_product(vendor_id: int, product: ProductBase):
    """创建新产品"""
    try:
        return product_service.create_product(
            vendor_id, product.product_name, product.listed_price,
            product.stock_quantity, product.tag1, product.tag2, product.tag3
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/search")
async def search_products(tag: str):
    """根据标签搜索产品"""
    try:
        return product_service.search_products_by_tag(tag)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CUSTOMERS 端点
# ============================================================================

@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers():
    """获取所有客户"""
    try:
        return customer_service.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customers", response_model=CustomerResponse)
async def create_customer(customer: CustomerBase):
    """创建新客户"""
    try:
        return customer_service.create_customer(
            customer.customer_name, customer.contact_number, customer.shipping_address
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int):
    """获取特定客户"""
    try:
        return customer_service.get_customer_by_id(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ORDERS 端点
# ============================================================================

@router.get("/orders")
async def get_orders(customer_id: Optional[int] = None):
    """获取所有订单或按客户筛选"""
    try:
        if customer_id:
            return order_service.get_orders_by_customer(customer_id)
        return order_service.get_all_orders()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orders")
async def create_order(order: OrderBase):
    """创建新订单"""
    try:
        items = [
            {'product_id': item.product_id, 'quantity': item.quantity}
            for item in order.items
        ]
        return order_service.create_order(order.customer_id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    """获取特定订单"""
    try:
        return order_service.get_order_by_id(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/orders/{order_id}")
async def update_order_status(order_id: int, status: str):
    """更新订单状态"""
    try:
        order_service.update_order_status(order_id, status)
        return {"message": "订单状态已更新"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/orders/{order_id}")
async def cancel_order(order_id: int):
    """取消订单"""
    try:
        order_service.cancel_order(order_id)
        return {"message": "订单已取消"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/orders/{order_id}/items/{product_id}")
async def remove_order_item(order_id: int, product_id: int):
    """从订单中删除商品"""
    try:
        order_service.remove_order_item(order_id, product_id)
        return {"message": "商品已删除"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TRANSACTIONS 端点
# ============================================================================

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(vendor_id: Optional[int] = None):
    """获取所有交易或按供应商筛选"""
    try:
        if vendor_id:
            return transaction_service.get_transactions_by_vendor(vendor_id)
        return transaction_service.get_all_transactions()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "E-Commerce Platform API is running"}
