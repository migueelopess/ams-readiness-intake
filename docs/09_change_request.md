# Change Request Impact

## Change request received (CR-01 — official text, Moodle)

> **New requirement:**
> Transition Lead: "I need a RFC (Request For Comment) tool to request further information for any
> intake from contributors. The RFC Tool is not just a chat or a simple demand for clarification,
> it can be use as documentation for transitions or for future FAQ in the AMS. In short, It could
> act somewhat as IETF norms for technical documentation to avoid the problems that brought as to
> the situation we have now."

**Release condition respected:** this change request was processed **only after** the traceability
baseline commit `D7 Add traceability matrix baseline`.

## Interpretation
The RFC tool is a **new, additive** feature. It does not contradict the baseline (evidence
freshness and role rules are unchanged). Modelled on **IETF-style RFCs**, it must produce
*structured, traceable documentation* (title, content, author, status, responses) — not a chat —
so that transition knowledge is captured and can feed future AMS FAQs. The RFC is implemented at
the **data + logic + automated-test** level and is also **surfaced in the app UI** as a dedicated
RFC tab (decisions DEC-006 and DEC-009 in `docs/08_decision_log.md`). Role control reuses REQ-008
("only the Transition Lead can raise an RFC").

## Impact analysis

| Artefact | Impact | Updated? |
|---|---|---|
| Requirements | Added REQ-011 (raise RFC) and REQ-012 (respond/knowledge); updated REQ-003 (missing info can raise an RFC) and REQ-008 (role rule now covers raising an RFC). | Yes |
| Use Cases | Added UC-07 (Raise/answer RFC), with `extend` to UC-04; updated the diagram and the UC↔REQ table. | Yes |
| User Stories | Added US-006 (Transition Lead raises an RFC). | Yes |
| Test Cases | Added TC-009 (RFC happy path) and TC-010 (Contributor cannot raise RFC). | Yes |
| BDD Scenarios | Added scenario "RFC — only the Transition Lead can raise an RFC" to `readiness.feature`. | Yes |
| Traceability Matrix | Added REQ-011/REQ-012 chains (→ UC-07 → US-006 → TC-009/TC-010 → RFC → AT-005). | Yes |
| Decision Log | Added DEC-006 (RFC as own entity, data+logic+test scope) and DEC-007 (reuse role auth for RFC). | Yes |
| Data Architecture | Add `RFC` and `RFCResponse` entities, linked to Assessment and to the acting role. | Yes (defined in `docs/10`) |
| Test Database / Test Data | Add RFC and RFCResponse seed records (valid + invalid/role cases). | Yes (in `docs/12` / seed) |
| Automated Tests | Add AT-005 (only Transition Lead can raise an RFC; RFC + response persist and link). | Yes (implemented in `docs/12`) |
| Application (UI) | Add an RFC tab to `app/app.py` (raise / respond / mark answered), showing the role rule live. | Yes (DEC-009) |

## Summary of updates applied
- **Requirements updated:** REQ-003, REQ-008 (2 updated) + REQ-011, REQ-012 (2 added).
- **1 use case** (UC-07), **1 user story** (US-006), **2 test cases** (TC-009, TC-010), **1 BDD scenario** (RFC).
- **Traceability matrix** and **decision log** updated.
- **Data architecture, test data and automated tests** updated in the corresponding deliverables (D10, D12), because the change affects a new entity and a role rule.

## New RFC traceability chain (for the defense)
`OBJ-02 → CSF-02 → REQ-011 → UC-07 → US-006 → REQ-011 AC-1/AC-2 → TC-009 / TC-010 / BDD "RFC — only the Transition Lead can raise an RFC" → RFC (+RFCResponse) → AT-005`.
- Why it supports the objective: OBJ-02 requires information to be complete and current; the RFC
  closes documentation gaps by capturing missing transition knowledge in a structured, reusable form.
- Why the test validates the requirement: AT-005 asserts that only a Transition Lead can raise an
  RFC and that the RFC and its response persist and link correctly.
- What would be affected if the requirement changed: changing REQ-011/REQ-008 (e.g. allowing
  Contributors to raise RFCs) would propagate to UC-07, US-006, TC-010, the BDD RFC scenario, the
  `RFC` seed data and AT-005.
