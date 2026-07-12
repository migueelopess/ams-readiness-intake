# Test Cases, BDD and Validation

This deliverable defines 8 manual test cases (traceable to requirements and user stories), a BDD
feature with three scenarios (in `bdd/features/readiness.feature`), and the Definition of Done for
requirements, user stories and the final delivery.

Coverage summary: 2 happy path, 2 negative, 2 boundary/validation, 1 NFR, 1 role/security.

| TC | Type | Linked REQ/US |
|---|---|---|
| TC-001 | Happy path | REQ-002, REQ-010 / US-001 |
| TC-002 | Happy path | REQ-005 / US-003, US-003b |
| TC-003 | Negative | REQ-002, REQ-010 / US-001 |
| TC-004 | Negative | REQ-003, REQ-005 / US-002, US-003b |
| TC-005 | Boundary / validation | REQ-004 / US-004 |
| TC-006 | Boundary / validation | REQ-004 / US-004 |
| TC-007 | NFR (performance) | REQ-007 / US-005 |
| TC-008 | Role / security | REQ-008, REQ-005 / US-003a |
| TC-009 | Happy path *(CR-01)* | REQ-011, REQ-012 / US-006 |
| TC-010 | Role / security *(CR-01)* | REQ-011, REQ-008 / US-006 |

---

## TC-001 — Add evidence with all mandatory fields (happy path)
- Linked REQ/US: REQ-002, REQ-010 / US-001
- Type: Integration
- Priority: High
- Preconditions: An assessment exists in status `draft`.
- Test data: source="Grafana dashboard", owner="Ops Team", freshness_date=today, category="monitoring", criticality="high".
- Steps:
  1. Open the evidence form on the draft assessment.
  2. Fill source, owner and freshness_date.
  3. Save the evidence item.
- Expected result: The item is saved and appears in the evidence list with freshness status "current".

## TC-002 — Transition Lead submits a complete, valid assessment (happy path)
- Linked REQ/US: REQ-005 / US-003, US-003b
- Type: System
- Priority: High
- Preconditions: All mandatory readiness areas have complete, non-stale evidence; user role = Transition Lead.
- Test data: assessment with valid evidence in all mandatory areas (monitoring, DR, access, integrations, SLA).
- Steps:
  1. Log in as Transition Lead.
  2. Open the complete draft assessment.
  3. Request submission.
- Expected result: Status becomes `submitted`; the readiness result and score are shown; no missing critical information.

## TC-003 — Add evidence missing the owner (negative)
- Linked REQ/US: REQ-002, REQ-010, REQ-009 / US-001
- Type: Integration
- Priority: High
- Preconditions: An assessment exists in status `draft`.
- Test data: source="Runbook", owner="" (empty), freshness_date=today.
- Steps:
  1. Open the evidence form.
  2. Fill source and freshness_date, leave owner empty.
  3. Try to save.
- Expected result: The item is rejected; an inline message indicates that `owner` is required; nothing is persisted.

## TC-004 — Submit with missing critical information (negative)
- Linked REQ/US: REQ-003, REQ-005 / US-002, US-003b
- Type: System
- Priority: High
- Preconditions: At least one mandatory readiness area has no complete evidence; user role = Transition Lead.
- Test data: assessment missing DR evidence.
- Steps:
  1. Log in as Transition Lead.
  2. Open the incomplete draft assessment.
  3. Request submission.
- Expected result: Submission is blocked; the missing critical information (DR) is listed; the assessment stays `draft`.

## TC-005 — Evidence exactly 90 days old is not stale (boundary)
- Linked REQ/US: REQ-004 / US-004
- Type: Unit / Integration
- Priority: Medium
- Preconditions: An assessment exists; assessment/reference date is fixed.
- Test data: evidence with freshness_date = reference_date − 90 days.
- Steps:
  1. Add evidence with freshness_date exactly 90 days before the reference date.
  2. Run freshness evaluation.
- Expected result: The item is **not** marked stale (90 days is within the allowed period).

## TC-006 — Evidence 91 days old is stale and blocks submission (boundary/validation)
- Linked REQ/US: REQ-004 / US-004
- Type: Integration
- Priority: High
- Preconditions: An assessment with otherwise complete evidence; user role = Transition Lead.
- Test data: one critical evidence item with freshness_date = reference_date − 91 days.
- Steps:
  1. Add the 91-day-old critical evidence item.
  2. Run freshness evaluation.
  3. Attempt submission as Transition Lead.
- Expected result: The item is marked `stale`; submission is blocked (baseline) with the stale item listed; assessment stays `draft`.

## TC-007 — Readiness validation performance (NFR)
- Linked REQ/US: REQ-007 / US-005
- Type: System (performance)
- Priority: Medium
- Preconditions: An assessment with 50 evidence items.
- Test data: 50 evidence items across mandatory areas.
- Steps:
  1. Trigger readiness validation (completeness + freshness + score).
  2. Measure elapsed time.
- Expected result: Validation returns in ≤ 3 seconds.

## TC-008 — Contributor cannot submit final assessment (role/security)
- Linked REQ/US: REQ-008, REQ-005 / US-003a
- Type: System (security)
- Priority: High
- Preconditions: A complete, valid draft assessment; user role = Contributor.
- Test data: complete assessment; Contributor user.
- Steps:
  1. Log in as Contributor.
  2. Open the complete draft assessment.
  3. Attempt submission.
- Expected result: Submission is denied; the attempt is recorded; the assessment stays `draft`.

## TC-009 — Transition Lead raises an RFC and a Contributor responds (happy path) *(CR-01)*
- Linked REQ/US: REQ-011, REQ-012 / US-006
- Type: Integration
- Priority: High
- Preconditions: An intake/assessment exists; a Transition Lead and a Contributor exist.
- Test data: RFC title="Clarify integration dependencies", content="List external integrations of OrderCare".
- Steps:
  1. Log in as Transition Lead and raise an RFC on the intake.
  2. Log in as Contributor and add a response, marked as reusable knowledge.
  3. Log in as Transition Lead and move the RFC to `answered`.
- Expected result: The RFC is persisted with status `open` then `answered`; the response is linked to the RFC and flagged as reusable knowledge.

## TC-010 — Contributor cannot raise an RFC (role/security) *(CR-01)*
- Linked REQ/US: REQ-011, REQ-008 / US-006
- Type: System (security)
- Priority: High
- Preconditions: An intake/assessment exists; user role = Contributor.
- Test data: Contributor user; RFC title="Unauthorized RFC".
- Steps:
  1. Log in as Contributor.
  2. Attempt to raise an RFC.
- Expected result: The request is denied; no RFC is created.

---

## BDD / Gherkin

The feature is defined in `bdd/features/readiness.feature` with three baseline scenarios:
happy path (Transition Lead submits complete assessment), missing evidence (submission blocked),
and unauthorized user (Contributor cannot submit). A fourth scenario was added by the change
request (CR-01): only the Transition Lead can raise an RFC. See that file for the Gherkin source.

---

## Definition of Done

### DoD — Requirement
A requirement is done when:
1. It has a unique ID, a type (FR/NFR/constraint), a stakeholder and a priority.
2. It is clear, atomic, feasible and **testable** (measurable acceptance criteria, not implementation-specific).
3. It is linked to an objective and a CSF, and appears in the traceability matrix.
4. It has at least one acceptance criterion covered by a test case or BDD scenario.

### DoD — User Story
A user story is done when:
1. It follows the "As a … I want … so that …" format and is linked to at least one requirement.
2. It has acceptance criteria that are verifiable.
3. Each acceptance criterion maps to at least one test case or BDD scenario.
4. It is small enough to be delivered and tested independently (split if not).

### DoD — Final Delivery (AMS Readiness Intake increment)
The delivery of the AMS Readiness Intake increment is done when:
1. All in-scope requirements (REQ-001…REQ-010, plus any change-request requirements) are implemented or specified and appear in the traceability matrix.
2. Every requirement's acceptance criteria are covered by at least one test case or BDD scenario.
3. The data architecture (`Assessment`, `Evidence`, `UserRole`) is implemented in SQLite and matches the application behaviour.
4. The evidence-validation slice runs and demonstrates the mandatory business rules: mandatory evidence fields, the 90-day freshness rule, and role-based submission.
5. For the demonstration data, the missing critical information and the readiness status/score are shown correctly.
6. The automated database-backed tests are reproducible and pass, with execution evidence recorded in `evidence/test_results.md`.
7. Documentation (README, data architecture, tests) is consistent with the delivered behaviour, and there are no known critical defects.
8. The change request has been assessed and its impact incorporated (requirements, tests, data and traceability updated).

> Note: the *academic submission gate* — the 14 deliverables, each with a dedicated commit,
> distributed across at least 4 days, in the required repository structure — is a **process**
> requirement governed by the commit rules and the README, and is deliberately kept **separate**
> from this product-level Definition of Done to avoid mixing levels.
