
# Project Atlas — Failure Analysis

Note: These are anticipated failure scenarios. They must be reproduced and verified before being reported as observed failures.

## 1. Unauthorized Report Access
**Scenario:** Client C-02 asks for information from R-101.
**Expected behavior:** The system must not reveal R-101 because C-02 is authorized only for R-103.
**Risk:** Cross-client data leakage.
**Mitigation:** Apply client entitlements before returning retrieved documents.
**Validation:** Test C-02 queries and verify returned metadata contains only R-103.

## 2. Conflicting Market Figures
**Scenario:** R-101 reports USD 4.21B for hardware, software, and services, while R-102 reports USD 3.87B for hardware only.
**Expected behavior:** Explain that the scopes differ; do not average the figures or present them as directly comparable.
**Risk:** Misleading business conclusions.
**Mitigation:** Preserve report scope, period, and citation metadata.
**Validation:** Ask a comparison question and inspect the answer and citations.

## 3. Prompt Injection in Retrieved Content
**Scenario:** A report contains instructions asking the assistant to ignore permissions or reveal secrets.
**Expected behavior:** Treat report text as untrusted evidence, not as system instructions.
**Risk:** Data disclosure or policy bypass.
**Mitigation:** Separate trusted instructions from retrieved content and test adversarial documents.
**Validation:** Submit a prompt-injection test and record the actual response.

## 4. Unsupported Calculation
**Scenario:** A user requests a CAGR or future market size without sufficient starting values, ending values, or time period.
**Expected behavior:** Use a verified calculation method when inputs are available; otherwise explain what information is missing.
**Risk:** Incorrect forecasts or invented figures.
**Mitigation:** Validate inputs and use a deterministic calculator.
**Validation:** Test known calculations and cases with missing inputs.

## 5. Insufficient Evidence and Escalation
**Scenario:** Retrieval returns no relevant authorized evidence, or a comparison lacks sufficient sources.
**Expected behavior:** Avoid unsupported claims and create an escalation ticket when required.
**Risk:** Fabricated or incomplete answers.
**Mitigation:** Set confidence thresholds and persist escalation details in MySQL.
**Validation:** Check the API response and verify the escalation record in the database.
