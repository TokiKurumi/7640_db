from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import (
    VendorBase, VendorResponse, ProductBase, ProductResponse,
    CustomerBase, CustomerResponse, OrderBase, OrderResponse, 
    TransactionResponse
)
from services import VendorService, ProductService, CustomerService, OrderService, TransactionService
from dao import DatabaseConfig

# config the db
db_config = DatabaseConfig(
    host='localhost',
    port=3306,
    user='root',
    password='3333',
    database='ecommerce_platform'
)

vendor_service = VendorService(db_config)
product_service = ProductService(db_config)
customer_service = CustomerService(db_config)
order_service = OrderService(db_config)
transaction_service = TransactionService(db_config)


# Create router
# api `http://localhost:8000/docs`
router = APIRouter(prefix="/api", tags=["ecommerce"])

@router.get("/vendors", response_model=List[VendorResponse])
async def get_vendors():
    return vendor_service.get_all_vendors()


@router.post("/vendors", response_model=VendorResponse)
async def create_vendor(vendor: VendorBase):
    return vendor_service.create_vendor(vendor.business_name, vendor.geographical_presence)


@router.get("/vendors/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: int):
    return vendor_service.get_vendor_by_id(vendor_id)



@router.get("/products", response_model=List[ProductResponse])
async def get_products(vendor_id: Optional[int] = None):
    if vendor_id:
        return product_service.get_products_by_vendor(vendor_id)

    return product_service.get_all_products()


@router.post("/products", response_model=ProductResponse)
async def create_product(vendor_id: int, product: ProductBase):
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
    try:
        return product_service.search_products_by_tag(tag)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers():
    try:
        return customer_service.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customers", response_model=CustomerResponse)
async def create_customer(customer: CustomerBase):
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
    try:
        return customer_service.get_customer_by_id(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders")
async def get_orders(customer_id: Optional[int] = None):
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
    try:
        return order_service.get_order_by_id(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/orders/{order_id}")
async def update_order_status(order_id: int, status: str):
    order_service.update_order_status(order_id, status)
    return {"message": "Order status updated"}


@router.delete("/orders/{order_id}")
async def cancel_order(order_id: int):
    order_service.cancel_order(order_id)
    return {"message": "Order canceled"}


@router.delete("/orders/{order_id}/items/{product_id}")
async def remove_order_item(order_id: int, product_id: int):
    order_service.remove_order_item(order_id, product_id)
    return {"message": "Item removed from order"}


@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(vendor_id: Optional[int] = None):
    if vendor_id:
        return transaction_service.get_transactions_by_vendor(vendor_id)
    return transaction_service.get_all_transactions()



@router.get("/health")
async def health_check():
    # 心跳检测
    return {"status": "healthy", "message": "E-Commerce Platform API is running"}