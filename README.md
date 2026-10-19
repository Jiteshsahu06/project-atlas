
# Project Atlas — Generative & Agentic AI

## 1. Overview
Project Atlas is a prototype market-research assistant designed to retrieve evidence from PDF reports, apply client-level access controls, and expose functionality through a FastAPI service.

The current implementation includes PDF ingestion, text chunking, sentence embeddings, ChromaDB retrieval, client entitlements, MySQL persistence, basic request routing, and API-key authentication.

## 2. Architecture

PDF Reports → PDF Loader → Chunking → Sentence Embeddings → ChromaDB  
User → FastAPI → API-Key Validation → Question Router → Entitlement-Aware Retrieval → Response / Escalation → MySQL

## 3. Technology Stack
- Python 3.12
- FastAPI and Uvicorn
- ChromaDB
- Sentence Transformers (`all-MiniLM-L6-v2`)
- MySQL
- Pydantic
- Pytest
- PHP / CodeIgniter 3 integration: pending or partial; see limitations.

## 4. Project Structure
- `backend/app/main.py` — FastAPI application and authentication
- `backend/app/api/routes.py` — API routes
- `backend/app/ingestion/` — PDF ingestion and chunking
- `backend/app/rag/` — embeddings and retrieval
- `backend/app/agents/` — question routing and evidence checks
- `backend/app/services/` — chat and escalation logic
- `backend/tests/` — automated tests
- `data/reports/` — synthetic demonstration PDFs
- `evaluation/` — evaluation questions, results, and failure analysis

## 5. Setup

Create and activate a Python virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

Configure `backend/.env` with your local MySQL settings and a private API key. Never commit `.env` or real secrets.

Ensure the MySQL database and required tables exist before starting the API.

## 6. Run the API

From the project root:

```powershell
$env:PYTHONPATH = ".\backend"
uvicorn app.main:app --app-dir backend --reload
```

API documentation: `http://127.0.0.1:8000/docs`

## 7. API Endpoints
- `GET /health` — health status
- `GET /` — service status
- `POST /chat` — submit a question
- `GET /escalations?client_id=C-01` — retrieve a client's escalation tickets

Protected endpoints require the `X-API-Key` header.

Example request:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/chat" `
  -Headers @{"X-API-Key"="YOUR_LOCAL_API_KEY"} `
  -ContentType "application/json" `
  -Body '{"client_id":"C-01","message":"What was the enterprise AI market revenue in 2024?"}'
```

## 8. Client Entitlements
- C-01: R-101 and R-103
- C-02: R-103 only

The retriever filters results by client ID and authorized report IDs. Synthetic report content is used for demonstration and must not be treated as real market research.

## 9. Tests

Run the backend tests:

```powershell
$env:PYTHONPATH = ".\backend"
python -m pytest .\backend\tests\ -v
```

Last recorded result: 12 tests passed. Rerun the suite before submission.

## 10. Evaluation
See `evaluation/evaluation_questions.csv`, `evaluation/evaluation_results.csv`, and `evaluation/failure_analysis.md`.

Evaluation statuses must reflect actual test runs. Pending or unverified behaviors must not be reported as successful.

## 11. Current Limitations
- The current response pipeline is primarily retrieval-based and does not yet provide a complete production-grade LLM agent workflow.
- Fact checking is basic and does not independently verify every claim.
- Calculator-tool integration requires validation.
- Conflict handling and confidence-based escalation need further evaluation.
- PHP/CodeIgniter 3 frontend integration and Docker Compose may be incomplete.
- The evaluation results require actual execution and evidence.
- Synthetic PDFs are demonstration data, not published market reports.

## 12. Future Improvements
- Add a production-grade LLM with structured prompts and source-grounded answers.
- Implement deterministic calculation tools and stronger claim verification.
- Improve conflict detection and confidence-based escalation.
- Complete the CodeIgniter 3 interface and Docker Compose deployment.
- Expand automated security, entitlement, and evaluation coverage.
- Add monitoring, structured logs, and deployment documentation.

## 13. AI Assistance Disclosure
AI assistance was used for parts of implementation, debugging, documentation, and test preparation. Review and update this disclosure to accurately describe the tools used and the work completed by the author.
