# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()

def test_generate_missing_prompt():
    r = client.post("/generate", json={}, headers={"X-API-Key": "bhiv-secret-key-2024"})
    assert r.status_code == 422  # Missing prompt field

def test_generate_valid_prompt():
    r = client.post("/generate", json={"prompt": "Modern office building"}, headers={"X-API-Key": "bhiv-secret-key-2024"})
    assert r.status_code == 200
    assert "spec" in r.json()

def test_evaluate_missing_spec():
    r = client.post("/evaluate", json={}, headers={"X-API-Key": "bhiv-secret-key-2024"})
    assert r.status_code == 422  # Missing required fields

def test_generate_no_auth():
    r = client.post("/generate", json={"prompt": "test"})
    assert r.status_code == 401  # No API key

def test_evaluate_no_auth():
    r = client.post("/evaluate", json={})
    assert r.status_code == 401  # No API key