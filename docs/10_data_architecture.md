# Data Architecture

The data architecture is defined **before** the application so that the AI tool does not invent a
data model. It is aligned with the requirements, use cases, user stories, test cases and the
automated database-backed tests. It includes the `RFC` / `RFCResponse` entities added by the
change request (CR-01).

## Persistence option
- **SQLite / JSON:** **SQLite**
- Justification: the exam emphasises *database-backed* tests; SQLite gives real tables and
  relationships, a reproducible seed/reset, and standard SQL — while staying a single local file
  with zero server setup. See decision **DEC-005** in `docs/08_decision_log.md`.
- Where it lives: schema in `app/schema.sql`, seed data in `app/seed_data.sql`, access/reset helper
  in `app/database.py`.

## Data model overview

| Entity / Model | Purpose | Related requirements |
|---|---|---|
| UserRole | The user and their role; drives authorization. | REQ-005, REQ-008, REQ-011 |
| Assessment | A readiness assessment for an application (status draft/submitted). | REQ-001, REQ-003, REQ-005, REQ-006 |
| Evidence | Evidence items attached to an assessment (source/owner/freshness). | REQ-002, REQ-004, REQ-010 |
| RFC | A Request for Comment raised on an intake *(CR-01)*. | REQ-011, REQ-008 |
| RFCResponse | A response to an RFC, optionally reusable knowledge *(CR-01)*. | REQ-012 |

## Entity details

### UserRole
| Field | Type | Required? | Notes |
|---|---|---:|---|
| id | INTEGER | Yes | Primary key |
| username | TEXT | Yes | Unique |
| role | TEXT | Yes | One of: `Transition Lead`, `AMS Manager`, `Contributor`, `Security Officer` |

### Assessment
| Field | Type | Required? | Notes |
|---|---|---:|---|
| id | INTEGER | Yes | Primary key |
| name | TEXT | Yes | Assessment name |
| status | TEXT | Yes | `draft` or `submitted` (default `draft`) |
| created_date | TEXT (ISO date) | Yes | Creation date |

### Evidence
| Field | Type | Required? | Notes |
|---|---|---:|---|
| id | INTEGER | Yes | Primary key |
| assessment_id | INTEGER | Yes | FK → Assessment.id |
| area | TEXT | Yes | Readiness area: `monitoring`, `DR`, `access`, `integrations`, `SLA` |
| source | TEXT | Yes | Evidence source (mandatory — REQ-010) |
| owner | TEXT | Yes | Evidence owner (mandatory — REQ-010) |
| freshness_date | TEXT (ISO date) | Yes | Used for the 90-day stale rule (REQ-004) |
| category | TEXT | No | Optional |
| criticality | TEXT | No | `high` / `medium` / `low` (optional) |

### RFC *(CR-01)*
| Field | Type | Required? | Notes |
|---|---|---:|---|
| id | INTEGER | Yes | Primary key (acts as the RFC number) |
| assessment_id | INTEGER | Yes | FK → Assessment.id |
| title | TEXT | Yes | RFC title |
| content | TEXT | Yes | The request / question |
| raised_by | INTEGER | Yes | FK → UserRole.id (must be a Transition Lead — REQ-008) |
| status | TEXT | Yes | `open` / `answered` |
| created_date | TEXT (ISO date) | Yes | Creation date |

### RFCResponse *(CR-01)*
| Field | Type | Required? | Notes |
|---|---|---:|---|
| id | INTEGER | Yes | Primary key |
| rfc_id | INTEGER | Yes | FK → RFC.id |
| author | INTEGER | Yes | FK → UserRole.id (typically a Contributor) |
| comment | TEXT | Yes | The response |
| is_knowledge | INTEGER | No | 1 if reusable knowledge (feeds FAQ), else 0 |
| created_date | TEXT (ISO date) | Yes | Creation date |

## Relationships

| Source entity | Relationship | Target entity |
|---|---|---|
| Assessment | has many | Evidence |
| Assessment | has many | RFC |
| RFC | has many | RFCResponse |
| UserRole | raises | RFC |
| UserRole | authors | RFCResponse |

## Validation rules supported

| Rule | Related REQ | Implemented in app? | Tested by |
|---|---|---|---|
| Evidence must have source, owner and freshness_date | REQ-002, REQ-010 | Yes | AT-002 / TC-003 |
| Evidence older than 90 days is flagged stale | REQ-004 | Yes | AT-003 / TC-005, TC-006 |
| Assessment cannot be submitted with missing critical evidence | REQ-003 | Yes | AT-002 / TC-004 |
| Only a Transition Lead can submit a final assessment | REQ-005, REQ-008 | Yes | AT-004 / TC-008 |
| Only a Transition Lead can raise an RFC | REQ-008, REQ-011 | Yes | AT-005 / TC-010 |
| An RFC and its response persist and link correctly | REQ-011, REQ-012 | Yes | AT-005 / TC-009 |

## Notes on reproducibility
The database is rebuilt from `app/schema.sql` + `app/seed_data.sql` by `app/database.py`
(`build_database()` / in-memory option for tests). Freshness rules receive an explicit
`reference_date` so the stale checks are deterministic and reproducible regardless of the run date;
the seed uses `2026-07-01` as the reference for the boundary examples (90 vs 91 days).
