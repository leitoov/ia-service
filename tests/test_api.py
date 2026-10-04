import pytest
from fastapi.testclient import TestClient
from src.main import app

# El TestClient de FastAPI es equivalente a MockMvc en Spring Boot
client = TestClient(app)

def test_health_check():
    """TDD: El health check debe devolver 200 y status ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "tools_loaded" in response.json()

def test_chat_endpoint_without_message_fails():
    """TDD: Si envío un payload vacío, debe fallar por validación (Pydantic)"""
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422 # Unprocessable Entity

def test_chat_endpoint_with_message():
    """TDD: Si envío un mensaje correcto, debe responder con el array de tools disponibles"""
    payload = {"message": "Hola, ¿qué puedes hacer?", "user_id": "123"}
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "tools_available" in data
