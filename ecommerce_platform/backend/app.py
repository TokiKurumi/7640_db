"""
COMP7640 E-Commerce Platform - Backend API
FastAPI-based REST API server
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pymysql
from pymysql.cursors import DictCursor
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import logging

# ============================================================================
# Configuration
# ============================================================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Change as per your MySQL setup
    'database': 'ecommerce_platform',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Pydantic Models
# ============================================================================
class VendorBase(BaseModel):
    business_name: str
    geographical_presence: Optional[str] = None

class VendorResponse(VendorBase):
    vendor_id: int
    average_rating: float
    created_date: datetime

class ProductBase(BaseModel):
    product_name: str
    listed_price: float
    stock_quantity: int
    tag1: Optional[str] = None
    tag2: Optional[str] = None
    tag3: Optional[str] = None

class ProductResponse(ProductBase):
    product_id: int
    vendor_id: int
    created_date: datetime

class CustomerBase(BaseModel):
    customer_name: str
    contact_number: str
    shipping_address: str

class CustomerResponse(CustomerBase):
    customer_id: int
    created_date: datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(OrderItemBase):
    order_item_id: int
    unit_price: float
    subtotal: float

class OrderBase(BaseModel):
    customer_id: int
    items: List[OrderItemBase]

class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    total_price: float
    status: str
    order_date: datetime
    items: List[OrderItemResponse]

class TransactionResponse(BaseModel):
    transaction_id: int
    order_id: int
    vendor_id: int
    customer_id: int
    product_id: int
    quantity: int
    transaction_amount: float
    transaction_date: datetime
    status: str

# ============================================================================
# Database Connection Helper
# ============================================================================
def get_db_connection():
    """Create and return a database connection"""
    return pymysql.connect(**DB_CONFIG)

def execute_query(query: str, params: tuple = (), fetch_one: bool = False):
    """Execute a database query"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise

def execute_update(query: str, params: tuple = ()):
    """Execute an INSERT/UPDATE/DELETE query"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected_rows = cursor.rowcount
        last_id = cursor.lastrowid
        conn.close()
        return affected_rows, last_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {str(e)}")
        raise

# ============================================================================
# FastAPI App Initialization
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("E-Commerce Platform API Starting...")
    yield
    # Shutdown
    logger.info("E-Commerce Platform API Shutting down...")

app = FastAPI(
    title="COMP7640 E-Commerce Platform API",
    description="RESTful API for e-commerce platform",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# VENDORS ENDPOINTS
# ============================================================================
@app.get("/api/vendors", response_model=List[VendorResponse])
async def get_vendors():
    """Get all vendors"""
    query = "SELECT vendor_id, business_name, average_rating, geographical_presence, created_date FROM vendors ORDER BY vendor_id"
    results = execute_query(query)
    return results

@app.post("/api/vendors", response_model=VendorResponse)
async def create_vendor(vendor: VendorBase):
    """Create a new vendor"""
    query = """
        INSERT INTO vendors (business_name, geographical_presence, average_rating)
        VALUES (%s, %s, 0.0)
    """
    try:
        affected_rows, last_id = execute_update(query, (vendor.business_name, vendor.geographical_presence))
        if affected_rows > 0:
            result = execute_query(
                "SELECT vendor_id, business_name, average_rating, geographical_presence, created_date FROM vendors WHERE vendor_id = %s",
                (last_id,),
                fetch_one=True
            )
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create vendor: {str(e)}")

@app.get("/api/vendors/{vendor_id}", response_model=VendorResponse)
async def get_vendor(vendor_id: int):
    """Get a specific vendor"""
    query = "SELECT vendor_id, business_name, average_rating, geographical_presence, created_date FROM vendors WHERE vendor_id = %s"
    result = execute_query(query, (vendor_id,), fetch_one=True)
    if not result:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return result

# ============================================================================
# PRODUCTS ENDPOINTS
# ============================================================================
@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(vendor_id: Optional[int] = None):
    """Get all products or filter by vendor"""
    if vendor_id:
        query = "SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3, created_date FROM products WHERE vendor_id = %s ORDER BY product_id"
        results = execute_query(query, (vendor_id,))
    else:
        query = "SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3, created_date FROM products ORDER BY product_id"
        results = execute_query(query)
    return results

@app.post("/api/products", response_model=ProductResponse)
async def create_product(product: ProductBase, vendor_id: int):
    """Create a new product for a vendor"""
    query = """
        INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        affected_rows, last_id = execute_update(
            query,
            (vendor_id, product.product_name, product.listed_price, product.stock_quantity,
             product.tag1, product.tag2, product.tag3)
        )
        if affected_rows > 0:
            result = execute_query(
                "SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3, created_date FROM products WHERE product_id = %s",
                (last_id,),
                fetch_one=True
            )
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create product: {str(e)}")

@app.get("/api/products/search")
async def search_products(tag: str = Query(..., min_length=1)):
    """Search products by tag or partial name match"""
    query = """
        SELECT product_id, vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3, created_date
        FROM products
        WHERE product_name LIKE %s OR tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
        ORDER BY product_name
    """
    search_term = f"%{tag}%"
    results = execute_query(query, (search_term, search_term, search_term, search_term))
    return results

# ============================================================================
# CUSTOMERS ENDPOINTS
# ============================================================================
@app.get("/api/customers", response_model=List[CustomerResponse])
async def get_customers():
    """Get all customers"""
    query = "SELECT customer_id, customer_name, contact_number, shipping_address, created_date FROM customers ORDER BY customer_id"
    results = execute_query(query)
    return results

@app.post("/api/customers", response_model=CustomerResponse)
async def create_customer(customer: CustomerBase):
    """Create a new customer"""
    query = """
        INSERT INTO customers (customer_name, contact_number, shipping_address)
        VALUES (%s, %s, %s)
    """
    try:
        affected_rows, last_id = execute_update(query, (customer.customer_name, customer.contact_number, customer.shipping_address))
        if affected_rows > 0:
            result = execute_query(
                "SELECT customer_id, customer_name, contact_number, shipping_address, created_date FROM customers WHERE customer_id = %s",
                (last_id,),
                fetch_one=True
            )
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create customer: {str(e)}")

@app.get("/api/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int):
    """Get a specific customer"""
    query = "SELECT customer_id, customer_name, contact_number, shipping_address, created_date FROM customers WHERE customer_id = %s"
    result = execute_query(query, (customer_id,), fetch_one=True)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result

# ============================================================================
# ORDERS ENDPOINTS
# ============================================================================
@app.get("/api/orders")
async def get_orders(customer_id: Optional[int] = None):
    """Get all orders or filter by customer"""
    if customer_id:
        query = """
            SELECT o.order_id, o.customer_id, o.total_price, o.status, o.order_date
            FROM orders o
            WHERE o.customer_id = %s
            ORDER BY o.order_date DESC
        """
        results = execute_query(query, (customer_id,))
    else:
        query = """
            SELECT order_id, customer_id, total_price, status, order_date
            FROM orders
            ORDER BY order_date DESC
        """
        results = execute_query(query)
    return results

@app.post("/api/orders")
async def create_order(order: OrderBase):
    """Create a new order with items"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Calculate total price
        total_price = 0
        items_data = []
        
        for item in order.items:
            # Get product price and update stock
            product_query = "SELECT listed_price, stock_quantity FROM products WHERE product_id = %s"
            cursor.execute(product_query, (item.product_id,))
            product = cursor.fetchone()
            
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            if product['stock_quantity'] < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
            
            subtotal = product['listed_price'] * item.quantity
            total_price += subtotal
            items_data.append({
                'product_id': item.product_id,
                'quantity': item.quantity,
                'unit_price': product['listed_price'],
                'subtotal': subtotal
            })
        
        # Create order
        order_query = """
            INSERT INTO orders (customer_id, total_price, status)
            VALUES (%s, %s, 'pending')
        """
        cursor.execute(order_query, (order.customer_id, total_price))
        order_id = cursor.lastrowid
        
        # Add order items and update stock
        for item_data in items_data:
            # Insert order item
            item_query = """
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(item_query, (
                order_id,
                item_data['product_id'],
                item_data['quantity'],
                item_data['unit_price'],
                item_data['subtotal']
            ))
            
            # Update product stock
            stock_query = """
                UPDATE products SET stock_quantity = stock_quantity - %s
                WHERE product_id = %s
            """
            cursor.execute(stock_query, (item_data['quantity'], item_data['product_id']))
            
            # Create transaction
            # Get vendor_id for this product
            vendor_query = "SELECT vendor_id FROM products WHERE product_id = %s"
            cursor.execute(vendor_query, (item_data['product_id'],))
            vendor = cursor.fetchone()
            
            transaction_query = """
                INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'completed')
            """
            cursor.execute(transaction_query, (
                order_id,
                vendor['vendor_id'],
                order.customer_id,
                item_data['product_id'],
                item_data['quantity'],
                item_data['subtotal']
            ))
        
        conn.commit()
        
        # Return created order
        return {
            'order_id': order_id,
            'customer_id': order.customer_id,
            'total_price': total_price,
            'status': 'pending',
            'order_date': datetime.now(),
            'items': items_data
        }
        
    except HTTPException as he:
        conn.rollback()
        raise he
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create order: {str(e)}")
    finally:
        conn.close()

@app.get("/api/orders/{order_id}")
async def get_order(order_id: int):
    """Get a specific order with items"""
    # Get order
    order_query = "SELECT order_id, customer_id, total_price, status, order_date FROM orders WHERE order_id = %s"
    order = execute_query(order_query, (order_id,), fetch_one=True)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get order items
    items_query = "SELECT order_item_id, product_id, quantity, unit_price, subtotal FROM order_items WHERE order_id = %s"
    items = execute_query(items_query, (order_id,))
    
    return {**order, 'items': items}

@app.put("/api/orders/{order_id}")
async def update_order(order_id: int, status: str):
    """Update order status"""
    query = "UPDATE orders SET status = %s WHERE order_id = %s"
    try:
        affected_rows, _ = execute_update(query, (status, order_id))
        if affected_rows == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update order: {str(e)}")

@app.delete("/api/orders/{order_id}")
async def cancel_order(order_id: int):
    """Cancel an order (before shipping)"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check order status
        status_query = "SELECT status FROM orders WHERE order_id = %s"
        cursor.execute(status_query, (order_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if result['status'] in ['shipped', 'delivered']:
            raise HTTPException(status_code=400, detail="Cannot cancel shipped or delivered orders")
        
        # Restore stock for all items
        items_query = "SELECT product_id, quantity FROM order_items WHERE order_id = %s"
        cursor.execute(items_query, (order_id,))
        items = cursor.fetchall()
        
        for item in items:
            stock_query = """
                UPDATE products SET stock_quantity = stock_quantity + %s
                WHERE product_id = %s
            """
            cursor.execute(stock_query, (item['quantity'], item['product_id']))
        
        # Update order status
        cancel_query = "UPDATE orders SET status = 'cancelled' WHERE order_id = %s"
        cursor.execute(cancel_query, (order_id,))
        
        conn.commit()
        return {"message": "Order cancelled successfully"}
        
    except HTTPException as he:
        conn.rollback()
        raise he
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to cancel order: {str(e)}")
    finally:
        conn.close()

@app.delete("/api/orders/{order_id}/items/{product_id}")
async def remove_order_item(order_id: int, product_id: int):
    """Remove a specific product from an order"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check order status
        status_query = "SELECT status FROM orders WHERE order_id = %s"
        cursor.execute(status_query, (order_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if result['status'] in ['shipped', 'delivered']:
            raise HTTPException(status_code=400, detail="Cannot modify shipped or delivered orders")
        
        # Get item quantity to restore stock
        item_query = "SELECT quantity, subtotal FROM order_items WHERE order_id = %s AND product_id = %s"
        cursor.execute(item_query, (order_id, product_id))
        item = cursor.fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Order item not found")
        
        # Restore stock
        stock_query = """
            UPDATE products SET stock_quantity = stock_quantity + %s
            WHERE product_id = %s
        """
        cursor.execute(stock_query, (item['quantity'], product_id))
        
        # Remove order item
        delete_query = "DELETE FROM order_items WHERE order_id = %s AND product_id = %s"
        cursor.execute(delete_query, (order_id, product_id))
        
        # Update order total price
        total_query = "SELECT COALESCE(SUM(subtotal), 0) as total FROM order_items WHERE order_id = %s"
        cursor.execute(total_query, (order_id,))
        new_total = cursor.fetchone()['total']
        
        update_total_query = "UPDATE orders SET total_price = %s WHERE order_id = %s"
        cursor.execute(update_total_query, (new_total, order_id))
        
        conn.commit()
        return {"message": "Order item removed successfully"}
        
    except HTTPException as he:
        conn.rollback()
        raise he
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to remove order item: {str(e)}")
    finally:
        conn.close()

# ============================================================================
# TRANSACTIONS ENDPOINTS
# ============================================================================
@app.get("/api/transactions")
async def get_transactions(vendor_id: Optional[int] = None):
    """Get all transactions or filter by vendor"""
    if vendor_id:
        query = """
            SELECT transaction_id, order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, transaction_date, status
            FROM transactions
            WHERE vendor_id = %s
            ORDER BY transaction_date DESC
        """
        results = execute_query(query, (vendor_id,))
    else:
        query = """
            SELECT transaction_id, order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, transaction_date, status
            FROM transactions
            ORDER BY transaction_date DESC
        """
        results = execute_query(query)
    return results

# ============================================================================
# Health Check
# ============================================================================
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "E-Commerce Platform API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
