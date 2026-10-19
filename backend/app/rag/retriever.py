
import chromadb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[3] / "chroma_db"

_client = chromadb.PersistentClient(path=str(DB_PATH))

_collection = _client.get_or_create_collection(
    name="project_atlas_reports"
)

# Demo assignment permissions: only these report grants are allowed.
CLIENT_REPORTS = {
    "C-01": ["R-101", "R-103"],
    "C-02": ["R-103"],
}


def add_chunks(chunks: list[dict], embeddings: list[list[float]]):
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings must have equal lengths.")

    if not chunks:
        return

    ids = [
        f"{chunk['metadata']['client_id']}-"
        f"{chunk['metadata']['report_id']}-"
        f"p{chunk['metadata']['page']}-c{i}"
        for i, chunk in enumerate(chunks)
    ]

    _collection.upsert(
        ids=ids,
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "report_id": chunk["metadata"]["report_id"],
                "source": chunk["metadata"]["source"],
                "page": int(chunk["metadata"]["page"]),
                "client_id": chunk["metadata"]["client_id"],
                "sector": chunk["metadata"]["sector"],
                "region": chunk["metadata"]["region"],
                "year": int(chunk["metadata"]["year"]),
            }
            for chunk in chunks
        ],
    )




def search_chunks(
    query_embedding: list[float],
    client_id: str,
    limit: int = 5,
):
    if client_id not in CLIENT_REPORTS:
        raise ValueError("Unknown client.")

    if limit < 1 or limit > 20:
        raise ValueError("Limit must be between 1 and 20.")

    allowed_reports = CLIENT_REPORTS[client_id]

    return _collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        where={
            "$and": [
                {"client_id": client_id},
                {"report_id": {"$in": allowed_reports}},
            ]
        },
        include=["documents", "metadatas", "distances"],
    )
