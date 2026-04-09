# 7640_db

## Environment Setup

- **Install Python 3.5+**

- **Install PyMySQL dependency:**
  ```bash
  pip install pymysql
  ```

- **Install MySQL 5.7+** and ensure the service is running.

## Database Initialization

1.  Open your MySQL client (e.g., Navicat, command line).
2.  Execute all SQL statements within `groupX_insert_sql.txt` to initialize the database, table structures, and test data.

## Code Configuration

1.  Open `ecommerce_main.py`.
2.  Modify the `DB_CONFIG` dictionary with your local MySQL credentials (update `user` and `password`).

## Running the Program

1.  Execute the following command to start the application:
    ```bash
    python ecommerce_main.py
    ```
2.  Follow the numeric prompts in the command-line menu to use all the basic features.