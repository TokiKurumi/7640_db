# Layered Architecture Design Document

## 📐 Architecture Overview

The refactored E-Commerce Platform adopts a standard **four-layer architecture**:

```
┌─────────────────────────────────────────────────────────┐
│              API Interface Layer (Routes/Controllers)    │
│  - FastAPI route endpoints                               │
│  - HTTP request handling                                 │
│  - Request validation and error handling                 │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP Call
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Business Logic Layer (Services)             │
│  - VendorService: Vendor business logic                  │
│  - ProductService: Product business logic                │
│  - CustomerService: Customer business logic              │
│  - OrderService: Order business logic                    │
│  - TransactionService: Transaction business logic        │
└──────────────────────┬──────────────────────────────────┘
                       │ Business Call
                       ↓
┌─────────────────────────────────────────────────────────┐
│           Data Access Layer (DAO - Data Access Object)   │
│  - BaseDAO: Base DAO class                               │
│  - VendorDAO: Vendor data access                         │
│  - ProductDAO: Product data access                       │
│  - CustomerDAO: Customer data access                     │
│  - OrderDAO: Order data access                           │
│  - TransactionDAO: Transaction data access               │
└──────────────────────┬──────────────────────────────────┘
                       │ SQL Query
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   Database Layer (MySQL)                 │
│  - vendors table                                         │
│  - products table                                        │
│  - customers table                                       │
│  - orders table                                          │
│  - order_items table                                     │
│  - transactions table                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 Project File Structure

```
backend/
├── main.py                  # FastAPI main application entry point
├── models/                  # Data Model Layer
│   ├── __init__.py         # Export models
│   ├── vendor.py           # Vendor model
│   ├── product.py          # Product model
│   ├── customer.py         # Customer model
│   ├── order.py            # Order model
│   └── transaction.py      # Transaction model
│
├── routes/                  # API Route Layer (Interface Layer)
│   └── __init__.py         # All route definitions
│
├── services/               # Business Logic Layer
│   ├── __init__.py        # Export services
│   ├── vendor_service.py   # Vendor service
│   ├── product_service.py  # Product service
│   ├── customer_service.py # Customer service
│   ├── order_service.py    # Order service
│   └── transaction_service.py  # Transaction service
│
└── dao/                     # Data Access Layer
    ├── __init__.py         # DAO base class and export
    ├── vendor_dao.py       # Vendor DAO
    ├── product_dao.py      # Product DAO
    ├── customer_dao.py     # Customer DAO
    ├── order_dao.py        # Order DAO
    └── transaction_dao.py  # Transaction DAO
```

---

## 🔄 Data Flow

### Complete Flow for Creating an Order

```
1. User Request (HTTP POST /api/orders)
   ↓
2. Routes receive the request (routes/__init__.py)
   - Validate request data
   - Call OrderService.create_order()
   ↓
3. Services handle business logic (services/order_service.py)
   - Verify customer existence
   - Verify product and stock
   - Calculate order total
   - Call DAO for data operations
   ↓
4. DAO executes database operations (dao/order_dao.py, dao/product_dao.py, etc.)
   - Create order record
   - Add order items
   - Deduct stock
   - Create transaction record
   ↓
5. Database (MySQL)
   - Insert data
   - Commit transaction
   ↓
6. Return Response (HTTP 200)
   - Return the newly created order data
```

---

## 📝 Responsibilities of Each Layer

### 1️⃣ Models Layer

**Responsibility**: Define data structures and validation rules.

**File**: `models/*.py`

**Features**:
- Uses the Pydantic library
- Defines request and response models
- Automatically validates data types and constraints

**Example**:
```python
# models/product.py
class ProductBase(BaseModel):
    product_name: str
    listed_price: float = Field(gt=0)  # Price must be > 0
    stock_quantity: int = Field(ge=0)  # Stock must be >= 0
```

---

### 2️⃣ Routes Layer (API Interface)

**Responsibility**: Handle HTTP requests and responses.

**File**: `routes/__init__.py`

**Features**:
- Defines REST endpoints
- Validates request format
- Calls the Service layer
- Handles exceptions and returns appropriate HTTP status codes

**Example**:
```python
# routes/__init__.py
@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderBase):
    """Create a new order"""
    try:
        return order_service.create_order(order.customer_id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

### 3️⃣ Services Layer (Business Logic)

**Responsibility**: Handle complex business logic and rules.

**File**: `services/*.py`

**Features**:
- Contains all business rules
- Data validation
- Transaction handling
- Calls multiple DAOs
- Returns processed data

**Example**:
```python
# services/order_service.py
class OrderService:
    def create_order(self, customer_id: int, items: List):
        # 1. Verify customer existence
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # 2. Verify product and stock
        for item in items:
            product = self.product_dao.get_product_by_id(item['product_id'])
            if product['stock_quantity'] < item['quantity']:
                raise ValueError("Insufficient stock")
        
        # 3. Create order
        order_id = self.order_dao.create_order(...)
        
        # 4. Deduct stock
        for item in items:
            self.product_dao.update_stock(item['product_id'], -item['quantity'])
```

---

### 4️⃣ DAO Layer (Data Access)

**Responsibility**: Interact with the database.

**File**: `dao/*.py`

**Features**:
- Encapsulates all SQL operations
- Provides common database methods
- Connection management
- Only responsible for database operations, no business logic

**Example**:
```python
# dao/product_dao.py
class ProductDAO(BaseDAO):
    def update_stock(self, product_id: int, quantity_change: int):
        """Update stock"""
        query = "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s"
        return self.execute_update(query, (quantity_change, product_id))
```

---

## ✅ Advantages of Layered Architecture

### 1. **Separation of Concerns**
- Each layer has clear responsibilities.
- Easy to maintain and modify.

### 2. **Code Reusability**
- The DAO layer can be used by multiple Services.
- The Service layer can be called by multiple routes.

### 3. **Easy to Test**
- Each layer can be tested independently.
- Mock objects can be used for unit testing.

### 4. **Scalability**
- Adding new features only requires adding logic to the Service layer.
- Modifying the database only requires modifying the DAO layer.

### 5. **Code Quality**
- Avoids duplicate code.
- Single Responsibility Principle.
- Easy for code review.

---

## 🔐 Data Flow Security

Validation is performed at each layer:

```
Request Data
  ↓
① Models Layer: Type and format validation
  - Automatically done by Pydantic
  ↓
② Routes Layer: HTTP level validation
  - Check if the request is correctly formatted
  ↓
③ Services Layer: Business logic validation
  - Check if business rules are met
  - Check if data is valid
  ↓
④ DAO Layer: Database operations
  - Use parameterized queries to prevent SQL injection
  ↓
Database
```

---

## 📊 Example: Get Product List

### User Request
```
GET /api/products?vendor_id=1
```

### Processing Flow

**1. Routes Receive Request**
```python
@router.get("/products", response_model=List[ProductResponse])
async def get_products(vendor_id: Optional[int] = None):
    if vendor_id:
        return product_service.get_products_by_vendor(vendor_id)
```

**2. Service Handles Business Logic**
```python
def get_products_by_vendor(self, vendor_id: int):
    # Verify vendor existence
    vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
    if not vendor:
        raise ValueError(f"Vendor ID {vendor_id} not found")
    
    # Get product list
    return self.product_dao.get_products_by_vendor(vendor_id)
```

**3. DAO Executes Database Query**
```python
def get_products_by_vendor(self, vendor_id: int):
    query = """
        SELECT product_id, vendor_id, product_name, listed_price, stock_quantity
        FROM products
        WHERE vendor_id = %s
        ORDER BY product_id
    """
    return self.execute_query(query, (vendor_id,))
```

**4. Return Response**
```json
[
    {
        "product_id": 1,
        "vendor_id": 1,
        "product_name": "Wireless Headphones",
        "listed_price": 299.99,
        "stock_quantity": 50
    }
]
```

---

## 🚀 Running the Application

### How to Start

```bash
# Start using main.py
python backend/main.py

# Or start directly with uvicorn
uvicorn backend.main:app --reload --port 8000
```

### Accessing the API

```
API Docs: http://localhost:8000/docs
Redoc:    http://localhost:8000/redoc
```

---

## 📈 Extension Suggestions

### Adding a New Entity

For example, adding a payment feature:

1. **Create Model** (`models/payment.py`)
2. **Create DAO** (`dao/payment_dao.py`)
3. **Create Service** (`services/payment_service.py`)
4. **Add Route** (`routes/__init__.py`)

### Adding Caching

Add caching in the Service layer:
```python
def get_product_by_id(self, product_id: int):
    cache_key = f"product:{product_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    product = self.product_dao.get_product_by_id(product_id)
    cache.set(cache_key, product)
    return product
```

---

## Summary

This layered architecture provides:
- ✅ Clear code organization
- ✅ Easy maintenance and extension
- ✅ High testability
- ✅ Code reusability
- ✅ Separation of concerns
- ✅ Scalable infrastructure

Each layer can be developed, tested, and deployed independently!