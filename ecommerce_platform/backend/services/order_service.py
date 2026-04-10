

from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO
from dao.customer_dao import CustomerDAO
from dao.transaction_dao import TransactionDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class OrderService:
    """Order business logic class"""

    # ORM inject
    def __init__(self, config: DatabaseConfig):
        self.order_dao = OrderDAO(config)
        self.product_dao = ProductDAO(config)
        self.customer_dao = CustomerDAO(config)
        self.transaction_dao = TransactionDAO(config)

    def get_all_orders(self) -> List[Dict[str, Any]]:
        return self.order_dao.get_all_orders()


    def get_orders_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        # Validate customer
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")


        return self.order_dao.get_orders_by_customer(customer_id)


    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        if not order_id or order_id <= 0:
            raise ValueError("Invalid order ID")

        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist")

        # Get order items list
        items = self.order_dao.get_order_items(order_id)
        order['items'] = items
        return order

    def create_order(self, customer_id: int, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        # 1/ require order list

        # Validate customer
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist")

        # Validate items
        if not items or len(items) == 0:
            raise ValueError("Order must have at least one item")

        # Calculate total price and validate stock
        total_price = 0
        items_data = []

        for item in items:
            # for loop to map into dict and total price

            product_id = item.get('product_id')
            quantity = item.get('quantity')

            # Get product information
            product = self.product_dao.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist")

            # Check stock
            if product['stock_quantity'] < quantity:
                raise ValueError(f"Product '{product['product_name']}' is out of stock (requires {quantity}, has {product['stock_quantity']})")

            subtotal = product['listed_price'] * quantity
            total_price += subtotal

            items_data.append({
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': product['listed_price'],
                'subtotal': subtotal,
                'vendor_id': product['vendor_id']
            })

        # Create order
        try:
            affected_rows, order_id = self.order_dao.create_order(customer_id, total_price, 'pending')

            if affected_rows > 0:
                # Add order items and deduct stock
                for item_data in items_data:
                    # Add order item
                    self.order_dao.add_order_item(
                        order_id,
                        item_data['product_id'],
                        item_data['quantity'],
                        item_data['unit_price'],
                        item_data['subtotal']
                    )

                    # Deduct stock
                    self.product_dao.update_stock(item_data['product_id'], -item_data['quantity'])

                    # Create transaction record
                    self.transaction_dao.create_transaction(
                        order_id,
                        item_data['vendor_id'],
                        customer_id,
                        item_data['product_id'],
                        item_data['quantity'],
                        item_data['subtotal'],
                        # order state[complete,finish]
                        'completed'
                    )

                return self.get_order_by_id(order_id)
            else:
                raise Exception("Failed to create order")
        except Exception as e:
            raise Exception(f"Failed to create order: {str(e)}")


    def cancel_order(self, order_id: int) -> bool:
        """
        Cancel an order (only for unshipped orders)
        :param order_id: Order ID
        :return: Whether the operation was successful
        """
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist")

        # Check order status
        if order['status'] in ['shipped', 'delivered']:
            raise ValueError(f"Cannot cancel a shipped order (current status: {order['status']})")

        try:
            # Restore stock
            items = self.order_dao.get_order_items(order_id)
            for item in items:
                self.product_dao.update_stock(item['product_id'], item['quantity'])

            # Update order status
            self.order_dao.update_order_status(order_id, 'cancelled')
            return True
        except Exception as e:
            raise Exception(f"Failed to cancel order: {str(e)}")

    def remove_order_item(self, order_id: int, product_id: int) -> bool:
        """
        Remove an item from an order
            remove from list if user second click
        """
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist")

        # 'shipped', 'delivered' 'complete'
        if order['status'] in ['shipped', 'delivered']:
            raise ValueError(f"Cannot modify a shipped order (current status: {order['status']})")

        try:
            # 1 Get order items
            items = self.order_dao.get_order_items(order_id)
            item_to_remove = None

            for item in items:
                if item['product_id'] == product_id:
                    item_to_remove = item
                    break

            if not item_to_remove:
                raise ValueError(f"Product with ID {product_id} does not exist in this order")

            # 2 Restore stock
            self.product_dao.update_stock(product_id, item_to_remove['quantity'])

            # 3 Remove order item
            self.order_dao.remove_order_item(order_id, product_id)

            # 4 Update order total
            new_total = order['total_price'] - item_to_remove['subtotal']
            self.order_dao.update_order_total(order_id, new_total)

            return True
        except Exception as e:
            raise Exception(f"Failed to remove order item: {str(e)}")

    def update_order_status(self, order_id: int, status: str) -> bool:
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

        if status not in valid_statuses:
            raise ValueError(f"Invalid order status. Allowed statuses: {', '.join(valid_statuses)}")

        try:
            affected_rows = self.order_dao.update_order_status(order_id, status)
            return affected_rows > 0
        except Exception as e:
            raise Exception(f"Failed to update order status: {str(e)}")