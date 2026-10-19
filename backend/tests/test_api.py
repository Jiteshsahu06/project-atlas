
import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("ATLAS_API_KEY", "atlas-demo-key-change-this")

from app.main import app

client = TestClient(app)
API_KEY = os.getenv("ATLAS_API_KEY", "atlas-demo-key-change-this")
HEADERS = {"X-API-Key": API_KEY}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat",
        headers=HEADERS,
        json={"client_id": "C-01", "message": ""},
    )
    assert response.status_code == 422


def test_chat_rejects_missing_client_id():
    response = client.post(
        "/chat",
        headers=HEADERS,
        json={"message": "What was the market revenue?"},
    )
    assert response.status_code == 422


def test_chat_requires_api_key():
    response = client.post(
        "/chat",
        json={"client_id": "C-01", "message": "Hello"},
    )
    assert response.status_code == 401
