#!/bin/bash

# COMP7640 E-Commerce Platform - Setup Script
# This script helps set up the database and start the application

echo "======================================"
echo "COMP7640 E-Commerce Platform Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✓ Found: $python_version"
else
    echo "✗ Python not found. Please install Python 3.5 or higher."
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [[ $? -eq 0 ]]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "Database Setup"
echo "======================================"
echo "Choose an option:"
echo "1) I'll create the database manually"
echo "2) Create database (requires MySQL command line)"
echo ""
read -p "Enter choice (1 or 2): " db_choice

if [[ "$db_choice" == "2" ]]; then
    echo ""
    read -p "MySQL root username (default: root): " mysql_user
    mysql_user=${mysql_user:-root}
    
    echo "Creating database and tables..."
    mysql -u "$mysql_user" -p < database/schema.sql
    
    echo "Inserting sample data..."
    mysql -u "$mysql_user" -p < database/sample_data.sql
    
    echo "✓ Database setup complete"
else
    echo ""
    echo "To set up the database manually:"
    echo "1. Open MySQL Workbench or MySQL command line"
    echo "2. Execute: mysql -u root -p < database/schema.sql"
    echo "3. Execute: mysql -u root -p < database/sample_data.sql"
    echo ""
fi

echo ""
echo "======================================"
echo "Configuration"
echo "======================================"
echo "Configuring database connection..."
echo "Default settings:"
echo "  Host: localhost"
echo "  Port: 3306"
echo "  User: root"
echo "  Password: (blank)"
echo "  Database: ecommerce_platform"
echo ""
read -p "Press Enter to continue (or Ctrl+C to edit backend/app.py first)..."

echo ""
echo "======================================"
echo "Starting Application"
echo "======================================"
echo ""
echo "To start the backend server, run:"
echo "  python backend/app.py"
echo ""
echo "In another terminal, start the frontend GUI:"
echo "  python frontend/gui.py"
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "API Documentation at: http://localhost:8000/docs"
echo ""

read -p "Start backend server now? (y/n): " start_backend

if [[ "$start_backend" == "y" ]]; then
    echo "Starting backend server..."
    python backend/app.py
else
    echo "Setup complete! You can start the backend with: python backend/app.py"
fi
