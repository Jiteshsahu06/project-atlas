
import pytest
from app.rag.retriever import search_chunks
from app.rag.embeddings import generate_embeddings


@pytest.fixture(scope="module")
def query_embedding():
    return generate_embeddings(
        ["Artificial intelligence market and adoption reports"]
    )[0]


def test_c01_can_access_r101_and_r103(query_embedding):
    result = search_chunks(query_embedding, "C-01", limit=20)
    reports = {
        item["report_id"]
        for item in result["metadatas"][0]
    }
    assert reports == {"R-101", "R-103"}


def test_c02_can_access_only_r103(query_embedding):
    result = search_chunks(query_embedding, "C-02", limit=20)
    reports = {
        item["report_id"]
        for item in result["metadatas"][0]
    }
    assert reports == {"R-103"}


def test_unknown_client_is_rejected(query_embedding):
    with pytest.raises(ValueError, match="Unknown client"):
        search_chunks(query_embedding, "C-99", limit=20)
