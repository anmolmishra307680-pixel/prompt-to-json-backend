# 🚀 API Documentation

## Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://your-app.render.com` (or deployed URL)

## Authentication
No authentication required for current version.

## Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "agents": ["prompt", "evaluator", "rl"]
}
```

### 2. Generate Specification
```http
POST /generate
```

**Request:**
```json
{
  "prompt": "Modern office building with steel frame"
}
```

**Response:**
```json
{
  "spec": {
    "building_type": "office",
    "stories": 1,
    "materials": [{"type": "steel", "grade": null}],
    "dimensions": {"length": 30.0, "width": 25.0, "height": 3.5, "area": 750.0},
    "features": ["parking"],
    "requirements": ["Modern office building with steel frame"]
  },
  "success": true,
  "message": "Specification generated successfully"
}
```

### 3. Evaluate Specification
```http
POST /evaluate
```

**Request:**
```json
{
  "spec": {
    "building_type": "office",
    "stories": 1,
    "materials": [{"type": "steel"}]
  },
  "prompt": "Modern office building"
}
```

**Response:**
```json
{
  "evaluation": {
    "score": 85.0,
    "completeness": 80.0,
    "format_validity": 100.0,
    "feedback": ["Good specification"],
    "suggestions": []
  },
  "success": true,
  "message": "Evaluation completed successfully"
}
```

### 4. RL Training (Iterate)
```http
POST /iterate
```

**Request:**
```json
{
  "prompt": "Smart office building",
  "n_iter": 3
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid-here",
  "prompt": "Smart office building",
  "total_iterations": 3,
  "iterations": [
    {
      "iteration_number": 1,
      "iteration_id": "uuid",
      "before": {
        "spec": null,
        "score": 0
      },
      "after": {
        "spec": {...},
        "score": 85.0
      },
      "evaluation": {...},
      "feedback": {
        "feedback_type": "heuristic",
        "suggestions": ["Add elevator for multi-story building"],
        "confidence": 0.9
      },
      "reward": 1.7,
      "improvement": 85.0
    }
  ],
  "final_spec": {...},
  "learning_insights": {...}
}
```

### 5. Get Report
```http
GET /reports/{report_id}
```

**Response:**
```json
{
  "report_id": "uuid",
  "spec": {
    "id": "uuid",
    "prompt": "Office building",
    "spec_data": {...},
    "created_at": "2025-09-12T14:30:00"
  },
  "evaluation": {
    "id": "uuid",
    "eval_data": {...},
    "score": 85.0,
    "created_at": "2025-09-12T14:30:01"
  }
}
```

### 6. Log Values (HIDG)
```http
POST /log-values
```

**Request:**
```json
{
  "date": "2025-09-12",
  "day": "DAY 4",
  "task": "Deployment",
  "values_reflection": {
    "honesty": "Transparent about deployment challenges",
    "discipline": "Systematic deployment process",
    "gratitude": "Grateful for team support"
  },
  "achievements": {
    "deployment": "Successfully deployed to production"
  }
}
```

### 7. Batch Evaluate
```http
POST /batch-evaluate
```

**Request:**
```json
["Office building", "Warehouse facility", "Residential complex"]
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "prompt": "Office building",
      "spec": {...},
      "evaluation": {...}
    }
  ],
  "count": 3,
  "message": "Batch processed 3 prompts"
}
```

### 8. Get Iteration Logs
```http
GET /iterations/{session_id}
```

### 9. Advanced RL Training
```http
POST /advanced-rl
```

**Request:**
```json
{
  "prompt": "Smart building system",
  "n_iter": 3
}
```

### 10. Admin: Prune Logs
```http
POST /admin/prune-logs?retention_days=30
```

**Response:**
```json
{
  "success": true,
  "results": {
    "total_pruned": 150
  }
}
```

## Error Responses

All endpoints return errors in this format:
```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## BHIV Integration Points

### For BHIV Core Orchestration:
- All agents expose `run()` methods
- Database-first storage with file fallback
- Session-based iteration tracking
- Detailed feedback loops

### For BHIV Bucket:
- PostgreSQL/SQLite database integration
- Complete CRUD operations
- Fallback to file storage
- UUID-based entity tracking