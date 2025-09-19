"""Test monitoring and metrics endpoints"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint returns proper status"""
    response = client.get("/health")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Check required health check fields
    assert "status" in json_response
    assert "database" in json_response
    assert "agents" in json_response
    assert "timestamp" in json_response
    
    # Status should be healthy or degraded
    assert json_response["status"] in ["healthy", "degraded"]

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    
    assert response.status_code == 200
    
    # Check if it's Prometheus format or JSON format
    content_type = response.headers.get("content-type", "")
    
    if "text/plain" in content_type or "text/html" in content_type:
        # Prometheus format - check for common metrics
        metrics_text = response.text
        assert "http_requests_total" in metrics_text or "http_request" in metrics_text
    else:
        # JSON format - our custom metrics
        json_response = response.json()
        assert "generated_specs" in json_response
        assert "timestamp" in json_response

def test_basic_metrics_endpoint():
    """Test our custom basic metrics endpoint"""
    response = client.get("/basic-metrics")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Check basic metrics structure
    assert "generated_specs" in json_response
    assert "evaluation_reports" in json_response
    assert "log_files" in json_response
    assert "active_sessions" in json_response
    assert "timestamp" in json_response
    
    # Values should be non-negative integers
    assert json_response["generated_specs"] >= 0
    assert json_response["evaluation_reports"] >= 0
    assert json_response["log_files"] >= 0

def test_system_overview_endpoint():
    """Test system overview endpoint for comprehensive monitoring"""
    response = client.get("/system-overview")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Check system overview structure
    assert "success" in json_response
    assert "system_info" in json_response
    assert "health" in json_response
    assert "performance" in json_response
    assert "timestamp" in json_response
    
    # Check system info details
    system_info = json_response["system_info"]
    assert "api_version" in system_info
    assert "production_ready" in system_info
    assert "features" in system_info

def test_agent_status_endpoint():
    """Test agent status monitoring"""
    response = client.get("/agent-status")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Should have success field and timestamp
    assert "success" in json_response
    assert "timestamp" in json_response

def test_cache_stats_endpoint():
    """Test cache statistics endpoint"""
    response = client.get("/cache-stats")
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Should have success field and timestamp
    assert "success" in json_response
    assert "timestamp" in json_response

if __name__ == "__main__":
    test_health_endpoint()
    test_metrics_endpoint()
    test_basic_metrics_endpoint()
    test_system_overview_endpoint()
    test_agent_status_endpoint()
    test_cache_stats_endpoint()
    print("✅ All monitoring tests passed")