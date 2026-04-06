# COMP7640 E-Commerce Platform

## Overview
A multi-vendor e-commerce platform built with Python, FastAPI, Tkinter GUI, and MySQL. This system allows vendors to manage products, customers to browse and purchase items, and handles orders and transactions.

## Project Structure

```
ecommerce_platform/
├── backend/
│   └── app.py                 # FastAPI application
├── frontend/
│   └── gui.py                 # Tkinter GUI application
├── database/
│   ├── schema.sql            # Database schema creation
│   └── sample_data.sql       # Sample data insertion
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Prerequisites

1. **Python 3.5+** (3.8+ recommended)
2. **MySQL Server** (5.7+ or 8.0+)
3. **pip** (Python package manager)

## Installation

### 1. Clone/Download Project
```bash
cd ecommerce_platform
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MySQL Database

#### Option A: Using MySQL Command Line
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Create new query tab
3. Copy and paste contents of `database/schema.sql`, execute
4. Copy and paste contents of `database/sample_data.sql`, execute

### 4. Configure Database Connection
Edit `backend/app.py` and update the `DB_CONFIG`:
```python
DB_CONFIG = {
    'host': 'localhost',      # Your MySQL host
    'port': 3306,             # Your MySQL port
    'user': 'root',           # Your MySQL username
    'password': '',           # Your MySQL password (leave empty if no password)
    'database': 'ecommerce_platform',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}
```

## Running the Application

### 1. Start FastAPI Backend Server
```bash
python backend/app.py
```
Or use uvicorn directly:
```bash
uvicorn backend.app:app --reload --port 8000
```

The backend will start on `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 2. Start Tkinter GUI Frontend (in a new terminal)
```bash
python frontend/gui.py
```

## Features Implemented

### ✅ Vendor Administration
- Display all vendors with ratings and locations
- Onboard new vendors to the marketplace
- View vendor profiles

### ✅ Product Catalog Management
- Browse all products offered by each vendor
- Introduce new products to vendor catalogs
- View product details (price, stock, tags)

### ✅ Product Discovery
- Search products by tags or partial name match
- Filter products by vendor
- Support for up to 3 tags per product

### ✅ Product Purchase
- Add products to shopping cart
- Create orders with multiple items
- Purchase confirmation with transaction records
- Automatic stock management

### ✅ Order Modification
- View all orders and their details
- Modify orders before shipping
- Remove specific products from orders
- Cancel entire orders (before shipping)
- Order status tracking

### ✅ Additional Features
- Customer management
- Transaction history with vendor filtering
- Real-time stock updates
- Order status management
- Multi-vendor support in single order

## Database Schema

### Tables
1. **vendors** - Vendor information and ratings
2. **products** - Product catalog with tags and stock
3. **customers** - Customer profiles and addresses
4. **orders** - Order records with status
5. **order_items** - Line items for each order
6. **transactions** - Transaction history per vendor

## API Endpoints

### Vendors
- `GET /api/vendors` - List all vendors
- `POST /api/vendors` - Create new vendor
- `GET /api/vendors/{vendor_id}` - Get vendor details

### Products
- `GET /api/products` - List all products
- `GET /api/products?vendor_id={id}` - Filter by vendor
- `POST /api/products?vendor_id={id}` - Create new product
- `GET /api/products/search?tag={tag}` - Search by tag

### Customers
- `GET /api/customers` - List all customers
- `POST /api/customers` - Create new customer
- `GET /api/customers/{customer_id}` - Get customer details

### Orders
- `GET /api/orders` - List all orders
- `GET /api/orders?customer_id={id}` - Filter by customer
- `GET /api/orders/{order_id}` - Get order details
- `POST /api/orders` - Create new order
- `PUT /api/orders/{order_id}` - Update order status
- `DELETE /api/orders/{order_id}` - Cancel order
- `DELETE /api/orders/{order_id}/items/{product_id}` - Remove item from order

### Transactions
- `GET /api/transactions` - List all transactions
- `GET /api/transactions?vendor_id={id}` - Filter by vendor

## GUI Features

The Tkinter GUI provides 5 main tabs:

### 1. Vendors Tab
- Create new vendors
- View all vendors with ratings
- Manage vendor information

### 2. Products Tab
- Browse all products
- Create new products with tags
- Search products by tag or name
- View stock levels and prices

### 3. Customers Tab
- Register new customers
- View customer information
- Manage shipping addresses

### 4. Orders Tab
- Create new orders
- Add multiple items to orders
- Modify and cancel orders
- Remove individual items from pending orders
- View order details and history

### 5. Transactions Tab
- View complete transaction history
- Filter transactions by vendor
- Track revenue by vendor

## Sample Data

The database includes:
- 5 sample vendors (TechHub, Fashion, Green Market, Electronics, Books)
- 20 sample products across vendors
- 7 sample customers
- 7 sample orders
- Multiple sample transactions

## Error Handling

The application includes comprehensive error handling:
- Input validation
- Database connection error recovery
- API error responses with meaningful messages
- User-friendly error dialogs

## Performance Considerations

- Indexed database fields for fast queries
- Connection pooling available
- API uses efficient queries
- GUI updates status bar for user feedback

## Technical Stack

- **Backend**: FastAPI (async Python web framework)
- **Frontend**: Tkinter (Python built-in GUI)
- **Database**: MySQL with PyMySQL connector
- **API**: RESTful with JSON
- **Server**: Uvicorn ASGI server

## Notes

1. **First Run**: Ensure MySQL is running before starting the application
2. **Database Password**: Update credentials in `backend/app.py` if using authentication
3. **Port Conflicts**: If port 8000 is in use, modify the port in `app.py`
4. **Large Datasets**: For production use, add pagination to API endpoints

## Troubleshooting

### Connection Error: "Can't connect to MySQL"
- Verify MySQL server is running
- Check host, port, username, password in `DB_CONFIG`
- Ensure database `ecommerce_platform` exists

### Import Error: "No module named fastapi"
```bash
pip install -r requirements.txt
```

### GUI won't start
- Ensure backend server is running first
- Check that `http://localhost:8000` is accessible
- Verify requests library is installed

### Database not found
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

## Future Enhancements

- User authentication and authorization
- Payment gateway integration
- Email notifications
- Advanced analytics and reporting
- Rating and review system
- Inventory management dashboard
- Real-time notifications

## Academic Integrity

This project is developed for educational purposes as part of COMP7640 Database Systems & Administration course at Hong Kong Baptist University. All code and documentation are original work.

## Contact

For questions or issues, please refer to the course instructors.
