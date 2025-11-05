#!/bin/bash
# Lucky Wheel Startup Script - Ubuntu Optimized

echo "🎰 ==================== LUCKY WHEEL SYSTEM ==================== 🎰"
echo "                LUCKY WHEEL ROULETTE SYSTEM"
echo "🎰 ========================================================== 🎰"
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Working directory: $SCRIPT_DIR"

# Check .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "🔑 Creating .env file template..."
    cat > .env << EOF
# Telegram Bot Configuration
API_ID=21907798
API_HASH=4b2a03775b7c4850dac648f921a70ff8
BOT_TOKEN=7706718688:AAFbLJ3H0ei7BC4ADaUf_KYH8jwGZNA8KCs
OWNER_ID=6395738130

# Database Configuration  
MONGO_URL=mongodb://localhost:27017
DB_NAME=ata_bot

# Lucky Wheel Backend URL
REACT_APP_BACKEND_URL=http://localhost:8000
EOF
    echo "⚠️  Please edit .env file with your actual values!"
    echo
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# Install required packages
python3 -m pip install fastapi uvicorn[standard] motor pydantic python-telegram-bot pyrogram python-dotenv

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please install manually:"
    echo "   pip3 install fastapi uvicorn[standard] motor pydantic python-telegram-bot pyrogram python-dotenv"
    exit 1
fi

echo "✅ Dependencies installed!"

# Find backend directory
BACKEND_DIR=""
for path in "app/backend" "backend" "ATA-main/ATA-main/ATA/app/backend"; do
    if [ -d "$path" ]; then
        BACKEND_DIR="$path"
        echo "✅ Found backend at: $BACKEND_DIR"
        break
    fi
done

if [ -z "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found!"
    echo "🔍 Searched in:"
    echo "   - $SCRIPT_DIR/app/backend"
    echo "   - $SCRIPT_DIR/backend"
    echo "   - $SCRIPT_DIR/ATA-main/ATA-main/ATA/app/backend"
    exit 1
fi

# Start backend server
echo "🌐 Starting Lucky Wheel Backend Server..."
cd "$BACKEND_DIR"

# Check if server.py exists
if [ ! -f server.py ]; then
    echo "❌ server.py not found in $BACKEND_DIR"
    exit 1
fi

echo "🚀 Starting FastAPI server..."
echo "💡 Backend will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo
echo "🎮 FRONTEND SETUP (run in new terminal):"
echo "   cd $SCRIPT_DIR"
echo "   npm install (if not done)"
echo "   npm run dev"
echo
echo "🌐 Frontend will be available at: http://localhost:5173"
echo
echo "🛑 Press Ctrl+C to stop the server"
echo "============================================"

# Start the server
python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
