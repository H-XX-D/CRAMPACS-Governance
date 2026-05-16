# CRAMPS Assurance Case Framework

**Document ID:** CRAMPS-ACF-001

## 1. Purpose

A CRAMPS result should be defended as an assurance case, not as a loose report.

An assurance case links:

- claim
- argument
- evidence
- assumptions
- rebuttals
- residual risk
- signoff

This structure makes the package inspectable by safety supervisors, auditors, and domain reviewers.

## 2. Top Claim

For a full `CRAMPS-*` study, the top claim is:

> The study provides a reproducible, pre-specified, dependence-aware, bias-reviewed test of recurrence at registered coordinates under a documented null model.

It is not:

> The study proves the domain phenomenon is real.

## 3. Assurance Claims

| Claim ID | Claim | Required evidence | Common rebuttal |
|---|---|---|---|
| AC-01 | The coordinate was pre-specified | protocol hash, candidate registry, lock timestamp | coordinate moved after rows were known |
| AC-02 | The source universe was not cherry-picked | search log, source flow, exclusion reasons | negative/null sources omitted |
| AC-03 | Rows are traceable and correctly extracted | row table, source references, review status | AI or analyst inferred values incorrectly |
| AC-04 | Units and transforms are controlled | raw/normalized split, transform registry | hidden conversion created apparent recurrence |
| AC-05 | Dependence is modeled or controlled | evidence-family map, independence grades, weights | duplicate evidence counted as independent |
| AC-06 | Missing evidence and bias are assessed | bias assessment, missing-evidence memo | publication/reporting bias explains recurrence |
| AC-07 | Null model is fit for purpose | null model spec, validation checks, negative controls | null is too weak or unrealistic |
| AC-08 | Multiple testing is addressed | global correction, multiplicity groups | local result is a look-elsewhere artifact |
| AC-09 | Result is robust enough for assigned tier | sensitivity tests, leave-family-out checks | one source or era drives result |
| AC-10 | Package is reproducible | checksums, run log, environment, clean reproduction | output cannot be recreated |
| AC-11 | Claim language matches evidence | evidence tier, approved report language | report overstates causality or certainty |

## 4. Assurance Case Template

For each claim:

```text
claim_id:
claim:
argument:
evidence_files:
assumptions:
rebuttals_considered:
residual_risk:
reviewer:
status: open / accepted / accepted_with_residual_risk / rejected
```

## 5. Release Rule

A full `CRAMPS-*` package may not be released externally with any open Critical assurance claim.

Major unresolved claims require either:

- remediation, or
- demotion of the evidence tier, or
- explicit signed acceptance by the authorized domain supervisor.
