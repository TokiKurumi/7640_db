# 7640_db

环境准备 

安装 Python 3.5+ 版本

安装 PyMySQL 依赖：执行 pip install pymysql

安装 MySQL 5.7+ 版本，确保服务正常运行

数据库初始化

打开 MySQL 客户端（Navicat / 命令行），执行 groupX_insert_sql.txt 内的全部 SQL 语句，完成数据库、表结构和测试数据的初始化

代码配置修改

打开 ecommerce_main.py，修改 DB_CONFIG 内的数据库配置，将 user 和 password 改为你本地 MySQL 的账号密码

程序运行

执行 python ecommerce_main.py 启动程序

按照命令行菜单的数字提示，即可使用全部基础功能