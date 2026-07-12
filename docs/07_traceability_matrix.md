# Traceability Matrix

This deliverable links the artefacts end to end:
`OBJ → CSF → REQ → UC → US → AC → TC/BDD → Data Entity / Model → Automated Test`.

> **Baseline note.** This is the **traceability baseline** committed *before* the change request
> (commit message `D7 Add traceability matrix baseline`). The data entities (`Assessment`,
> `Evidence`, `UserRole`) are defined in `docs/10_data_architecture.md`, and the automated tests
> (`AT-001…AT-004`) in `docs/12_automated_tests.md`; both are referenced here so the chains are
> complete. The RFC-tool chain from the change request will be added in `docs/09_change_request.md`
> only after this baseline is committed.

## Matrix

| Objective | CSF | Requirement | Use Case | User Story | Acceptance Criteria | Test Case / BDD Scenario | Data Entity / Model | Automated Test |
|---|---|---|---|---|---|---|---|---|
| OBJ-01 | CSF-01 | REQ-001 Create assessment | UC-01 | US-003 | REQ-001 AC-1, AC-2 | TC-002 | Assessment | AT-001 |
| OBJ-02 | CSF-02 | REQ-002 Add evidence metadata | UC-02 | US-001 | REQ-002 AC-1, AC-2 | TC-001, TC-003 | Evidence | AT-001, AT-002 |
| OBJ-01 | CSF-01 | REQ-003 Identify missing critical info | UC-04 | US-002, US-003b | REQ-003 AC-1, AC-2 | TC-004 / Scenario: Missing evidence | Assessment, Evidence | AT-002 |
| OBJ-02 | CSF-02 | REQ-004 Detect stale evidence (baseline: block) | UC-03 | US-004 | REQ-004 AC-1, AC-2, AC-3 | TC-005, TC-006 | Evidence | AT-003 |
| OBJ-03 | CSF-03 | REQ-005 Submit final assessment | UC-05 | US-003, US-003b | REQ-005 AC-1, AC-2, AC-3 | TC-002, TC-004, TC-008 / Scenario: Happy path | Assessment, UserRole | AT-001, AT-004 |
| OBJ-01 | CSF-01 | REQ-006 Readiness result and score | UC-06 | US-005 | REQ-006 AC-1, AC-2 | TC-002 | Assessment | AT-001 |
| OBJ-01 | CSF-01 | REQ-007 Validation performance | UC-06 | US-005 | REQ-007 AC-1 | TC-007 | Assessment, Evidence | (performance — measured in TC-007) |
| OBJ-03 | CSF-03 | REQ-008 Role-based authorization | UC-05 | US-003a | REQ-008 AC-1, AC-2 | TC-008 / Scenario: Unauthorized user | UserRole | AT-004 |
| OBJ-01 | CSF-01 | REQ-009 Guided evidence entry | UC-02 | US-001 | REQ-009 AC-1, AC-2 | TC-003 | Evidence | AT-002 |
| OBJ-02 | CSF-02 | REQ-010 Mandatory evidence fields | UC-02 | US-001 | REQ-010 AC-1, AC-2 | TC-001, TC-003 | Evidence | AT-002 |
| OBJ-02 | CSF-02 | REQ-011 Raise an RFC *(CR-01)* | UC-07 | US-006 | REQ-011 AC-1, AC-2 | TC-009, TC-010 / Scenario: RFC — only the Transition Lead can raise an RFC | RFC | AT-005 |
| OBJ-02 | CSF-02 | REQ-012 Respond to an RFC *(CR-01)* | UC-07 | US-006 | REQ-012 AC-1, AC-2 | TC-009 | RFC, RFCResponse | AT-005 |

> **Post-change-request update.** The rows marked *(CR-01)* (REQ-011, REQ-012 — the RFC tool) were
> added **after** the baseline commit, as part of processing the change request (`docs/09`). The
> `RFC` / `RFCResponse` entities are defined in `docs/10_data_architecture.md` and the automated
> test `AT-005` in `docs/12_automated_tests.md`.

## Traceability chain (explained)

Chain type: **security / role rule** (also exercised by the app logic and an automated test).

- Objective: **OBJ-03** — Enable prioritized and accountable action for the first 90 days.
- CSF: **CSF-03** — Only authorized roles can submit the final assessment, and missing critical information is summarized.
- Requirement: **REQ-008** — The system enforces role-based authorization so that only the `Transition Lead` role can submit a final assessment; unauthorized attempts are denied and recorded.
- Use Case / User Story: **UC-05** (Submit final assessment, exception EX-1 unauthorized) / **US-003a** (Enforce role authorization on submission).
- Acceptance Criteria: REQ-008 AC-1 (non-Transition-Lead submission denied), AC-2 (denied attempt leaves assessment in `draft`).
- Test Case / BDD Scenario: **TC-008** (Contributor cannot submit) and BDD **Scenario: Unauthorized user — Contributor cannot submit the final assessment**.
- Data Entity / Model: **UserRole** (role of the acting user) and **Assessment** (status unchanged on denial).
- Automated Test: **AT-004** — loads a Contributor and a Transition Lead from the test database and asserts the Contributor cannot submit while the Transition Lead can.

### Explanation
- **Why the requirement supports the objective:** OBJ-03 requires *accountable* action. Accountability only holds if submissions come from an authorized owner. REQ-008 guarantees that only the Transition Lead — the accountable role for the transition — can commit a final assessment, so the readiness decision has a clear owner.
- **Why the test validates the requirement:** AT-004 (and TC-008 / the BDD unauthorized scenario) exercises the exact rule using real stored users: a Contributor's submission must be denied and must not change the assessment status, while the Transition Lead's must succeed. If authorization were not enforced, AT-004 would fail because the Contributor's submission would change the status.
- **What would be affected if the requirement changed:** if REQ-008 changed (for example, if the change request allowed AMS Managers to submit, or allowed Contributors to submit under conditions), then UC-05, US-003a, TC-008, the BDD unauthorized scenario, the `UserRole` handling and AT-004 would all have to be updated together. This is the propagation the change request is designed to test.
