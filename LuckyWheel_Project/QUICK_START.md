# 🚀 QUICK START GUIDE - Lucky Wheel Roulette

## ⚡ Setup in 5 Minutes

### 1. **Setup Environment** (1 menit)
```bash
cd ATA-main/ATA-main/ATA
cp .env.example .env
```
Edit `.env` dengan data Anda:
- `TELEGRAM_BOT_TOKEN=your_token`
- `TELEGRAM_GROUP_ID=group_id`
- `MONGO_URL=mongodb://localhost:27017`

### 2. **Start Backend** (1 menit)
```bash
# Install dependencies
pip install fastapi uvicorn motor pydantic python-telegram-bot pyrogram

# Start server
cd app/backend
python server.py
```

### 3. **Start Frontend** (1 menit)
```bash
# New terminal
cd ATA-main/ATA-main/ATA
npm install
npm run dev
```

### 4. **Start Telegram Bot** (1 menit)
```bash
# New terminal  
cd ATA-main/ATA-main/ATA
python __main__.py
```

### 5. **Test System** (1 menit)
- 🌐 Web: http://localhost:5173
- 📱 Telegram: `/activate`
- 📚 API: http://localhost:8000

---

## 🎮 COMMAND CHEAT SHEET

### Telegram Bot
- `/activate` - Main menu game
- `/start` - Register user
- `/mytickets` - Check tickets & points
- `/buyticket 5` - Buy 5 tickets
- `/giveticket 3` - Give away tickets

### Web Interface
- Login dengan Telegram ID
- Click tombol "SPIN THE WHEEL!"
- Lihat history kemenangan

### API Endpoints
- `GET /api/prizes` - Daftar hadiah
- `POST /api/spin` - Putar lucky wheel
- `GET /api/health` - Health check

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Backend error port 8000 | Tutup aplikasi lain yang pakai port 8000 |
| MongoDB connection error | Install MongoDB atau pakai MongoDB Atlas |
| Frontend can't connect backend | Pastikan backend running di port 8000 |
| Bot not responding | Cek BOT_TOKEN di .env |
| Can't spin wheel | User harus punya tiket (minimal 1) |

---

## 📞 NEED HELP?

1. **Check logs** di terminal untuk error messages
2. **Test API** dengan curl: `curl http://localhost:8000/api/health`
3. **Read full documentation** di `LUCKY_WHEEL_GUIDE.md`

**🎰 Ready to play? Good luck! 🍀**