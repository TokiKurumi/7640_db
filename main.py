import pymysql
from datetime import datetime

# 数据库连接配置（请根据本地MySQL环境修改）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # 你的MySQL用户名
    "password": "123456",  # 你的MySQL密码
    "database": "ecommerce_platform",
    "charset": "utf8mb4"
}


# 数据库连接工具函数
def get_db_connection():
    """创建并返回MySQL数据库连接"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败：{e}")
        return None


# ====================== 1. 供应商管理模块 ======================
def show_all_vendors():
    """显示平台所有供应商（要求功能1）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM vendors ORDER BY vendor_id ASC"
            cursor.execute(sql)
            vendors = cursor.fetchall()
            if not vendors:
                print("平台暂无供应商数据")
                return
            print("\n===== 平台供应商列表 =====")
            for vendor in vendors:
                print(f"供应商ID：{vendor['vendor_id']} | 商家名称：{vendor['business_name']}")
                print(f"平均评分：{vendor['avg_rating']} | 地理位置：{vendor['geo_presence']}\n")
    except Exception as e:
        print(f"查询供应商失败：{e}")
    finally:
        conn.close()


def add_new_vendor():
    """新增供应商入驻平台（要求功能2）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        print("\n===== 新增供应商入驻 =====")
        business_name = input("请输入商家名称：").strip()
        geo_presence = input("请输入商家地理位置：").strip()
        if not business_name or not geo_presence:
            print("商家名称和地理位置为必填项！")
            return

        with conn.cursor() as cursor:
            sql = "INSERT INTO vendors (business_name, geo_presence) VALUES (%s, %s)"
            cursor.execute(sql, (business_name, geo_presence))
            conn.commit()
            print(f"供应商【{business_name}】入驻成功！供应商ID：{cursor.lastrowid}")
    except Exception as e:
        conn.rollback()
        print(f"新增供应商失败：{e}")
    finally:
        conn.close()


# ====================== 2. 产品目录管理模块 ======================
def browse_vendor_products():
    """浏览指定供应商的所有产品（要求功能1）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        vendor_id = input("\n请输入要浏览的供应商ID：").strip()
        if not vendor_id.isdigit():
            print("请输入有效的数字ID！")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 先校验供应商是否存在
            cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
            if not cursor.fetchone():
                print("该供应商不存在！")
                return

            # 查询供应商所有产品
            sql = "SELECT * FROM products WHERE vendor_id = %s ORDER BY product_id ASC"
            cursor.execute(sql, (vendor_id,))
            products = cursor.fetchall()
            if not products:
                print("该供应商暂无上架产品")
                return

            print(f"\n===== 供应商ID:{vendor_id} 产品列表 =====")
            for product in products:
                tags = [product['tag1'], product['tag2'], product['tag3']]
                valid_tags = [tag for tag in tags if tag]
                print(f"产品ID：{product['product_id']} | 产品名称：{product['product_name']}")
                print(f"售价：{product['price']}元 | 库存：{product['stock_quantity']}件")
                print(f"产品标签：{','.join(valid_tags) if valid_tags else '无'}\n")
    except Exception as e:
        print(f"浏览产品失败：{e}")
    finally:
        conn.close()


def add_new_product():
    """为供应商新增产品到目录（要求功能2）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        print("\n===== 新增产品 =====")
        vendor_id = input("请输入所属供应商ID：").strip()
        product_name = input("请输入产品名称：").strip()
        price = input("请输入产品售价：").strip()
        stock_quantity = input("请输入产品库存数量：").strip()
        tag1 = input("请输入产品标签1（选填）：").strip() or None
        tag2 = input("请输入产品标签2（选填）：").strip() or None
        tag3 = input("请输入产品标签3（选填）：").strip() or None

        # 基础校验
        if not vendor_id.isdigit():
            print("供应商ID必须为有效数字！")
            return
        if not product_name:
            print("产品名称为必填项！")
            return
        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
            if price <= 0 or stock_quantity < 0:
                print("售价必须大于0，库存不能为负数！")
                return
        except ValueError:
            print("售价和库存必须为有效数字！")
            return

        with conn.cursor() as cursor:
            # 校验供应商是否存在
            cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
            if not cursor.fetchone():
                print("该供应商不存在，无法新增产品！")
                return

            # 插入产品
            sql = """
                  INSERT INTO products (vendor_id, product_name, price, stock_quantity, tag1, tag2, tag3)
                  VALUES (%s, %s, %s, %s, %s, %s, %s) \
                  """
            cursor.execute(sql, (vendor_id, product_name, price, stock_quantity, tag1, tag2, tag3))
            conn.commit()
            print(f"产品【{product_name}】新增成功！产品ID：{cursor.lastrowid}")
    except Exception as e:
        conn.rollback()
        print(f"新增产品失败：{e}")
    finally:
        conn.close()


# ====================== 3. 产品搜索模块 ======================
def search_products_by_tag():
    """按标签/名称搜索产品（要求功能：匹配名称或标签任意部分）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        keyword = input("\n请输入搜索关键词（匹配产品名称/标签）：").strip()
        if not keyword:
            print("搜索关键词不能为空！")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 模糊匹配名称或三个标签的任意部分
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
                print("未找到匹配的产品")
                return

            print(f"\n===== 关键词「{keyword}」搜索结果 =====")
            for product in products:
                tags = [product['tag1'], product['tag2'], product['tag3']]
                valid_tags = [tag for tag in tags if tag]
                print(f"产品ID：{product['product_id']} | 产品名称：{product['product_name']}")
                print(
                    f"所属商家：{product['business_name']} | 售价：{product['price']}元 | 库存：{product['stock_quantity']}件")
                print(f"产品标签：{','.join(valid_tags) if valid_tags else '无'}\n")
    except Exception as e:
        print(f"产品搜索失败：{e}")
    finally:
        conn.close()


# ====================== 4. 产品购买&订单管理模块 ======================
def create_order():
    """产品购买，创建订单（要求功能：记录客户购买产品）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        print("\n===== 创建订单（产品购买） =====")
        customer_id = input("请输入您的客户ID：").strip()
        if not customer_id.isdigit():
            print("客户ID必须为有效数字！")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 校验客户是否存在
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if not cursor.fetchone():
                print("该客户不存在！")
                return

            # 创建订单主表
            cursor.execute("INSERT INTO orders (customer_id) VALUES (%s)", (customer_id,))
            order_id = cursor.lastrowid
            total_price = 0.00

            # 循环添加产品到订单
            while True:
                product_id = input("\n请输入要购买的产品ID（输入0结束选购）：").strip()
                if product_id == "0":
                    break
                if not product_id.isdigit():
                    print("产品ID必须为有效数字！")
                    continue

                # 校验产品是否存在、库存是否充足
                cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                product = cursor.fetchone()
                if not product:
                    print("该产品不存在！")
                    continue

                try:
                    quantity = int(input(f"请输入「{product['product_name']}」购买数量：").strip())
                    if quantity <= 0:
                        print("购买数量必须大于0！")
                        continue
                    if quantity > product['stock_quantity']:
                        print(f"库存不足！当前库存仅{product['stock_quantity']}件")
                        continue
                except ValueError:
                    print("购买数量必须为有效数字！")
                    continue

                # 计算订单项金额，添加到订单详情
                item_price = product['price']
                item_total = item_price * quantity
                total_price += item_total

                # 插入订单项
                item_sql = """
                           INSERT INTO order_items (order_id, product_id, vendor_id, quantity, item_price)
                           VALUES (%s, %s, %s, %s, %s) \
                           """
                cursor.execute(item_sql, (order_id, product_id, product['vendor_id'], quantity, item_price))

                # 扣减产品库存
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (quantity, product_id)
                )
                print(f"产品「{product['product_name']}」已添加到订单！")

            # 订单无产品，取消创建
            if total_price <= 0:
                conn.rollback()
                print("未选购任何产品，订单已取消")
                return

            # 更新订单总价
            cursor.execute("UPDATE orders SET total_price = %s WHERE order_id = %s", (total_price, order_id))
            conn.commit()
            print(f"\n订单创建成功！订单ID：{order_id} | 订单总价：{total_price}元")
            print("请完成支付，支付后订单将进入待发货状态")
    except Exception as e:
        conn.rollback()
        print(f"创建订单失败：{e}")
    finally:
        conn.close()


def pay_order():
    """订单支付，生成交易记录（匹配transaction要求）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        order_id = input("\n请输入要支付的订单ID：").strip()
        if not order_id.isdigit():
            print("订单ID必须为有效数字！")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 校验订单
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            if not order:
                print("该订单不存在！")
                return
            if order['order_status'] != 'pending_payment':
                print("仅待付款状态的订单可支付！")
                return

            # 按供应商分组，生成交易记录（一个订单跨多个供应商时，每个供应商对应一条交易）
            cursor.execute("""
                           SELECT vendor_id, SUM(item_price * quantity) as vendor_total
                           FROM order_items
                           WHERE order_id = %s
                           GROUP BY vendor_id
                           """, (order_id,))
            vendor_trans = cursor.fetchall()

            # 插入交易记录
            for trans in vendor_trans:
                trans_sql = """
                            INSERT INTO transactions (order_id, customer_id, vendor_id, transaction_amount)
                            VALUES (%s, %s, %s, %s) \
                            """
                cursor.execute(trans_sql, (
                    order_id, order['customer_id'],
                    trans['vendor_id'], trans['vendor_total']
                ))

            # 更新订单状态为待发货
            cursor.execute(
                "UPDATE orders SET order_status = 'pending_shipment' WHERE order_id = %s",
                (order_id,)
            )
            conn.commit()
            print(f"订单ID:{order_id} 支付成功！已生成对应交易记录，订单进入待发货状态")
    except Exception as e:
        conn.rollback()
        print(f"订单支付失败：{e}")
    finally:
        conn.close()


def query_customer_orders():
    """查询客户的订单历史（匹配customer基础要求）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        customer_id = input("\n请输入客户ID：").strip()
        if not customer_id.isdigit():
            print("客户ID必须为有效数字！")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 查询客户所有订单
            sql = "SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC"
            cursor.execute(sql, (customer_id,))
            orders = cursor.fetchall()
            if not orders:
                print("该客户暂无订单记录")
                return

            print(f"\n===== 客户ID:{customer_id} 订单历史 =====")
            for order in orders:
                print(f"\n订单ID：{order['order_id']} | 下单时间：{order['order_date']}")
                print(f"订单总价：{order['total_price']}元 | 订单状态：{order['order_status']}")

                # 查询订单详情
                cursor.execute("""
                               SELECT oi.*, p.product_name, v.business_name
                               FROM order_items oi
                                        LEFT JOIN products p ON oi.product_id = p.product_id
                                        LEFT JOIN vendors v ON oi.vendor_id = v.vendor_id
                               WHERE oi.order_id = %s
                               """, (order['order_id'],))
                items = cursor.fetchall()
                print("订单商品明细：")
                for item in items:
                    print(f"- 商家：{item['business_name']} | 商品：{item['product_name']}")
                    print(
                        f"  单价：{item['item_price']}元 | 数量：{item['quantity']}件 | 小计：{item['item_price'] * item['quantity']}元")
    except Exception as e:
        print(f"查询订单失败：{e}")
    finally:
        conn.close()


# ====================== 5. 订单修改模块 ======================
def modify_order():
    """修改订单（要求功能：发货前删除产品/取消整个订单）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        order_id = input("\n请输入要修改的订单ID：").strip()
        if not order_id.isdigit():
            print("订单ID必须为有效数字！")
            return

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 校验订单状态：仅待发货状态可修改（发货前）
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            if not order:
                print("该订单不存在！")
                return
            if order['order_status'] != 'pending_shipment':
                print("仅待发货状态（发货前）的订单可修改！")
                return

            # 操作菜单
            print("\n===== 订单修改操作 =====")
            print("1 - 删除订单内指定商品")
            print("2 - 取消整个订单")
            choice = input("请选择操作（输入数字）：").strip()

            if choice == "1":
                # 先展示订单内商品
                cursor.execute("""
                               SELECT oi.order_item_id, oi.product_id, p.product_name, oi.quantity
                               FROM order_items oi
                                        LEFT JOIN products p ON oi.product_id = p.product_id
                               WHERE oi.order_id = %s
                               """, (order_id,))
                items = cursor.fetchall()
                if not items:
                    print("订单内无商品，无法修改")
                    return

                print("\n订单内商品列表：")
                for item in items:
                    print(
                        f"订单项ID：{item['order_item_id']} | 产品ID：{item['product_id']} | 产品名称：{item['product_name']} | 数量：{item['quantity']}件")

                item_id = input("\n请输入要删除的订单项ID：").strip()
                if not item_id.isdigit():
                    print("订单项ID必须为有效数字！")
                    return

                # 校验订单项是否属于该订单
                cursor.execute("""
                               SELECT *
                               FROM order_items
                               WHERE order_item_id = %s
                                 AND order_id = %s
                               """, (item_id, order_id))
                target_item = cursor.fetchone()
                if not target_item:
                    print("该订单项不属于当前订单！")
                    return

                # 恢复商品库存
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                    (target_item['quantity'], target_item['product_id'])
                )

                # 删除订单项
                cursor.execute("DELETE FROM order_items WHERE order_item_id = %s", (item_id,))

                # 重新计算订单总价
                cursor.execute("""
                               SELECT SUM(item_price * quantity) as new_total
                               FROM order_items
                               WHERE order_id = %s
                               """, (order_id,))
                new_total = cursor.fetchone()['new_total'] or 0.00

                # 订单无商品，自动取消
                if new_total <= 0:
                    cursor.execute("UPDATE orders SET order_status = 'cancelled', total_price = 0 WHERE order_id = %s",
                                   (order_id,))
                    # 删除对应交易记录
                    cursor.execute("DELETE FROM transactions WHERE order_id = %s", (order_id,))
                    conn.commit()
                    print("订单内已无商品，订单已自动取消")
                else:
                    # 更新订单总价
                    cursor.execute("UPDATE orders SET total_price = %s WHERE order_id = %s", (new_total, order_id))
                    # 更新对应交易金额
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
                    print(f"订单项删除成功！订单最新总价：{new_total}元")

            elif choice == "2":
                # 取消整个订单：恢复库存、更新状态、删除交易记录
                # 恢复所有商品库存
                cursor.execute("""
                               UPDATE products p
                                   JOIN order_items oi
                               ON p.product_id = oi.product_id
                                   SET p.stock_quantity = p.stock_quantity + oi.quantity
                               WHERE oi.order_id = %s
                               """, (order_id,))

                # 更新订单状态为已取消
                cursor.execute(
                    "UPDATE orders SET order_status = 'cancelled' WHERE order_id = %s",
                    (order_id,)
                )

                # 删除对应交易记录
                cursor.execute("DELETE FROM transactions WHERE order_id = %s", (order_id,))
                conn.commit()
                print(f"订单ID:{order_id} 已成功取消，商品库存已恢复")
            else:
                print("无效的操作选择！")
    except Exception as e:
        conn.rollback()
        print(f"订单修改失败：{e}")
    finally:
        conn.close()


# ====================== 主程序命令行菜单 ======================
def main_menu():
    """主程序入口，命令行交互菜单"""
    print("=" * 50)
    print("  COMP7640 多供应商电商平台 基础功能系统")
    print("=" * 50)
    while True:
        print("\n===== 主功能菜单 =====")
        print("1. 供应商管理 - 查看所有供应商")
        print("2. 供应商管理 - 新增供应商入驻")
        print("3. 产品管理 - 浏览指定供应商的产品")
        print("4. 产品管理 - 新增产品到供应商目录")
        print("5. 产品搜索 - 按关键词搜索产品")
        print("6. 订单管理 - 创建订单（购买产品）")
        print("7. 订单管理 - 订单支付（生成交易记录）")
        print("8. 订单管理 - 查询客户订单历史")
        print("9. 订单管理 - 修改/取消订单（发货前）")
        print("0. 退出系统")

        choice = input("\n请选择操作（输入对应数字）：").strip()
        if choice == "0":
            print("感谢使用，系统已退出")
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
            print("无效的选择，请输入菜单内的数字！")


# 程序启动入口
if __name__ == "__main__":
    main_menu()