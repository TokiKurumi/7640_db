# COMP7640 E-Commerce Platform - Testing Guide

## Overview
This guide provides comprehensive testing procedures to verify all functionalities of the e-commerce platform.

## Prerequisites
- Backend running at `http://localhost:8000`
- Frontend GUI running
- Sample database loaded
- MySQL connection active

## 1. Backend API Testing

### Using Swagger UI Documentation
1. Open browser and go to `http://localhost:8000/docs`
2. You'll see interactive API documentation
3. Click on any endpoint to expand it
4. Click "Try it out" to test

### Using cURL (Command Line)

#### Health Check
```bash
curl http://localhost:8000/api/health
Expected: {"status": "healthy", "message": "E-Commerce Platform API is running"}
```

#### Get All Vendors
```bash
curl http://localhost:8000/api/vendors
Expected: JSON array of vendors
```

#### Create New Vendor
```bash
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Store",
    "geographical_presence": "Hong Kong"
  }'
Expected: New vendor object with ID
```

#### Search Products by Tag
```bash
curl "http://localhost:8000/api/products/search?tag=electronics"
Expected: Products containing "electronics" in name or tags
```

## 2. Frontend GUI Testing

### Tab 1: Vendors

**Test Case 1.1: View All Vendors**
- [ ] Open Vendors tab
- [ ] Verify list shows all 5 sample vendors
- [ ] Check ratings display correctly (e.g., 4.5)
- [ ] Verify geographical presence visible

**Test Case 1.2: Create New Vendor**
- [ ] Enter business name: "New Tech Store"
- [ ] Enter location: "Singapore"
- [ ] Click "Create Vendor"
- [ ] Verify success message appears
- [ ] Check vendor appears in list

**Test Case 1.3: Duplicate Vendor Name**
- [ ] Try to create vendor with existing name
- [ ] Verify error message appears

### Tab 2: Products

**Test Case 2.1: View All Products**
- [ ] Open Products tab
- [ ] Verify list shows all ~20 sample products
- [ ] Check vendor names, prices, stock levels
- [ ] Verify tags display correctly

**Test Case 2.2: Search by Tag**
- [ ] Enter search tag: "electronics"
- [ ] Click "Search"
- [ ] Verify only electronics products appear
- [ ] Try search: "clothing"
- [ ] Verify clothing products appear
- [ ] Try search: "nonexistent"
- [ ] Verify no results message

**Test Case 2.3: Show All Products**
- [ ] After searching, click "Show All"
- [ ] Verify full product list returns

**Test Case 2.4: Create New Product**
- [ ] Select vendor from dropdown
- [ ] Enter product name: "Test Product"
- [ ] Enter price: "99.99"
- [ ] Enter stock: "50"
- [ ] Enter tags: "test", "sample", "demo"
- [ ] Click "Create Product"
- [ ] Verify success message
- [ ] Product appears in list

**Test Case 2.5: Invalid Product Data**
- [ ] Leave name empty, try create → Error
- [ ] Enter price as "abc" → Error
- [ ] Enter stock as "1.5" → Error

### Tab 3: Customers

**Test Case 3.1: View All Customers**
- [ ] Open Customers tab
- [ ] Verify list shows all 7 sample customers
- [ ] Check names, contact numbers, addresses

**Test Case 3.2: Create New Customer**
- [ ] Enter name: "John Doe"
- [ ] Enter phone: "98765432"
- [ ] Enter address: "123 Test Street"
- [ ] Click "Create Customer"
- [ ] Verify success message
- [ ] Customer appears in list

**Test Case 3.3: Duplicate Phone Number**
- [ ] Try to create customer with existing phone
- [ ] Verify error message

**Test Case 3.4: Missing Required Fields**
- [ ] Try create with empty name → Error
- [ ] Try create with empty phone → Error
- [ ] Try create with empty address → Error

### Tab 4: Orders

**Test Case 4.1: View All Orders**
- [ ] Open Orders tab
- [ ] Verify list shows all 7 sample orders
- [ ] Check customer names, dates, totals, status

**Test Case 4.2: Create Simple Order**
- [ ] Select customer: "John Smith"
- [ ] Select product: "Wireless Bluetooth Headphones"
- [ ] Set quantity: 1
- [ ] Click "Add Item"
- [ ] Verify item appears in order items list
- [ ] Click "Create Order"
- [ ] Verify success with Order ID
- [ ] Check order appears in list with "pending" status

**Test Case 4.3: Create Multi-Item Order**
- [ ] Select customer: "Jane Doe"
- [ ] Add item 1: "Classic Cotton T-Shirt" qty 2
- [ ] Add item 2: "Blue Denim Jeans" qty 1
- [ ] Click "Create Order"
- [ ] Verify success
- [ ] Check order total calculated correctly

**Test Case 4.4: Duplicate Item in Order**
- [ ] Try to add same product twice
- [ ] Verify error message

**Test Case 4.5: View Order Details**
- [ ] Double-click on an order OR select and click "View Details"
- [ ] Verify details window shows:
  - Order ID
  - Customer ID
  - Total price
  - Status
  - Order date
  - All items with quantities and prices

**Test Case 4.6: Modify Pending Order**
- [ ] Open order details for a pending order
- [ ] Select an item
- [ ] Click "Remove Selected Item"
- [ ] Verify item removed
- [ ] Check total price updated

**Test Case 4.7: Cancel Order**
- [ ] Select a pending order
- [ ] Click "Cancel Selected Order"
- [ ] Confirm cancellation
- [ ] Verify status changes to "cancelled"

**Test Case 4.8: Cannot Modify Shipped Order**
- [ ] Try to cancel/modify a shipped order
- [ ] Verify error message appears

### Tab 5: Transactions

**Test Case 5.1: View All Transactions**
- [ ] Open Transactions tab
- [ ] Verify list shows all transactions
- [ ] Check columns: ID, Order, Vendor, Customer, Product, Qty, Amount, Date, Status

**Test Case 5.2: Filter by Vendor**
- [ ] Select a vendor from dropdown
- [ ] Click "Filter"
- [ ] Verify only that vendor's transactions shown
- [ ] Try different vendors

**Test Case 5.3: Show All Transactions**
- [ ] After filtering, click "Show All"
- [ ] Verify full transaction list returns

## 3. Database Testing

### Using MySQL Command Line

**Test 3.1: Verify Tables Exist**
```sql
USE ecommerce_platform;
SHOW TABLES;
```
Expected: 6 tables (vendors, products, customers, orders, order_items, transactions)

**Test 3.2: Check Sample Data**
```sql
SELECT COUNT(*) FROM vendors;     -- Should be 5 or more
SELECT COUNT(*) FROM products;    -- Should be 20 or more
SELECT COUNT(*) FROM customers;   -- Should be 7 or more
SELECT COUNT(*) FROM orders;      -- Should be 7 or more
SELECT COUNT(*) FROM transactions; -- Should be 30 or more
```

**Test 3.3: Verify Stock Updated After Order**
```sql
SELECT product_id, product_name, stock_quantity FROM products WHERE product_id = 1;
-- Create order with this product
-- Check stock_quantity reduced
```

**Test 3.4: Check Referential Integrity**
```sql
-- Try to insert order with non-existent customer (should fail)
INSERT INTO orders (customer_id, total_price) VALUES (999, 100);
```

## 4. Integration Testing

### Order Workflow (End-to-End)

**Test 4.1: Complete Order Flow**

1. **Create Customer**
   - [ ] Add new customer via GUI
   - [ ] Verify in database

2. **Browse Products**
   - [ ] Search for specific category
   - [ ] Note product ID and price

3. **Create Order**
   - [ ] Create order with new customer
   - [ ] Add 2-3 products
   - [ ] Verify total calculated correctly

4. **Verify Database**
   - [ ] Check order inserted in `orders` table
   - [ ] Check items in `order_items` table
   - [ ] Check transactions created for each vendor
   - [ ] Verify stock quantities reduced

5. **Modify Order**
   - [ ] Remove one item
   - [ ] Verify stock restored
   - [ ] Check total updated

6. **Cancel Order**
   - [ ] Cancel the order
   - [ ] Verify status = "cancelled"
   - [ ] Check all stock restored

**Test 4.2: Multi-Vendor Order**
1. Create order with products from 2+ vendors
2. Verify separate transaction created per vendor
3. Check payment split correctly

## 5. Performance Testing

### Test 5.1: Large Product List
```sql
-- In database, verify indexes exist
SHOW INDEX FROM products;
-- Should see indexes on: product_id, vendor_id, product_name, tags
```

### Test 5.2: Search Performance
- [ ] Search for common tag should be fast (< 1 second)
- [ ] Filter by vendor should be fast
- [ ] Load full product list should be fast

## 6. Error Handling Testing

### Test 6.1: Invalid Inputs
- [ ] Negative price: Should reject
- [ ] Negative quantity: Should reject
- [ ] Duplicate business names: Should reject
- [ ] Duplicate contact numbers: Should reject

### Test 6.2: Business Logic Validation
- [ ] Cannot cancel shipped orders: ✓
- [ ] Cannot modify delivered orders: ✓
- [ ] Cannot remove items from cancelled orders: ✓
- [ ] Insufficient stock: Shows error: ✓

### Test 6.3: API Error Responses
- [ ] Invalid endpoint returns 404
- [ ] Missing required fields returns 400
- [ ] Invalid data type returns 422

## 7. UI/UX Testing

### Test 7.1: Responsiveness
- [ ] All buttons respond to clicks
- [ ] Dropdowns update correctly
- [ ] Treeviews populate and update
- [ ] Status bar updates with messages

### Test 7.2: Data Display
- [ ] Currency formatted correctly ($X.XX)
- [ ] Dates formatted readably
- [ ] All columns visible and aligned
- [ ] Scrollbars appear when needed

### Test 7.3: Error Messages
- [ ] All errors display meaningful messages
- [ ] No silent failures
- [ ] Users understand what went wrong

## Test Data Scenarios

### Scenario 1: Complete Purchase Journey
- Customer browses products
- Searches for specific tag
- Selects 2 products
- Places order
- Modifies order (removes 1 item)
- Completes purchase
- Checks order status

### Scenario 2: Vendor Management
- Add new vendor
- View vendor details
- Add products for vendor
- Create orders containing vendor's products
- View vendor's transactions

### Scenario 3: Inventory Management
- Track initial stock
- Create order (stock decreases)
- Cancel order (stock restores)
- Verify stock history

## Regression Testing

After making changes, verify:
- [ ] All existing functionality still works
- [ ] New features don't break old features
- [ ] Database consistency maintained
- [ ] API responses correct format
- [ ] GUI displays correctly

## Test Results Documentation

Keep track of test results:

| Test Case | Expected Result | Actual Result | Status | Notes |
|---|---|---|---|---|
| 1.1 | 5 vendors display | | ✓ | |
| 1.2 | New vendor created | | ✓ | |
| 2.1 | 20 products display | | ✓ | |
| ... | ... | ... | ... | ... |

## Performance Benchmarks

Expected performance metrics:
- API response time: < 100ms (normal operations)
- Product search: < 500ms (typical)
- Order creation: < 1s (including stock update)
- GUI response: Immediate (< 100ms)

## Troubleshooting Common Issues

### Issue: "Connection refused" at localhost:8000
- [ ] Verify backend is running
- [ ] Check port 8000 not in use
- [ ] Check database connection in backend

### Issue: Database connection error
- [ ] Verify MySQL is running
- [ ] Check DB_CONFIG credentials
- [ ] Verify database exists and tables created

### Issue: No data in GUI
- [ ] Check database has sample data
- [ ] Verify API endpoints respond
- [ ] Check GUI's API calls in console

### Issue: Order won't create
- [ ] Check product has stock
- [ ] Verify customer exists
- [ ] Check all fields populated
- [ ] See console for error details

## Success Criteria

All tests should pass:
- ✅ All required features functional
- ✅ No errors in normal operations
- ✅ Database consistency maintained
- ✅ API returns correct responses
- ✅ GUI displays data correctly
- ✅ Order workflow works end-to-end
- ✅ Stock management working
- ✅ Transaction tracking accurate

## Sign-Off

Testing completed by: _________________
Date: _________________
All tests passed: ☐ Yes ☐ No
Issues found: _________________

