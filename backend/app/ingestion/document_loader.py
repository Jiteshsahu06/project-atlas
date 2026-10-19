
from pathlib import Path
from pypdf import PdfReader


def load_pdf(
    file_path: str,
    report_id: str,
    sector: str,
    region: str,
    year: int,
) -> list[dict]:
    path = Path(file_path)

    if not path.exists() or path.suffix.lower() != ".pdf":
        raise ValueError("A valid PDF file path is required.")

    reader = PdfReader(str(path))
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append({
                "text": text,
                "metadata": {
                    "report_id": report_id,
                    "sector": sector,
                    "region": region,
                    "year": year,
                    "page": page_number,
                    "source": path.name,
                },
            })

    return documents
