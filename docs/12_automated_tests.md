# Automated Tests

## Framework used
- **PyTest** with a reproducible **SQLite** test database.

## Test scope
- validation rules (mandatory evidence fields, freshness);
- role rules (only a Transition Lead can submit / raise an RFC);
- evidence freshness boundary (90 vs 91 days);
- readiness assessment logic (missing critical information, readiness result);
- database-backed test scenarios (data is read from the seeded SQLite database);
- the RFC tool from the change request (CR-01).

## Test database / test data
### Persistence option
- **SQLite**, rebuilt from `app/schema.sql` + `app/seed_data.sql`.

### Database or test data setup
- How it is created: `tests/conftest.py` provides a `conn` fixture that calls
  `database.build_database(":memory:")`, which runs the schema and the seed script.
- How test data is inserted: from `app/seed_data.sql` (5 tables, 23 records).
- How it is reset before tests: each test gets a **fresh in-memory database** (the fixture runs
  per test), so tests are isolated and repeatable regardless of order or run date.

### Test data summary
| Data item | Purpose | Related scenario |
|---|---|---|
| Assessment 1 (complete, fresh evidence) | Happy path | AT-001 |
| Assessment 2 (missing DR evidence) | Negative | AT-002 |
| Assessment 3 (DR at 91 days, access at 90 days) | Boundary / validation | AT-003 |
| Contributor (bob) and Transition Lead (alice) | Role/security | AT-004, AT-005 |
| RFC + RFCResponse | RFC persistence (CR-01) | AT-005 |

## Automated tests implemented
| Test ID | Test name | Type | Linked REQ | Uses DB/test data? | Purpose |
|---|---|---|---|---|---|
| AT-001 | test_at001_complete_assessment_is_ready | Happy path | REQ-003, REQ-005, REQ-006 | Yes | A complete assessment is read from the DB and recognised as ready (100%). |
| AT-002 | test_at002_missing_critical_evidence_detected | Negative | REQ-003 | Yes | An assessment with missing DR evidence is detected as not ready. |
| AT-003 | test_at003_freshness_boundary_90_vs_91 | Boundary / validation | REQ-004 | Yes | 90 days is not stale; 91 days is stale; stored assessment 3 confirms it. |
| AT-004 | test_at004_only_transition_lead_can_submit | Role / security | REQ-005, REQ-008 | Yes | A Contributor cannot submit; a Transition Lead can. |
| AT-005 | test_at005_rfc_role_and_persistence | Role / security (CR-01) | REQ-011, REQ-008, REQ-012 | Yes | Only a Transition Lead can raise an RFC; RFC and response persist and link. |

## How to run tests
```bash
# from the repository root
pip install -r requirements.txt
python -m pytest -v
```

## Test result
```
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-9.1.1, pluggy-1.6.0
collected 5 items

tests/test_readiness_database.py::test_at001_complete_assessment_is_ready PASSED [ 20%]
tests/test_readiness_database.py::test_at002_missing_critical_evidence_detected PASSED [ 40%]
tests/test_readiness_database.py::test_at003_freshness_boundary_90_vs_91 PASSED [ 60%]
tests/test_readiness_database.py::test_at004_only_transition_lead_can_submit PASSED [ 80%]
tests/test_readiness_database.py::test_at005_rfc_role_and_persistence PASSED [100%]

============================== 5 passed in 0.03s ===============================
```

## Reflection
- **Easiest requirement to test:** REQ-004 (freshness), because the rule is a single deterministic
  comparison — the boundary values (90 vs 91 days) make it very clear.
- **Hardest requirement to test:** REQ-005 (submission), because it combines three conditions
  (role, missing information, stale evidence); it needed careful seed data to isolate each cause.
- **Ambiguity revealed:** testing the freshness rule forced the block-vs-flag question (Q-007) to
  be made explicit and led to the deterministic `reference_date` design.
- **How the database/test data supported the scenarios:** the seed provides valid and invalid
  cases (complete / missing / stale) so each test reads a real stored situation instead of
  hand-built objects, which is closer to how the app behaves in production.
- **What changed after the change request:** AT-005 was added to cover the RFC role rule and the
  RFC/response persistence introduced by CR-01.
- **What to improve next:** add a test that adds evidence through the app layer and re-reads it,
  and a performance check for REQ-007 with a larger dataset.
