# 🚀 BHIV Backend Deployment Guide

**Primary Deployment: Render (Recommended)**

## 1. Supabase Setup (BHIV Bucket)

### Create Supabase Project:
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get connection details from Settings > Database

### Configure Environment:
```bash
# Copy and edit environment file
cp .env.example .env

# Add your Supabase credentials:
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=your_anon_key
OPENAI_API_KEY=your_openai_key
```

## 2. Render Deployment

### Deploy to Render:
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Connect to Render
# - Go to render.com
# - Connect GitHub repo
# - Use render.yaml configuration
# - Set environment variables in Render dashboard
```

### Environment Variables in Render:
- `DATABASE_URL`: Your Supabase connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `PRODUCTION_MODE`: true

## 3. Alternative: Docker Deployment

### Local Docker Testing:
```bash
# Build and test locally
docker build -t bhiv-backend .
docker run -p 8000:8000 -e DATABASE_URL=your_supabase_url bhiv-backend

# Test endpoints
curl http://localhost:8000/health
```

## 4. Docker Deployment

### Local Docker:
```bash
# Build and run
docker build -t bhiv-backend .
docker run -p 8000:8000 -e DATABASE_URL=your_supabase_url bhiv-backend
```

### Docker Compose with Supabase:
```bash
# Update docker-compose.yml with Supabase URL
# Run full stack
docker-compose up -d
```

## 5. Load Testing (50 Users)

### Test Concurrent Load:
```bash
# Install dependencies
pip install aiohttp

# Run load test
python load_test.py

# Expected results:
# - 50 concurrent requests
# - < 5 second total time
# - > 90% success rate
```

### Production Scaling:
- **Render**: Auto-scales 1-10 instances
- **Docker**: Use multiple containers with load balancer
- **Local**: Single container for development

## 6. Monitoring

### Health Checks:
```bash
# Check Render deployment health
curl https://your-app.onrender.com/health

# Check local Docker health
curl http://localhost:8000/health
```

### Database Monitoring:
- Monitor Supabase dashboard
- Check connection pool usage
- Monitor query performance

## 7. Production Checklist

- ✅ Supabase database configured
- ✅ Environment variables set
- ✅ Health checks working
- ✅ Load testing passed (50 users)
- ✅ Error handling tested
- ✅ Logging configured
- ✅ Auto-scaling enabled

## 8. Scaling for 50+ Users

### Configuration:
- **Workers**: 4 (configured in render.yaml)
- **Connections**: 1000 per worker
- **Timeout**: 30s keep-alive
- **Database**: Connection pooling enabled
- **Auto-scaling**: 1-10 instances on Render

### Expected Performance:
- **Throughput**: 100+ requests/second
- **Latency**: < 2 seconds per request
- **Concurrent Users**: 50+ supported
- **Uptime**: 99.9% with auto-restart

**🎯 Ready for production deployment with 50+ concurrent user support!**