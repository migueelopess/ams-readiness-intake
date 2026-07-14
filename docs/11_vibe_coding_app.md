# Vibe Coding App

## Tool used
- Tool: AI-assisted coding (LLM: Claude) used as a Vibe Coding assistant.
- Environment: Python 3.10+, SQLite (standard library), Streamlit for the UI.

## Selected slice
- **Option A — Evidence validation slice.**
- Why this slice was selected: it is the smallest self-contained flow that exercises the core
  business rules (mandatory evidence fields and the 90-day freshness rule) and maps directly to
  requirements REQ-002, REQ-004, REQ-010, plus the readiness output REQ-003/REQ-006.
- The app has **two tabs**: *Evidence validation* (the main slice) and *RFC* (the change request
  CR-01). The RFC tab lets a Transition Lead raise an RFC and a Contributor respond, showing the
  role rule live (decision **DEC-009**, which extended the earlier data/logic-only scope of DEC-006).

## Data architecture used
- Persistence option: **SQLite**.
- Main entities/models used: `Assessment`, `Evidence`, `UserRole`, `RFC`, `RFCResponse`.
- Link to the model: `docs/10_data_architecture.md`. The schema is `app/schema.sql`; the app does
  not invent a different model.

## Requirements implemented
| Requirement | App behaviour |
|---|---|
| REQ-002 / REQ-010 | Evidence form requires source, owner and freshness date; missing fields are rejected. |
| REQ-004 | Evidence older than 90 days (vs the reference date) is flagged as stale. |
| REQ-003 | The app lists mandatory areas without complete, current evidence as missing critical information. |
| REQ-006 | The app shows a readiness status and a readiness score. |
| REQ-005 / REQ-008 | Submission is restricted to the Transition Lead (logic layer / `main.py`, tests). |
| REQ-011 / REQ-012 | RFC tab: a Transition Lead raises an RFC; a Contributor responds and can mark it as reusable knowledge; only a Transition Lead can raise/close it. |

## App flow
**Evidence validation tab**
1. Select an assessment (seeded: complete / missing DR / stale evidence).
2. Add an evidence item (area, source, owner, freshness date, criticality).
3. The app validates the mandatory fields and flags the item as current or stale.
4. The app shows the evidence list and the readiness result: status, missing critical information,
   stale critical evidence and readiness score.

**RFC tab (CR-01)**
5. Choose the acting user (to demonstrate the role rule).
6. Raise an RFC (title + content). If the acting user is not a Transition Lead, the app denies it (REQ-008).
7. A Contributor adds a response, optionally flagged as reusable knowledge (FAQ) (REQ-012).
8. The Transition Lead marks the RFC as answered.

## Validation / business rules implemented
| Rule | Related REQ | Implemented where |
|---|---|---|
| Mandatory evidence fields (source, owner, freshness date) | REQ-010 | `readiness_rules.evidence_is_valid` / `add_evidence`; UI form |
| Evidence older than 90 days is stale | REQ-004 | `readiness_rules.is_stale` |
| Missing critical information | REQ-003 | `readiness_rules.missing_critical_areas` |
| Readiness status and score | REQ-006 | `readiness_rules.readiness_result` / `readiness_score` |
| Only Transition Lead submits | REQ-005, REQ-008 | `readiness_rules.can_submit` / `submit_assessment` |
| Only Transition Lead raises an RFC | REQ-008, REQ-011 | `readiness_rules.raise_rfc` (shown live in the RFC tab of `app.py`) |

## Prompt log
### Prompt 1
Summary: "Given the data architecture in `docs/10_data_architecture.md` (SQLite entities Assessment,
Evidence, UserRole, RFC, RFCResponse), generate a small evidence-validation slice: a SQLite schema,
reproducible seed data with valid and invalid cases, a business-rules module and a Streamlit UI that
validates mandatory fields and flags stale evidence."
- What was generated: `schema.sql`, `seed_data.sql`, `database.py`, `readiness_rules.py`, `app.py`.
- What was kept: the entity structure, the mandatory-field and freshness rules, the readiness result.
- What was rejected: an initial version that computed staleness against the current system date
  (non-deterministic), and a version that mixed the business rules inside the Streamlit script.

### Prompt 2
Summary: "Make the freshness rule deterministic for tests, separate the rules from the UI, and add
the change-request RFC rule (only a Transition Lead can raise an RFC)."
- What was generated: an explicit `reference_date` parameter, a standalone `readiness_rules.py`, and
  the `raise_rfc` / `respond_rfc` functions.
- What was kept: all of the above.
- What was rejected: storing ages as pre-computed integers (kept ISO dates for clarity).

## Manual changes
| Change | Reason |
|---|---|
| Added an explicit `reference_date` (default 2026-07-01) to all freshness functions | Make the 90-day rule deterministic and testable (boundary 90 vs 91). |
| Separated business logic (`readiness_rules.py`) from the UI (`app.py`) | So the automated tests exercise the rules without Streamlit. |
| Added a dependency-free CLI (`main.py`) | Guarantee a runnable flow even without Streamlit installed. |
| Gitignored the generated `*.db` | The database is rebuilt from `schema.sql` + `seed_data.sql`; only the reproducible sources are committed. |

## How to run the app
```bash
# from the repository root
python -m venv .venv
# Windows:  .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# Option 1 — Streamlit UI (evidence validation slice)
streamlit run app/app.py

# Option 2 — dependency-free CLI demonstration flow
python app/main.py
```
