# Deviation and CAPA Procedure

**Document ID:** CRAMPS-CAPA-001  
**Version:** 0.1  
**Status:** Draft procedure  

## 1. Purpose

This procedure governs deviations, corrective actions, and preventive actions.

## 2. When to Open a Deviation

Open a deviation when:

- protocol is not followed
- coordinate, transform, tolerance, source, or statistic changes after lock
- source evidence is missing or misclassified
- row extraction error is found
- dependence or bias was under-assessed
- null model fails validation
- reproduction fails
- release language exceeds evidence tier
- emergency override is used

## 3. Severity

| Severity | Definition | Required action |
|---|---|---|
| Critical | Could invalidate result or produce unsafe/misleading action | stop release, contain, CAPA required |
| Major | Could materially change interpretation | hold or demote until resolved |
| Minor | Traceability or documentation issue unlikely to change result | fix or accept with rationale |
| Observation | Improvement opportunity | track |

## 4. CAPA Lifecycle

1. Detect and log.
2. Contain affected package.
3. Assign owner and due date.
4. Assess impact.
5. Identify root cause.
6. Define corrective action.
7. Define preventive action.
8. Verify corrective action.
9. Run effectiveness check after defined interval.
10. Close or reopen.

## 5. Due Dates

Default due dates:

- Critical: containment immediately, corrective plan within 2 business days
- Major: corrective plan within 5 business days
- Minor: correction before release
- Observation: next management review

## 6. Effectiveness Review

CAPA closure requires an effectiveness check unless the issue is administrative.

Effectiveness evidence may include:

- rerun sidecar
- rerun reproduction
- retraining record
- updated template
- audit resample
- no recurrence after defined interval

## 7. Reopening

Reopen CAPA if:

- same failure recurs
- corrective action cannot be verified
- new evidence shows impact was underestimated
- reviewer rejects closure

