# Objectives, CSFs and Requirements

This deliverable defines the product objectives, the Critical Success Factors (CSFs) that
support them, and 10 structured requirements (6 functional, 3 non-functional, 1 constraint /
business rule) for the **AMS Transition Intake & Readiness Assessment** module. It also rewrites
five of the poorly written initial requirements (R1–R10).

## A) Product Objectives

| ID | Objective |
|---|---|
| OBJ-01 | Improve readiness visibility for AMS transition stakeholders — make it clear whether *OrderCare* is ready to be supported by the AMS team. |
| OBJ-02 | Ensure transition information is evidence-backed and current — every readiness claim is supported by traceable, non-stale evidence. |
| OBJ-03 | Enable prioritized and accountable action for the first 90 days — surface missing critical information and control who can submit the final assessment. |

## B) Critical Success Factors

| ID | CSF | Linked objective |
|---|---|---|
| CSF-01 | Critical AMS transition information is complete and its readiness status is clearly visible to stakeholders. | OBJ-01 |
| CSF-02 | Every evidence item has a verifiable source, owner and freshness date, and stale evidence is detected. | OBJ-02 |
| CSF-03 | Only authorized roles can submit the final assessment, and missing critical information is summarized so the team can act. | OBJ-03 |

## C) Structured requirements

Summary: **6 functional (REQ-001…006), 3 non-functional (REQ-007…009), 1 constraint / business rule (REQ-010)**.

### REQ-001 — Create readiness assessment
- Type: Functional
- Stakeholder: Transition Lead
- Priority: High
- Description: A Transition Lead can create a new readiness assessment for an application. A new assessment starts in status `draft`.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Creating an assessment persists a record with a unique id and status `draft`.
  - AC-2: A newly created assessment has no evidence and is not submittable until critical evidence is present.
- Validation method: Test / Demo

### REQ-002 — Add evidence metadata
- Type: Functional
- Stakeholder: Contributor, Transition Lead
- Priority: High
- Description: A user can add evidence items to an assessment. Each evidence item records `source`, `owner`, `freshness_date`, `category` and `criticality`.
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: An evidence item can only be saved when `source`, `owner` and `freshness_date` are all provided.
  - AC-2: If any of `source`, `owner` or `freshness_date` is missing, the item is rejected with a validation message.
- Validation method: Test / Demo

### REQ-003 — Identify missing critical information
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: High
- Description: The system identifies which mandatory readiness areas (e.g. monitoring, DR, access, integrations, SLA) have no complete evidence and lists them as *missing critical information*.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: For each mandatory area without complete evidence, the area is listed as missing critical information.
  - AC-2: When all mandatory areas have complete evidence, the missing-information list is empty.
- Validation method: Test / Demo

### REQ-004 — Detect stale evidence and block submission *(baseline)*
- Type: Functional
- Stakeholder: Security Officer, Transition Lead
- Priority: High
- Description: Evidence whose `freshness_date` is more than **90 days** before the assessment date is considered **stale**. In the baseline, stale critical evidence is treated as invalid and **prevents final submission**.
  > Note: Q-007 (D1) leaves *block vs flag* open. The baseline assumes **block**; this is a
  > candidate for the change request (`docs/09_change_request.md`).
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: Evidence with `freshness_date` older than 90 days is marked `stale = true`.
  - AC-2: Evidence exactly 90 days old is **not** stale; 91 days old **is** stale (boundary).
  - AC-3: An assessment with stale critical evidence cannot be submitted.
- Validation method: Test

### REQ-005 — Submit final assessment (role-controlled)
- Type: Functional
- Stakeholder: Transition Lead
- Priority: High
- Description: A final assessment can be submitted only when all critical information is present and valid. In the baseline, **only the Transition Lead** role may submit; other roles are denied.
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: A Transition Lead can submit when no critical information is missing and no critical evidence is stale; status becomes `submitted`.
  - AC-2: A non-Transition-Lead user attempting to submit is denied and the assessment remains `draft`.
  - AC-3: Submission is blocked while critical information is missing, regardless of role.
- Validation method: Test / Demo

### REQ-006 — Display readiness result and risk/readiness score
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: Medium
- Description: The system shows a readiness result: overall status, the list of missing critical information, and a simple readiness/risk score computed from complete vs missing/stale critical items.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: The result shows a status (e.g. `ready` / `not ready`) and the list of missing critical information.
  - AC-2: The readiness score is a value derived from the ratio of complete critical items to total critical items (deterministic for the same input).
- Validation method: Test / Demo

### REQ-007 — Readiness validation performance
- Type: Non-functional (Performance)
- Stakeholder: Client Manager
- Priority: Medium
- Description: Readiness validation (completeness + freshness + score) for a typical assessment (≤ 50 evidence items) completes in **≤ 3 seconds** on a standard laptop.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: For an assessment with 50 evidence items, validation returns in ≤ 3 seconds (measured).
- Validation method: Measurement
- Rewrites: R1 ("The system must be fast").

### REQ-008 — Role-based authorization for submission
- Type: Non-functional (Security)
- Stakeholder: Security Officer
- Priority: High
- Description: The system enforces role-based authorization so that only users with the `Transition Lead` role can submit a final assessment. Unauthorized submission attempts are denied and recorded.
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: A submission request from a role other than `Transition Lead` is denied.
  - AC-2: A denied attempt does not change the assessment status.
- Validation method: Test
- Rewrites: R3 ("The system should be secure"), refines R8 ("Use Microsoft authentication").

### REQ-009 — Guided evidence entry (usability)
- Type: Non-functional (Usability)
- Stakeholder: Contributor
- Priority: Low
- Description: A user can complete the evidence-entry flow using only the three mandatory fields, with inline validation messages, without external documentation.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: The evidence form requires exactly three mandatory fields (`source`, `owner`, `freshness_date`).
  - AC-2: When a mandatory field is empty, an inline message identifies the missing field.
- Validation method: Demo / Review
- Rewrites: R10 ("It should be user-friendly").

### REQ-010 — Mandatory evidence fields *(constraint / business rule)*
- Type: Constraint / Business rule
- Stakeholder: Transition Lead, Security Officer
- Priority: High
- Description: Every evidence item **must** include `source`, `owner` and `freshness_date`. An assessment cannot be submitted while any critical evidence item is missing one of these fields. Persistence for the module is limited to **SQLite** (see `docs/10_data_architecture.md`).
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: Persistence rejects an evidence item without `source`, `owner` or `freshness_date`.
  - AC-2: Submission is blocked while a critical evidence item lacks a mandatory field.
- Validation method: Test / Review

### Requirement summary table

| ID | Title | Type | Priority | OBJ | CSF |
|---|---|---|---|---|---|
| REQ-001 | Create readiness assessment | Functional | High | OBJ-01 | CSF-01 |
| REQ-002 | Add evidence metadata | Functional | High | OBJ-02 | CSF-02 |
| REQ-003 | Identify missing critical information | Functional | High | OBJ-01 | CSF-01 |
| REQ-004 | Detect stale evidence and block submission | Functional | High | OBJ-02 | CSF-02 |
| REQ-005 | Submit final assessment (role-controlled) | Functional | High | OBJ-03 | CSF-03 |
| REQ-006 | Display readiness result and score | Functional | Medium | OBJ-01 | CSF-01 |
| REQ-007 | Readiness validation performance | NFR (Performance) | Medium | OBJ-01 | CSF-01 |
| REQ-008 | Role-based authorization for submission | NFR (Security) | High | OBJ-03 | CSF-03 |
| REQ-009 | Guided evidence entry | NFR (Usability) | Low | OBJ-01 | CSF-01 |
| REQ-010 | Mandatory evidence fields | Constraint / Business rule | High | OBJ-02 | CSF-02 |

## D) Rewrite of initial poor requirements

| Original | Problem | Rewritten version | Justification |
|---|---|---|---|
| R1: The system must be fast | NFR with no metric or context; not testable | **REQ-007** — Readiness validation for a typical assessment (≤50 evidence items) completes in ≤ 3 seconds on a standard laptop. | Adds a measurable threshold, a defined scope (validation operation) and a validation method (measurement), making it testable. |
| R3: The system should be secure | Vague; "secure" undefined; not testable | **REQ-008** — Only users with the `Transition Lead` role can submit a final assessment; unauthorized attempts are denied and recorded. | Turns an abstract quality into a concrete, testable authorization rule tied to the real stakeholder need (Security Officer). |
| R7: Managers need to know what is missing | No definition of "missing"; stakeholder imprecise; no acceptance criteria | **REQ-003** — The system lists each mandatory readiness area without complete evidence as *missing critical information* for the Transition Lead / AMS Manager. | Defines what "missing" means, names the consumer, and provides acceptance criteria that can be tested. |
| R9: The system should support risk scoring | Underspecified; no inputs, formula or output | **REQ-006** — The system computes a deterministic readiness/risk score from the ratio of complete critical items to total critical items, shown with the readiness result. | Specifies inputs, a deterministic computation and a visible output, making the requirement implementable and testable. |
| R10: It should be user-friendly | Subjective; no usability criteria | **REQ-009** — The evidence-entry flow uses exactly three mandatory fields with inline validation messages and needs no external documentation. | Replaces a subjective adjective with observable, demonstrable usability criteria. |
