import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Breast Friend Forever" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chatbot_greeting():
    """Test chatbot greeting endpoint"""
    response = client.get("/api/v1/chat/greeting")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "suggested_questions" in data

def test_hospitals_endpoint():
    """Test hospitals endpoint"""
    response = client.get("/api/v1/hospitals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)