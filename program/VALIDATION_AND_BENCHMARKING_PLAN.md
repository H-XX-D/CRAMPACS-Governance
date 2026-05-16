# CRAMPS Validation and Benchmarking Plan

**Document ID:** CRAMPS-VAL-001

## 1. Purpose

The CRAMPS program must be validated before strong institutional claims are made about its effectiveness.

Validation asks whether the method recovers controlled recurrence injections, rejects false recurrence, and remains stable under reviewer and source variation.

## 2. Validation Batteries

### Battery A: Known Negative

Create or select datasets where recurrence should not exist.

Pass:

- negative controls do not produce high confidence recurrence
- sidecar blocks incomplete packages
- reports remain Tier 0 or stop

### Battery B: Controlled Recurrence Injection

Inject known coordinate recurrence into a controlled evidence set.

Pass:

- method recovers controlled recurrence under registered statistic
- global correction behaves as expected
- sensitivity tests do not erase true signal unless designed to

### Battery C: Duplicate-Evidence Trap

Create evidence where many rows derive from one source family.

Pass:

- independence controls collapse or down-weight duplicates
- result is demoted if dependence drives recurrence

### Battery D: Missing-Null Trap

Create evidence where positive rows are visible and nulls are hidden until audit.

Pass:

- missing-evidence assessment flags risk
- result is held or demoted when nulls are added

### Battery E: Unit-Conversion Trap

Create evidence with mixed units, reference systems, or timestamps.

Pass:

- raw/normalized split detects drift
- conversion audit catches mismatches

### Battery F: Inter-Rater Reliability

Two independent reviewers extract and grade the same sample.

Pass:

- extraction disagreements are measured
- dependence and bias disagreements are adjudicated
- training updates are issued

## 3. Validation Metrics

Track:

- false escalation rate
- missed controlled recurrence rate
- extraction disagreement rate
- dependence-grade disagreement rate
- bias-grade disagreement rate
- reproducibility failure rate
- critical finding rate
- time to preflight decision
- time to full package

## 4. Acceptance Targets

Initial operational targets:

- 0 unresolved Critical findings at release
- 100 percent row provenance for full studies
- 100 percent candidate lock coverage
- 100 percent required checksum coverage
- 100 percent clean-run reproduction for release packages where source data can be packaged
- 95 percent or better clean-run reproduction for restricted-data packages where controlled live systems must be re-queried
- documented adjudication for all reviewer disagreements

These targets should tighten after pilot experience.

## 5. Minimum Validation Protocol

Before an organization uses CRAMPS for safety, regulated, public, financial, clinical, security, or operational decisions, run at least:

| Battery | Minimum cases | Minimum seeds or reviewers | Acceptance threshold |
|---|---:|---:|---|
| Known negative | 3 packages | 10 null-model seeds each | 0 false Tier 2 or higher escalations |
| Controlled recurrence injection | 3 packages | 10 null-model seeds each | recovers controlled recurrence in at least 2 of 3 packages without prohibited overclaiming |
| Duplicate-evidence trap | 2 packages | 5 source-family configurations each | duplicate family does not drive a release-ready result |
| Missing-null trap | 2 packages | 1 hidden-null reveal each | package is held or demoted after null reveal when effect changes materially |
| Unit-conversion trap | 2 packages | 5 mixed-unit cases each | all material unit/reference mismatches caught before release |
| Inter-rater reliability | 2 packages | 2 independent reviewers minimum | disagreements adjudicated; extraction and grading disagreement rates reported |

## 6. Required Validation Record

Every validation run must produce:

- validation protocol or test plan
- package list and test-condition description
- seeds, reviewer assignments, and software versions
- expected result before execution
- observed result after execution
- sidecar outputs
- deviations and CAPA records
- validation report using `VALIDATION_REPORT_TEMPLATE.md`
- approval, hold, or rejection decision
