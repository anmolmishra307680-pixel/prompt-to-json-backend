# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def get_auth_headers():
    """Get JWT token and return headers with API key and token"""
    token_response = client.post("/token", json={"username": "admin", "password": "bhiv2024"})
    if token_response.status_code == 200:
        token = token_response.json()["access_token"]
        return {
            "X-API-Key": "bhiv-secret-key-2024",
            "Authorization": f"Bearer {token}"
        }
    return {"X-API-Key": "bhiv-secret-key-2024"}

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
    r = client.post("/generate", json={"prompt": "test"})
    assert r.status_code == 401  # No API key

def test_evaluate_no_auth():
    r = client.post("/evaluate", json={})
    assert r.status_code == 401  # No API key