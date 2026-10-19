
from pathlib import Path
from reportlab.pdfgen import canvas

REPORTS_DIR = Path(__file__).resolve().parents[1] / "data" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

reports = [
    ("R-101", "Enterprise AI Market", [
        "Enterprise AI market revenue was USD 4.21 billion in 2024.",
        "The market is projected to grow at a CAGR of 11.2% from 2025 to 2030.",
        "Asia Pacific accounted for 38% of the market in 2024.",
        "Scope includes hardware, software and services."
    ]),
    ("R-102", "Enterprise AI Hardware Market", [
        "Enterprise AI hardware revenue was USD 3.87 billion in 2024.",
        "The market is projected to grow at a CAGR of 9.8% from 2024 to 2029.",
        "Asia Pacific accounted for 41% of the market in 2024.",
        "Scope covers hardware only, not software or services."
    ]),
    ("R-103", "Global AI Adoption", [
        "AI adoption varies across industries and regions.",
        "Enterprise adoption depends on cost, infrastructure and skills.",
        "This report does not provide a directly comparable total market revenue."
    ]),
    ("R-104", "Healthcare AI", [
        "Healthcare AI applications include medical imaging and workflow automation.",
        "Adoption depends on privacy, regulation and clinical validation."
    ]),
    ("R-105", "Financial Services AI", [
        "Financial institutions use AI for fraud detection and risk analysis.",
        "Model governance and data quality are important implementation factors."
    ]),
    ("R-106", "Retail AI", [
        "Retail AI applications include demand forecasting and personalization.",
        "Results depend on data quality, customer behavior and deployment scope."
    ]),
]

for report_id, title, lines in reports:
    path = REPORTS_DIR / f"{report_id}.pdf"
    pdf = canvas.Canvas(str(path))
    pdf.setTitle(title)
    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, title)
    y -= 35

    pdf.setFont("Helvetica", 11)
    for line in lines:
        pdf.drawString(50, y, line)
        y -= 25

    pdf.save()
    print(f"Created: {path.name}")

print(f"\nDone! Created {len(reports)} sample PDFs in {REPORTS_DIR}")
