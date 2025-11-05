#!/usr/bin/env python3
"""
Lucky Wheel System Startup Script
This script helps start both backend server and shows instructions for frontend
"""

import os
import subprocess
import time
import signal
import sys
import asyncio
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("🎰" + "="*60 + "🎰")
    print("        LUCKY WHEEL ROULETTE SYSTEM")
    print("🎰" + "="*60 + "🎰")
    print()

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Creating .env file from example...")
        example_env = Path(".env.example")
        if example_env.exists():
            example_env.rename(env_file)
            print("📝 Please edit .env file with your actual values!")
            print("🔑 Required variables:")
            print("   - TELEGRAM_BOT_TOKEN")
            print("   - TELEGRAM_GROUP_ID") 
            print("   - OWNER_ID")
            print("   - MONGO_URL")
            print("   - API_ID (for main bot)")
            print("   - API_HASH (for main bot)")
            print()
            return False
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "fastapi", "uvicorn[standard]", "motor", "pydantic",
            "python-telegram-bot", "pyrogram", "python-dotenv"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("🌐 Starting Lucky Wheel Backend Server...")
    
    # Change to backend directory
    backend_dir = Path("ATA-main/ATA-main/ATA/app/backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return None
        
    os.chdir(backend_dir)
    
    # Start server
    try:
        process = subprocess.Popen([
            sys.executable, "server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def main():
    """Main function to start the system"""
    print_banner()
    
    # Check environment
    if not check_env_file():
        print("📝 Please configure your .env file and run again.")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please install manually.")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server.")
        return
    
    # Wait a moment for server to start
    time.sleep(3)
    
    # Check if backend is running
    if backend_process.poll() is None:
        print("✅ Backend server started successfully!")
        print("🌐 Backend URL: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print()
        
        print("🎨 FRONTEND SETUP:")
        print("1. Open new terminal")
        print("2. Navigate to: cd ATA-main/ATA-main/ATA")
        print("3. Install frontend dependencies:")
        print("   npm install")
        print("4. Start frontend:")
        print("   npm run dev")
        print()
        print("🌐 Frontend URL: http://localhost:5173")
        print()
        print("🎮 TELEGRAM BOT COMMANDS:")
        print("   /activate - Open main game menu")
        print("   /mytickets - Check your tickets")
        print("   /buyticket [amount] - Buy tickets")
        print()
        print("🎰 WEB LUCKY WHEEL:")
        print("   Visit http://localhost:5173 to play via web!")
        print()
        print("🛑 Press Ctrl+C to stop the server")
        
        # Keep running and show logs
        try:
            while True:
                # Check if process is still running
                if backend_process.poll() is not None:
                    print("❌ Backend server stopped unexpectedly")
                    break
                    
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            backend_process.terminate()
            backend_process.wait()
            print("✅ Server stopped")

if __name__ == "__main__":
    main()