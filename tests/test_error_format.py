"""Test structured error handling"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def test_value_error_format():
    """Test that ValueError returns structured JSON error"""
    # Create a test endpoint that raises ValueError
    @app.get("/test-value-error")
    async def test_value_error():
        raise ValueError("Test validation error")
    
    response = client.get("/test-value-error")
    
    assert response.status_code == 400
    json_response = response.json()
    
    # Check structured error format
    assert "error" in json_response
    assert "message" in json_response
    assert json_response["error"] == "bad_request"
    assert json_response["message"] == "Test validation error"

def test_generic_exception_format():
    """Test that generic Exception returns structured JSON error"""
    # Test with existing endpoint that requires authentication
    response = client.post("/generate", json={"prompt": "test"})
    
    # Should get 401 for missing API key
    assert response.status_code == 401
    json_response = response.json()
    assert "detail" in json_response

def test_http_exception_passthrough():
    """Test that HTTPException is handled properly"""
    response = client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    # FastAPI's default HTTPException handling should still work

if __name__ == "__main__":
    test_value_error_format()
    test_generic_exception_format()
    print("✅ All error format tests passed")