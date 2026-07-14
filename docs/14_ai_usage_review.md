# AI Usage Review

## Tools used
| Tool | Used for | Output accepted? | Notes |
|---|---|---|---|
| LLM assistant (Claude) | Drafting and structuring the documentation (D1–D14), generating the app and the automated tests, reviewing requirement wording | Partially | Every artefact was reviewed and adjusted; several AI proposals were rejected or changed (see below). |
| Git (CLI) | Version control and phased commits | N/A | Commits, messages and history managed manually by the student. |
| Streamlit / PyTest / SQLite | App UI, automated tests, persistence | N/A | Standard libraries/frameworks. |

## Prompts used or summarized
- Prompt 1 (requirements): "From these raw notes and 10 poor requirements, identify problems,
  write elicitation questions and assumptions, then produce structured objectives, CSFs and
  requirements with acceptance criteria."
- Prompt 2 (traceability): "Build a traceability matrix OBJ → CSF → REQ → UC → US → AC → TC/BDD →
  data entity → automated test, and explain one full chain."
- Prompt 3 (app + data): "Following the data architecture, generate a SQLite evidence-validation
  slice with mandatory-field and 90-day freshness rules, plus a role rule."
- Prompt 4 (tests): "Write PyTest database-backed tests covering happy, negative, boundary and
  role/security scenarios using the seeded SQLite data."
- Prompt 5 (change request): "Apply the RFC change request across requirements, use cases, user
  stories, tests, BDD, the matrix and the decision log."

## Human review
- **What was manually reviewed:** all requirements and their acceptance criteria; the traceability
  matrix chains; the business rules and the seed data; every commit message; the change-request
  propagation; the quality review corrections.
- **What was changed:** made the 90-day freshness rule deterministic with an explicit reference
  date; separated the business logic from the Streamlit UI; corrected REQ-004 (atomicity),
  REQ-006 (removed UI-specific wording) and REQ-009 (testable criteria); decided to surface the RFC
  in the app UI (DEC-009).
- **What was rejected:** an initial app version that computed staleness against the live system
  date (non-deterministic and untestable); a suggestion to invent extra entities not required by
  the scope; vague, non-measurable acceptance criteria proposed for the NFRs.
- **One limitation or risk observed:** the AI tends to produce artefacts that *look* complete but
  can be internally inconsistent (e.g. a matrix row pointing to a test that does not exist yet), so
  the traceability and the test/requirement links had to be verified by hand. The AI also
  occasionally reintroduced the risk/readiness terminology inconsistency that the quality review
  removed. This is exactly why the oral defense and manual review matter: the AI supports the work
  but does not replace understanding or accountability.
