# Project Atlas — Generative & Agentic AI Market Research Assistant

## 1. Project Overview

Project Atlas is a prototype market research assistant designed to retrieve evidence from PDF reports, enforce client-level report access controls, and expose its functionality through a FastAPI service.

The project demonstrates PDF ingestion, text chunking, sentence embeddings, ChromaDB vector retrieval, MySQL persistence, question routing, API-key authentication, and escalation handling.

**Important:** The reports included in this repository are synthetic demonstration data. They do not represent real market research or published commercial findings.

## 2. Problem Statement

Market research analysts often need to review multiple reports, verify figures, identify differences in source scope, and respond to client questions.

Project Atlas explores how a retrieval-based assistant can help analysts by:

- Retrieving relevant report evidence.
- Enforcing client-specific report entitlements.
- Returning evidence with report and page references.
- Rejecting unsafe or out-of-scope requests.
- Recording conversations and escalating uncertain requests for human review.

## 3. Architecture

```text
PDF Reports
    |
    v
PDF Loader
    |
    v
Text Chunking + Metadata
    |
    v
Sentence Transformer Embeddings
    |
    v
ChromaDB Vector Store

Client Question
    |
    v
FastAPI + API-Key Authentication
    |
    v
Question Router
    |
    v
Entitlement-Aware Retrieval
    |
    v
Evidence Response / Escalation
    |
    v
MySQL Persistence
```

The current implementation is primarily retrieval-based. A complete production-grade LLM agent workflow has not yet been validated.

## 4. Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- ChromaDB
- Sentence Transformers (`all-MiniLM-L6-v2`)
- MySQL
- Pydantic
- Pytest
- Git and GitHub

PHP/CodeIgniter 3 and Docker Compose are planned integration components whose end-to-end operation still requires validation.

## 5. Repository Structure

```text
project-atlas/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── database/
│   │   ├── ingestion/
│   │   ├── rag/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── data/
│   ├── reports/
│   └── evaluation/
├── database/
├── docs/
├── evaluation/
├── frontend/
│   └── ci3/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 6. Prerequisites

- Python 3.12
- MySQL Server
- Git
- Windows PowerShell or a compatible terminal

Docker is required only if testing the containerized deployment.

## 7. Local Setup

Run commands from the project root.

### Create a virtual environment

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

If the environment already exists in the parent directory, activate that existing environment instead of creating another one.

### Install dependencies

```powershell
pip install -r backend\requirements.txt
```

### Configure environment variables

Create `backend/.env` using `backend/.env.example` as a reference.

Configure the required local settings, including:

- `ATLAS_API_KEY`
- MySQL host
- MySQL port
- MySQL database name
- MySQL username
- MySQL password

Use your own credentials. Never commit `.env` files, API keys, or database passwords to Git.

### Prepare the database

Create the required database and tables using the SQL files in `database/`. Ensure the local MySQL credentials match the application configuration.

## 8. Start the API

From the project root:

```powershell
$env:PYTHONPATH = ".\backend"
uvicorn app.main:app --app-dir backend --reload
```

The API should be available at:

- API root: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

The interactive documentation can be used to submit requests and inspect actual responses.

## 9. API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | API status |
| `GET /health` | Health status |
| `POST /chat` | Submit a client question |
| `GET /escalations?client_id=C-01` | Retrieve escalation records for a client |

Protected routes require the `X-API-Key` header.

**Ingestion endpoint:** The assignment requests `POST /ingest`. Its availability and behavior must be verified before it is considered complete. The current ingestion functionality also has a Python ingestion entry point.

### Example chat request

Replace the placeholder API key with your local value. Do not share or commit the key.

```powershell
$headers = @{
    "X-API-Key" = "YOUR_LOCAL_API_KEY"
}

$body = @{
    client_id = "C-01"
    message = "What was the enterprise AI market revenue in 2024?"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/chat" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body
```

## 10. Knowledge Base and Client Entitlements

The prototype includes six synthetic PDF reports, `R-101` through `R-106`.

The demonstration entitlement configuration is:

| Client | Authorized reports |
|---|---|
| C-01 | R-101, R-103 |
| C-02 | R-103 |

The retriever filters results by client ID and authorized report IDs before returning report text.

This is a prototype-level entitlement implementation. A production deployment would require authorization data to be managed centrally and verified on every relevant request.

## 11. Design Decisions and Trade-offs

- **ChromaDB:** Selected for local vector retrieval and a straightforward development setup.
- **Sentence Transformers:** Provides local embeddings without requiring a paid embedding API for vectorization.
- **Metadata filtering:** Supports client-level report access restrictions during retrieval.
- **MySQL:** Stores conversation and escalation records.
- **FastAPI:** Provides typed request validation and interactive API documentation.
- **Synthetic reports:** Make the demonstration reproducible but cannot establish the accuracy of real market research.
- **Retrieval-first approach:** Prioritizes showing available evidence instead of presenting unverified generated conclusions.
- **Scope trade-off:** Full LLM orchestration, CI3 integration, and containerized deployment require further implementation and validation.

## 12. Testing

Run the automated backend tests from the project root:

```powershell
$env:PYTHONPATH = ".\backend"
python -m pytest .\backend\tests\ -v
```

The last recorded test run passed all 12 tests.

The test suite covers health and root endpoints, request validation, API-key requirements, and basic client entitlement checks.

Run the test suite again before submission and preserve the actual output.

**Important:** Passing these 12 tests does not establish that every assignment requirement is complete or that the 25-question evaluation is successful.

## 13. Evaluation

Evaluation-related files are located in `evaluation/`:

- `evaluation_questions.csv`
- `evaluation_results.csv`
- `evaluation_report.md`
- `failure_analysis.md`
- `run_evaluation.py`

The assignment requires at least 25 evaluation questions, measurement of correctness, citation accuracy, refusal accuracy and conflict detection, and an honest analysis of at least five failures.

The presence of evaluation files does not itself demonstrate that every evaluation was executed successfully. Results should be supported by actual runs and observed outputs. Do not mark untested scenarios as passing.

## 14. Security Considerations

The prototype includes API-key validation and client-level report filtering.

Before production use, additional verification is required for:

- Prompt-injection detection and logging.
- Read-only SQL enforcement and query timeouts.
- Request timeouts and rate limiting.
- Robust authorization and escalation policies.
- Output escaping and CSRF protection in a PHP interface.
- Secret management and deployment configuration.

Never expose private client information or credentials in a response, log, screenshot, video, or repository.

## 15. Current Limitations

- The response pipeline is primarily retrieval-based and is not a complete production-grade LLM agent system.
- The fact-checker performs basic checks and does not independently verify every numerical claim.
- Calculator-tool integration requires further validation.
- Conflict detection and confidence-based escalation need broader evaluation.
- Full PHP/CodeIgniter 3 integration has not been verified end to end.
- Docker Compose deployment has not been verified end to end.
- The requested `POST /ingest` API endpoint must be confirmed.
- The 25-question evaluation and its metrics require actual execution and evidence.
- The six PDFs contain synthetic demonstration data rather than published market reports.

## 16. What I Would Do With One More Week

With one additional week, I would prioritize the following improvements:

1. Complete the LLM-powered workflow with structured routing, retrieval, calculation, and evidence-grounded responses.
2. Strengthen conflict detection so that different report scopes and forecast periods are clearly explained rather than averaged.
3. Add deterministic CAGR calculations with explicit formulas, assumptions, and derived-value labels.
4. Improve prompt-injection handling and create auditable security logs.
5. Complete and test the CodeIgniter 3 controller, service library, chat view, feedback storage, CSRF protection, and XSS-safe output handling.
6. Validate Docker Compose from a clean environment and document reproducible startup instructions.
7. Execute the full 25-question evaluation, report metrics, and investigate at least five observed failures.
8. Add structured logging, latency measurements, and operational monitoring.

The priority would be correctness, client confidentiality, reproducibility, and honest reporting of system limitations.

## 17. AI-Assistance Disclosure

AI coding assistance was used during parts of project planning, implementation support, debugging, documentation drafting, and test preparation.

The author should review this statement and ensure that it accurately describes the tools used and the portions of work they assisted with. The author is responsible for understanding, validating, and explaining the submitted code.

## 18. Submission Checklist

- [ ] Git repository is accessible to the reviewer.
- [ ] Commit history is visible and no secrets have been committed.
- [ ] README setup instructions have been checked.
- [ ] Evaluation results reflect actual runs.
- [ ] At least five failures are analyzed honestly.
- [ ] A 3–5 minute demo video shows the required scenarios that actually run.
- [ ] The one-page improvement note is included.
- [ ] AI-assistance disclosure is accurate.
- [ ] Repository and demo video links have been sent to the recruiter.

## 19. Disclaimer

Project Atlas is an educational prototype developed for the take-home assignment. It is not a production-ready market research service. All demonstration report content and client examples are fictional.
