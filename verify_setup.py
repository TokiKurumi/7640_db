#!/usr/bin/env python3
"""
Quick Verification Script - Check if frontend and backend are working correctly
"""

import requests
import sys
from pathlib import Path

# Add project path
PROJECT_ROOT = Path(__file__).parent

def check_backend():
    """Check if the backend is running"""
    print("📋 Checking backend connection...")
    try:
        response = requests.get("http://localhost:8000/api/vendors", timeout=5)
        if response.status_code == 200:
            print("✅ Backend connection successful")
            return True
        else:
            print(f"❌ Backend returned an error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        print("   Please make sure the backend is started: python backend/app.py")
        return False

def check_imports():
    """Check all necessary imports"""
    print("\n📦 Checking Python module imports...")
    modules_to_check = [
        ("tkinter", "tkinter"),
        ("requests", "requests"),
        ("pymysql", "pymysql"),
    ]
    
    all_ok = True
    for module_name, import_name in modules_to_check:
        try:
            __import__(import_name)
            print(f"  ✅ {module_name}")
        except ImportError:
            print(f"  ❌ {module_name} - Please run: pip install {module_name}")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if critical frontend files exist"""
    print("\n📁 Checking frontend file structure...")
    files_to_check = [
        "ecommerce_platform/frontend/main_front.py",
        "ecommerce_platform/frontend/ui/base_components.py",
        "ecommerce_platform/frontend/controllers/product_tab.py",
        "ecommerce_platform/frontend/services/api_client.py",
        "ecommerce_platform/frontend/config/app_config.py",
    ]
    
    all_ok = True
    for file_path in files_to_check:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - File does not exist")
            all_ok = False
    
    return all_ok

def check_sample_data():
    """Check if there is sample data in the database"""
    print("\n📊 Checking database sample data...")
    try:
        response = requests.get("http://localhost:8000/api/products", timeout=5)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            print(f"  ✅ Database contains {len(data)} products")
            return True
        else:
            print("  ⚠️  Database is empty")
            return False
    except Exception as e:
        print(f"  ❌ Check failed: {e}")
        return False

def main():
    print("="*60)
    print("🚀 E-Commerce Platform Frontend Verification")
    print("="*60)
    
    results = {
        "Backend Connection": check_backend(),
        "Python Modules": check_imports(),
        "Frontend Files": check_files(),
        "Sample Data": check_sample_data(),
    }
    
    print("\n" + "="*60)
    print("📋 Check Result Summary")
    print("="*60)
    for task, result in results.items():
        status = "✅ Passed" if result else "❌ Failed"
        print(f"{task}: {status}")
    
    print("\n" + "="*60)
    if all(results.values()):
        print("✅ All checks passed!")
        print("\nStart the frontend:")
        print("  python ecommerce_platform/frontend/main_front.py")
        print("="*60)
        return 0
    else:
        print("❌ Some checks failed, please fix and retry")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())