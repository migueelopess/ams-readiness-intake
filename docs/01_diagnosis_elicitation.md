# Diagnosis and Elicitation

This deliverable analyses the raw interview notes, the poorly written initial requirements
(R1–R10) and the case constraints for the **AMS Transition Intake & Readiness Assessment**
module. It identifies problems in the provided material, defines elicitation questions to
resolve those problems, and records the assumptions made (with their risk and how to validate
them).

## A) Problems identified

| ID | Source | Problem | Why it is a problem |
|---|---|---|---|
| P-001 | R1 — "The system must be fast" | Non-functional requirement not measurable | No threshold, metric or context is given (fast for what operation, under what load). Cannot be tested or accepted objectively. |
| P-002 | R2 — "Users need to add project data" | Ambiguous and out of scope | "Users" (which role?) and "project data" (which data?) are undefined. Scope is *Intake & Readiness Assessment*, not generic "project data". |
| P-003 | R3 — "The system should be secure" | Vague NFR, not measurable | "Secure" has no definition, no criteria (authentication, authorization, auditability). Not testable. |
| P-004 | R4 — "Create a dashboard" | Solution stated as a requirement + missing owner | Prescribes an implementation ("a dashboard") instead of the underlying need. Interview also shows nobody owns existing dashboards (unresolved gap). |
| P-005 | R5 — "Use AI to generate recommendations" | Implementation imposed, not a need | Fixes a technology (AI) rather than the goal ("recommendations for the first 90 days"). Also a scope/feasibility risk for a one-week slice. |
| P-006 | R6 — "The app must allow evidence" | Incomplete / missing acceptance criteria | "Allow evidence" does not say what an evidence record contains. Constraints require source, owner and freshness date — these are missing from the requirement. |
| P-007 | R7 — "Managers need to know what is missing" | Missing stakeholder precision + no acceptance criteria | Which manager (AMS Manager? Transition Lead?)? What counts as "missing critical information"? Not measurable. |
| P-008 | R8 — "Use Microsoft authentication" | Solution/constraint imposed without justified need | Prescribes a specific technology. Unclear whether it is a hard constraint or a preference; potential conflict with the vague R3 "secure". |
| P-009 | R9 — "The system should support risk scoring" | Underspecified requirement | No definition of inputs, formula, weights or thresholds for the risk/readiness score. Cannot be implemented or tested as written. |
| P-010 | R10 — "It should be user-friendly" | Non-functional requirement not measurable | Subjective and untestable; no usability criteria or target. |
| P-011 | Interview — Ops Engineer / Service Owner (dashboards old, alerts maybe invalid; ownership unknown) | Missing owner + unresolved dependency | Dashboard ownership and alert validity are undefined, yet readiness depends on them. Ownership/traceability gap. |
| P-012 | Interview — Client Manager ("easy and fast... need it next week") | Conflict between scope, quality and time | Simultaneous demands for fast, easy, secure and delivered "next week" conflict; priorities are not ranked, timeline is unrealistic for full scope. |
| P-013 | Interview — Security Officer ("only approved AMS leads should change assessments") vs Users list including Contributor | Role/authorization ambiguity (conflict) | It is not defined who may *edit draft* vs who may *submit final* assessment. Direct conflict to resolve (later clarified by the change request). |
| P-014 | Interview — Developer ("integrations and dependencies not fully documented") | Incomplete input / information gap | Missing dependency and integration information weakens the completeness of any readiness assessment; a critical-information gap. |

> At least 8 problems are required; 14 are documented to cover ambiguity, non-measurable NFRs,
> requirement-vs-solution confusion, missing stakeholders, missing acceptance criteria, scope
> issues, conflicts and unresolved dependencies.

## B) Elicitation questions

| ID | Topic | Question | Target stakeholder |
|---|---|---|---|
| Q-001 | Business | What does "ready to be supported by AMS" concretely mean, and who formally signs off the readiness decision? | Client Manager / Transition Lead |
| Q-002 | Business | Is the "next week" expectation for a working prototype/slice or for the full module, and what is the minimum acceptable scope? | Client Manager |
| Q-003 | AMS operation | Which operational areas are mandatory for readiness (monitoring, DR, access procedures, integrations, SLAs)? | Service Owner |
| Q-004 | AMS operation | Who owns each monitoring dashboard and are the current alerts still validated? | Ops Engineer / Service Owner |
| Q-005 | Evidence | What metadata is mandatory for each evidence item — is it source, owner and freshness date only, or also category and criticality? | Transition Lead |
| Q-006 | Evidence | What is the freshness threshold beyond which evidence is considered stale (e.g. 90 days)? | Security Officer / Service Owner |
| Q-007 | Evidence | Should stale or missing evidence *block* submission or only be *flagged*? | Security Officer |
| Q-008 | Security | Which roles can create, edit draft and submit a final readiness assessment (Transition Lead, AMS Manager, Contributor, Security Officer)? | Security Officer |
| Q-009 | Security | Is Microsoft authentication (SSO) a hard constraint or a preference for this module? | Security Officer / IT |
| Q-010 | Risk / continuity | How should the readiness/risk score be calculated, and which inputs and weights feed it? | Transition Lead / Service Owner |
| Q-011 | Risk / continuity | When was the last Disaster Recovery test and what counts as acceptable evidence of it? | Service Owner / Ops Engineer |
| Q-012 | Reporting | What must the "missing critical information" summary contain, and who consumes it? | Transition Lead / AMS Manager |
| Q-013 | Reporting | What recommendations are expected for the first 90 days, and in what format? | Transition Lead |
| Q-014 | Testing / validation | What acceptance criteria define an assessment as "complete" and as "submitted"? | Transition Lead |
| Q-015 | Testing / validation | Which data and scenarios should validate the readiness rules (valid vs stale evidence, authorized vs unauthorized submission)? | Service Owner / Security Officer |

> At least 12 questions are required; 15 are documented, covering all seven topics: business,
> AMS operation, evidence, security, risk/continuity, reporting and testing/validation.

## C) Assumptions

| ID | Assumption | Risk if wrong | How to validate |
|---|---|---|---|
| A-001 | The freshness threshold for evidence is **90 days** (aligned with the "first 90 days" focus and DR-test recency). | Evidence is wrongly flagged as stale or wrongly accepted as current, distorting readiness. | Confirm the threshold with the Security Officer / Service Owner (Q-006). |
| A-002 | Only the **Transition Lead** role may submit the final readiness assessment; **Contributors** may only edit draft answers. | Incorrect authorization model; unauthorized submissions or blocked legitimate ones. | Confirm the role matrix with the Security Officer (Q-008). Aligned with the Security Officer's note. |
| A-003 | "Fast" means the readiness validation/result is computed in **≤ 3 seconds** for a typical assessment. | Over- or under-engineering performance; unclear acceptance. | Measure response time and confirm the target with the Client Manager (Q-001). |
| A-004 | Scope is limited to **Intake & Readiness Assessment only**, not full AMS management. | Scope creep; effort spent on out-of-scope features. | Confirm scope boundary with the Client Manager / Transition Lead (Q-002). |
| A-005 | Mandatory evidence metadata is **source, owner and freshness date**; category and criticality are optional. | Required fields missing or unnecessary fields enforced. | Confirm required fields with the Transition Lead (Q-005). |
| A-006 | **Microsoft authentication (R8) is a preference, not a hard constraint** for this exam slice; a simple local role check is acceptable. | Rework if SSO is mandatory for production. | Confirm with the Security Officer / IT whether SSO is mandatory (Q-009). |
| A-007 | "Missing critical information" = any mandatory readiness area (monitoring, DR, access, integrations, SLA) without complete, non-stale evidence. | Wrong completeness logic; false readiness status. | Confirm the definition of "critical/complete" with the Service Owner (Q-003, Q-012). |
| A-008 | Risk/readiness scoring is a **simple weighted count** of complete vs missing/stale critical items, not a complex model. | Score does not match stakeholder expectations. | Confirm the scoring approach with the Transition Lead (Q-010). |

> At least 6 assumptions are required; 8 are documented, each with its risk and a validation
> method. Assumptions A-001, A-002 and A-007 are the highest-risk and are revisited in the
> decision log (`docs/08_decision_log.md`) and, where relevant, by the change request
> (`docs/09_change_request.md`).
