# tests/test_api.py
import pytest
import os
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

# Use environment variables or test defaults
API_KEY = os.getenv("API_KEY", "test-api-key")
USERNAME = os.getenv("DEMO_USERNAME", "testuser")
PASSWORD = os.getenv("DEMO_PASSWORD", "testpass")

def get_auth_headers():
    """Get JWT token and return headers with API key and token"""
    try:
        # Token endpoint now requires API key
        token_response = client.post("/token", 
                                   json={"username": USERNAME, "password": PASSWORD},
                                   headers={"X-API-Key": API_KEY})
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
            return {
                "X-API-Key": API_KEY,
                "Authorization": f"Bearer {token}"
            }
    except Exception:
        pass
    return {"X-API-Key": API_KEY}

def test_health():
    headers = get_auth_headers()
    r = client.get("/health", headers=headers)
    assert r.status_code == 200
    assert "status" in r.json()

def test_generate_missing_prompt():
    headers = get_auth_headers()
    r = client.post("/generate", json={}, headers=headers)
    assert r.status_code == 422  # Missing prompt field

def test_generate_valid_prompt():
    headers = get_auth_headers()
    r = client.post("/generate", json={"prompt": "Modern office building"}, headers=headers)
    assert r.status_code == 200
    assert "spec" in r.json()

def test_evaluate_missing_spec():
    headers = get_auth_headers()
    r = client.post("/evaluate", json={}, headers=headers)
    assert r.status_code == 422  # Missing required fields

def test_generate_no_auth():
    # Test without any authentication
    r = client.post("/generate", json={"prompt": "test"})
    assert r.status_code == 401  # No API key

def test_evaluate_no_auth():
    # Test without any authentication
    r = client.post("/evaluate", json={})
    assert r.status_code == 401  # No API key