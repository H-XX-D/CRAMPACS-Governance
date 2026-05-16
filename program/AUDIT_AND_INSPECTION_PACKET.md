# Audit and Inspection Packet

**Document ID:** CRAMPS-AUD-001

## 1. Audit Objective

Determine whether the CRAMPS package followed its own controls and whether the evidence supports the assigned assurance level.

For audit execution mechanics, use `AUDIT_PROCEDURE.md`. For the written record, use `AUDIT_REPORT_TEMPLATE.md`.

## 2. Audit Scope

Audit:

- naming and assurance level
- protocol lock
- coordinate registry
- source universe
- row provenance
- null and non-event coverage
- dependence grades
- bias assessment
- null model
- sensitivity tests
- reproducibility
- claim language
- decision authority

## 3. Sampling Plan

Minimum for full package:

- 10 percent of sources or 10 sources, whichever is larger
- 10 percent of rows or 20 rows, whichever is larger
- all rows driving the primary result
- all high-bias rows
- all low-independence rows used in primary analysis
- all negative control rows

## 4. Audit Tests

| Test | Pass condition |
|---|---|
| Protocol hash matches | locked protocol hash equals package record |
| Candidate lock valid | coordinate lock predates scoring |
| Source trace valid | sampled rows trace to source |
| Unit trace valid | normalized values recompute from raw |
| Null coverage valid | null/non-event search is documented |
| Dependence valid | sampled dependence grades are justified |
| Bias valid | bias ratings have rationale |
| Null model valid | null preserves declared source/process structure |
| Sensitivity valid | required sensitivity tests exist |
| Repro valid | clean run reproduces output |
| Claim valid | report language matches evidence tier |

## 5. Finding Severity

Critical:

- post-hoc coordinate selection
- positive-only evidence in confirmatory study
- unmodeled major dependence
- unreproducible primary result
- unsupported safety/regulatory/domain claim

Major:

- incomplete source flow
- missing bias rationale
- weak null model
- missing sensitivity test
- incomplete checksum manifest

Minor:

- formatting issue
- incomplete owner field
- non-material link/path issue

Observation:

- improvement suggestion

## 6. Minimum Audit Outputs

An audit is not complete until it produces:

- audit scope and criteria
- sampled source and row list
- control evidence findings
- severity classification for each finding
- release impact for Critical and Major findings
- CAPA references for accepted findings
- auditor conclusion
- management or release-authority response
