# User Stories

This deliverable translates part of the requirements into user stories suitable for a backlog.
Each story is linked to at least one requirement and has acceptance criteria. One story (US-003)
is split into two smaller stories with justification.

## US-001 — Add evidence with traceable metadata
As a **Contributor**,
I want to add an evidence item with its source, owner and freshness date,
so that readiness claims are backed by traceable evidence.

- Linked requirement(s): REQ-002, REQ-010
- Acceptance Criteria:
  - AC-1: The evidence item is saved only when `source`, `owner` and `freshness_date` are all provided.
  - AC-2: If a mandatory field is missing, the item is rejected with an inline message.
  - AC-3: A saved item appears in the assessment's evidence list.

## US-002 — See missing critical information
As a **Transition Lead**,
I want to see which mandatory readiness areas still lack complete evidence,
so that I know what to collect before submitting.

- Linked requirement(s): REQ-003
- Acceptance Criteria:
  - AC-1: Each mandatory area without complete evidence is listed as missing.
  - AC-2: When every mandatory area has complete evidence, the missing list is empty.

## US-003 — Submit the final assessment
As a **Transition Lead**,
I want to submit the final assessment only when it is complete and I am authorized,
so that only valid and accountable assessments are recorded.

- Linked requirement(s): REQ-005, REQ-008, REQ-003, REQ-004
- Acceptance Criteria:
  - AC-1: A Transition Lead can submit when nothing critical is missing and no critical evidence is stale.
  - AC-2: A non-Transition-Lead user attempting to submit is denied; the assessment stays `draft`.
  - AC-3: Submission is blocked while critical information is missing or critical evidence is stale (baseline).

> US-003 is intentionally large — it bundles two independent concerns (authorization and
> data validity). It is split below.

## US-004 — Flag stale evidence
As a **Security Officer**,
I want evidence older than 90 days to be flagged as stale,
so that readiness is based on current evidence.

- Linked requirement(s): REQ-004
- Acceptance Criteria:
  - AC-1: Evidence with `freshness_date` older than 90 days is marked `stale`.
  - AC-2: Evidence exactly 90 days old is not stale; 91 days old is stale (boundary).

## US-005 — Review readiness result and score
As an **AMS Manager**,
I want to see the readiness status and a readiness/risk score,
so that I can prioritize actions for the first 90 days.

- Linked requirement(s): REQ-006, REQ-007
- Acceptance Criteria:
  - AC-1: The result shows a status (`ready` / `not ready`) and the missing-information list.
  - AC-2: The readiness score is deterministic for the same input.

---

## Story split

### Original story
**US-003 — Submit the final assessment** (linked to REQ-005, REQ-008, REQ-003, REQ-004).

### Split into
- **US-003a — Enforce role authorization on submission**
  As a **Security Officer**, I want only the Transition Lead role to be able to submit,
  so that submissions are accountable.
  - Linked requirement(s): REQ-008, REQ-005
  - Acceptance Criteria:
    - AC-1: A submission request from a role other than Transition Lead is denied.
    - AC-2: A denied attempt leaves the assessment in `draft`.

- **US-003b — Enforce completeness and validity on submission**
  As a **Transition Lead**, I want submission to be blocked while critical information is
  missing or critical evidence is stale, so that only valid assessments are submitted.
  - Linked requirement(s): REQ-003, REQ-004, REQ-005
  - Acceptance Criteria:
    - AC-1: Submission is blocked while any mandatory area lacks complete evidence.
    - AC-2: Submission is blocked while any critical evidence item is stale (baseline).
    - AC-3: When both checks pass, a Transition Lead submission sets status to `submitted`.

### Justification
The original US-003 mixes **two independent concerns**: *who is allowed to submit* (authorization)
and *whether the data is valid* (completeness and freshness). Following **INVEST** (each story
should be Independent, Small and Testable), splitting them lets each be developed and tested
separately — a dedicated role/security test for US-003a and completeness/boundary tests for
US-003b. It also produces smaller, independently deliverable increments and makes the change
request easier to absorb (the role rule and the freshness rule can change independently).
