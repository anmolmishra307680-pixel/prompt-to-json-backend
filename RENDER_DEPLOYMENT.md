# 🚀 Render Deployment Guide - BHIV Backend

## ✅ Ready for Render Deployment

### 📋 Pre-configured Files:
- ✅ `render.yaml` - Auto-deployment configuration
- ✅ `main_api.py` - Production scaling (4 workers, 1000 connections)
- ✅ `Dockerfile` - Multi-stage production build
- ✅ `.env.example` - Supabase configuration template
- ✅ `load_test.py` - 50 concurrent user testing

## 🔧 Deployment Steps

### 1. Setup Supabase (BHIV Bucket)
```bash
# 1. Go to supabase.com
# 2. Create new project
# 3. Go to Settings → Database
# 4. Copy connection string
```

### 2. Deploy to Render
```bash
# Push to GitHub
git add .
git commit -m "Deploy BHIV backend to Render"
git push origin main

# Go to render.com:
# 1. New → Web Service
# 2. Connect GitHub repository
# 3. Render auto-detects render.yaml
# 4. Click "Create Web Service"
```

### 3. Environment Variables (Render Dashboard)
```
DATABASE_URL = postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
OPENAI_API_KEY = your_openai_api_key
PRODUCTION_MODE = true
```

### 4. Verify Deployment
```bash
# Health check
curl https://your-app.onrender.com/health

# Test API
curl -X POST "https://your-app.onrender.com/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Modern office building"}'

# Test 50 concurrent users
python load_test.py
```

## 📊 Render Configuration (Auto-Applied)

### Scaling Settings:
- **Workers**: 4 (for 50+ concurrent users)
- **Connections**: 1000 per worker
- **Auto-scaling**: 1-10 instances
- **Health checks**: `/health` endpoint
- **Timeout**: 30s keep-alive

### Expected Performance:
- **Concurrent Users**: 50+ supported
- **Response Time**: < 2 seconds
- **Throughput**: 100+ requests/second
- **Uptime**: 99.9% with auto-restart

## 🎯 Production Features

### ✅ BHIV Integration Ready:
- All agents expose `run()` methods
- Database operations via Supabase
- Complete logging system
- Error handling with fallbacks

### ✅ API Endpoints (10 total):
- `/generate` - Specification generation
- `/evaluate` - Evaluation with reports
- `/iterate` - RL training with logs
- `/advanced-rl` - Policy gradient training
- `/log-values` - HIDG values logging
- `/health` - System monitoring
- And 4 more endpoints...

### ✅ File Generation:
- `logs/iteration_logs.json`
- `logs/feedback_log.json`
- `logs/values_log.json`
- `spec_outputs/design_spec_*.json`

## 🔍 Monitoring

### Health Monitoring:
```bash
# Check system health
curl https://your-app.onrender.com/health

# Check database connection
curl https://your-app.onrender.com/admin/prune-logs
```

### Performance Testing:
```bash
# Load test 50 users
python load_test.py

# Expected results:
# - 50 requests completed
# - < 5 second total time
# - > 90% success rate
```

## 🎉 Deployment Complete!

**Your BHIV backend is now:**
- ✅ Deployed on Render with auto-scaling
- ✅ Connected to Supabase (BHIV Bucket)
- ✅ Optimized for 50+ concurrent users
- ✅ Production-ready with monitoring
- ✅ Ready for BHIV Core integration

**🚀 Access your deployed API at: `https://your-app.onrender.com`**