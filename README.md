# AMS Readiness Intake — Requirements Rescue Challenge

## Student
- Name: Miguel Lopes
- Number: a22404033

## Repository purpose
This repository contains the work developed for the resit exam of Requirements Engineering and Testing.
Theme: **AMS Transition Intake & Readiness Assessment** — a small module to collect transition
information, link evidence, identify missing critical information and produce an initial
readiness/risk view for the AMS takeover of the *OrderCare* application (Northwind Retail Services).

## Work plan
- Day 1: Create repo and structure. README. Diagnosis and elicitation (problems, questions, assumptions). Share repo link.
- Day 2: Objectives, CSFs and 10 structured requirements. Rewrite of poor requirements. Macro/Mezzo/Micro model.
- Day 3: Use cases (diagram + 2 detailed). User stories (4 + 1 split). Start requirements quality review.
- Day 4: Test cases (8) + BDD scenarios + Definition of Done. Traceability matrix baseline commit (before change request).
- Day 5: Receive and process change request. Update impacted artefacts. Decision log.
- Day 6: Data architecture (SQLite). Simple app via Vibe Coding. Prompt log and evidence.
- Day 7: Automated database-backed tests. Test results evidence. AI usage review. Final traceability and README update.

## Use of AI tools
- AI tool(s) used: LLM assistant (Claude) for drafting/structuring; Git, PyTest, Streamlit, SQLite as tooling.
- What AI was used for: drafting and structuring documentation, generating the app and tests, reviewing requirement wording. Full detail in `docs/14_ai_usage_review.md`.
- What was manually reviewed/changed: all requirements, traceability links, validation rules and test logic were reviewed and adjusted; made the freshness rule deterministic, separated logic from UI, corrected REQ-004/006/009.
- Main assumptions introduced: see `docs/01_diagnosis_elicitation.md` (Assumptions) and `docs/08_decision_log.md`.
- Main limitations observed: AI produced artefacts that looked complete but could be internally inconsistent (e.g. matrix rows referencing not-yet-existing tests), and reintroduced terminology it had been asked to fix — so traceability and links were verified by hand.

## Data architecture
- Persistence option used: **SQLite**
- Main entities/models: `Assessment`, `Evidence`, `UserRole` (see `docs/10_data_architecture.md`)
- Where the schema/model is defined: `app/schema.sql` (+ `app/database.py`)
- How test data is created: `app/seed_data.sql` (seed with valid and invalid cases)

## Application
- Technology used: Python (business logic) + SQLite persistence; simple UI (Streamlit) / CLI flow
- How to run the app: see "How to run the app" section below
- Main implemented feature(s): Evidence validation slice — capture evidence metadata (source, owner, freshness date) and flag missing or stale (>90 days) evidence

## Automated tests
- Test framework used: PyTest (database-backed). BDD scenarios in `bdd/features/readiness.feature`.
- How to run the tests: `python -m pytest -v`
- Number of tests: 5 automated (AT-001…AT-005) + 4 BDD scenarios
- Current result: **5 passed**

## Test database / test data
- Database or persistence type used: SQLite
- How the database/test data is created: `app/schema.sql` + `app/seed_data.sql`, applied by a fixture/setup helper
- How to reset the test database: the test fixture rebuilds a fresh SQLite database (in-memory or temp file) before each test run
- Seed/test data file(s): `app/seed_data.sql`

## How to run the app
```bash
# from repo root
python -m venv .venv
# Windows:  .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# Streamlit UI (evidence validation + RFC tabs)
streamlit run app/app.py

# or the dependency-free CLI flow
python app/main.py
```

## Final deliverables
- [x] Diagnosis and elicitation — `docs/01_diagnosis_elicitation.md`
- [x] Objectives, CSFs and requirements — `docs/02_objectives_csfs_requirements.md`
- [x] Macro/Mezzo/Micro model — `docs/03_macro_mezzo_micro.md`
- [x] Use cases — `docs/04_use_cases.md`
- [x] User stories — `docs/05_user_stories.md`
- [x] Test cases and BDD scenarios — `docs/06_tests_validation.md`, `bdd/features/readiness.feature`
- [x] Traceability matrix — `docs/07_traceability_matrix.md`
- [x] Decision log — `docs/08_decision_log.md`
- [x] Change request impact — `docs/09_change_request.md`
- [x] Data architecture — `docs/10_data_architecture.md`
- [x] Simple app generated with Vibe Coding — `docs/11_vibe_coding_app.md`, `app/`
- [x] Automated database-backed tests — `docs/12_automated_tests.md`, `tests/`
- [x] Requirements quality review — `docs/13_requirements_quality_review.md`
- [x] AI usage review — `docs/14_ai_usage_review.md`
