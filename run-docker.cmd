@echo off
echo Stopping any existing container...
docker stop test-container 2>nul

echo Starting Docker container with authentication...
docker run --rm -d --name test-container -p 8000:8000 ^
  -e API_KEY=test-api-key ^
  -e DEMO_USERNAME=testuser ^
  -e DEMO_PASSWORD=testpass ^
  -e JWT_SECRET=test-jwt-secret ^
  -e SECRET_KEY=test-secret-key ^
  prompt-backend

echo Waiting for startup...
timeout /t 5 /nobreak >nul

echo Testing authentication...
python -c "import requests; r = requests.post('http://localhost:8000/token', json={'username':'testuser','password':'testpass'}); print('Token Status:', r.status_code); token = r.json()['access_token']; h = requests.get('http://localhost:8000/health', headers={'X-API-Key': 'test-api-key', 'Authorization': f'Bearer {token}'}); print('Health Status:', h.status_code); print('SUCCESS: Container is working!')"

echo.
echo Container is running at http://localhost:8000
echo Use: docker stop test-container (to stop)