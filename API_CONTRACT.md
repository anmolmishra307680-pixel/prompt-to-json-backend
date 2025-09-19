# API Contract for Frontend Integration

## Base URL
- **Production**: `https://prompt-to-json-backend.onrender.com`
- **Local**: `http://localhost:8000`

## Authentication
All protected endpoints require:
```
X-API-Key: bhiv-secret-key-2024
```

## CORS Configuration
```javascript
// Allowed origins for production
const allowedOrigins = [
  'https://your-frontend-domain.com',
  'http://localhost:3000', // Development
  'http://localhost:5173'  // Vite dev server
];
```

## Core Endpoints

### 1. Generate Specification
```http
POST /generate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024

{
  "prompt": "Modern 5-story office building with steel frame"
}
```

**Response:**
```json
{
  "spec": {
    "building_type": "office",
    "stories": 5,
    "materials": [{"type": "steel", "grade": "A36"}],
    "dimensions": {"length": 30, "width": 25, "height": 17.5, "area": 750},
    "features": ["elevator", "parking"],
    "requirements": ["Modern office building"]
  },
  "success": true,
  "message": "Specification generated successfully"
}
```

### 2. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": true,
  "agents": ["prompt", "evaluator", "rl"],
  "timestamp": "2024-01-17T10:00:00Z"
}
```

### 3. Agent Status
```http
GET /agent-status
```

**Response:**
```json
{
  "success": true,
  "agents": {
    "prompt": "✅ Ready",
    "evaluator": "✅ Ready",
    "rl": "✅ Ready",
    "feedback": "✅ Ready"
  },
  "timestamp": "2024-01-17T10:00:00Z"
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "HTTP Error",
  "message": "Invalid or missing API key",
  "status_code": 401
}
```

### 422 Validation Error
```json
{
  "error": "Validation Error",
  "message": "Invalid input data",
  "details": [
    {
      "loc": ["prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": "Server error"
}
```

## Rate Limits
- **Generate endpoint**: 20 requests/minute per IP
- **Other endpoints**: No specific limits

## Frontend Integration Example

```javascript
// React/Next.js example
const API_BASE = 'https://prompt-to-json-backend.onrender.com';
const API_KEY = 'bhiv-secret-key-2024';

async function generateSpec(prompt) {
  try {
    const response = await fetch(`${API_BASE}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const data = await response.json();
    return data.spec;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// Usage
generateSpec('Modern office building')
  .then(spec => console.log('Generated spec:', spec))
  .catch(error => console.error('Error:', error));
```