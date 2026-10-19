
from app.ingestion.indexer import ingest_pdf
from pathlib import Path

reports_dir = Path("data/reports")

tasks = [
    ("C-01", "R-101", "Enterprise AI", "Global", 2024),
    ("C-01", "R-103", "AI Adoption", "Global", 2024),
    ("C-02", "R-103", "AI Adoption", "Global", 2024),
]

for client_id, report_id, sector, region, year in tasks:
    file_path = reports_dir / f"{report_id}.pdf"

    count = ingest_pdf(
        file_path=str(file_path),
        client_id=client_id,
        report_id=report_id,
        sector=sector,
        region=region,
        year=year,
    )

    print(f"{client_id} | {report_id} | {count} chunks ingested")

print("Re-ingestion completed.")

