import pytest
import requests
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

class TestFullWorkflow:
    def test_complete_user_journey(self):
        """Test: Generate → Evaluate → Iterate → Report"""
        # Get JWT token
        token_response = client.post("/token", json={"username": "admin", "password": "bhiv2024"}, headers={"X-API-Key": "bhiv-secret-key-2024"})
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
        else:
            token = "dummy-token"
        headers = {
            "X-API-Key": "bhiv-secret-key-2024",
            "Authorization": f"Bearer {token}"
        }
        
        # Step 1: Generate specification
        generate_response = client.post(
            "/generate",
            json={"prompt": "Sustainable office building"},
            headers=headers
        )
        assert generate_response.status_code == 200
        spec = generate_response.json()["spec"]
        
        # Step 2: Evaluate specification  
        eval_response = client.post(
            "/evaluate",
            json={"spec": spec, "prompt": "Sustainable office building"},
            headers=headers
        )
        assert eval_response.status_code == 200
        report_id = eval_response.json()["report_id"]
        
        # Step 3: RL iteration
        rl_response = client.post(
            "/iterate", 
            json={"prompt": "Sustainable office building", "n_iter": 2},
            headers=headers
        )
        assert rl_response.status_code == 200
        session_id = rl_response.json()["session_id"]
        
        # Step 4: Retrieve reports
        report_response = client.get(f"/reports/{report_id}", headers=headers)
        assert report_response.status_code == 200
        
        iteration_response = client.get(f"/iterations/{session_id}", headers=headers)
        assert iteration_response.status_code == 200

    def test_batch_processing_workflow(self):
        """Test batch evaluation functionality"""
        # Get JWT token
        token_response = client.post("/token", json={"username": "admin", "password": "bhiv2024"}, headers={"X-API-Key": "bhiv-secret-key-2024"})
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
        else:
            token = "dummy-token"
        headers = {
            "X-API-Key": "bhiv-secret-key-2024",
            "Authorization": f"Bearer {token}"
        }
        
        prompts = ["Office building", "Warehouse facility", "Residential complex"]
        
        response = client.post("/batch-evaluate", json=prompts, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["count"] == 3
        assert len(data["results"]) == 3

    def test_health_and_metrics_endpoints(self):
        """Test monitoring endpoints"""
        # Get JWT token
        token_response = client.post("/token", json={"username": "admin", "password": "bhiv2024"}, headers={"X-API-Key": "bhiv-secret-key-2024"})
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
        else:
            token = "dummy-token"
        headers = {
            "X-API-Key": "bhiv-secret-key-2024",
            "Authorization": f"Bearer {token}"
        }
        
        # Health check
        health_response = client.get("/health", headers=headers)
        assert health_response.status_code == 200
        assert "status" in health_response.json()
        
        # Metrics (Prometheus format)
        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200
        # Prometheus metrics are text format, not JSON
        assert "http_requests" in metrics_response.text

    def test_authentication_workflow(self):
        """Test API key authentication"""
        # Without API key - should fail
        no_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"}
        )
        assert no_auth_response.status_code == 401
        
        # With wrong API key - should fail
        wrong_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"},
            headers={"X-API-Key": "wrong-key"}
        )
        assert wrong_auth_response.status_code == 401
        
        # With correct API key and JWT token - should succeed
        token_response = client.post("/token", json={"username": "admin", "password": "bhiv2024"}, headers={"X-API-Key": "bhiv-secret-key-2024"})
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
        else:
            token = "dummy-token"
        correct_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"},
            headers={
                "X-API-Key": "bhiv-secret-key-2024",
                "Authorization": f"Bearer {token}"
            }
        )
        assert correct_auth_response.status_code == 200