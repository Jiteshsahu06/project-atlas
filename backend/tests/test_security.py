
import os
from fastapi.testclient import TestClient

os.environ.setdefault("ATLAS_API_KEY", "atlas-demo-key-change-this")

from app.main import app

client = TestClient(app)


def test_chat_without_api_key_is_rejected():
    response = client.post(
        "/chat",
        json={"client_id": "C-01", "message": "What is the market revenue?"},
    )
    assert response.status_code == 401


def test_escalations_without_api_key_are_rejected():
    response = client.get("/escalations", params={"client_id": "C-01"})
    assert response.status_code == 401


def test_invalid_api_key_is_rejected():
    response = client.get(
        "/escalations",
        params={"client_id": "C-01"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_unknown_client_is_rejected_by_retriever():
    from app.rag.retriever import search_chunks

    try:
        search_chunks([0.0] * 384, "C-99")
        assert False, "Unknown client should be rejected"
    except ValueError:
        pass
