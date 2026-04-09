import pymysql
from datetime import datetime

# Database connection configuration (please modify according to your local MySQL environment)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Your MySQL username
    "password": "123456",  # Your MySQL password
    "database": "ecommerce_platform",
    "charset": "utf8mb4"
}


# Database connection utility function
def get_db_connection():
    """Create and return a MySQL database connection"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


# ====================== 1. Vendor Management Module ======================
def show_all_vendors():
    """Display all vendors on the platform (Requirement 1)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM vendors ORDER BY vendor_id ASC"
            cursor.execute(sql)
            vendors = cursor.fetchall()
            if not vendors:
                print("No vendor data on the platform yet")
                return
            print("\n===== Platform Vendor List =====")
            for vendor in vendors:
                print(f"Vendor ID: {vendor['vendor_id']} | Business Name: {vendor['business_name']}")
                print(f"Average Rating: {vendor['avg_rating']} | Geo Presence: {vendor['geo_presence']}\n")
    except Exception as e:
        print(f"Failed to query vendors: {e}")
    finally:
        conn.close()


def add_new_vendor():
    """Add a new vendor to the platform (Requirement 2)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        print("\n===== Add New Vendor =====")
        business_name = input("Please enter the business name: ").strip()
        geo_presence = input("Please enter the business geo presence: ").strip()
        if not business_name or not geo_presence:
            print("Business name and geo presence are required!")
            return

        with conn.cursor() as cursor:
            sql = "INSERT INTO vendors (business_name, geo_presence) VALUES (%s, %s)"
            cursor.execute(sql, (business_name, geo_presence))
            conn.commit()
            print(f"Vendor [{business_name}] added successfully! Vendor ID: {cursor.lastrowid}")
    except Exception as e:
        conn.rollback()
        print(f"Failed to add new vendor: {e}")
    finally:
        conn.close()


# ====================== 2. Product Catalog Management Module ======================
def browse_vendor_products():
    """Browse all products of a specified vendor (Requirement 1)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        vendor_id = input("\nPlease enter the vendor ID to browse: ").strip()
        if not vendor_id.isdigit():
            print("Please enter a valid numeric ID!")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # First, check if the vendor exists
            cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
            if not cursor.fetchone():
                print("This vendor does not exist!")
                return

            # Query all products of the vendor
            sql = "SELECT * FROM products WHERE vendor_id = %s ORDER BY product_id ASC"
            cursor.execute(sql, (vendor_id,))
            products = cursor.fetchall()
            if not products:
                print("This vendor has no products listed yet")
                return

            print(f"\n===== Vendor ID:{vendor_id} Product List =====")
            for product in products:
                tags = [product['tag1'], product['tag2'], product['tag3']]
                valid_tags = [tag for tag in tags if tag]
                print(f"Product ID: {product['product_id']} | Product Name: {product['product_name']}")
                print(f"Price: {product['price']} | Stock: {product['stock_quantity']}")
                print(f"Product Tags: {','.join(valid_tags) if valid_tags else 'None'}\n")
    except Exception as e:
        print(f"Failed to browse products: {e}")
    finally:
        conn.close()


def add_new_product():
    """Add a new product to the catalog for a vendor (Requirement 2)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        print("\n===== Add New Product =====")
        vendor_id = input("Please enter the vendor ID: ").strip()
        product_name = input("Please enter the product name: ").strip()
        price = input("Please enter the product price: ").strip()
        stock_quantity = input("Please enter the product stock quantity: ").strip()
        tag1 = input("Please enter product tag 1 (optional): ").strip() or None
        tag2 = input("Please enter product tag 2 (optional): ").strip() or None
        tag3 = input("Please enter product tag 3 (optional): ").strip() or None

        # Basic validation
        if not vendor_id.isdigit():
            print("Vendor ID must be a valid number!")
            return
        if not product_name:
            print("Product name is required!")
            return
        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
            if price <= 0 or stock_quantity < 0:
                print("Price must be greater than 0, and stock cannot be negative!")
                return
        except ValueError:
            print("Price and stock must be valid numbers!")
            return

        with conn.cursor() as cursor:
            # Check if the vendor exists
            cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
            if not cursor.fetchone():
                print("The vendor does not exist, cannot add product!")
                return

            # Insert the product
            sql = """
                  INSERT INTO products (vendor_id, product_name, price, stock_quantity, tag1, tag2, tag3)
                  VALUES (%s, %s, %s, %s, %s, %s, %s) \
                  """
            cursor.execute(sql, (vendor_id, product_name, price, stock_quantity, tag1, tag2, tag3))
            conn.commit()
            print(f"Product [{product_name}] added successfully! Product ID: {cursor.lastrowid}")
    except Exception as e:
        conn.rollback()
        print(f"Failed to add new product: {e}")
    finally:
        conn.close()


# ====================== 3. Product Search Module ======================
def search_products_by_tag():
    """Search for products by tag/name (Requirement: match any part of the name or tags)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        keyword = input("\nPlease enter a search keyword (matches product name/tags): ").strip()
        if not keyword:
            print("Search keyword cannot be empty!")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fuzzy match any part of the name or the three tags
            sql = """
                  SELECT p.*, v.business_name \
                  FROM products p \
                           LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
                  WHERE p.product_name LIKE %s
                     OR p.tag1 LIKE %s
                     OR p.tag2 LIKE %s
                     OR p.tag3 LIKE %s
                  ORDER BY p.product_id ASC \
                  """
            fuzzy_keyword = f"%{keyword}%"
            cursor.execute(sql, (fuzzy_keyword, fuzzy_keyword, fuzzy_keyword, fuzzy_keyword))
            products = cursor.fetchall()
            if not products:
                print("No matching products found")
                return

            print(f"\n===== Search Results for '{keyword}' =====")
            for product in products:
                tags = [product['tag1'], product['tag2'], product['tag3']]
                valid_tags = [tag for tag in tags if tag]
                print(f"Product ID: {product['product_id']} | Product Name: {product['product_name']}")
                print(
                    f"Vendor: {product['business_name']} | Price: {product['price']} | Stock: {product['stock_quantity']}")
                print(f"Product Tags: {','.join(valid_tags) if valid_tags else 'None'}\n")
    except Exception as e:
        print(f"Product search failed: {e}")
    finally:
        conn.close()


# ====================== 4. Product Purchase & Order Management Module ======================
def create_order():
    """Purchase a product, create an order (Requirement: record customer product purchases)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        print("\n===== Create Order (Product Purchase) =====")
        customer_id = input("Please enter your customer ID: ").strip()
        if not customer_id.isdigit():
            print("Customer ID must be a valid number!")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Check if the customer exists
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if not cursor.fetchone():
                print("This customer does not exist!")
                return

            # Create the main order table entry
            cursor.execute("INSERT INTO orders (customer_id) VALUES (%s)", (customer_id,))
            order_id = cursor.lastrowid
            total_price = 0.00

            # Loop to add products to the order
            while True:
                product_id = input("\nPlease enter the ID of the product to purchase (enter 0 to finish shopping): ").strip()
                if product_id == "0":
                    break
                if not product_id.isdigit():
                    print("Product ID must be a valid number!")
                    continue

                # Check if the product exists and has sufficient stock
                cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                product = cursor.fetchone()
                if not product:
                    print("This product does not exist!")
                    continue

                try:
                    quantity = int(input(f"Please enter the quantity for '{product['product_name']}': ").strip())
                    if quantity <= 0:
                        print("Purchase quantity must be greater than 0!")
                        continue
                    if quantity > product['stock_quantity']:
                        print(f"Insufficient stock! Current stock is only {product['stock_quantity']}")
                        continue
                except ValueError:
                    print("Purchase quantity must be a valid number!")
                    continue

                # Calculate the item total and add to order details
                item_price = product['price']
                item_total = item_price * quantity
                total_price += item_total

                # Insert the order item
                item_sql = """
                           INSERT INTO order_items (order_id, product_id, vendor_id, quantity, item_price)
                           VALUES (%s, %s, %s, %s, %s) \
                           """
                cursor.execute(item_sql, (order_id, product_id, product['vendor_id'], quantity, item_price))

                # Deduct product stock
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (quantity, product_id)
                )
                print(f"Product '{product['product_name']}' has been added to the order!")

            # If no products in the order, cancel creation
            if total_price <= 0:
                conn.rollback()
                print("No products selected, order has been cancelled")
                return

            # Update the total price of the order
            cursor.execute("UPDATE orders SET total_price = %s WHERE order_id = %s", (total_price, order_id))
            conn.commit()
            print(f"\nOrder created successfully! Order ID: {order_id} | Total Price: {total_price}")
            print("Please complete the payment. After payment, the order will be in 'pending_shipment' status")
    except Exception as e:
        conn.rollback()
        print(f"Failed to create order: {e}")
    finally:
        conn.close()


def pay_order():
    """Pay for an order, generate transaction records (matches transaction requirement)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        order_id = input("\nPlease enter the order ID to pay for: ").strip()
        if not order_id.isdigit():
            print("Order ID must be a valid number!")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Check the order
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            if not order:
                print("This order does not exist!")
                return
            if order['order_status'] != 'pending_payment':
                print("Only orders in 'pending_payment' status can be paid for!")
                return

            # Group by vendor to generate transaction records (one transaction per vendor for orders spanning multiple vendors)
            cursor.execute("""
                           SELECT vendor_id, SUM(item_price * quantity) as vendor_total
                           FROM order_items
                           WHERE order_id = %s
                           GROUP BY vendor_id
                           """, (order_id,))
            vendor_trans = cursor.fetchall()

            # Insert transaction records
            for trans in vendor_trans:
                trans_sql = """
                            INSERT INTO transactions (order_id, customer_id, vendor_id, transaction_amount)
                            VALUES (%s, %s, %s, %s) \
                            """
                cursor.execute(trans_sql, (
                    order_id, order['customer_id'],
                    trans['vendor_id'], trans['vendor_total']
                ))

            # Update order status to 'pending_shipment'
            cursor.execute(
                "UPDATE orders SET order_status = 'pending_shipment' WHERE order_id = %s",
                (order_id,)
            )
            conn.commit()
            print(f"Order ID:{order_id} payment successful! Corresponding transaction records have been generated, and the order is now pending shipment.")
    except Exception as e:
        conn.rollback()
        print(f"Order payment failed: {e}")
    finally:
        conn.close()


def query_customer_orders():
    """Query a customer's order history (matches basic customer requirement)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        customer_id = input("\nPlease enter customer ID: ").strip()
        if not customer_id.isdigit():
            print("Customer ID must be a valid number!")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Query all of the customer's orders
            sql = "SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC"
            cursor.execute(sql, (customer_id,))
            orders = cursor.fetchall()
            if not orders:
                print("This customer has no order history yet")
                return

            print(f"\n===== Customer ID:{customer_id} Order History =====")
            for order in orders:
                print(f"\nOrder ID: {order['order_id']} | Order Date: {order['order_date']}")
                print(f"Total Price: {order['total_price']} | Order Status: {order['order_status']}")

                # Query order details
                cursor.execute("""
                               SELECT oi.*, p.product_name, v.business_name
                               FROM order_items oi
                                        LEFT JOIN products p ON oi.product_id = p.product_id
                                        LEFT JOIN vendors v ON oi.vendor_id = v.vendor_id
                               WHERE oi.order_id = %s
                               """, (order['order_id'],))
                items = cursor.fetchall()
                print("Order Item Details:")
                for item in items:
                    print(f"- Vendor: {item['business_name']} | Product: {item['product_name']}")
                    print(
                        f"  Unit Price: {item['item_price']} | Quantity: {item['quantity']} | Subtotal: {item['item_price'] * item['quantity']}")
    except Exception as e:
        print(f"Failed to query orders: {e}")
    finally:
        conn.close()


# ====================== 5. Order Modification Module ======================
def modify_order():
    """Modify an order (Requirement: delete a product/cancel the entire order before shipment)"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        order_id = input("\nPlease enter the order ID to modify: ").strip()
        if not order_id.isdigit():
            print("Order ID must be a valid number!")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Check order status: only 'pending_shipment' status can be modified (before shipment)
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            if not order:
                print("This order does not exist!")
                return
            if order['order_status'] != 'pending_shipment':
                print("Only orders in 'pending_shipment' status (before shipment) can be modified!")
                return

            # Operation menu
            print("\n===== Order Modification Operations =====")
            print("1 - Delete a specific product from the order")
            print("2 - Cancel the entire order")
            choice = input("Please select an operation (enter a number): ").strip()

            if choice == "1":
                # First, display the products in the order
                cursor.execute("""
                               SELECT oi.order_item_id, oi.product_id, p.product_name, oi.quantity
                               FROM order_items oi
                                        LEFT JOIN products p ON oi.product_id = p.product_id
                               WHERE oi.order_id = %s
                               """, (order_id,))
                items = cursor.fetchall()
                if not items:
                    print("No products in the order, cannot modify")
                    return

                print("\nProduct list in the order:")
                for item in items:
                    print(
                        f"Order Item ID: {item['order_item_id']} | Product ID: {item['product_id']} | Product Name: {item['product_name']} | Quantity: {item['quantity']}")

                item_id = input("\nPlease enter the order item ID to delete: ").strip()
                if not item_id.isdigit():
                    print("Order item ID must be a valid number!")
                    return

                # Check if the order item belongs to this order
                cursor.execute("""
                               SELECT *
                               FROM order_items
                               WHERE order_item_id = %s
                                 AND order_id = %s
                               """, (item_id, order_id))
                target_item = cursor.fetchone()
                if not target_item:
                    print("This order item does not belong to the current order!")
                    return

                # Restore product stock
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                    (target_item['quantity'], target_item['product_id'])
                )

                # Delete the order item
                cursor.execute("DELETE FROM order_items WHERE order_item_id = %s", (item_id,))

                # Recalculate the order total
                cursor.execute("""
                               SELECT SUM(item_price * quantity) as new_total
                               FROM order_items
                               WHERE order_id = %s
                               """, (order_id,))
                new_total = cursor.fetchone()['new_total'] or 0.00

                # If no products left in the order, cancel it automatically
                if new_total <= 0:
                    cursor.execute("UPDATE orders SET order_status = 'cancelled', total_price = 0 WHERE order_id = %s",
                                   (order_id,))
                    # Delete corresponding transaction records
                    cursor.execute("DELETE FROM transactions WHERE order_id = %s", (order_id,))
                    conn.commit()
                    print("There are no items left in the order, and the order has been automatically cancelled.")
                else:
                    # Update order total price
                    cursor.execute("UPDATE orders SET total_price = %s WHERE order_id = %s", (new_total, order_id))
                    # Update corresponding transaction amounts
                    cursor.execute("""
                                   SELECT vendor_id, SUM(item_price * quantity) as vendor_total
                                   FROM order_items
                                   WHERE order_id = %s
                                   GROUP BY vendor_id
                                   """, (order_id,))
                    vendor_trans = cursor.fetchall()
                    for trans in vendor_trans:
                        cursor.execute("""
                                       UPDATE transactions
                                       SET transaction_amount = %s
                                       WHERE order_id = %s
                                         AND vendor_id = %s
                                       """, (trans['vendor_total'], order_id, trans['vendor_id']))
                    conn.commit()
                    print(f"Order item deleted successfully! The new order total is: {new_total} yuan")

            elif choice == "2":
                # Cancel the entire order: restore stock, update status, delete transaction records
                # Restore stock for all products
                cursor.execute("""
                               UPDATE products p
                                   JOIN order_items oi
                               ON p.product_id = oi.product_id
                                   SET p.stock_quantity = p.stock_quantity + oi.quantity
                               WHERE oi.order_id = %s
                               """, (order_id,))

                # Update order status to 'cancelled'
                cursor.execute(
                    "UPDATE orders SET order_status = 'cancelled' WHERE order_id = %s",
                    (order_id,)
                )

                # Delete corresponding transaction records
                cursor.execute("DELETE FROM transactions WHERE order_id = %s", (order_id,))
                conn.commit()
                print(f"Order ID:{order_id} has been successfully cancelled, and product stock has been restored")
            else:
                print("Invalid operation choice!")
    except Exception as e:
        conn.rollback()
        print(f"Failed to modify order: {e}")
    finally:
        conn.close()


# ====================== Main Program Command Line Menu ======================
def main_menu():
    """Main program entry point, command line interactive menu"""
    print("=" * 50)
    print("  COMP7640 Multi-vendor E-commerce Platform Basic Function System")
    print("=" * 50)
    while True:
        print("\n===== Main Menu =====")
        print("1. Vendor Management - View All Vendors")
        print("2. Vendor Management - Add New Vendor")
        print("3. Product Management - Browse Products of a Specific Vendor")
        print("4. Product Management - Add New Product to Vendor's Catalog")
        print("5. Product Search - Search Products by Keyword")
        print("6. Order Management - Create Order (Purchase Product)")
        print("7. Order Management - Pay for Order (Generate Transaction)")
        print("8. Order Management - Query Customer Order History")
        print("9. Order Management - Modify/Cancel Order (Before Shipment)")
        print("0. Exit System")

        choice = input("\nPlease select an operation (enter the corresponding number): ").strip()
        if choice == "0":
            print("Thank you for using the system. Exiting.")
            break
        elif choice == "1":
            show_all_vendors()
        elif choice == "2":
            add_new_vendor()
        elif choice == "3":
            browse_vendor_products()
        elif choice == "4":
            add_new_product()
        elif choice == "5":
            search_products_by_tag()
        elif choice == "6":
            create_order()
        elif choice == "7":
            pay_order()
        elif choice == "8":
            query_customer_orders()
        elif choice == "9":
            modify_order()
        else:
            print("Invalid choice, please enter a number from the menu!")


# Program entry point
if __name__ == "__main__":
    main_menu()