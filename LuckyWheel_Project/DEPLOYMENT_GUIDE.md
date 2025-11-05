# 🚀 PRODUCTION DEPLOYMENT GUIDE

## 📋 Pre-Deployment Checklist

### ✅ **Environment Variables Required**
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here
OWNER_ID=your_owner_id_here

# Database Configuration
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority
DB_NAME=lucky_wheel_prod

# Frontend Configuration
REACT_APP_BACKEND_URL=https://your-backend-domain.com

# Pyrogram Configuration
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_main_bot_token
```

---

## 🌍 Option 1: Railway Deployment (Recommended)

### Backend Deployment
1. **Create account di railway.app**
2. **Create new project**
3. **Connect GitHub repository**
4. **Set environment variables** di Railway dashboard:
   ```
   TELEGRAM_BOT_TOKEN=your_token
   MONGO_URL=your_mongodb_atlas_url
   DB_NAME=lucky_wheel_prod
   REACT_APP_BACKEND_URL=https://your-railway-backend.up.railway.app
   ```
5. **Deploy**: Railway akan otomatis deploy dari GitHub

### Frontend Deployment
1. **Install Railway CLI**: `npm install -g @railway/cli`
2. **Login**: `railway login`
3. **Deploy**: `railway deploy`
4. **Set backend URL**: Edit `src/App.tsx` atau environment

---

## 🌍 Option 2: Heroku Deployment

### Backend Setup
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-lucky-wheel-backend

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set MONGO_URL=your_mongodb_url
heroku config:set DB_NAME=lucky_wheel_prod
heroku config:set REACT_APP_BACKEND_URL=https://your-lucky-wheel-frontend.herokuapp.com

# Add Procfile
echo "web: uvicorn app.backend.server:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Deploy
git add . && git commit -m "Deploy to Heroku" && git push heroku main
```

### Frontend Setup
```bash
# Install Heroku CLI
heroku create your-lucky-wheel-frontend

# Set buildpack
heroku buildpacks:set heroku/nodejs

# Deploy
git add . && git commit -m "Deploy frontend" && git push heroku main
```

---

## 🌍 Option 3: DigitalOcean + Docker

### Backend (Docker)
```dockerfile
# Dockerfile for backend
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.backend.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and deploy
docker build -t lucky-wheel-backend .
docker run -p 8000:8000 \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e MONGO_URL=your_url \
  lucky-wheel-backend
```

### Frontend (Docker)
```dockerfile
# Dockerfile for frontend
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## 🌍 Option 4: Vercel + MongoDB Atlas

### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy frontend
vercel --prod
```

### Backend Configuration
Edit `app/backend/server.py` untuk production:

```python
# Add production CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add production settings
import os
PORT = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
```

---

## 🔒 Security Configuration

### 1. **Environment Security**
```bash
# Never commit .env files
echo ".env" >> .gitignore
echo ".env*" >> .gitignore
```

### 2. **CORS Configuration**
```python
# Production CORS
allowed_origins = [
    "https://your-domain.com",
    "https://www.your-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 3. **Rate Limiting (Optional)**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
async def spin_roulette(request: Request, spin_request: SpinRequest):
    # Your spin logic
```

---

## 📊 Database Setup (MongoDB Atlas)

### 1. **Create MongoDB Atlas Account**
- Go to https://www.mongodb.com/atlas
- Create free cluster
- Get connection string

### 2. **Database Collections**
Collections akan dibuat otomatis:
- `users` - User data
- `spin_history` - Lucky wheel history  
- `ticket_claims` - Ticket giveaway data

### 3. **Indexes (Optional)**
```javascript
// Add indexes for better performance
db.users.createIndex({"telegram_id": 1})
db.spin_history.createIndex({"telegram_id": 1, "timestamp": -1})
db.ticket_claims.createIndex({"message_id": 1})
```

---

## 🔧 Environment Variable Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token untuk Lucky Wheel | Yes | `1234567890:ABC...` |
| `TELEGRAM_GROUP_ID` | Group ID untuk giveaways | Yes | `-1001234567890` |
| `OWNER_ID` | Telegram ID owner | Yes | `1234567890` |
| `MONGO_URL` | MongoDB connection string | Yes | `mongodb+srv://...` |
| `DB_NAME` | Database name | Yes | `lucky_wheel_prod` |
| `REACT_APP_BACKEND_URL` | Backend API URL | Yes | `https://api.yourapp.com` |
| `API_ID` | Telegram API ID (main bot) | Yes | `123456` |
| `API_HASH` | Telegram API Hash (main bot) | Yes | `abc123...` |
| `BOT_TOKEN` | Main bot token | Yes | `1234567890:DEF...` |

---

## 🛠️ Troubleshooting Production Issues

### Backend Issues
1. **CORS Errors**: Check CORS_ORIGINS in environment
2. **MongoDB Connection**: Verify MONGO_URL is correct
3. **Bot Token**: Ensure TELEGRAM_BOT_TOKEN is valid
4. **Port Issues**: Use PORT environment variable

### Frontend Issues  
1. **API Calls**: Check REACT_APP_BACKEND_URL environment variable
2. **Build Errors**: Ensure all dependencies are in package.json
3. **Domain Issues**: Update API URL for production domain

### Telegram Bot Issues
1. **Bot not responding**: Check BOT_TOKEN and webhook settings
2. **Commands not working**: Verify bot permissions in group
3. **Database issues**: Check MongoDB connection in logs

---

## 📞 Post-Deployment Testing

### 1. **Backend API Test**
```bash
# Health check
curl https://your-backend-url.com/api/health

# Test spin endpoint
curl -X POST https://your-backend-url.com/api/spin \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": 123456}'
```

### 2. **Frontend Test**
1. Open https://your-frontend-url.com
2. Login dengan Telegram ID
3. Test lucky wheel functionality
4. Check responsive design

### 3. **Telegram Bot Test**
1. Start bot dengan `/start`
2. Test `/activate` command
3. Test `/mytickets` functionality
4. Verify group integration

---

## 💰 Cost Estimates (Monthly)

| Service | Free Tier | Paid Plans |
|---------|-----------|------------|
| **Railway** | 1000 hours | $5-20/month |
| **Heroku** | Limited | $7-25/month |
| **Vercel** | 100GB bandwidth | $20/month |
| **MongoDB Atlas** | 512MB | $9-57/month |
| **DigitalOcean** | - | $5-12/month |

**Total estimated cost: $15-50/month for full production**

---

**🎰 Deploy and start earning! Good luck! 🍀**