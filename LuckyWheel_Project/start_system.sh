#!/bin/bash

echo "🚀 Starting Lucky Wheel System..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your actual values!"
    echo "🔑 Required variables:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_GROUP_ID" 
    echo "   - OWNER_ID"
    echo "   - MONGO_URL"
    echo "   - API_ID"
    echo "   - API_HASH"
    echo ""
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt 2>/dev/null || echo "⚠️  requirements.txt not found, installing manually..."

# Install required packages
pip install fastapi uvicorn motor pydantic python-telegram-bot pyrogram

# Check MongoDB
echo "🗄️  Checking MongoDB..."
if command -v mongod &> /dev/null; then
    echo "✅ MongoDB found"
    # Start MongoDB if not running
    if ! pgrep -x "mongod" > /dev/null; then
        echo "🔄 Starting MongoDB..."
        mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db
    fi
else
    echo "⚠️  MongoDB not found. Please install MongoDB or use MongoDB Atlas."
    echo "💡 For cloud MongoDB: Set MONGO_URL to your MongoDB Atlas connection string"
fi

# Start backend server
echo "🌐 Starting backend server on port 8000..."
cd app/backend
python server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend (if available)
echo "🎨 Starting frontend..."
cd ../frontend
if command -v npm &> /dev/null; then
    npm install
    npm start &
    FRONTEND_PID=$!
else
    echo "⚠️  npm not found. Install Node.js to run frontend."
fi

echo ""
echo "✅ System started!"
echo "🌐 Backend API: http://localhost:8000"
echo "🎨 Frontend: http://localhost:3000"
echo ""
echo "📋 Commands:"
echo "   /activate - Main game menu (Telegram)"
echo "   Web Lucky Wheel - http://localhost:3000"
echo ""
echo "🛑 To stop: kill $BACKEND_PID $FRONTEND_PID"

# Keep script running
wait