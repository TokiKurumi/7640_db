# 分层架构设计文档

## 📐 架构概述

重构后的E-Commerce Platform采用标准的**四层分层架构**：

```
┌─────────────────────────────────────────────────────────┐
│              API 接口层 (Routes/Controllers)             │
│  - FastAPI 路由端点                                      │
│  - HTTP 请求处理                                         │
│  - 请求验证和错误处理                                    │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP 调用
                       ↓
┌─────────────────────────────────────────────────────────┐
│              业务逻辑层 (Services)                       │
│  - VendorService: 供应商业务逻辑                        │
│  - ProductService: 产品业务逻辑                         │
│  - CustomerService: 客户业务逻辑                        │
│  - OrderService: 订单业务逻辑                           │
│  - TransactionService: 交易业务逻辑                     │
└──────────────────────┬──────────────────────────────────┘
                       │ 业务调用
                       ↓
┌─────────────────────────────────────────────────────────┐
│           数据访问层 (DAO - Data Access Object)         │
│  - BaseDAO: 基础 DAO 类                                 │
│  - VendorDAO: 供应商数据访问                            │
│  - ProductDAO: 产品数据访问                             │
│  - CustomerDAO: 客户数据访问                            │
│  - OrderDAO: 订单数据访问                               │
│  - TransactionDAO: 交易数据访问                         │
└──────────────────────┬──────────────────────────────────┘
                       │ SQL 查询
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   数据库层 (MySQL)                       │
│  - vendors 表                                            │
│  - products 表                                           │
│  - customers 表                                          │
│  - orders 表                                             │
│  - order_items 表                                        │
│  - transactions 表                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 项目文件结构

```
backend/
├── main.py                  # FastAPI 主应用入口
├── models/                  # 数据模型层
│   ├── __init__.py         # 模型导出
│   ├── vendor.py           # 供应商模型
│   ├── product.py          # 产品模型
│   ├── customer.py         # 客户模型
│   ├── order.py            # 订单模型
│   └── transaction.py      # 交易模型
│
├── routes/                  # API 路由层 (接口层)
│   └── __init__.py         # 所有路由定义
│
├── services/               # 业务逻辑层
│   ├── __init__.py        # 服务导出
│   ├── vendor_service.py   # 供应商服务
│   ├── product_service.py  # 产品服务
│   ├── customer_service.py # 客户服务
│   ├── order_service.py    # 订单服务
│   └── transaction_service.py  # 交易服务
│
└── dao/                     # 数据访问层
    ├── __init__.py         # DAO 基类和导出
    ├── vendor_dao.py       # 供应商 DAO
    ├── product_dao.py      # 产品 DAO
    ├── customer_dao.py     # 客户 DAO
    ├── order_dao.py        # 订单 DAO
    └── transaction_dao.py  # 交易 DAO
```

---

## 🔄 数据流向

### 创建订单的完整流程

```
1. 用户请求 (HTTP POST /api/orders)
   ↓
2. Routes 接收请求 (routes/__init__.py)
   - 验证请求数据
   - 调用 OrderService.create_order()
   ↓
3. Services 处理业务逻辑 (services/order_service.py)
   - 验证客户是否存在
   - 验证产品和库存
   - 计算订单总额
   - 调用 DAO 进行数据操作
   ↓
4. DAO 执行数据库操作 (dao/order_dao.py, dao/product_dao.py, etc.)
   - 创建订单记录
   - 添加订单项
   - 扣减库存
   - 创建交易记录
   ↓
5. 数据库 (MySQL)
   - 插入数据
   - 提交事务
   ↓
6. 返回响应 (HTTP 200)
   - 返回新创建的订单数据
```

---

## 📝 各层的职责

### 1️⃣ Models 层 (数据模型)

**职责**: 定义数据结构和验证规则

**文件**: `models/*.py`

**特点**:
- 使用 Pydantic 库
- 定义请求和响应模型
- 自动验证数据类型和约束

**示例**:
```python
# models/product.py
class ProductBase(BaseModel):
    product_name: str
    listed_price: float = Field(gt=0)  # 价格必须 > 0
    stock_quantity: int = Field(ge=0)  # 库存必须 >= 0
```

---

### 2️⃣ Routes 层 (API接口)

**职责**: 处理 HTTP 请求和响应

**文件**: `routes/__init__.py`

**特点**:
- 定义 REST 端点
- 验证请求格式
- 调用 Service 层
- 处理异常并返回适当的 HTTP 状态码

**示例**:
```python
# routes/__init__.py
@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderBase):
    """创建新订单"""
    try:
        return order_service.create_order(order.customer_id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

### 3️⃣ Services 层 (业务逻辑)

**职责**: 处理复杂的业务逻辑和规则

**文件**: `services/*.py`

**特点**:
- 包含所有业务规则
- 数据验证
- 事务处理
- 调用多个 DAO
- 返回处理后的数据

**示例**:
```python
# services/order_service.py
class OrderService:
    def create_order(self, customer_id: int, items: List):
        # 1. 验证客户存在
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError("客户不存在")
        
        # 2. 验证产品和库存
        for item in items:
            product = self.product_dao.get_product_by_id(item['product_id'])
            if product['stock_quantity'] < item['quantity']:
                raise ValueError("库存不足")
        
        # 3. 创建订单
        order_id = self.order_dao.create_order(...)
        
        # 4. 扣减库存
        for item in items:
            self.product_dao.update_stock(item['product_id'], -item['quantity'])
```

---

### 4️⃣ DAO 层 (数据访问)

**职责**: 与数据库交互

**文件**: `dao/*.py`

**特点**:
- 封装所有 SQL 操作
- 提供通用的数据库方法
- 连接管理
- 只负责数据库操作，不包含业务逻辑

**示例**:
```python
# dao/product_dao.py
class ProductDAO(BaseDAO):
    def update_stock(self, product_id: int, quantity_change: int):
        """更新库存"""
        query = "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s"
        return self.execute_update(query, (quantity_change, product_id))
```

---

## ✅ 分层架构的优势

### 1. **关注点分离 (Separation of Concerns)**
- 每一层都有明确的职责
- 易于维护和修改

### 2. **代码复用**
- DAO 层可被多个 Service 使用
- Service 层可被多个路由调用

### 3. **易于测试**
- 可以独立测试每一层
- 可以使用 Mock 对象进行单元测试

### 4. **可扩展性**
- 添加新功能时只需在 Service 层添加逻辑
- 修改数据库只需修改 DAO 层

### 5. **代码质量**
- 避免重复代码
- 单一职责原则
- 易于代码审查

---

## 🔐 数据流安全

每一层都进行验证:

```
请求数据
  ↓
① Models 层: 类型和格式验证
  - 由 Pydantic 自动进行
  ↓
② Routes 层: HTTP 级别验证
  - 检查请求是否正确格式
  ↓
③ Services 层: 业务逻辑验证
  - 检查业务规则是否满足
  - 检查数据是否有效
  ↓
④ DAO 层: 数据库操作
  - 使用参数化查询防止 SQL 注入
  ↓
数据库
```

---

## 📊 例子：获取产品列表

### 用户请求
```
GET /api/products?vendor_id=1
```

### 处理流程

**1. Routes 接收请求**
```python
@router.get("/products", response_model=List[ProductResponse])
async def get_products(vendor_id: Optional[int] = None):
    if vendor_id:
        return product_service.get_products_by_vendor(vendor_id)
```

**2. Service 处理业务逻辑**
```python
def get_products_by_vendor(self, vendor_id: int):
    # 验证供应商是否存在
    vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
    if not vendor:
        raise ValueError(f"供应商ID {vendor_id} 不存在")
    
    # 获取产品列表
    return self.product_dao.get_products_by_vendor(vendor_id)
```

**3. DAO 执行数据库查询**
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

**4. 返回响应**
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

## 🚀 运行应用

### 启动方式

```bash
# 使用 main.py 启动
python backend/main.py

# 或使用 uvicorn 直接启动
uvicorn backend.main:app --reload --port 8000
```

### 访问 API

```
API 文档: http://localhost:8000/docs
Redoc:    http://localhost:8000/redoc
```

---

## 📈 扩展建议

### 添加新的实体

例如添加支付功能:

1. **创建模型** (`models/payment.py`)
2. **创建 DAO** (`dao/payment_dao.py`)
3. **创建 Service** (`services/payment_service.py`)
4. **添加路由** (`routes/__init__.py`)

### 添加缓存

在 Service 层添加缓存:
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

## 总结

这种分层架构提供了:
- ✅ 清晰的代码组织
- ✅ 易于维护和扩展
- ✅ 高度可测试性
- ✅ 代码复用
- ✅ 关注点分离
- ✅ 可扩展的基础设施

每一层都可以独立开发、测试和部署！

