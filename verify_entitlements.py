
from app.rag.retriever import search_chunks
from app.rag.embeddings import generate_embeddings

query_embedding = generate_embeddings(
    ["Artificial intelligence market and adoption reports"]
)[0]

for client_id, expected in {
    "C-01": {"R-101", "R-103"},
    "C-02": {"R-103"},
}.items():
    result = search_chunks(
        query_embedding=query_embedding,
        client_id=client_id,
        limit=20,
    )

    metadata = result.get("metadatas", [[]])[0]
    actual = {item["report_id"] for item in metadata}

    print(f"{client_id}: {sorted(actual)}")
    assert actual == expected, (
        f"Permission mismatch for {client_id}: expected {expected}, got {actual}"
    )

print("All entitlement checks passed!")
