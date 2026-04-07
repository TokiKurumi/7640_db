#!/usr/bin/env python3
"""
快速验证脚本 - 检查前端和后端是否正常工作
"""

import requests
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent

def check_backend():
    """检查后端是否运行"""
    print("📋 检查后端连接...")
    try:
        response = requests.get("http://localhost:8000/api/vendors", timeout=5)
        if response.status_code == 200:
            print("✅ 后端连接成功")
            return True
        else:
            print(f"❌ 后端返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端连接失败: {e}")
        print("   请确保后端已启动: python backend/app.py")
        return False

def check_imports():
    """检查所有必要的导入"""
    print("\n📦 检查 Python 模块导入...")
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
            print(f"  ❌ {module_name} - 请运行: pip install {module_name}")
            all_ok = False
    
    return all_ok

def check_files():
    """检查前端关键文件是否存在"""
    print("\n📁 检查前端文件结构...")
    files_to_check = [
        "ecommerce_platform/frontend/main_new.py",
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
            print(f"  ❌ {file_path} - 文件不存在")
            all_ok = False
    
    return all_ok

def check_sample_data():
    """检查数据库中是否有样本数据"""
    print("\n📊 检查数据库样本数据...")
    try:
        response = requests.get("http://localhost:8000/api/products", timeout=5)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            print(f"  ✅ 数据库中有 {len(data)} 个产品")
            return True
        else:
            print("  ⚠️  数据库为空")
            return False
    except Exception as e:
        print(f"  ❌ 检查失败: {e}")
        return False

def main():
    print("="*60)
    print("🚀 E-Commerce Platform 前端验证")
    print("="*60)
    
    results = {
        "后端连接": check_backend(),
        "Python 模块": check_imports(),
        "前端文件": check_files(),
        "样本数据": check_sample_data(),
    }
    
    print("\n" + "="*60)
    print("📋 检查结果摘要")
    print("="*60)
    for task, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{task}: {status}")
    
    print("\n" + "="*60)
    if all(results.values()):
        print("✅ 所有检查通过！")
        print("\n启动前端:")
        print("  python ecommerce_platform/frontend/main_new.py")
        print("="*60)
        return 0
    else:
        print("❌ 某些检查失败，请修复后重试")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
