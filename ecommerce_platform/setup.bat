@echo off
REM COMP7640 E-Commerce Platform - Setup Script for Windows
REM This script helps set up the database and start the application

echo ======================================
echo COMP7640 E-Commerce Platform Setup
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo X Python not found. Please install Python 3.5 or higher.
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
echo OK Found: %python_version%

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo X Failed to install dependencies
    exit /b 1
)
echo OK Dependencies installed successfully

echo.
echo ======================================
echo Database Setup
echo ======================================
echo Choose an option:
echo 1) I'll create the database manually
echo 2) Create database (requires MySQL command line)
echo.
set /p db_choice="Enter choice (1 or 2): "

if "%db_choice%"=="2" (
    echo.
    set /p mysql_user="MySQL root username (default: root): "
    if "%mysql_user%"=="" set mysql_user=root
    
    echo Creating database and tables...
    mysql -u %mysql_user% -p < database/schema.sql
    
    echo Inserting sample data...
    mysql -u %mysql_user% -p < database/sample_data.sql
    
    echo OK Database setup complete
) else (
    echo.
    echo To set up the database manually:
    echo 1. Open MySQL Workbench or MySQL command line
    echo 2. Execute: mysql -u root -p ^< database/schema.sql
    echo 3. Execute: mysql -u root -p ^< database/sample_data.sql
    echo.
)

echo.
echo ======================================
echo Configuration
echo ======================================
echo Configuring database connection...
echo Default settings:
echo   Host: localhost
echo   Port: 3306
echo   User: root
echo   Password: (blank)
echo   Database: ecommerce_platform
echo.
pause

echo.
echo ======================================
echo Starting Application
echo ======================================
echo.
echo To start the backend server, run:
echo   python backend/app.py
echo.
echo In another terminal, start the frontend GUI:
echo   python frontend/gui.py
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.

set /p start_backend="Start backend server now? (y/n): "

if "%start_backend%"=="y" (
    echo Starting backend server...
    python backend/app.py
) else (
    echo Setup complete! You can start the backend with: python backend/app.py
)
