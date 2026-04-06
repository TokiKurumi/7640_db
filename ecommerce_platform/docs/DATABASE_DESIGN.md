# E-Commerce Platform Database Design

## Entity-Relationship (ER) Diagram Description

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    E-COMMERCE PLATFORM DATABASE                          │
└─────────────────────────────────────────────────────────────────────────┘

                              VENDORS (1)
                         ─────────────────────
                        │ vendor_id (PK)       │
                        │ business_name (U)    │
                        │ average_rating       │
                        │ geographical_presence│
                         ─────────────────────
                                  │
                    ┌─────────────┼─────────────┐
                    │ (1:N)       │             │
                    │             │             │
              PRODUCTS (N)   TRANSACTIONS (N)  │
          ─────────────────                    │
         │ product_id (PK)  │                  │
         │ vendor_id (FK)   │◄─────────────────┼──────────────────┐
         │ product_name     │                  │                  │
         │ listed_price     │                  │                  │
         │ stock_quantity   │                  │                  │
         │ tag1, tag2, tag3 │                  │                  │
          ─────────────────                    │                  │
                    │                          │                  │
        ┌───────────┼──────────────────┐       │                  │
        │ (N:M)     │                  │       │                  │
        │           │                  │       │                  │
    ORDERS (N)   ORDER_ITEMS (N)       │       │                  │
   ─────────────   ──────────────      │       │                  │
  │ order_id (PK)││ order_item_id(PK)│       │                  │
  │customer_id(FK)││ order_id (FK)    │───┐   │                  │
  │ order_date    ││ product_id (FK)  │──┼───┼──────────────────┤
  │ total_price   ││ quantity         │  │   │                  │
  │ status        ││ unit_price       │  │   │                  │
   ─────────────   ││ subtotal         │  │   │                  │
        │           ──────────────     │  │   │                  │
        │ (1:N)              │         │  │   │                  │
        │                    └──────────┼──┼───┼─(N:1)─────────────
        │ (1:N)                        │  │   │
        │                              │  │   │    TRANSACTIONS (N)
  CUSTOMERS (N)                        │  │   │   ─────────────────
  ──────────────                       │  │   │  │transaction_id(PK)
 │customer_id(PK)                      │  │   │  │order_id (FK)
 │customer_name  │◄─────────────────────  │   │  │vendor_id (FK)
 │contact_number │                       │   │  │customer_id (FK)
 │shipping_address                       │   │  │product_id (FK)
  ──────────────                         │   │  │quantity
                                         │   │  │transaction_amount
                                         │   │  │transaction_date
                                         │   │  │status
                                         │   │   ─────────────────
                                         │   │
                                         └───┘
```

## Detailed Table Specifications

### 1. VENDORS Table
**Purpose**: Store vendor/seller information
**Attributes**:
- `vendor_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `business_name` (VARCHAR 255, UNIQUE, NOT NULL)
- `average_rating` (DECIMAL 3,2, CHECK between 0-5, DEFAULT 0.0)
- `geographical_presence` (VARCHAR 500)
- `created_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

**Indexes**:
- PRIMARY KEY: vendor_id
- UNIQUE: business_name
- INDEX: average_rating

### 2. PRODUCTS Table
**Purpose**: Store product information from vendors
**Attributes**:
- `product_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `vendor_id` (INT, FOREIGN KEY → vendors.vendor_id)
- `product_name` (VARCHAR 255, NOT NULL)
- `listed_price` (DECIMAL 10,2, NOT NULL, CHECK > 0)
- `stock_quantity` (INT, DEFAULT 0, CHECK ≥ 0)
- `tag1` (VARCHAR 100) - Optional tag
- `tag2` (VARCHAR 100) - Optional tag
- `tag3` (VARCHAR 100) - Optional tag
- `created_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

**Indexes**:
- PRIMARY KEY: product_id
- FOREIGN KEY: vendor_id
- INDEX: vendor_id (for product filtering)
- INDEX: product_name
- INDEX: tag1, tag2, tag3 (for search functionality)

**Relationships**:
- (N:1) with VENDORS
- (N:M) with ORDERS via ORDER_ITEMS
- (1:N) with TRANSACTIONS

### 3. CUSTOMERS Table
**Purpose**: Store customer/buyer information
**Attributes**:
- `customer_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `customer_name` (VARCHAR 255, NOT NULL)
- `contact_number` (VARCHAR 20, UNIQUE, NOT NULL)
- `shipping_address` (VARCHAR 500, NOT NULL)
- `created_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

**Indexes**:
- PRIMARY KEY: customer_id
- UNIQUE: contact_number
- INDEX: customer_name

**Relationships**:
- (1:N) with ORDERS
- (1:N) with TRANSACTIONS

### 4. ORDERS Table
**Purpose**: Store order records
**Attributes**:
- `order_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `customer_id` (INT, FOREIGN KEY → customers.customer_id)
- `order_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `total_price` (DECIMAL 12,2, NOT NULL, CHECK ≥ 0)
- `status` (ENUM: 'pending', 'processing', 'shipped', 'delivered', 'cancelled')
- `created_date` (TIMESTAMP)
- `updated_date` (TIMESTAMP, AUTO UPDATE)

**Indexes**:
- PRIMARY KEY: order_id
- FOREIGN KEY: customer_id
- INDEX: customer_id, order_date
- INDEX: status

**Relationships**:
- (N:1) with CUSTOMERS
- (1:N) with ORDER_ITEMS
- (1:N) with TRANSACTIONS

### 5. ORDER_ITEMS Table (Join Table)
**Purpose**: Link multiple products to each order (N:M relationship)
**Attributes**:
- `order_item_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `order_id` (INT, FOREIGN KEY → orders.order_id)
- `product_id` (INT, FOREIGN KEY → products.product_id)
- `quantity` (INT, NOT NULL, CHECK > 0)
- `unit_price` (DECIMAL 10,2, NOT NULL, CHECK > 0)
- `subtotal` (DECIMAL 12,2, NOT NULL, CHECK > 0)

**Indexes**:
- PRIMARY KEY: order_item_id
- FOREIGN KEY: order_id
- FOREIGN KEY: product_id
- INDEX: order_id (for retrieving items per order)

**Relationships**:
- (N:1) with ORDERS
- (N:1) with PRODUCTS

### 6. TRANSACTIONS Table
**Purpose**: Track individual transactions between customers and vendors
**Attributes**:
- `transaction_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `order_id` (INT, FOREIGN KEY → orders.order_id)
- `vendor_id` (INT, FOREIGN KEY → vendors.vendor_id)
- `customer_id` (INT, FOREIGN KEY → customers.customer_id)
- `product_id` (INT, FOREIGN KEY → products.product_id)
- `quantity` (INT, NOT NULL, CHECK > 0)
- `transaction_amount` (DECIMAL 12,2, NOT NULL, CHECK > 0)
- `transaction_date` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `status` (ENUM: 'completed', 'pending', 'failed')

**Indexes**:
- PRIMARY KEY: transaction_id
- FOREIGN KEY: order_id, vendor_id, customer_id, product_id
- INDEX: vendor_id, transaction_date (for vendor reporting)
- INDEX: transaction_date

**Relationships**:
- (N:1) with ORDERS
- (N:1) with VENDORS
- (N:1) with CUSTOMERS
- (N:1) with PRODUCTS

## Relationship Summary

| Relationship | Type | Description |
|---|---|---|
| VENDORS ↔ PRODUCTS | 1:N | One vendor has many products |
| CUSTOMERS ↔ ORDERS | 1:N | One customer places many orders |
| ORDERS ↔ ORDER_ITEMS | 1:N | One order has many items |
| PRODUCTS ↔ ORDER_ITEMS | 1:N | One product can be in many orders |
| ORDERS ↔ TRANSACTIONS | 1:N | One order generates many transactions (one per vendor) |
| VENDORS ↔ TRANSACTIONS | 1:N | One vendor receives many transactions |
| CUSTOMERS ↔ TRANSACTIONS | 1:N | One customer makes many transactions |

## Key Design Considerations

### 1. **Normalization**
- **First Normal Form (1NF)**: All tables have atomic values, no repeating groups
- **Second Normal Form (2NF)**: All non-key attributes depend on the entire primary key
- **Third Normal Form (3NF)**: No transitive dependencies between non-key attributes
- **De-normalization Decision**: Tags (tag1, tag2, tag3) kept in PRODUCTS table for simplicity vs. creating separate TAGS table

### 2. **Data Integrity**
- Primary key constraints ensure unique identification
- Foreign key constraints maintain referential integrity
- CHECK constraints validate numeric ranges (ratings 0-5, prices > 0)
- UNIQUE constraint on contact_number and business_name

### 3. **Query Performance**
- Strategic indexes on frequently searched columns
- Composite indexes for common filter combinations
- Foreign key columns are indexed for JOIN operations

### 4. **Multi-Vendor Support**
- ORDER_ITEMS tracks each product with vendor association
- TRANSACTIONS table creates separate transaction record per vendor in each order
- Enables accurate vendor settlement and revenue tracking

### 5. **Stock Management**
- Real-time stock updates via quantity checks
- Prevents overselling with stock_quantity validation
- Order cancellation restores stock

## Sample ER Diagram (ASCII)

```
┌─────────────┐
│   VENDORS   │
├─────────────┤
│ vendor_id*  │────────────┐
│ business_name           │
│ avg_rating              │ (1:N)
│ geo_presence            │
└─────────────┘            │
                           │
                    ┌──────────────┐
                    │  PRODUCTS    │
                    ├──────────────┤
                    │ product_id*  │───────────┐
                    │ vendor_id*FK │           │
                    │ product_name │           │ (N:M via
                    │ price        │           │  ORDER_ITEMS)
                    │ stock        │           │
                    │ tags (3)     │           │
                    └──────────────┘           │
                                              │
┌──────────────┐                              │
│  CUSTOMERS   │                              │
├──────────────┤                              │
│ customer_id* │────────────┐                 │
│ name         │            │                 │
│ contact      │    (1:N)    │                 │
│ address      │            │                 │
└──────────────┘            │                 │
                    ┌────────────────┐        │
                    │    ORDERS      │        │
                    ├────────────────┤        │
                    │ order_id*      │────────┼────┐
                    │ customer_id*FK │        │    │
                    │ order_date     │        │    │
                    │ total_price    │        │    │
                    │ status         │        │    │
                    └────────────────┘        │    │
                             │               │    │
                    (1:N)     │               │    │
                             │               │    │
                    ┌──────────────────┐     │    │
                    │ ORDER_ITEMS (JT) │     │    │
                    ├──────────────────┤     │    │
                    │ order_item_id*   │     │    │
                    │ order_id*FK      │─────┘    │
                    │ product_id*FK    │─────────┘
                    │ quantity         │
                    │ unit_price       │
                    └──────────────────┘

TRANSACTIONS:
┌──────────────────────────┐
│ transaction_id* (PK)     │
│ order_id (FK) ───────────┤─→ ORDERS
│ vendor_id (FK) ──────────┤─→ VENDORS
│ customer_id (FK) ────────┤─→ CUSTOMERS
│ product_id (FK) ─────────┤─→ PRODUCTS
│ quantity                 │
│ amount                   │
│ date & status            │
└──────────────────────────┘
```

## Database Size Estimation

With sample data:
- VENDORS: ~5 rows
- PRODUCTS: ~20 rows
- CUSTOMERS: ~7 rows
- ORDERS: ~7 rows
- ORDER_ITEMS: ~25 rows (multiple items per order)
- TRANSACTIONS: ~30 rows (one per vendor-item pair)

**Estimated size**: < 1 MB for sample data, scalable to millions of records.

