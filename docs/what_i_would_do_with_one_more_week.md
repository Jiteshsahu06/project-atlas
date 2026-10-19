# What I Would Do With One More Week

If I had one additional week to work on Project Atlas, I would focus on completing the remaining functionality, improving security, and validating the application end to end.

## 1. Complete the Agent Workflow
I would implement and validate the complete workflow for question routing, entitlement-aware retrieval, deterministic calculations, conflict detection, evidence verification, and final response generation.

## 2. Strengthen Security
I would expand entitlement tests, validate read-only SQL restrictions, test prompt-injection attacks, and ensure that confidential information and API credentials are never exposed.

## 3. Improve Conflict Detection and Citations
I would ensure that every numerical claim is supported by the correct report citation. Conflicting market figures would be explained using their market scope and reporting periods rather than averaged.

## 4. Complete Escalation and Evaluation
I would verify that questions with insufficient evidence generate escalation tickets in MySQL. I would execute the evaluation dataset, measure correctness and citation accuracy, and document at least five reproducible failures.

## 5. Complete CI3 Integration and Deployment
I would complete and test the CodeIgniter 3 controller, Python API integration, feedback functionality, and Docker Compose setup. I would verify that a reviewer can run the application using only the README instructions.

## 6. Improve Observability and Documentation
I would add structured logging, latency and error tracking, improve setup instructions, and make the evaluation process reproducible.

**Priority:** My primary goal would be to deliver a reliable, secure, and fully tested end-to-end application, prioritizing correctness and transparency over adding unverified features.