# Macro / Mezzo / Micro

This deliverable represents the domain of the **AMS Transition Intake & Readiness Assessment**
module at three levels: Macro (high-level capabilities), Mezzo (functional areas) and Micro
(specific rules/validations). Each Micro rule is linked to a Mezzo area and to a requirement
from `docs/02_objectives_csfs_requirements.md`.

## Macro

| ID | Capability | Description |
|---|---|---|
| MAC-001 | AMS Readiness Assessment | Capture intake information and evaluate whether the application is ready to be supported by AMS. |
| MAC-002 | Evidence-based Transition Governance | Manage evidence (source, owner, freshness) and control who can change or submit assessments, keeping everything traceable. |
| MAC-003 | Readiness Reporting & Prioritization | Surface missing critical information and produce a readiness/risk view to prioritize the first 90 days. |

## Mezzo

| ID | Functional area | Related Macro |
|---|---|---|
| MEZ-001 | Create assessment / capture intake answers | MAC-001 |
| MEZ-002 | Manage evidence metadata | MAC-002 |
| MEZ-003 | Identify missing critical information | MAC-001, MAC-003 |
| MEZ-004 | Evaluate evidence freshness | MAC-002 |
| MEZ-005 | Role-based submission control | MAC-002 |
| MEZ-006 | Review readiness status / result | MAC-003 |

## Micro

| ID | Rule / Validation | Related Mezzo | Related REQ |
|---|---|---|---|
| MIC-001 | Every evidence item must have `source`, `owner` and `freshness_date`; otherwise it is rejected. | MEZ-002 | REQ-002, REQ-010 |
| MIC-002 | Evidence with `freshness_date` more than 90 days before the assessment date is marked `stale`. | MEZ-004 | REQ-004 |
| MIC-003 | Boundary: evidence exactly 90 days old is **not** stale; 91 days old **is** stale. | MEZ-004 | REQ-004 |
| MIC-004 | An assessment cannot be submitted while any mandatory readiness area lacks complete evidence. | MEZ-003, MEZ-005 | REQ-003, REQ-005 |
| MIC-005 | Only the `Transition Lead` role can submit the final assessment. | MEZ-005 | REQ-005, REQ-008 |
| MIC-006 | A submission attempt by a non-authorized role is denied and leaves the assessment in `draft`. | MEZ-005 | REQ-008 |
| MIC-007 | The readiness result shows status, the missing-critical-information list and a deterministic readiness/risk score. | MEZ-006 | REQ-006 |
| MIC-008 | Readiness validation for a typical assessment (≤50 evidence items) completes in ≤ 3 seconds. | MEZ-006 | REQ-007 |

> Note: MIC-002/MIC-003 (freshness → stale) and MIC-005 (only Transition Lead submits) are the
> rules most likely to be affected by the change request. In the baseline, stale critical
> evidence **blocks** submission (via MIC-004); the change request may relax this to "flag, not
> block" and may add that Contributors can edit drafts.
