# Requirements Quality Review

A self-review of the project's own requirements against standard quality dimensions:
**clear, testable, atomic, feasible, traceable, not implementation-specific, aligned with scope.**
All requirements were reviewed; real issues were identified and three requirements were corrected
(the corrections are already applied in `docs/02_objectives_csfs_requirements.md`).

## Review of all requirements

| Requirement | clear | testable | atomic | feasible | traceable | not impl-specific | in scope | Verdict |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| REQ-001 Create assessment | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OK |
| REQ-002 Add evidence | ✅ | ✅ | ⚠ | ✅ | ✅ | ✅ | ✅ | Overlaps REQ-010 (QI-4) |
| REQ-003 Missing critical info | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OK |
| REQ-004 Stale evidence | ✅ | ✅ | ⚠→✅ | ✅ | ✅ | ✅ | ✅ | **Corrected (QI-1)** |
| REQ-005 Submit | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OK |
| REQ-006 Readiness result/score | ⚠→✅ | ✅ | ⚠→✅ | ✅ | ✅ | ⚠→✅ | ✅ | **Corrected (QI-2)** |
| REQ-007 Performance | ✅ | ⚠ | ✅ | ✅ | ✅ | ✅ | ✅ | Minor (QI-5) |
| REQ-008 Role authorization | ✅ | ✅ | ⚠ | ✅ | ✅ | ✅ | ✅ | Not atomic after CR (QI-3) |
| REQ-009 Guided entry | ✅ | ⚠→✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **Corrected (QI-2)** |
| REQ-010 Mandatory fields | ✅ | ✅ | ⚠ | ✅ | ✅ | ✅ | ✅ | Overlaps REQ-002 (QI-4) |
| REQ-011 Raise RFC (CR-01) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OK |
| REQ-012 Respond RFC (CR-01) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | OK |

## Quality issues identified (real)

- **QI-1 — REQ-004 was not atomic.** The original "Detect stale evidence **and block submission**"
  bundled two behaviours: flagging staleness and blocking submission. Blocking also overlapped
  REQ-005. Two behaviours in one requirement make it harder to test and to change independently.
- **QI-2 — REQ-006 was implementation-specific and not atomic.** It said the system "**Display**s"
  a result (prescribes a UI presentation) and mixed *status*, *missing information* and *score*; it
  also used "risk/readiness score" inconsistently (two terms for one concept).
- **QI-3 — REQ-008 became non-atomic after the change request.** It now covers both "submit a final
  assessment" and "raise/close an RFC" in a single requirement.
- **QI-4 — REQ-002 and REQ-010 overlap.** Both state that evidence must have source, owner and
  freshness date. Two requirements expressing the same rule reduce independence and can drift apart.
- **QI-5 — REQ-007 is weakly testable.** "On a standard laptop" is not a defined reference
  environment, so the ≤3 s target is not fully reproducible.

## Corrections applied (3)

### 1. REQ-004 — atomicity (QI-1)
- Before: "Detect stale evidence **and block submission**" (detection + blocking + AC-3 about submission).
- After: "**Detect and flag stale evidence**" — detection/flagging only; the submission block is
  specified once, in REQ-005 (which already validates completeness and staleness on submit).
- Why better: each requirement now expresses **one** behaviour, so it is independently testable
  (AT-003 tests only flagging) and can change without touching submission logic. Removes the
  duplicated blocking rule.

### 2. REQ-006 — remove implementation wording, fix terminology (QI-2)
- Before: "**Display** readiness result and **risk/readiness** score."
- After: "**Provide** readiness status and **readiness** score" — presentation-neutral wording and a
  single, consistent term.
- Why better: it no longer prescribes *how* the result is shown (a requirement should state the
  need, not the UI), and it removes the risk/readiness ambiguity, so it is clearer and truly testable.

### 3. REQ-009 — make the acceptance criteria testable (QI-2)
- Before: "…without external documentation" and "requires **exactly three** mandatory fields".
- After: objective criteria — an inline message identifies the missing field, and a valid item is
  added in a single submission.
- Why better: "without external documentation" is subjective and not verifiable; the corrected
  criteria are observable and demonstrable, and they no longer over-constrain the number of fields.

## Issues acknowledged but not corrected (with reasoning)
- **QI-3 (REQ-008 not atomic):** kept as one requirement because both actions are the *same*
  authorization rule (only the Transition Lead), and splitting it now would fragment a coherent
  security control; recorded as a known trade-off (DEC-007).
- **QI-4 (REQ-002 / REQ-010 overlap):** kept intentionally — REQ-002 is the functional "add
  evidence" behaviour and REQ-010 is the standalone data constraint used by the data architecture
  and persistence checks. The overlap is documented so it does not drift.
- **QI-5 (REQ-007 environment):** low priority NFR; the reference environment can be pinned before a
  real performance test. Noted for future work.
