
def chunk_documents(
    documents: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap.")

    chunks = []

    for document in documents:
        text = document["text"]
        metadata = document["metadata"]

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata.copy(),
                })

            if end == len(text):
                break

            start = end - overlap

    return chunks
