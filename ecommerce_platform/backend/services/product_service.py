
from dao.product_dao import ProductDAO
from dao.vendor_dao import VendorDAO
from dao import DatabaseConfig
from typing import List, Dict, Any, Optional


class ProductService:

    def __init__(self, config: DatabaseConfig):
        self.product_dao = ProductDAO(config)
        self.vendor_dao = VendorDAO(config)


    def get_all_products(self) -> List[Dict[str, Any]]:
        return self.product_dao.get_all_products()




    def get_products_by_vendor(self, vendor_id: int) -> List[Dict[str, Any]]:

        # Validate if vendor exists
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")

        return self.product_dao.get_products_by_vendor(vendor_id)




    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        if not product_id or product_id <= 0:
            raise ValueError("Invalid product ID")

        product = self.product_dao.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist")
        return product



    def search_products_by_tag(self, tag: str) -> List[Dict[str, Any]]:

        if not tag or len(tag.strip()) == 0:
            raise ValueError("Search tag cannot be empty")

        try:
            return self.product_dao.search_by_tag(tag.strip())
        except Exception as e:
            raise Exception(f"Failed to search for products: {str(e)}")

    def create_product(self, vendor_id: int, product_name: str, listed_price: float,
                      stock_quantity: int, tag1: Optional[str] = None,
                      tag2: Optional[str] = None, tag3: Optional[str] = None) -> Dict[str, Any]:

        # Validate vendor
        vendor = self.vendor_dao.get_vendor_by_id(vendor_id)
        if not vendor:
            raise ValueError(f"Vendor with ID {vendor_id} does not exist")

        # Validate input
        if not product_name or len(product_name.strip()) == 0:
            raise ValueError("Product name cannot be empty")

        if listed_price <= 0:
            raise ValueError("Product price must be greater than 0")

        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")

        try:
            affected_rows, product_id = self.product_dao.create_product(
                vendor_id, product_name.strip(), listed_price, stock_quantity, tag1, tag2, tag3
            )

            if affected_rows > 0:
                return self.get_product_by_id(product_id)
            else:
                raise Exception("Failed to create product")
        except Exception as e:
            raise Exception(f"Failed to create product: {str(e)}")



    def get_product_stock(self, product_id: int) -> int:
        """Get product stock"""
        stock = self.product_dao.get_stock_quantity(product_id)
        if stock is None:
            raise ValueError(f"Product with ID {product_id} does not exist")
        return stock




    def check_stock_availability(self, product_id: int, required_quantity: int) -> bool:
        """Check if a product has enough stock"""
        stock = self.get_product_stock(product_id)
        return stock >= required_quantity