@echo off
title Lucky Wheel System Startup

echo.
echo  🎰 LUCKY WHEEL ROULETTE SYSTEM 🎰
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Creating .env file from template...
    copy ".env.example" ".env"
    echo 📝 Please edit .env file with your actual values!
    echo 🔑 Required variables:
    echo    - TELEGRAM_BOT_TOKEN
    echo    - TELEGRAM_GROUP_ID
    echo    - OWNER_ID
    echo    - MONGO_URL
    echo    - API_ID
    echo    - API_HASH
    echo.
    echo 📝 Please configure your .env file and run again.
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install fastapi uvicorn motor pydantic python-telegram-bot pyrogram python-dotenv

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo 💡 Try running: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Dependencies installed!

REM Check for MongoDB
echo 🗄️  Checking MongoDB...
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  MongoDB not found in PATH
    echo 💡 Please install MongoDB or use MongoDB Atlas
    echo 💡 Set MONGO_URL in .env to your connection string
)

REM Start backend server
echo.
echo 🌐 Starting Lucky Wheel Backend Server...
cd ATA-main\ATA-main\ATA\app\backend

if not exist "server.py" (
    echo ❌ Backend server file not found!
    echo 💡 Please make sure you're in the correct directory
    pause
    exit /b 1
)

echo 🚀 Starting backend server on port 8000...
echo 📚 API will be available at: http://localhost:8000
echo 🎨 Frontend should be started separately
echo.

REM Start the server
python server.py

pause