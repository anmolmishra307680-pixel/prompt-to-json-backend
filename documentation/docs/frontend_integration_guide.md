# Frontend Integration Guide

## Quick Start Integration

### 1. Authentication Setup
```javascript
// Frontend authentication service
class APIService {
  constructor() {
    this.baseURL = 'https://prompt-to-json-backend.onrender.com';
    this.apiKey = 'bhiv-secret-key-2024';
    this.token = localStorage.getItem('jwt_token');
  }

  async authenticate(username, password) {
    const response = await fetch(`${this.baseURL}/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('jwt_token', this.token);
      return true;
    }
    return false;
  }

  getHeaders() {
    return {
      'Content-Type': 'application/json',
      'X-API-Key': this.apiKey,
      'Authorization': `Bearer ${this.token}`
    };
  }
}
```

### 2. API Integration Examples
```javascript
const api = new APIService();

// Generate specification
async function generateSpec(prompt) {
  try {
    const response = await fetch(`${api.baseURL}/generate`, {
      method: 'POST',
      headers: api.getHeaders(),
      body: JSON.stringify({ prompt })
    });
    
    if (response.status === 401) {
      // Token expired, re-authenticate
      await api.authenticate('admin', 'bhiv2024');
      return generateSpec(prompt); // Retry
    }
    
    return await response.json();
  } catch (error) {
    console.error('Generation failed:', error);
    throw error;
  }
}

// Evaluate specification
async function evaluateSpec(spec, prompt) {
  const response = await fetch(`${api.baseURL}/evaluate`, {
    method: 'POST',
    headers: api.getHeaders(),
    body: JSON.stringify({ spec, prompt })
  });
  return await response.json();
}

// RL Training
async function runRLTraining(prompt, iterations = 3) {
  const response = await fetch(`${api.baseURL}/iterate`, {
    method: 'POST',
    headers: api.getHeaders(),
    body: JSON.stringify({ prompt, n_iter: iterations })
  });
  return await response.json();
}
```

### 3. React Integration
```jsx
import React, { useState, useEffect } from 'react';

function SpecGenerator() {
  const [prompt, setPrompt] = useState('');
  const [spec, setSpec] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateSpec(prompt);
      setSpec(result.spec);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter building description..."
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Spec'}
      </button>
      {spec && <pre>{JSON.stringify(spec, null, 2)}</pre>}
    </div>
  );
}
```

### 4. Error Handling
```javascript
class APIErrorHandler {
  static handle(response, error) {
    if (response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    } else if (response?.status === 429) {
      // Rate limit exceeded
      alert('Too many requests. Please wait a moment.');
    } else if (response?.status >= 500) {
      // Server error
      console.error('Server error:', error);
      alert('Server error. Please try again later.');
    }
  }
}
```

### 5. Rate Limiting Client-Side
```javascript
class RateLimiter {
  constructor(maxRequests = 20, windowMs = 60000) {
    this.requests = [];
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
  }

  canMakeRequest() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.windowMs);
    return this.requests.length < this.maxRequests;
  }

  recordRequest() {
    this.requests.push(Date.now());
  }
}
```

## Production Configuration

### Environment Variables
```javascript
// config.js
export const config = {
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  API_KEY: process.env.REACT_APP_API_KEY || 'bhiv-secret-key-2024',
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3
};
```

### CORS Setup
```javascript
// For production deployment
const corsOptions = {
  origin: ['https://your-frontend-domain.com'],
  credentials: true,
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'X-API-Key', 'Authorization']
};
```