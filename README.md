# 🚀 Prompt-to-JSON Backend

**Production-Ready AI Backend** - FastAPI system for prompt-to-JSON conversion with AI agents, reinforcement learning, and comprehensive database integration.

## ✨ Features

- **🤖 AI Agents**: Prompt processing, evaluation, and RL training
- **🔐 API Authentication**: Secure endpoints with API key validation
- **💾 Database Integration**: Supabase PostgreSQL with file fallback
- **⚡ Caching**: Redis caching with in-memory fallback
- **📊 Monitoring**: Prometheus metrics and health checks
- **🔒 Security**: Rate limiting (20/min), CORS, error handling
- **🚀 Production Ready**: Docker, CI/CD, scalable deployment

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone and setup
git clone <repository-url>
cd prompt-to-json-backend
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your credentials
```

### 4. Setup Database
```bash
# Create database tables
python create-tables.py
```

### 5. Start Server
```bash
# Run API server
python main_api.py
# Access: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## 📊 API Endpoints

### 🔐 Authentication Required
All main endpoints require API key: `X-API-Key: bhiv-secret-key-2024`

### Core Endpoints
```bash
# Generate Specification
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"prompt":"Modern office building"}'

# Evaluate Specification
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"spec":{"building_type":"office","stories":5},"prompt":"Office building"}'

# RL Training
curl -X POST "http://localhost:8000/iterate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"prompt":"Smart building","n_iter":3}'

# System Health
curl -X GET "http://localhost:8000/health"

# Metrics
curl -X GET "http://localhost:8000/metrics"
```

## 🏗️ Project Structure

```
prompt-to-json-backend/
├── 🎯 Core API
│   ├── main_api.py              # FastAPI server (12 endpoints)
│   ├── main.py                  # CLI interface
│   ├── schema.py                # Pydantic models
│   └── cache.py                 # Redis caching system
├── 🤖 AI Agents
│   ├── prompt_agent/            # Prompt processing
│   ├── evaluator/               # Specification evaluation
│   ├── rl_agent/                # Reinforcement learning
│   └── feedback/                # Feedback processing
├── 💾 Database
│   ├── db/
│   │   ├── database.py          # Supabase integration
│   │   ├── models.py            # Database models
│   │   ├── iteration_models.py  # RL tracking
│   │   └── log_pruning.py       # Log management
│   └── alembic/                 # Migrations
├── 🚀 Deployment
│   ├── Dockerfile               # Container build
│   ├── docker-compose.yml       # Stack deployment
│   ├── start.sh                 # Production startup
│   └── render.yaml              # Render config
├── 📁 Output Directories
│   ├── logs/                    # Training logs
│   ├── spec_outputs/            # Generated specs
│   ├── reports/                 # Evaluation reports
│   └── sample_outputs/          # Examples
├── 🧪 Testing
│   ├── tests/                   # Unit tests
│   ├── load_test.py             # Performance testing
│   └── load-test.js             # K6 load testing
└── 📚 Documentation
    ├── README.md                # This file
    ├── docs/api.md              # API documentation
    └── DEPLOYMENT_RELEASE.md    # Deployment guide
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
SUPABASE_URL=https://project.supabase.co
SUPABASE_KEY=your_supabase_key

# Authentication
API_KEY=bhiv-secret-key-2024

# Caching
REDIS_URL=redis://localhost:6379/0

# Security
FRONTEND_URL=https://your-frontend.com
SENTRY_DSN=your_sentry_dsn

# OpenAI (if used)
OPENAI_API_KEY=your_openai_key
```

## 📊 Database Schema

### Tables
- **specs**: Generated specifications
- **evals**: Evaluation results
- **feedback_logs**: RL feedback data
- **hidg_logs**: Daily values logging
- **iteration_logs**: RL training sessions

### File Fallback
- Automatic JSON file backup if database unavailable
- Files stored in `logs/`, `spec_outputs/`, `reports/`

## 🧪 Testing

### Load Testing
```bash
# Python load test (50 concurrent users)
python load_test.py

# K6 load test
k6 run load-test.js
```

### System Test
```bash
# Test all endpoints
curl http://localhost:8000/system-test
```

## 🚀 Deployment

### Docker
```bash
# Build and run
docker build -t prompt-backend .
docker run -p 8000:8000 --env-file .env prompt-backend
```

### Production
```bash
# Using gunicorn
./start.sh
```

## 📈 Monitoring

### Health Check
- **Endpoint**: `/health`
- **Checks**: Database, agents, system status

### Metrics
- **Endpoint**: `/metrics`
- **Prometheus**: Request metrics, response times
- **Custom**: File counts, active sessions

### Rate Limiting
- **Generate**: 20 requests/minute per IP
- **Global**: Configurable per endpoint

## 🔒 Security

### Authentication
- API key required for main endpoints
- Header: `X-API-Key: your-api-key`

### CORS
- Configurable allowed origins
- Secure headers and methods

### Error Handling
- Graceful degradation
- Detailed error responses
- Sentry integration (optional)

## 🎯 API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Root endpoint |
| `/health` | GET | No | System health |
| `/metrics` | GET | No | System metrics |
| `/generate` | POST | Yes | Generate specs |
| `/evaluate` | POST | Yes | Evaluate specs |
| `/iterate` | POST | Yes | RL training |
| `/advanced-rl` | POST | Yes | Advanced RL |
| `/log-values` | POST | No | Log HIDG values |
| `/batch-evaluate` | POST | No | Batch processing |
| `/reports/{id}` | GET | No | Get reports |
| `/iterations/{id}` | GET | No | Get RL logs |
| `/system-test` | GET | No | System test |
| `/admin/prune-logs` | POST | No | Log cleanup |

## 🏆 Production Features

- ✅ **12 API Endpoints**: Complete functionality
- ✅ **Authentication**: Secure API key system
- ✅ **Database**: Supabase PostgreSQL integration
- ✅ **Caching**: Redis with memory fallback
- ✅ **Monitoring**: Prometheus + health checks
- ✅ **Security**: Rate limiting, CORS, error handling
- ✅ **Deployment**: Docker, CI/CD ready
- ✅ **Testing**: Load testing, system tests
- ✅ **Documentation**: Complete API docs

**🚀 Ready for production deployment!**