# API Contract - Prompt-to-JSON Backend

## Base Information
- **Base URL**: `https://prompt-to-json-backend.onrender.com`
- **Local URL**: `http://localhost:8000`
- **API Version**: 2.1.0
- **OpenAPI Spec**: `/openapi.json`
- **Interactive Docs**: `/docs`

## Authentication

### Maximum Security Authentication (Required for ALL Endpoints)
```http
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>
```

**Note**: API key is required for ALL 17 endpoints. JWT token is additionally required for 16 endpoints (all except `/token`).

#### Get JWT Token (Requires API Key)
```http
POST /token
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024

{
  "username": "admin",
  "password": "bhiv2024"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

## Core AI Endpoints

### 1. Generate Specification
```http
POST /generate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>

{
  "prompt": "Modern office building with sustainable features"
}
```

**Response:**
```json
{
  "spec": {
    "building_type": "commercial",
    "stories": 5,
    "materials": [
      {
        "type": "steel",
        "grade": "A36",
        "properties": {}
      }
    ],
    "dimensions": {
      "length": 50.0,
      "width": 30.0,
      "height": 20.0,
      "area": 1500.0
    },
    "features": ["HVAC", "elevator", "parking"],
    "requirements": ["Modern office building with sustainable features"],
    "timestamp": "2024-01-15T10:30:45.123456"
  },
  "success": true,
  "message": "Specification generated successfully"
}
```

### 2. Evaluate Specification
```http
POST /evaluate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>

{
  "spec": {
    "building_type": "commercial",
    "stories": 5,
    "materials": [{"type": "steel", "grade": "A36"}],
    "dimensions": {"length": 50, "width": 30, "height": 20, "area": 1500}
  },
  "prompt": "Modern office building"
}
```

**Response:**
```json
{
  "report_id": "eval_abc123def456",
  "evaluation": {
    "score": 8.5,
    "criteria": {
      "structural_integrity": 9.0,
      "cost_efficiency": 8.0,
      "sustainability": 8.5,
      "feasibility": 8.5
    },
    "feedback": "Well-designed commercial building with good structural properties",
    "recommendations": ["Consider adding renewable energy features"],
    "timestamp": "2024-01-15T10:31:15.789012"
  },
  "success": true,
  "message": "Evaluation completed successfully"
}
```

### 3. RL Training Iterations
```http
POST /iterate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>

{
  "prompt": "Smart building with IoT integration",
  "n_iter": 3
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "rl_session_xyz789",
  "prompt": "Smart building with IoT integration",
  "total_iterations": 3,
  "iterations": [
    {
      "iteration_number": 1,
      "before": {"spec": {...}, "score": 7.2},
      "after": {"spec": {...}, "score": 7.8},
      "evaluation": {...},
      "feedback": "Improved IoT integration",
      "reward": 0.6,
      "improvement": 0.6
    }
  ],
  "final_spec": {...},
  "learning_insights": {...},
  "message": "RL training completed with 3 iterations"
}
```

### 4. Multi-Agent Coordination
```http
POST /coordinated-improvement
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>

{
  "prompt": "Eco-friendly residential complex"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "coordinated_spec": {...},
    "agent_contributions": {
      "main_agent": "Initial specification generation",
      "evaluator_agent": "Quality assessment and scoring",
      "rl_agent": "Iterative improvement",
      "feedback_agent": "Learning integration"
    },
    "final_score": 9.2,
    "coordination_metrics": {...}
  },
  "message": "Coordinated improvement completed"
}
```

## Monitoring Endpoints

### Health Check (Public)
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": true,
  "agents": ["prompt", "evaluator", "rl"],
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Note**: This endpoint is public for monitoring purposes and does not require authentication.

### Prometheus Metrics (Protected)
```http
GET /metrics
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>
```

**Response:** Prometheus format metrics

**Note**: This endpoint now requires full authentication for maximum security.

### Agent Status (Protected)
```http
GET /agent-status
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "success": true,
  "agents": {
    "main_agent": {"status": "healthy", "response_time": "45ms"},
    "evaluator_agent": {"status": "healthy", "response_time": "32ms"},
    "rl_agent": {"status": "healthy", "response_time": "78ms"}
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## Rate Limiting
- **Protected Endpoints**: 20 requests/minute per IP (16 endpoints)
- **Token Endpoint**: 10 requests/minute per IP
- **Public Health Endpoint**: 20 requests/minute per IP
- **One Public Endpoint**: /health for monitoring

## Error Responses

### 400 Bad Request
```json
{
  "error": "bad_request",
  "message": "Invalid input parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing API key. Include X-API-Key header."
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "20 requests per minute allowed"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_server_error",
  "message": "An unexpected error occurred."
}
```

## CORS Configuration
- **Development**: `*` (all origins)
- **Production**: Only `FRONTEND_URL` environment variable
- **Methods**: GET, POST
- **Headers**: Content-Type, X-API-Key, Authorization

## Frontend Integration Notes

1. **Authentication Flow**:
   - Get JWT token from `/token` endpoint (API key required for this step)
   - Include **BOTH** `X-API-Key` and `Authorization` headers for all 16 other endpoints
   - Token expires in 60 minutes, implement refresh logic
   - Store token securely (avoid localStorage in production)

2. **Error Handling**:
   - All errors return structured JSON with `error` and `message` fields
   - Check `success` field in responses
   - Handle 401 responses by refreshing token

3. **Rate Limiting**:
   - Implement client-side rate limiting: 20 requests/minute for protected endpoints
   - Token endpoint: 10 requests/minute limit
   - Health endpoint: 20 requests/minute (public)
   - Handle 429 responses with exponential backoff

4. **CORS**:
   - Set `FRONTEND_URL` environment variable in production
   - Development allows all origins (`*`)
   - Ensure credentials are included in requests

5. **Security Best Practices**:
   - Never expose API keys in client-side code
   - Implement token refresh before expiration
   - Use HTTPS in production
   - Validate all responses on client side

## OpenAPI Integration
- **Spec URL**: `/openapi.json`
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`