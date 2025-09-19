#!/bin/bash

# Docker run script with proper environment variables
docker run --rm -d \
  --name prompt-backend \
  -p 8000:8000 \
  -e API_KEY="test-api-key" \
  -e DEMO_USERNAME="testuser" \
  -e DEMO_PASSWORD="testpass" \
  -e JWT_SECRET="test-jwt-secret" \
  -e SECRET_KEY="test-secret-key" \
  -e TESTING="false" \
  -e PRODUCTION_MODE="false" \
  879b4a0be9f5d8add257d33fb09a482a9c431e3abe742628084f811e66ea61b5

echo "Container started. Testing endpoints..."
sleep 5

# Test token endpoint (public)
echo "1. Testing token endpoint..."
TOKEN_RESPONSE=$(curl -s -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}')

echo "Token response: $TOKEN_RESPONSE"

# Extract token
TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
  echo "✅ Token obtained: ${TOKEN:0:20}..."
  
  # Test protected endpoint
  echo "2. Testing protected health endpoint..."
  curl -s -X GET "http://localhost:8000/health" \
    -H "X-API-Key: test-api-key" \
    -H "Authorization: Bearer $TOKEN" | jq .
  
  echo "3. Testing generate endpoint..."
  curl -s -X POST "http://localhost:8000/generate" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: test-api-key" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"prompt":"Test building"}' | jq .
else
  echo "❌ Failed to get token"
fi