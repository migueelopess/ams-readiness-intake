# Test Results Evidence

## Date/time
- 2026-07-14 (run during development on Python 3.10).

## Command executed
```bash
python -m pytest -v
```

## Database/test data used
- Persistence option: SQLite (in-memory, rebuilt per test).
- Seed file: `app/seed_data.sql` (applied over `app/schema.sql`).
- Number of records: 23 across 5 tables (user_role, assessment, evidence, rfc, rfc_response).
- Reset strategy before tests: each test gets a fresh in-memory database via the `conn` fixture
  in `tests/conftest.py`.

## Result summary
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

## Notes
- Tests passed: 5 / 5.
- Tests failed: 0.
- Known limitations: tests exercise the business-rules layer against the seeded database; the
  Streamlit UI is not automated. Freshness uses a fixed reference date (2026-07-01) for determinism.
