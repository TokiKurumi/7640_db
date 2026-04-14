/*
 Navicat MySQL Data Transfer

 Source Server         : 7640_db
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : ecommerce_platform

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 13/04/2026 01:43:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
CREATE DATABASE IF NOT EXISTS ecommerce_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 选择使用这个数据库（关键！解决 1046 错误）
USE ecommerce_platform;
-- ----------------------------
-- Table structure for customers
-- ----------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers`  (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipping_address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`) USING BTREE,
  UNIQUE INDEX `contact_number`(`contact_number`) USING BTREE,
  INDEX `idx_customer_name`(`customer_name`) USING BTREE,
  INDEX `idx_contact_number`(`contact_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of customers
-- ----------------------------
INSERT INTO `customers` VALUES (1, 'John Smith', '98765432', '123 Main Street, Hong Kong', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (2, 'Jane Doe', '97654321', '456 Park Avenue, Kowloon', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (3, 'Michael Wong', '96543210', '789 Ocean Drive, Shatin', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (4, 'Sarah Johnson', '95432109', '321 Harbor View, Central', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (5, 'Peter Chen', '94321098', '654 Mountain Road, New Territories', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (6, 'Alice Lee', '93210987', '987 Valley Lane, Quarry Bay', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (7, 'Robert Wilson', '92109876', '246 Hill Street, Sheung Wan', '2026-04-07 11:26:03');
INSERT INTO `customers` VALUES (8, 'kurumi', '3333', 'TKSK', '2026-04-07 22:55:02');
INSERT INTO `customers` VALUES (9, 'tokisaki', '333333333', 'here my heart', '2026-04-08 00:25:31');
INSERT INTO `customers` VALUES (10, 'ac', '123456', '123 hkbu', '2026-04-11 11:52:12');
INSERT INTO `customers` VALUES (11, 'zwt', '1234', 'hkbuntt', '2026-04-11 12:02:06');

-- ----------------------------
-- Table structure for order_items
-- ----------------------------
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items`  (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10, 2) NOT NULL,
  `subtotal` decimal(12, 2) NOT NULL,
  PRIMARY KEY (`order_item_id`) USING BTREE,
  INDEX `idx_order_id`(`order_id`) USING BTREE,
  INDEX `idx_product_id`(`product_id`) USING BTREE,
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 46 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order_items
-- ----------------------------
INSERT INTO `order_items` VALUES (1, 1, 1, 1, 299.99, 299.99);
INSERT INTO `order_items` VALUES (2, 1, 3, 1, 49.99, 49.99);
INSERT INTO `order_items` VALUES (3, 2, 5, 2, 99.99, 199.98);
INSERT INTO `order_items` VALUES (4, 2, 7, 1, 149.99, 149.99);
INSERT INTO `order_items` VALUES (5, 2, 11, 2, 79.99, 159.98);
INSERT INTO `order_items` VALUES (6, 3, 13, 1, 499.99, 499.99);
INSERT INTO `order_items` VALUES (7, 4, 2, 1, 199.99, 199.99);
INSERT INTO `order_items` VALUES (8, 4, 15, 1, 249.99, 249.99);
INSERT INTO `order_items` VALUES (9, 4, 16, 2, 149.99, 299.98);
INSERT INTO `order_items` VALUES (10, 5, 10, 1, 99.99, 99.99);
INSERT INTO `order_items` VALUES (11, 5, 12, 1, 149.99, 149.99);
INSERT INTO `order_items` VALUES (20, 6, 18, 2, 129.99, 259.98);
INSERT INTO `order_items` VALUES (21, 6, 19, 1, 109.99, 109.99);
INSERT INTO `order_items` VALUES (22, 6, 20, 2, 119.99, 239.98);
INSERT INTO `order_items` VALUES (23, 6, 21, 1, 139.99, 139.99);
INSERT INTO `order_items` VALUES (24, 7, 6, 1, 199.99, 199.99);
INSERT INTO `order_items` VALUES (25, 7, 8, 1, 349.99, 349.99);
INSERT INTO `order_items` VALUES (26, 7, 9, 1, 59.99, 59.99);
INSERT INTO `order_items` VALUES (27, 8, 3, 2, 129.99, 259.98);
INSERT INTO `order_items` VALUES (28, 8, 4, 3, 79.99, 239.97);
INSERT INTO `order_items` VALUES (29, 9, 5, 2, 99.99, 199.98);
INSERT INTO `order_items` VALUES (30, 9, 4, 33, 79.99, 2639.67);
INSERT INTO `order_items` VALUES (31, 10, 10, 1, 79.99, 79.99);
INSERT INTO `order_items` VALUES (32, 10, 3, 2, 129.99, 259.98);
INSERT INTO `order_items` VALUES (33, 10, 6, 3, 199.99, 599.97);
INSERT INTO `order_items` VALUES (34, 11, 3, 2, 129.99, 259.98);
INSERT INTO `order_items` VALUES (35, 11, 5, 3, 99.99, 299.97);
INSERT INTO `order_items` VALUES (36, 12, 4, 2, 79.99, 159.98);
INSERT INTO `order_items` VALUES (37, 12, 4, 3, 79.99, 239.97);
INSERT INTO `order_items` VALUES (38, 12, 4, 2, 79.99, 159.98);
INSERT INTO `order_items` VALUES (39, 13, 4, 2, 79.99, 159.98);
INSERT INTO `order_items` VALUES (40, 13, 2, 2, 49.99, 99.98);
INSERT INTO `order_items` VALUES (41, 14, 22, 3, 3.00, 9.00);
INSERT INTO `order_items` VALUES (42, 15, 2, 3, 49.99, 149.97);
INSERT INTO `order_items` VALUES (43, 15, 5, 2, 99.99, 199.98);
INSERT INTO `order_items` VALUES (44, 16, 6, 2, 199.99, 399.98);
INSERT INTO `order_items` VALUES (45, 16, 9, 3, 89.99, 269.97);
INSERT INTO `order_items` VALUES (46, 17, 4, 3, 79.99, 239.97);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `order_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total_price` decimal(12, 2) NOT NULL,
  `status` enum('pending','processing','shipped','delivered','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `idx_customer_id`(`customer_id`) USING BTREE,
  INDEX `idx_order_date`(`order_date`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_order_customer_date`(`customer_id`, `order_date`) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, 1, '2026-04-07 11:26:03', 349.98, 'delivered', '2026-04-07 11:26:03', '2026-04-07 11:26:03');
INSERT INTO `orders` VALUES (2, 2, '2026-04-07 11:26:03', 599.97, 'processing', '2026-04-07 11:26:03', '2026-04-07 11:26:03');
INSERT INTO `orders` VALUES (3, 3, '2026-04-07 11:26:03', 479.98, 'cancelled', '2026-04-07 11:26:03', '2026-04-07 23:50:59');
INSERT INTO `orders` VALUES (4, 4, '2026-04-07 11:26:03', 699.97, 'shipped', '2026-04-07 11:26:03', '2026-04-07 11:26:03');
INSERT INTO `orders` VALUES (5, 5, '2026-04-07 11:26:03', 249.99, 'pending', '2026-04-07 11:26:03', '2026-04-07 11:26:03');
INSERT INTO `orders` VALUES (6, 6, '2026-04-07 11:26:03', 899.98, 'processing', '2026-04-07 11:26:03', '2026-04-07 11:26:03');
INSERT INTO `orders` VALUES (7, 7, '2026-04-07 11:26:03', 579.96, 'delivered', '2026-04-07 11:26:03', '2026-04-07 11:26:03');
INSERT INTO `orders` VALUES (8, 7, '2026-04-08 00:15:48', 499.95, 'cancelled', '2026-04-08 00:15:48', '2026-04-08 00:25:46');
INSERT INTO `orders` VALUES (9, 2, '2026-04-08 00:45:08', 2839.65, 'pending', '2026-04-08 00:45:08', '2026-04-08 00:45:08');
INSERT INTO `orders` VALUES (10, 8, '2026-04-08 00:47:56', 939.94, 'cancelled', '2026-04-08 00:47:56', '2026-04-08 01:03:48');
INSERT INTO `orders` VALUES (11, 3, '2026-04-08 01:04:35', 559.95, 'pending', '2026-04-08 01:04:35', '2026-04-08 01:04:35');
INSERT INTO `orders` VALUES (12, 3, '2026-04-08 01:06:37', 559.93, 'pending', '2026-04-08 01:06:37', '2026-04-08 01:06:37');
INSERT INTO `orders` VALUES (13, 9, '2026-04-08 01:25:33', 259.96, 'cancelled', '2026-04-08 01:25:33', '2026-04-08 01:25:53');
INSERT INTO `orders` VALUES (14, 6, '2026-04-08 01:27:09', 9.00, 'cancelled', '2026-04-08 01:27:09', '2026-04-13 01:21:17');
INSERT INTO `orders` VALUES (15, 1, '2026-04-11 11:52:54', 349.95, 'cancelled', '2026-04-11 11:52:54', '2026-04-11 11:53:14');
INSERT INTO `orders` VALUES (16, 4, '2026-04-11 12:02:51', 669.95, 'cancelled', '2026-04-11 12:02:51', '2026-04-11 12:03:14');
INSERT INTO `orders` VALUES (17, 9, '2026-04-13 01:21:37', 239.97, 'pending', '2026-04-13 01:21:37', '2026-04-13 01:21:37');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `vendor_id` int NOT NULL,
  `product_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `listed_price` decimal(10, 2) NOT NULL,
  `stock_quantity` int NULL DEFAULT 0,
  `tag1` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `tag2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `tag3` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`) USING BTREE,
  INDEX `idx_vendor_id`(`vendor_id`) USING BTREE,
  INDEX `idx_product_name`(`product_name`) USING BTREE,
  INDEX `idx_tag1`(`tag1`) USING BTREE,
  INDEX `idx_tag2`(`tag2`) USING BTREE,
  INDEX `idx_tag3`(`tag3`) USING BTREE,
  INDEX `idx_vendor_product`(`vendor_id`, `product_name`) USING BTREE,
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`vendor_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (1, 1, 'Wireless Bluetooth Headphones', 299.99, 50, 'electronics', 'audio', 'wireless', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (2, 1, 'USB-C Charging Cable', 49.99, 200, 'electronics', 'accessories', 'charging', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (3, 1, 'Laptop Stand Aluminum', 129.99, 83, 'electronics', 'accessories', 'stand', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (4, 1, 'USB Hub 7-Port', 79.99, 72, 'electronics', 'connectivity', 'hub', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (5, 2, 'Classic Cotton T-Shirt', 99.99, 115, 'clothing', 'casual', 'cotton', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (6, 2, 'Blue Denim Jeans', 199.99, 80, 'clothing', 'casual', 'denim', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (7, 2, 'Leather Belt Brown', 149.99, 60, 'fashion', 'accessories', 'leather', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (8, 2, 'Casual Sneakers White', 349.99, 40, 'footwear', 'casual', 'sneakers', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (9, 3, 'Organic Green Tea', 89.99, 150, 'beverages', 'organic', 'tea', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (10, 3, 'Organic Almond Butter', 79.99, 100, 'food', 'organic', 'nuts', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (11, 3, 'Eco-Friendly Bamboo Utensils', 59.99, 200, 'eco-friendly', 'kitchen', 'bamboo', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (12, 3, 'Organic Honey Raw', 99.99, 80, 'food', 'organic', 'honey', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (13, 4, 'Smart Watch Pro', 499.99, 31, 'electronics', 'wearable', 'smartwatch', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (14, 4, '4K Webcam', 199.99, 45, 'electronics', 'camera', '4k', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (15, 4, 'Mechanical Keyboard RGB', 249.99, 60, 'electronics', 'gaming', 'keyboard', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (16, 4, 'Gaming Mouse Wireless', 149.99, 90, 'electronics', 'gaming', 'mouse', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (17, 5, 'The Art of Python Programming', 129.99, 100, 'books', 'programming', 'python', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (18, 5, 'Database Design Fundamentals', 109.99, 80, 'books', 'databases', 'technical', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (19, 5, 'Web Development with FastAPI', 119.99, 70, 'books', 'web-development', 'api', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (20, 5, 'Data Science Handbook', 139.99, 60, 'books', 'data-science', 'technical', '2026-04-07 11:26:03');
INSERT INTO `products` VALUES (21, 5, 'Comic Book', 33.33, 900, 'books', 'gaming', 'comic', '2026-04-07 11:33:29');
INSERT INTO `products` VALUES (22, 12, 'ASDF', 3.00, 3, 'TAG1', 'TAG2', 'TAG3', '2026-04-08 00:24:43');
INSERT INTO `products` VALUES (23, 2, 'hkbu', 3.00, 3, 'school', 'books', 'students', '2026-04-11 11:51:36');
INSERT INTO `products` VALUES (24, 11, 'BOOKSS', 3.00, 3, 'books', 'student', 'school', '2026-04-11 12:01:16');

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions`  (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `vendor_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `transaction_amount` decimal(12, 2) NOT NULL,
  `transaction_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('completed','pending','failed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'completed',
  PRIMARY KEY (`transaction_id`) USING BTREE,
  INDEX `product_id`(`product_id`) USING BTREE,
  INDEX `idx_order_id`(`order_id`) USING BTREE,
  INDEX `idx_vendor_id`(`vendor_id`) USING BTREE,
  INDEX `idx_customer_id`(`customer_id`) USING BTREE,
  INDEX `idx_transaction_date`(`transaction_date`) USING BTREE,
  INDEX `idx_transaction_vendor_date`(`vendor_id`, `transaction_date`) USING BTREE,
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`vendor_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_4` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of transactions
-- ----------------------------
INSERT INTO `transactions` VALUES (1, 1, 1, 1, 1, 1, 299.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (2, 1, 1, 1, 3, 1, 49.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (3, 2, 2, 2, 5, 2, 199.98, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (4, 2, 2, 2, 7, 1, 149.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (5, 2, 3, 2, 11, 2, 159.98, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (6, 3, 4, 3, 13, 1, 499.99, '2026-04-07 11:34:18', 'pending');
INSERT INTO `transactions` VALUES (7, 4, 2, 4, 2, 1, 199.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (8, 4, 4, 4, 15, 1, 249.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (9, 4, 4, 4, 16, 2, 299.98, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (10, 5, 3, 5, 10, 1, 99.99, '2026-04-07 11:34:18', 'pending');
INSERT INTO `transactions` VALUES (11, 5, 4, 5, 12, 1, 149.99, '2026-04-07 11:34:18', 'pending');
INSERT INTO `transactions` VALUES (12, 6, 5, 6, 18, 2, 259.98, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (13, 6, 5, 6, 19, 1, 109.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (14, 6, 5, 6, 20, 2, 239.98, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (15, 6, 5, 6, 21, 1, 139.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (16, 7, 2, 7, 6, 1, 199.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (17, 7, 2, 7, 8, 1, 349.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (18, 7, 3, 7, 9, 1, 59.99, '2026-04-07 11:34:18', 'completed');
INSERT INTO `transactions` VALUES (19, 8, 1, 7, 3, 2, 259.98, '2026-04-08 00:15:48', 'completed');
INSERT INTO `transactions` VALUES (20, 8, 1, 7, 4, 3, 239.97, '2026-04-08 00:15:48', 'completed');
INSERT INTO `transactions` VALUES (21, 9, 2, 2, 5, 2, 199.98, '2026-04-08 00:45:08', 'completed');
INSERT INTO `transactions` VALUES (22, 9, 1, 2, 4, 33, 2639.67, '2026-04-08 00:45:08', 'completed');
INSERT INTO `transactions` VALUES (23, 10, 3, 8, 10, 1, 79.99, '2026-04-08 00:47:56', 'completed');
INSERT INTO `transactions` VALUES (24, 10, 1, 8, 3, 2, 259.98, '2026-04-08 00:47:56', 'completed');
INSERT INTO `transactions` VALUES (25, 10, 2, 8, 6, 3, 599.97, '2026-04-08 00:47:56', 'completed');
INSERT INTO `transactions` VALUES (26, 11, 1, 3, 3, 2, 259.98, '2026-04-08 01:04:35', 'completed');
INSERT INTO `transactions` VALUES (27, 11, 2, 3, 5, 3, 299.97, '2026-04-08 01:04:35', 'completed');
INSERT INTO `transactions` VALUES (28, 12, 1, 3, 4, 2, 159.98, '2026-04-08 01:06:37', 'completed');
INSERT INTO `transactions` VALUES (29, 12, 1, 3, 4, 3, 239.97, '2026-04-08 01:06:37', 'completed');
INSERT INTO `transactions` VALUES (30, 12, 1, 3, 4, 2, 159.98, '2026-04-08 01:06:37', 'completed');
INSERT INTO `transactions` VALUES (31, 13, 1, 9, 4, 2, 159.98, '2026-04-08 01:25:33', 'completed');
INSERT INTO `transactions` VALUES (32, 13, 1, 9, 2, 2, 99.98, '2026-04-08 01:25:33', 'completed');
INSERT INTO `transactions` VALUES (33, 14, 12, 6, 22, 3, 9.00, '2026-04-08 01:27:09', 'completed');
INSERT INTO `transactions` VALUES (34, 15, 1, 1, 2, 3, 149.97, '2026-04-11 11:52:54', 'completed');
INSERT INTO `transactions` VALUES (35, 15, 2, 1, 5, 2, 199.98, '2026-04-11 11:52:54', 'completed');
INSERT INTO `transactions` VALUES (36, 16, 2, 4, 6, 2, 399.98, '2026-04-11 12:02:51', 'completed');
INSERT INTO `transactions` VALUES (37, 16, 3, 4, 9, 3, 269.97, '2026-04-11 12:02:51', 'completed');
INSERT INTO `transactions` VALUES (38, 17, 1, 9, 4, 3, 239.97, '2026-04-13 01:21:37', 'completed');

-- ----------------------------
-- Table structure for vendors
-- ----------------------------
DROP TABLE IF EXISTS `vendors`;
CREATE TABLE `vendors`  (
  `vendor_id` int NOT NULL AUTO_INCREMENT,
  `business_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `average_rating` decimal(3, 2) NULL DEFAULT 0.00,
  `geographical_presence` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`vendor_id`) USING BTREE,
  UNIQUE INDEX `business_name`(`business_name`) USING BTREE,
  INDEX `idx_business_name`(`business_name`) USING BTREE,
  INDEX `idx_rating`(`average_rating`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of vendors
-- ----------------------------
INSERT INTO `vendors` VALUES (1, 'TechHub Store', 4.50, 'Hong Kong, Singapore', '2026-04-07 11:26:03');
INSERT INTO `vendors` VALUES (2, 'Fashion Forward', 4.20, 'Hong Kong, China', '2026-04-07 11:26:03');
INSERT INTO `vendors` VALUES (3, 'Green Organic Market', 4.80, 'Hong Kong', '2026-04-07 11:26:03');
INSERT INTO `vendors` VALUES (4, 'Electronics Plus', 4.30, 'Hong Kong, Taiwan', '2026-04-07 11:26:03');
INSERT INTO `vendors` VALUES (5, 'Book Universe', 4.60, 'Hong Kong, Singapore, Malaysia', '2026-04-07 11:26:03');
INSERT INTO `vendors` VALUES (11, 'tksk', 0.00, 'HK SK', '2026-04-07 23:47:06');
INSERT INTO `vendors` VALUES (12, 'TEST1', 0.00, 'LOC2', '2026-04-08 00:24:13');
INSERT INTO `vendors` VALUES (13, 'HKBU', 0.00, 'hongKONG', '2026-04-11 11:50:41');
INSERT INTO `vendors` VALUES (14, 'HKBUU', 0.00, 'HK', '2026-04-11 12:00:34');

SET FOREIGN_KEY_CHECKS = 1;
