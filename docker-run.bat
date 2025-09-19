@echo off
REM Windows batch script for Docker run with environment variables

echo Starting Docker container with environment variables...

docker run --rm -d ^
  --name prompt-backend ^
  -p 8000:8000 ^
  -e API_KEY=test-api-key ^
  -e DEMO_USERNAME=testuser ^
  -e DEMO_PASSWORD=testpass ^
  -e JWT_SECRET=test-jwt-secret ^
  -e SECRET_KEY=test-secret-key ^
  -e TESTING=false ^
  -e PRODUCTION_MODE=false ^
  879b4a0be9f5d8add257d33fb09a482a9c431e3abe742628084f811e66ea61b5

echo Container started. Waiting for startup...
timeout /t 5 /nobreak > nul

echo Testing token endpoint...
curl -X POST "http://localhost:8000/token" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"password\":\"testpass\"}"

echo.
echo Testing with authentication:
echo Get token first, then use both X-API-Key and Authorization headers
echo.
echo Example:
echo curl -X GET "http://localhost:8000/health" ^
  -H "X-API-Key: test-api-key" ^
  -H "Authorization: Bearer YOUR_TOKEN"