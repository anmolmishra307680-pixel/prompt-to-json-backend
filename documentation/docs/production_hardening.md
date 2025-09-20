# Production Hardening Guide

## Security Hardening

### 1. Environment Variables Security
```bash
# Production .env (never commit)
DATABASE_URL=postgresql://user:pass@host:5432/db
API_KEY=your-256-bit-secret-key
JWT_SECRET=your-jwt-secret-key-here
SENTRY_DSN=https://your-sentry-dsn
REDIS_URL=redis://user:pass@host:6379/0

# Rotate secrets regularly
API_KEY_ROTATION_DAYS=90
JWT_SECRET_ROTATION_DAYS=30
```

### 2. CORS Production Configuration
```python
# main_api.py - Production CORS
ALLOWED_ORIGINS = [
    "https://your-frontend.com",
    "https://www.your-frontend.com",
    "https://admin.your-frontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key", "Authorization"],
    expose_headers=["X-Request-ID"]
)
```

### 3. Rate Limiting Enhancement
```python
# Enhanced rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
import redis

# Redis-backed rate limiting for production
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

def get_user_id(request):
    """Get user ID from JWT for per-user rate limiting"""
    try:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub", get_remote_address(request))
    except:
        pass
    return get_remote_address(request)

limiter = Limiter(
    key_func=get_user_id,
    storage_uri=os.getenv("REDIS_URL", "memory://")
)
```

## Performance Optimization

### 1. Database Connection Pooling
```python
# database.py - Production connection pooling
engine = create_engine(
    database_url,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # Disable SQL logging in production
)
```

### 2. Caching Strategy
```python
# cache.py - Production caching
import redis
from functools import wraps
import json
import hashlib

class ProductionCache:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            os.getenv("REDIS_URL"),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
    
    def cache_result(self, ttl=3600):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and args
                cache_key = f"{func.__name__}:{hashlib.md5(str(args).encode()).hexdigest()}"
                
                try:
                    # Try to get from cache
                    cached = self.redis_client.get(cache_key)
                    if cached:
                        return json.loads(cached)
                except:
                    pass
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                try:
                    self.redis_client.setex(cache_key, ttl, json.dumps(result, default=str))
                except:
                    pass
                
                return result
            return wrapper
        return decorator
```

### 3. Async Database Operations
```python
# async_database.py - For high-concurrency scenarios
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class AsyncDatabase:
    def __init__(self):
        self.engine = create_async_engine(
            os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://"),
            pool_size=50,
            max_overflow=100
        )
        self.SessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def save_spec_async(self, prompt: str, spec_data: dict):
        async with self.SessionLocal() as session:
            spec = Spec(prompt=prompt, spec_data=spec_data)
            session.add(spec)
            await session.commit()
            return spec.id
```

## Monitoring & Alerting

### 1. Custom Health Checks
```python
# health_checks.py
class HealthChecker:
    @staticmethod
    async def check_database():
        try:
            db = Database()
            session = db.get_session()
            session.execute("SELECT 1")
            session.close()
            return {"status": "healthy", "response_time": "< 50ms"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    @staticmethod
    async def check_redis():
        try:
            redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))
            redis_client.ping()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    @staticmethod
    async def check_external_apis():
        # Check OpenAI API, Supabase, etc.
        checks = {}
        try:
            # Add your external API checks here
            checks["openai"] = {"status": "healthy"}
        except Exception as e:
            checks["openai"] = {"status": "unhealthy", "error": str(e)}
        return checks
```

### 2. Alerting Configuration
```python
# alerts.py
import sentry_sdk
from datetime import datetime

class AlertManager:
    @staticmethod
    def send_critical_alert(message: str, context: dict = None):
        # Send to Sentry
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_tag(key, value)
            sentry_sdk.capture_message(message, level="error")
    
    @staticmethod
    def send_performance_alert(metric: str, value: float, threshold: float):
        if value > threshold:
            AlertManager.send_critical_alert(
                f"Performance threshold exceeded: {metric}",
                {"metric": metric, "value": value, "threshold": threshold}
            )
```

## Deployment Configuration

### 1. Docker Production Optimization
```dockerfile
# Dockerfile.prod
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app
COPY --from=builder /root/.local /home/app/.local
COPY . .
RUN chown -R app:app /app
USER app
ENV PATH=/home/app/.local/bin:$PATH
EXPOSE 8000
CMD ["gunicorn", "main_api:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### 2. Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prompt-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prompt-backend
  template:
    metadata:
      labels:
        app: prompt-backend
    spec:
      containers:
      - name: prompt-backend
        image: prompt-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 3. Load Balancer Configuration
```nginx
# nginx.conf
upstream backend {
    server backend1:8000 weight=3;
    server backend2:8000 weight=3;
    server backend3:8000 weight=2;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    location /health {
        access_log off;
        proxy_pass http://backend;
    }
}
```

## Security Checklist

- [ ] Environment variables secured and rotated
- [ ] CORS configured for production domains only
- [ ] Rate limiting with Redis backend
- [ ] Database connections encrypted (SSL)
- [ ] JWT tokens with short expiration
- [ ] Input validation on all endpoints
- [ ] Error messages sanitized
- [ ] Dependency scanning enabled
- [ ] Container runs as non-root user
- [ ] Secrets management implemented
- [ ] Audit logging enabled
- [ ] HTTPS enforced
- [ ] Security headers configured