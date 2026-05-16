# Register Data Dictionary

**Document ID:** CRAMPACS-REG-001  
**Version:** 0.1  
**Status:** Draft procedure

## 1. Purpose

This document defines required fields, allowed values, and ownership for CRAMPACS registers.

## 2. Common Rules

Every register row must have:

- stable ID
- study ID where applicable
- owner
- status
- date or timestamp
- reviewer or approver where applicable

Allowed status values:

- draft
- open
- in_review
- accepted
- accepted_with_residual_risk
- rejected
- closed
- reopened
- superseded

Severity values:

- Critical
- Major
- Minor
- Observation

Gate decisions:

- pass
- hold
- fail
- demote
- not_applicable

## 3. Retention

Default retention:

- preflight package: 3 years unless superseded by full package
- full CRAMPACS package: 7 years
- regulated package: domain retention rule, minimum 7 years
- training and approval records: duration of active role plus 7 years

## 4. Review Cadence

Registers must be reviewed:

- before each gate
- before release
- after Critical or Major deviation
- during management review

## 5. Required Registers

| Register | Purpose | Release expectation |
|---|---|---|
| `document_register.csv` | controlled-document authority, version, approval, and review due dates | all effective program documents and package templates listed |
| `control_evidence_register.csv` | control-by-control evidence map | every applicable control has evidence, reviewer, status, and residual-risk disposition |
| `gate_review_record.csv` | gate decisions, findings, holds, and output records | every required gate has pass, hold, fail, demote, or not_applicable decision |
| `assurance_case_register.csv` | claim, evidence, rebuttal, and residual-risk tracking | every release claim maps to evidence and rebuttals |
| `deviation_capa_log.csv` | deviations, containment, corrective action, preventive action, and effectiveness review | all Critical and Major items closed or formally accepted by release authority |
| `decision_log.csv` | requested decision, evidence tier, conditions, prohibited claims, and approval record | final release decision exists and references the decision memo |
| `risk_register.csv` | active and residual risks | release-impacting risks have owners and disposition |
| `training_matrix.csv` | role training and competency | required roles have current competency evidence |

## 6. Field Rules

`status` must use the allowed values in Section 2 unless a domain addendum defines a stricter controlled vocabulary.

`release_hold` is `yes` when any unresolved issue prevents release. A package cannot be released while a gate row has `release_hold=yes`.

`required_field_complete` is `yes` only when the evidence artifact contains all fields required by the relevant data contract or procedure.

`evidence_sha256` is required for static package artifacts and may be marked `not_applicable` only for live restricted systems where a pointer, access log, or snapshot hash is used instead.

`reopen_flag` is `yes` when a closed CAPA must be reopened due to recurrence, failed effectiveness check, or underestimated impact.
