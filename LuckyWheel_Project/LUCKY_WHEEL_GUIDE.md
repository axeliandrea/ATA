# 🎰 Lucky Wheel Roulette - Sistem Lengkap

Sistem game MMORPG dengan fitur Lucky Wheel yang bisa diakses melalui Telegram dan Web Interface.

## 📋 Fitur Utama

✅ **Command `/activate`** - Menu game MMORPG lengkap  
✅ **Lucky Wheel Web Interface** - Interface web yang menarik  
✅ **Telegram Integration** - Bot Telegram untuk mobile gaming  
✅ **MongoDB Database** - Penyimpanan data user dan history  
✅ **Real-time API** - Backend FastAPI yang responsive  

## 🚀 Cara Menjalankan Sistem

### 1. Persiapan Environment

```bash
# 1. Copy file project ke direktori Anda
# 2. Masuk ke direktori project
cd ATA-main/ATA-main/ATA

# 3. Konfigurasi environment
cp .env.example .env
# Edit file .env dengan data Anda:
```

**Variabel yang diperlukan di `.env`:**
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

### 2. Menjalankan Backend Server

```bash
# Install dependencies Python
pip install -r requirements.txt

# Install additional packages yang diperlukan
pip install fastapi uvicorn motor pydantic python-telegram-bot pyrogram

# Jalankan backend server
cd app/backend
python server.py
```

Backend akan berjalan di: `http://localhost:8000`

### 3. Menjalankan Frontend Web

```bash
# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

Frontend akan berjalan di: `http://localhost:5173`

### 4. Menjalankan Bot Telegram

```bash
# Dari direktori utama
python __main__.py
```

## 🎮 Cara Menggunakan

### Via Telegram Bot

1. **Start Bot**: Kirim `/start` ke bot Anda
2. **Main Menu**: Kirim `/activate` untuk buka menu game
3. **Menu yang Tersedia**:
   - 📝 REGISTER - Pendaftaran user
   - ⚔️ MY HERO - Kelola karakter hero
   - 🏰 DUNGEON - Petualangan dungeon
   - 🎒 BAG - Inventory item
   - ACHIEVEMENT - Pencapaian game

### Via Web Interface

1. **Buka Browser**: http://localhost:5173
2. **Login**: Masukkan Telegram ID Anda
3. **Spin Lucky Wheel**: Klik tombol untuk putar roda
4. **Lihat History**: Lihat riwayat kemenangan

### Command Telegram Bot

- `/activate` - Buka main menu game
- `/mytickets` - Cek tiket dan points
- `/buyticket [amount]` - Beli tiket dengan points (25 points = 1 tiket)
- `/giveticket [amount]` - Beri giveaway tiket (hanya owner)
- `/start` - Register user baru
- `/help` - Tampilkan bantuan

## 🗄️ Database Structure

### Collections MongoDB:

1. **users** - Data user game
   ```json
   {
     "telegram_id": 123456,
     "username": "user123",
     "first_name": "John",
     "tickets": 5,
     "points": 100,
     "total_spins": 10,
     "created_at": "2024-01-01T00:00:00Z"
   }
   ```

2. **spin_history** - Riwayat lucky wheel
   ```json
   {
     "id": "uuid",
     "telegram_id": 123456,
     "username": "user123", 
     "prize": "Gold 100",
     "timestamp": "2024-01-01T00:00:00Z"
   }
   ```

3. **ticket_claims** - Data giveaway tiket
   ```json
   {
     "message_id": 123,
     "ticket_amount": 3,
     "claimed_by": [123456, 789012],
     "expires_at": "2024-01-01T00:01:00Z",
     "created_at": "2024-01-01T00:00:00Z"
   }
   ```

## 🏆 Prize System

**Hadiah Lucky Wheel:**
- Gold 100 💰
- Silver 50 🥈
- Bronze 25 🥉
- Jackpot 1000 🎯
- Diamond 💎
- Ruby 🔴
- Emerald 🟢
- Sapphire 🔵
- Pearl ⚪
- Lucky Star ⭐

## 📱 API Endpoints

### User Management
- `GET /api/user/{telegram_id}` - Get user data
- `GET /api/user/{telegram_id}/stats` - Get user statistics

### Lucky Wheel
- `GET /api/prizes` - Get available prizes
- `POST /api/spin` - Spin the wheel
- `GET /api/history/{telegram_id}` - Get spin history

### Health Check
- `GET /api/` - API information
- `GET /api/health` - Health check status

## 🔧 Troubleshooting

### Backend tidak bisa start:
1. Pastikan MongoDB sudah running
2. Cek konfigurasi .env file
3. Pastikan port 8000 tidak digunakan

### Frontend tidak connect ke backend:
1. Pastikan backend sudah running di port 8000
2. Cek REACT_APP_BACKEND_URL di .env
3. Buka browser developer tools untuk error

### Telegram Bot tidak respond:
1. Pastikan BOT_TOKEN valid
2. Cek OWNER_ID sudah benar
3. Pastikan bot sudah di-start dengan `/start`

### Lucky Wheel tidak bisa spin:
1. Pastikan user punya tiket (minimal 1)
2. Cek console untuk error API
3. Verify MongoDB connection

## 🚀 Deployment

### Production Deployment:
1. **Backend**: Deploy ke cloud (Heroku, Railway, etc.)
2. **Frontend**: Deploy ke Vercel/Netlify
3. **Database**: MongoDB Atlas
4. **Environment**: Set production variables

### Security:
- Never commit .env file
- Use environment variables in production
- Enable CORS only for your domain
- Set proper rate limits

## 📞 Support

Jika ada masalah, cek:
1. Console logs untuk error messages
2. MongoDB logs untuk database issues
3. Network tab di browser untuk API calls
4. Bot logs di Telegram untuk bot issues

---

**🎰 Selamat bermain Lucky Wheel Roulette! 🎰**