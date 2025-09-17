# API Documentation

## Overview
FastAPI backend for prompt-to-JSON conversion with AI agents, authentication, and monitoring.

## Base URL
- **Local**: `http://localhost:8000`
- **Docs**: `http://localhost:8000/docs`

## Authentication
Secure endpoints require API key:
```
X-API-Key: bhiv-secret-key-2024
```

## Endpoints

### 🔓 Public Endpoints

#### Root
**GET** `/`
```json
{"message": "Prompt-to-JSON API", "version": "1.0.0"}
```

#### Health Check
**GET** `/health`
```json
{
  "status": "healthy",
  "database": true,
  "agents": ["prompt", "evaluator", "rl"],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Metrics
**GET** `/metrics`
```json
{
  "generated_specs": 0,
  "evaluation_reports": 0,
  "log_files": 0,
  "active_sessions": 0,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 🔐 Authenticated Endpoints

#### Generate Specification
**POST** `/generate` (Rate limited: 20/min)

**Request:**
```json
{
  "prompt": "Modern office building with 5 stories"
}
```

**Response:**
```json
{
  "spec": {
    "building_type": "office",
    "stories": 5,
    "materials": [{"type": "steel"}],
    "dimensions": {"length": 30, "width": 25, "height": 17.5, "area": 750},
    "features": ["elevator", "parking"],
    "requirements": ["Modern office building"]
  },
  "success": true,
  "message": "Specification generated successfully"
}
```

#### Evaluate Specification
**POST** `/evaluate`

**Request:**
```json
{
  "spec": {
    "building_type": "office",
    "stories": 5,
    "materials": [{"type": "steel"}]
  },
  "prompt": "Office building"
}
```

**Response:**
```json
{
  "report_id": "uuid-string",
  "evaluation": {
    "score": 85.5,
    "completeness": 90.0,
    "format_validity": 95.0,
    "feedback": ["Good structural design"],
    "suggestions": ["Add more details"]
  },
  "success": true,
  "message": "Evaluation completed successfully"
}
```

#### RL Training
**POST** `/iterate`

**Request:**
```json
{
  "prompt": "Smart building system",
  "n_iter": 3
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid-string",
  "prompt": "Smart building system",
  "total_iterations": 3,
  "iterations": [
    {
      "iteration_number": 1,
      "before": {"spec": {}, "score": 70},
      "after": {"spec": {}, "score": 75},
      "feedback": "Improved design",
      "reward": 5
    }
  ],
  "final_spec": {},
  "message": "RL training completed with 3 iterations"
}
```

### 📊 Data Endpoints

#### Get Report
**GET** `/reports/{report_id}`

#### Get Iteration Logs
**GET** `/iterations/{session_id}`

#### Batch Evaluate
**POST** `/batch-evaluate`
```json
["Office building", "Warehouse design", "Hospital complex"]
```

#### Log Values
**POST** `/log-values`
```json
{
  "date": "2024-01-01",
  "day": "DAY 1",
  "task": "Backend development",
  "values_reflection": {
    "honesty": "Transparent development",
    "discipline": "Systematic approach",
    "gratitude": "Team collaboration"
  }
}
```

### 🔧 Admin Endpoints

#### System Test
**GET** `/system-test`

#### Prune Logs
**POST** `/admin/prune-logs?retention_days=30`

#### Advanced RL
**POST** `/advanced-rl`

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing API key. Include X-API-Key header."
}
```

### 429 Rate Limited
```json
{
  "detail": "Rate limit exceeded: 20 per 1 minute"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Rate Limits
- **Generate**: 20 requests/minute per IP
- **Other endpoints**: No limits

## Examples

### cURL
```bash
# Generate with auth
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"prompt":"Modern office building"}'

# Health check (no auth)
curl http://localhost:8000/health

# Metrics (no auth)
curl http://localhost:8000/metrics
```

### Python
```python
import requests

# Authenticated request
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'bhiv-secret-key-2024'
}

response = requests.post(
    'http://localhost:8000/generate',
    headers=headers,
    json={'prompt': 'Modern office building'}
)

print(response.json())

# Public endpoint
health = requests.get('http://localhost:8000/health')
print(health.json())
```

### JavaScript
```javascript
// Fetch with auth
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'bhiv-secret-key-2024'
  },
  body: JSON.stringify({
    prompt: 'Modern office building'
  })
});

const data = await response.json();
console.log(data);
```

## Schema Models

### DesignSpec
```json
{
  "building_type": "string",
  "stories": "integer",
  "materials": [{"type": "string", "grade": "string"}],
  "dimensions": {"length": "float", "width": "float", "height": "float", "area": "float"},
  "features": ["string"],
  "requirements": ["string"],
  "timestamp": "string (ISO)"
}
```

### EvaluationResult
```json
{
  "score": "float (0-100)",
  "completeness": "float (0-100)",
  "format_validity": "float (0-100)",
  "feedback": ["string"],
  "suggestions": ["string"],
  "timestamp": "string (ISO)"
}
```