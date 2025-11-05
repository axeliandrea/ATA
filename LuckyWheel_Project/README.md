# 🎰 Lucky Wheel Roulette - Ready to Deploy

## 🚀 Quick Deploy Guide

### 1. **Extract Files**
```bash
# Extract zip file ke direktori yang Anda inginkan
unzip LuckyWheel_Project.zip
cd LuckyWheel_Project
```

### 2. **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit .env dengan konfigurasi Anda:
nano .env  # atau editor favorite Anda
```

**Required Variables di `.env`:**
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here
OWNER_ID=your_owner_id_here

# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=lucky_wheel_db

# Frontend Configuration  
REACT_APP_BACKEND_URL=http://localhost:8000

# Pyrogram Configuration (Main Bot)
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_main_bot_token_here
```

### 3. **One-Command Start** (Recommended)
```bash
python run_lucky_wheel.py
```

### 4. **Or Manual Setup**
```bash
# Terminal 1 - Backend
pip install -r requirements.txt
cd app/backend && python server.py

# Terminal 2 - Frontend  
cd ../../
npm install
npm run dev

# Terminal 3 - Telegram Bot
python __main__.py
```

## 🌐 Access Points

| Service | URL |
|---------|-----|
| **Web Lucky Wheel** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |
| **Telegram Bot** | Kirim `/activate` ke bot |

## 📋 Features Included

✅ **Command `/activate`** - Main MMORPG game menu  
✅ **Lucky Wheel Web Interface** - Full featured web interface  
✅ **Telegram Bot Integration** - Complete bot functionality  
✅ **MongoDB Database** - User data and history  
✅ **API Endpoints** - RESTful API for all features  
✅ **Responsive Design** - Mobile and desktop ready  
✅ **Admin Panel** - Owner commands and management  

## 🎮 Commands

### Telegram Bot Commands:
- `/activate` - Open main game menu
- `/start` - Register new user
- `/mytickets` - Check tickets & points  
- `/buyticket [amount]` - Buy tickets (25 points = 1 ticket)
- `/giveticket [amount]` - Giveaway tickets (owner only)

### Web Interface:
- Login dengan Telegram ID
- Spin Lucky Wheel dengan animasi
- View win history
- Real-time statistics

## 📁 Project Structure

```
LuckyWheel_Project/
├── 📄 README.md                 # This file
├── 🚀 run_lucky_wheel.py        # Main startup script
├── 💻 start_lucky_wheel.bat     # Windows startup script
├── 📋 requirements.txt          # Python dependencies
├── 📋 package.json              # Node.js dependencies
├── ⚙️ .env.example             # Environment template
├── 🐍 __main__.py              # Telegram bot main
├── 🖥️ app/
│   ├── 🌐 backend/
│   │   └── server.py           # FastAPI backend
│   └── 🎨 frontend/
│       └── src/
│           └── components/
│               └── LuckyWheel.jsx # Lucky wheel component
├── 🎯 modules/
│   ├── ata_menu.py              # Game menu (contains /activate)
│   ├── menu_*.py               # Game modules
│   └── cekid.py                # ID checker
├── 📄 Documentation/
│   ├── LUCKY_WHEEL_GUIDE.md    # Complete guide
│   ├── PERBAIKAN_LAPORAN.md    # Fix report
│   └── QUICK_START.md          # Quick start
└── 📊 data/
    └── userbots.json.txt       # User data
```

## 🔧 Production Deployment

### Backend (Heroku/Railway/Deploy)
```bash
# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set MONGO_URL=your_mongodb_atlas_url
heroku config:set REACT_APP_BACKEND_URL=https://your-backend-url.com

# Deploy backend
git add . && git commit -m "Deploy backend"
git push origin main
```

### Frontend (Vercel/Netlify)
```bash
# Build production
npm run build

# Deploy to Vercel
vercel --prod
# or to Netlify
netlify deploy --prod --dir=dist
```

### Database (MongoDB Atlas)
- Create MongoDB Atlas cluster
- Get connection string
- Set MONGO_URL di environment variables

## 🛡️ Security Notes

1. **Never commit `.env` file**
2. **Use strong tokens and secrets**
3. **Set CORS origins for production**
4. **Enable rate limiting**
5. **Use HTTPS in production**

## 📞 Support

- **Documentation**: Check all .md files for detailed guides
- **Troubleshooting**: See QUICK_START.md for common issues
- **API Testing**: Visit http://localhost:8000/docs for API docs

---

**🎰 Ready to deploy and start winning! Good luck! 🍀**

## Quick Start Commands

```bash
# Extract and go
cd LuckyWheel_Project

# Setup
cp .env.example .env

# Edit .env with your values, then:
python run_lucky_wheel.py

# Access: http://localhost:5173
# Telegram: /activate command