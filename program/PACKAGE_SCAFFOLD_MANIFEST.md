# Package Scaffold Manifest

**Document ID:** CRAMPS-SCAF-001  
**Version:** 0.1  
**Status:** Draft procedure

## 1. Purpose

This manifest defines the files created by `tools/scaffold_cramps_package.py`.

The scaffold is the starting structure for an uppercase `CRAMPS-*` full assurance package. It is intentionally incomplete at creation. The sidecar should report blockers until evidence, registers, gate reviews, and decision records are populated.

## 2. Required Binder Directories

| Binder | Purpose |
|---|---|
| `00_charter` | decision, roles, intended use, prohibited use, constraints |
| `01_protocol_lock` | protocol, candidate registry, amendment log |
| `02_sources` | search strategy, source catalog, source flow, exclusions |
| `03_extraction` | raw rows, extraction notes, reviewer status |
| `04_coordinate_normalization` | transform registry, normalized rows, unit audit |
| `05_dependence_bias` | independence groups, bias assessment, missing evidence |
| `06_statistics` | analysis plan, null runs, results, controls, sensitivities |
| `07_reproducibility` | checksums, environment, run instructions, clean run |
| `08_assurance_case` | claims, rebuttals, residual risk |
| `09_review_and_release` | gate reviews, audit, decision memo, release signoff |
| `10_trust_maintenance` | build ledger, checkpoint reviews, assumptions, claim trace, trust debt |
| `registers` | package-level governance registers |

## 3. Sidecar Rule

The full sidecar checks:

- required binder presence
- required program records
- trust-maintenance records
- required scientific data contracts
- control evidence records
- gate review records
- decision records
- null/non-event coverage
- candidate lock coverage
- dependence and bias coverage
- null-model run presence
- checksum manifest

Missing structure is a package defect. Missing evidence is a release blocker.
