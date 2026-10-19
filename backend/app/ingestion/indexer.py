
from pathlib import Path

from app.ingestion.document_loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.rag.embeddings import generate_embeddings
from app.rag.retriever import add_chunks

REPORTS_DIR = Path(__file__).resolve().parents[3] / "data" / "reports"


def ingest_pdf(
    file_path: str,
    client_id: str,
    report_id: str,
    sector: str,
    region: str,
    year: int,
) -> int:
    documents = load_pdf(
        file_path=file_path,
        report_id=report_id,
        sector=sector,
        region=region,
        year=year,
    )

    chunks = chunk_documents(documents)

    for chunk in chunks:
        chunk["metadata"]["client_id"] = client_id

    embeddings = generate_embeddings(
        [chunk["text"] for chunk in chunks]
    )

    add_chunks(chunks, embeddings)
    return len(chunks)
