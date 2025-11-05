#!/usr/bin/env python3
"""
Advanced Lucky Wheel System Startup Script
Features: Auto-restart, logging, monitoring, multiple startup methods
"""

import os
import sys
import subprocess
import time
import signal
import json
import logging
from pathlib import Path
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lucky_wheel.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LuckyWheelManager:
    def __init__(self):
        self.processes = {}
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from .env file"""
        config = {}
        env_file = Path(".env")
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value.strip('"\'')
        return config
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        logger.info("🔍 Checking dependencies...")
        
        # Check Python packages
        required_packages = [
            'fastapi', 'uvicorn', 'motor', 'pydantic',
            'python-telegram-bot', 'pyrogram', 'python-dotenv'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"  ❌ {package}")
        
        if missing_packages:
            logger.info("📦 Installing missing packages...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install"
                ] + missing_packages, check=True)
                logger.info("✅ Dependencies installed!")
            except subprocess.CalledProcessError:
                logger.error("❌ Failed to install dependencies")
                return False
        
        # Check Node.js (optional)
        try:
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            logger.info("✅ Node.js found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️ Node.js not found (required for frontend)")
        
        return True
    
    def check_mongodb(self):
        """Check MongoDB connection"""
        logger.info("🗄️ Checking MongoDB...")
        
        mongo_url = self.config.get('MONGO_URL', 'mongodb://localhost:27017')
        
        try:
            # Simple MongoDB ping (basic check)
            if 'localhost' in mongo_url:
                result = subprocess.run(['mongosh', '--eval', 'db.runCommand("ping")'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logger.info("✅ MongoDB is running")
                    return True
                else:
                    logger.warning("⚠️ MongoDB may not be running")
            else:
                logger.info("✅ Using external MongoDB (MongoDB Atlas)")
                return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("⚠️ Could not verify MongoDB connection")
        
        return False
    
    def start_backend(self):
        """Start the FastAPI backend server"""
        logger.info("🌐 Starting backend server...")
        
        backend_dir = Path("app/backend")
        if not backend_dir.exists():
            logger.error("❌ Backend directory not found!")
            return None
        
        # Change to backend directory
        os.chdir(backend_dir)
        
        try:
            process = subprocess.Popen([
                sys.executable, "server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a bit and check if it's still running
            time.sleep(3)
            if process.poll() is None:
                self.processes['backend'] = process
                logger.info("✅ Backend server started successfully!")
                return process
            else:
                logger.error("❌ Backend server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to start backend: {e}")
            return None
    
    def start_frontend(self):
        """Start the React frontend (optional)"""
        logger.info("🎨 Starting frontend...")
        
        frontend_dir = Path("../frontend")
        if not frontend_dir.exists():
            logger.warning("⚠️ Frontend directory not found")
            return None
        
        try:
            # Check if npm is available
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
            
            os.chdir(frontend_dir.parent)
            
            process = subprocess.Popen([
                'npm', 'run', 'dev'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)
            if process.poll() is None:
                self.processes['frontend'] = process
                logger.info("✅ Frontend started successfully!")
                return process
            else:
                logger.warning("⚠️ Frontend failed to start")
                return None
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️ npm not found or frontend build failed")
            return None
    
    def start_telegram_bot(self):
        """Start the Telegram bot"""
        logger.info("🤖 Starting Telegram bot...")
        
        main_dir = Path("../..")
        if not main_dir.exists():
            logger.warning("⚠️ Main bot directory not found")
            return None
        
        try:
            os.chdir(main_dir)
            
            process = subprocess.Popen([
                sys.executable, "__main__.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)
            if process.poll() is None:
                self.processes['bot'] = process
                logger.info("✅ Telegram bot started successfully!")
                return process
            else:
                logger.warning("⚠️ Telegram bot failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            return None
    
    def check_services(self):
        """Check if all services are running"""
        logger.info("🔍 Checking services...")
        
        services_status = {}
        
        # Check backend
        if 'backend' in self.processes:
            try:
                response = requests.get('http://localhost:8000/api/health', timeout=5)
                services_status['backend'] = response.status_code == 200
            except:
                services_status['backend'] = False
        else:
            services_status['backend'] = False
        
        # Check frontend
        if 'frontend' in self.processes:
            try:
                response = requests.get('http://localhost:5173', timeout=5)
                services_status['frontend'] = response.status_code == 200
            except:
                services_status['frontend'] = False
        else:
            services_status['frontend'] = False
        
        # Report status
        for service, status in services_status.items():
            status_emoji = "✅" if status else "❌"
            logger.info(f"  {status_emoji} {service.title()}")
        
        return all(services_status.values())
    
    def start_all(self):
        """Start all services"""
        logger.info("🚀 Starting Lucky Wheel System...")
        
        # Setup
        if not self.check_dependencies():
            logger.error("❌ Dependency check failed")
            return False
        
        self.check_mongodb()
        
        # Start services
        backend = self.start_backend()
        if not backend:
            logger.error("❌ Failed to start backend, stopping...")
            return False
        
        # Optional frontend
        self.start_frontend()
        
        # Optional bot
        self.start_telegram_bot()
        
        # Check all services
        time.sleep(5)
        if self.check_services():
            logger.info("✅ All services are running!")
            return True
        else:
            logger.warning("⚠️ Some services may not be running properly")
            return True
    
    def stop_all(self):
        """Stop all running processes"""
        logger.info("🛑 Stopping all services...")
        
        for name, process in self.processes.items():
            try:
                logger.info(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {name}...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")
        
        self.processes.clear()
    
    def show_status(self):
        """Show current status"""
        print("\n" + "="*50)
        print("🎰 LUCKY WHEEL SYSTEM STATUS")
        print("="*50)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Processes: {len(self.processes)}")
        
        for name, process in self.processes.items():
            status = "Running" if process.poll() is None else "Stopped"
            print(f"  {name.title()}: {status}")
        
        if 'backend' in self.processes:
            print(f"🌐 Backend: http://localhost:8000")
            print(f"📚 API Docs: http://localhost:8000/docs")
        
        if 'frontend' in self.processes:
            print(f"🎨 Frontend: http://localhost:5173")
        
        print(f"🎮 Bot Command: /activate")
        print("="*50 + "\n")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutdown signal received...")
    manager.stop_all()
    sys.exit(0)

def main():
    global manager
    manager = LuckyWheelManager()
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🎰" + "="*48 + "🎰")
    print("       LUCKY WHEEL ROULETTE SYSTEM")
    print("🎰" + "="*48 + "🎰")
    
    # Check if .env exists
    if not Path(".env").exists():
        logger.warning("⚠️ .env file not found!")
        if Path(".env.example").exists():
            logger.info("📝 Creating .env from template...")
            Path(".env.example").rename(".env")
            logger.info("📝 Please edit .env file with your configuration!")
            logger.info("🔑 Required variables:")
            logger.info("   - TELEGRAM_BOT_TOKEN")
            logger.info("   - TELEGRAM_GROUP_ID")
            logger.info("   - OWNER_ID")
            logger.info("   - MONGO_URL")
            logger.info("   - API_ID, API_HASH, BOT_TOKEN")
            return
    
    # Start all services
    if not manager.start_all():
        logger.error("❌ Failed to start services")
        return
    
    # Show status
    manager.show_status()
    
    logger.info("🎰 System is ready! Press Ctrl+C to stop.")
    
    try:
        # Monitor services
        while True:
            time.sleep(30)  # Check every 30 seconds
            manager.show_status()
            
            # Restart failed processes
            for name, process in list(manager.processes.items()):
                if process.poll() is not None:
                    logger.warning(f"⚠️ {name} stopped unexpectedly, restarting...")
                    time.sleep(2)
                    if name == 'backend':
                        manager.start_backend()
                    elif name == 'frontend':
                        manager.start_frontend()
                    elif name == 'bot':
                        manager.start_telegram_bot()
                        
    except KeyboardInterrupt:
        pass
    finally:
        manager.stop_all()
        logger.info("✅ System stopped cleanly")

if __name__ == "__main__":
    main()