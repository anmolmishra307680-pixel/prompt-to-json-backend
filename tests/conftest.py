"""Test configuration and fixtures"""
import os
import pytest

# Set test environment variables
os.environ["API_KEY"] = "test-api-key"
os.environ["DEMO_USERNAME"] = "testuser"
os.environ["DEMO_PASSWORD"] = "testpass"
os.environ["JWT_SECRET"] = "test-jwt-secret"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["TESTING"] = "true"

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    # Ensure test environment is properly configured
    yield