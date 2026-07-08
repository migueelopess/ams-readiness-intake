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
- AI tool(s) used: <PREENCHER — ex.: ChatGPT / Claude / GitHub Copilot / Cursor>
- What AI was used for: drafting and structuring documentation, generating an initial version of the app and tests, reviewing requirement wording.
- What was manually reviewed/changed: all requirements, traceability links, validation rules and test logic were reviewed and adjusted by the student.
- Main assumptions introduced: see `docs/01_diagnosis_elicitation.md` (Assumptions) and `docs/08_decision_log.md`.
- Main limitations observed: <PREENCHER após o trabalho — ex.: AI proposed vague acceptance criteria that had to be made measurable>

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
- Test framework used: PyTest (database-backed) + Behave (BDD)
- How to run the tests: `python -m pytest` and `python -m behave bdd`
- Number of tests: 4+ automated (PyTest) + 3 BDD scenarios
- Current result: <PREENCHER após correr — ex.: 4 passed>

## Test database / test data
- Database or persistence type used: SQLite
- How the database/test data is created: `app/schema.sql` + `app/seed_data.sql`, applied by a fixture/setup helper
- How to reset the test database: the test fixture rebuilds a fresh SQLite database (in-memory or temp file) before each test run
- Seed/test data file(s): `app/seed_data.sql`

## How to run the app
> A ser completado no Dia 6.
```bash
# from repo root
python -m venv .venv
# Windows:  .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
# run app (example)
streamlit run app/app.py
```

## Final deliverables
- [ ] Diagnosis and elicitation — `docs/01_diagnosis_elicitation.md`
- [ ] Objectives, CSFs and requirements — `docs/02_objectives_csfs_requirements.md`
- [ ] Macro/Mezzo/Micro model — `docs/03_macro_mezzo_micro.md`
- [ ] Use cases — `docs/04_use_cases.md`
- [ ] User stories — `docs/05_user_stories.md`
- [ ] Test cases and BDD scenarios — `docs/06_tests_validation.md`, `bdd/features/readiness.feature`
- [ ] Traceability matrix — `docs/07_traceability_matrix.md`
- [ ] Decision log — `docs/08_decision_log.md`
- [ ] Change request impact — `docs/09_change_request.md`
- [ ] Data architecture — `docs/10_data_architecture.md`
- [ ] Simple app generated with Vibe Coding — `docs/11_vibe_coding_app.md`, `app/`
- [ ] Automated database-backed tests — `docs/12_automated_tests.md`, `tests/`
- [ ] Requirements quality review — `docs/13_requirements_quality_review.md`
- [ ] AI usage review — `docs/14_ai_usage_review.md`
