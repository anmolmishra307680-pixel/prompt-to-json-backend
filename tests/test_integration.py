import pytest
import requests
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

class TestFullWorkflow:
    def test_complete_user_journey(self):
        """Test: Generate → Evaluate → Iterate → Report"""
        headers = {"X-API-Key": "bhiv-secret-key-2024"}
        
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
        report_response = client.get(f"/reports/{report_id}")
        assert report_response.status_code == 200
        
        iteration_response = client.get(f"/iterations/{session_id}")
        assert iteration_response.status_code == 200

    def test_batch_processing_workflow(self):
        """Test batch evaluation functionality"""
        prompts = ["Office building", "Warehouse facility", "Residential complex"]
        
        response = client.post("/batch-evaluate", json=prompts)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["count"] == 3
        assert len(data["results"]) == 3

    def test_health_and_metrics_endpoints(self):
        """Test monitoring endpoints"""
        # Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert "status" in health_response.json()
        
        # Metrics
        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200
        assert "timestamp" in metrics_response.json()

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
        
        # With correct API key - should succeed
        correct_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"},
            headers={"X-API-Key": "bhiv-secret-key-2024"}
        )
        assert correct_auth_response.status_code == 200