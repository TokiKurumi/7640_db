-- ============================================================================
-- COMP7640 E-Commerce Platform - Sample Data
-- ============================================================================

USE ecommerce_platform;

-- ============================================================================
-- Insert Sample Vendors
-- ============================================================================
INSERT INTO vendors (business_name, average_rating, geographical_presence) VALUES
('TechHub Store', 4.5, 'Hong Kong, Singapore'),
('Fashion Forward', 4.2, 'Hong Kong, China'),
('Green Organic Market', 4.8, 'Hong Kong'),
('Electronics Plus', 4.3, 'Hong Kong, Taiwan'),
('Book Universe', 4.6, 'Hong Kong, Singapore, Malaysia');

-- ============================================================================
-- Insert Sample Products
-- ============================================================================
-- TechHub Store (vendor_id = 1)
INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3) VALUES
(1, 'Wireless Bluetooth Headphones', 299.99, 50, 'electronics', 'audio', 'wireless'),
(1, 'USB-C Charging Cable', 49.99, 200, 'electronics', 'accessories', 'charging'),
(1, 'Laptop Stand Aluminum', 129.99, 75, 'electronics', 'accessories', 'stand'),
(1, 'USB Hub 7-Port', 79.99, 100, 'electronics', 'connectivity', 'hub');

-- Fashion Forward (vendor_id = 2)
INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3) VALUES
(2, 'Classic Cotton T-Shirt', 99.99, 120, 'clothing', 'casual', 'cotton'),
(2, 'Blue Denim Jeans', 199.99, 80, 'clothing', 'casual', 'denim'),
(2, 'Leather Belt Brown', 149.99, 60, 'fashion', 'accessories', 'leather'),
(2, 'Casual Sneakers White', 349.99, 40, 'footwear', 'casual', 'sneakers');

-- Green Organic Market (vendor_id = 3)
INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3) VALUES
(3, 'Organic Green Tea', 89.99, 150, 'beverages', 'organic', 'tea'),
(3, 'Organic Almond Butter', 79.99, 100, 'food', 'organic', 'nuts'),
(3, 'Eco-Friendly Bamboo Utensils', 59.99, 200, 'eco-friendly', 'kitchen', 'bamboo'),
(3, 'Organic Honey Raw', 99.99, 80, 'food', 'organic', 'honey');

-- Electronics Plus (vendor_id = 4)
INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3) VALUES
(4, 'Smart Watch Pro', 499.99, 30, 'electronics', 'wearable', 'smartwatch'),
(4, '4K Webcam', 199.99, 45, 'electronics', 'camera', '4k'),
(4, 'Mechanical Keyboard RGB', 249.99, 60, 'electronics', 'gaming', 'keyboard'),
(4, 'Gaming Mouse Wireless', 149.99, 90, 'electronics', 'gaming', 'mouse');

-- Book Universe (vendor_id = 5)
INSERT INTO products (vendor_id, product_name, listed_price, stock_quantity, tag1, tag2, tag3) VALUES
(5, 'The Art of Python Programming', 129.99, 100, 'books', 'programming', 'python'),
(5, 'Database Design Fundamentals', 109.99, 80, 'books', 'databases', 'technical'),
(5, 'Web Development with FastAPI', 119.99, 70, 'books', 'web-development', 'api'),
(5, 'Data Science Handbook', 139.99, 60, 'books', 'data-science', 'technical');
(5, 'Comic Book', 33.33, 900, 'books', 'gaming', 'comic');
-- ============================================================================
-- Insert Sample Customers
-- ============================================================================
INSERT INTO customers (customer_name, contact_number, shipping_address) VALUES
('John Smith', '98765432', '123 Main Street, Hong Kong'),
('Jane Doe', '97654321', '456 Park Avenue, Kowloon'),
('Michael Wong', '96543210', '789 Ocean Drive, Shatin'),
('Sarah Johnson', '95432109', '321 Harbor View, Central'),
('Peter Chen', '94321098', '654 Mountain Road, New Territories'),
('Alice Lee', '93210987', '987 Valley Lane, Quarry Bay'),
('Robert Wilson', '92109876', '246 Hill Street, Sheung Wan');

-- ============================================================================
-- Insert Sample Orders
-- ============================================================================
INSERT INTO orders (customer_id, total_price, status) VALUES
(1, 349.98, 'delivered'),
(2, 599.97, 'processing'),
(3, 479.98, 'pending'),
(4, 699.97, 'shipped'),
(5, 249.99, 'pending'),
(6, 899.98, 'processing'),
(7, 579.96, 'delivered');

-- ============================================================================
-- Insert Sample Order Items
-- ============================================================================
-- Order 1: John Smith - 2 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 299.99, 299.99),
(1, 3, 1, 49.99, 49.99);

-- Order 2: Jane Doe - 3 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(2, 5, 2, 99.99, 199.98),
(2, 7, 1, 149.99, 149.99),
(2, 11, 2, 79.99, 159.98);

-- Order 3: Michael Wong - 1 item
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(3, 13, 1, 499.99, 499.99);

-- Order 4: Sarah Johnson - 2 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(4, 2, 1, 199.99, 199.99),
(4, 15, 1, 249.99, 249.99),
(4, 16, 2, 149.99, 299.98);

-- Order 5: Peter Chen - 2 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(5, 10, 1, 99.99, 99.99),
(5, 12, 1, 149.99, 149.99);

-- Order 6: Alice Lee - 3 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(6, 18, 2, 129.99, 259.98),
(6, 19, 1, 109.99, 109.99),
(6, 20, 2, 119.99, 239.98),
(6, 21, 1, 139.99, 139.99);

-- Order 7: Robert Wilson - 2 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(7, 6, 1, 199.99, 199.99),
(7, 8, 1, 349.99, 349.99),
(7, 9, 1, 59.99, 59.99);

-- ============================================================================
-- Insert Sample Transactions
-- ============================================================================
-- From Order 1
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(1, 1, 1, 1, 1, 299.99, 'completed'),
(1, 1, 1, 3, 1, 49.99, 'completed');

-- From Order 2
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(2, 2, 2, 5, 2, 199.98, 'completed'),
(2, 2, 2, 7, 1, 149.99, 'completed'),
(2, 3, 2, 11, 2, 159.98, 'completed');

-- From Order 3
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(3, 4, 3, 13, 1, 499.99, 'pending');

-- From Order 4
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(4, 2, 4, 2, 1, 199.99, 'completed'),
(4, 4, 4, 15, 1, 249.99, 'completed'),
(4, 4, 4, 16, 2, 299.98, 'completed');

-- From Order 5
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(5, 3, 5, 10, 1, 99.99, 'pending'),
(5, 4, 5, 12, 1, 149.99, 'pending');

-- From Order 6
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(6, 5, 6, 18, 2, 259.98, 'completed'),
(6, 5, 6, 19, 1, 109.99, 'completed'),
(6, 5, 6, 20, 2, 239.98, 'completed'),
(6, 5, 6, 21, 1, 139.99, 'completed');

-- From Order 7
INSERT INTO transactions (order_id, vendor_id, customer_id, product_id, quantity, transaction_amount, status) VALUES
(7, 2, 7, 6, 1, 199.99, 'completed'),
(7, 2, 7, 8, 1, 349.99, 'completed'),
(7, 3, 7, 9, 1, 59.99, 'completed');

-- ============================================================================
-- Verify Data Insertion
-- ============================================================================
SELECT 'Vendors' as table_name, COUNT(*) as count FROM vendors
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items
UNION ALL
SELECT 'Transactions', COUNT(*) FROM transactions;
