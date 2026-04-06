# 分层架构迁移指南

## 📋 新旧架构对比

### 旧架构 (单文件)
```
backend/
└── app.py (1,200+ 行)
    ├── 模型定义
    ├── 数据库连接
    ├── 业务逻辑
    ├── 路由定义
    └── 混乱的职责
```

### 新架构 (分层)
```
backend/
├── main.py                  # 主应用 (简洁)
├── models/                  # 数据模型
├── routes/                  # API 接口
├── services/               # 业务逻辑
└── dao/                    # 数据访问
```

---

## 🔄 迁移步骤

### Step 1: 更新导入

**旧代码:**
```python
from fastapi import FastAPI
from models import ProductResponse

app = FastAPI()
```

**新代码:**
```python
from fastapi import FastAPI
from routes import router

app = FastAPI()
app.include_router(router)
```

### Step 2: 调用 API

**旧方式:** 直接数据库操作
```python
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()
```

**新方式:** 通过服务层
```python
product_service = ProductService(db_config)
products = product_service.get_all_products()
```

### Step 3: 添加新功能

只需要三个步骤:

1. **在 Service 层添加业务逻辑**
   ```python
   # services/product_service.py
   def get_discounted_products(self, discount_percent: float):
       products = self.get_all_products()
       return [p for p in products if p['discount'] > discount_percent]
   ```

2. **在 Routes 层添加端点**
   ```python
   # routes/__init__.py
   @router.get("/products/discounted")
   async def get_discounted_products(discount: float):
       return product_service.get_discounted_products(discount)
   ```

3. **完成!** 无需修改 DAO 或模型

---

## 📁 文件说明

### Models 层文件

| 文件 | 功能 |
|-----|-----|
| `models/__init__.py` | 导出所有模型 |
| `models/vendor.py` | 供应商数据模型 |
| `models/product.py` | 产品数据模型 |
| `models/customer.py` | 客户数据模型 |
| `models/order.py` | 订单数据模型 |
| `models/transaction.py` | 交易数据模型 |

### Routes 层文件

| 文件 | 功能 |
|-----|-----|
| `routes/__init__.py` | 所有 API 端点定义 |

### Services 层文件

| 文件 | 功能 |
|-----|-----|
| `services/__init__.py` | 导出所有服务 |
| `services/vendor_service.py` | 供应商业务逻辑 |
| `services/product_service.py` | 产品业务逻辑 |
| `services/customer_service.py` | 客户业务逻辑 |
| `services/order_service.py` | 订单业务逻辑 |
| `services/transaction_service.py` | 交易业务逻辑 |

### DAO 层文件

| 文件 | 功能 |
|-----|-----|
| `dao/__init__.py` | 基类和导出 |
| `dao/vendor_dao.py` | 供应商数据访问 |
| `dao/product_dao.py` | 产品数据访问 |
| `dao/customer_dao.py` | 客户数据访问 |
| `dao/order_dao.py` | 订单数据访问 |
| `dao/transaction_dao.py` | 交易数据访问 |

---

## 🧪 如何在新架构中测试

### 测试 DAO 层

```python
# test_dao.py
from dao.product_dao import ProductDAO
from dao import DatabaseConfig

def test_get_product_by_id():
    config = DatabaseConfig()
    dao = ProductDAO(config)
    
    product = dao.get_product_by_id(1)
    assert product is not None
    assert product['product_id'] == 1
```

### 测试 Service 层

```python
# test_service.py
from services.product_service import ProductService
from dao import DatabaseConfig
from unittest.mock import Mock, patch

def test_create_product():
    config = DatabaseConfig()
    service = ProductService(config)
    
    # Mock DAO
    service.product_dao.create_product = Mock(return_value=(1, 1))
    
    result = service.create_product(1, "Test", 99.99, 10)
    service.product_dao.create_product.assert_called_once()
```

### 测试 Routes 层

```python
# test_routes.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## 🐛 常见错误

### 错误 1: 导入路径错误

❌ **错误:**
```python
from models.product import ProductBase  # 相对路径错误
```

✅ **正确:**
```python
from models import ProductBase  # 通过 __init__.py 导入
```

### 错误 2: 直接操作数据库

❌ **错误:**
```python
# 在 Route 中直接执行 SQL
conn = pymysql.connect(...)
cursor = conn.cursor()
cursor.execute("SELECT * FROM products")
```

✅ **正确:**
```python
# 通过 Service 层操作
return product_service.get_all_products()
```

### 错误 3: 业务逻辑在 Route 中

❌ **错误:**
```python
@router.post("/orders")
async def create_order(order: OrderBase):
    # 不要在这里写业务逻辑!
    if not customer.exists:
        raise HTTPException()
    # ...
```

✅ **正确:**
```python
@router.post("/orders")
async def create_order(order: OrderBase):
    # 让 Service 处理业务逻辑
    return order_service.create_order(order.customer_id, items)
```

---

## 📊 性能对比

### 代码行数

| 组件 | 旧架构 | 新架构 | 说明 |
|-----|--------|--------|------|
| app.py | 2000+ | - | 单个文件太大 |
| main.py | - | 50 | 简洁清晰 |
| routes | - | 250 | 所有端点 |
| services | - | 800 | 业务逻辑 |
| dao | - | 400 | 数据访问 |
| models | - | 150 | 数据模型 |
| **总计** | 2000+ | 1650 | 减少 17% |

### 维护性

| 方面 | 旧架构 | 新架构 |
|-----|--------|--------|
| 查找功能 | 困难 | 简单 |
| 添加新端点 | 修改大文件 | 新增小文件 |
| 单元测试 | 难 | 容易 |
| 代码复用 | 低 | 高 |
| 调试 | 困难 | 简单 |

---

## 🎯 最佳实践

### 1. 严格遵循分层原则

```
Routes → Services → DAO → Database

✓ 只能向下调用
✗ 不能跨层调用
✗ 不能向上调用
```

### 2. Service 层应该是薄的

```python
# ✓ 好的 Service
def create_product(self, vendor_id, name, price):
    self.vendor_dao.validate_vendor(vendor_id)  # 验证
    return self.product_dao.create(...)  # 创建
```

```python
# ✗ 不好的 Service (太厚了)
def create_product(self, ...):
    # 100 行业务逻辑
    # 50 行计算
    # 30 行验证
    # ...
```

### 3. DAO 应该是通用的

```python
# ✓ 好的 DAO (通用)
def execute_query(self, sql, params):
    # 可以用于任何查询

def execute_update(self, sql, params):
    # 可以用于任何更新
```

### 4. 使用类型提示

```python
# ✓ 使用类型提示
def create_product(self, vendor_id: int, name: str, price: float) -> Dict[str, Any]:
    ...

# ✗ 不使用类型提示
def create_product(self, vendor_id, name, price):
    ...
```

---

## 🚀 后续优化

### 1. 添加缓存层

```
Routes → Cache → Services → DAO → Database
```

### 2. 添加日志层

```python
# 在每一层记录日志
logger.info(f"获取产品 ID: {product_id}")
```

### 3. 添加监控

```python
# 监控 API 调用时间
@router.get("/products")
async def get_products():
    start_time = time.time()
    result = product_service.get_all_products()
    duration = time.time() - start_time
    metrics.record_duration("get_products", duration)
    return result
```

### 4. 添加认证层

```python
# 在 Routes 中验证用户身份
@router.post("/orders")
async def create_order(order: OrderBase, current_user: User = Depends(get_current_user)):
    ...
```

---

## 📚 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 数据验证](https://docs.pydantic.dev/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [MVC/MVP/MVVM 架构模式](https://en.wikipedia.org/wiki/Architectural_pattern)

---

## ✅ 总结

新的分层架构提供了:

- 🎯 **清晰的代码组织**
- 🔧 **易于维护和扩展**
- 🧪 **高度可测试**
- 🔄 **代码复用**
- 📊 **性能优化**
- 🚀 **可扩展基础**

现在你可以:
- 独立开发每一层
- 并行测试每个模块
- 快速添加新功能
- 轻松修复 Bug
- 安心地重构代码

**祝你在新架构下开发顺利! 🎉**

