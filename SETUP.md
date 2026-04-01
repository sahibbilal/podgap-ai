# PodGap AI - Local Development Setup

## ✅ Fixed Issues
- CORS configuration now includes port 3002 (frontend's port)
- SQLite configured for local dev (no C++ build tools needed)
- Redis/RabbitMQ configured to use localhost (your Docker containers)
- JWT settings properly configured
- Global error handling added

## 🚀 Quick Start

### 1. Start Docker Services
```bash
docker compose up -d db redis rabbitmq
```

### 2. Start Backend (Python)
```bash
cd backend
python run.py
```

Backend will be available at:
- API: http://localhost:8000/api/v1
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 3. Start Frontend (Next.js)
```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:3002

## 🔍 Testing

Test backend health:
```bash
cd backend
python test_server.py
```

## 📋 Configuration

### Backend (.env)
- Uses SQLite by default (no PostgreSQL/asyncpg needed)
- Connects to Redis at localhost:6379
- Connects to RabbitMQ at localhost:5672
- CORS allows ports 3000, 3001, 3002

### Frontend (.env)
- API URL: http://localhost:8000/api/v1

## 🐛 Troubleshooting

### CORS Errors
✅ FIXED - Frontend port 3002 now included in CORS config

### NetworkError
- Make sure backend is running on port 8000
- Check `http://localhost:8000/health` in browser
- Restart backend after config changes

### Database Errors
- Using SQLite (no C++ build tools needed)
- Database file: `backend/podgap.db`
- Auto-created on first run
