# Learner Workbook

**Document ID:** CRAMPS-TRN-WB-001  
**Version:** 0.1  
**Status:** Draft learner workbook

## 1. Quick Reference

| Term | Meaning |
|---|---|
| Coordinate | parameter value being tested for recurrence |
| Pre-specification | coordinate and rules locked before scoring |
| Null evidence | searched or exposed cases without the suspected recurrence |
| Non-event | source, unit, account, instrument, cohort, or system where no event occurred |
| Dependence | shared dataset, pipeline, instrument, vendor, model, calibration, or source family |
| Bias | process that can create or hide apparent recurrence |
| Sidecar | package readiness and blocker runner |
| Evidence tier | permitted strength of CRAMPS claim |

## 2. Assurance Boundary

`cramps-*` is a 1 to 2 day preflight.

`CRAMPS-*` is a full assurance package after protocol lock, evidence package assembly, gate review, and release decision.

## 3. Exercise Worksheet: Coordinate Lock

| Field | Your entry |
|---|---|
| Domain |  |
| Candidate coordinate |  |
| Units |  |
| Tolerance |  |
| Tolerance basis |  |
| Forbidden changes after lock |  |
| Negative control coordinate or class |  |

## 4. Exercise Worksheet: Source Universe

Use this as a printable version of `templates/preflight_sources.csv`.

| source_id | citation_or_label | url_or_path | source_type | source_role | publication_or_snapshot_date | unit_or_site | known_dependence | screening_status | notes |
|---|---|---|---|---|---|---|---|---|---|
| S1 |  |  |  |  |  |  |  |  |  |
| S2 |  |  |  |  |  |  |  |  |  |
| S3 |  |  |  |  |  |  |  |  |  |
| S4 |  |  |  |  |  |  |  |  |  |
| S5 |  |  |  |  |  |  |  |  |  |
| S6 |  |  |  |  |  |  |  |  |  |
| S7 |  |  |  |  |  |  |  |  |  |
| S8 |  |  |  |  |  |  |  |  |  |
| S9 |  |  |  |  |  |  |  |  |  |
| S10 |  |  |  |  |  |  |  |  |  |

## 5. Exercise Worksheet: Row Integrity

Use this as a printable version of `templates/preflight_rows.csv`.

| row_id | source_id | coordinate_label | coordinate_value | coordinate_units | row_type | result_direction | uncertainty_status | extraction_confidence | dependence_concern | bias_concern | null_or_non_event_flag | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 |  |  |  |  |  |  |  |  |  |  |  |  |
| R2 |  |  |  |  |  |  |  |  |  |  |  |  |
| R3 |  |  |  |  |  |  |  |  |  |  |  |  |
| R4 |  |  |  |  |  |  |  |  |  |  |  |  |
| R5 |  |  |  |  |  |  |  |  |  |  |  |  |
| R6 |  |  |  |  |  |  |  |  |  |  |  |  |
| R7 |  |  |  |  |  |  |  |  |  |  |  |  |
| R8 |  |  |  |  |  |  |  |  |  |  |  |  |
| R9 |  |  |  |  |  |  |  |  |  |  |  |  |
| R10 |  |  |  |  |  |  |  |  |  |  |  |  |

## 6. Exercise Worksheet: Decision

| Question | Answer |
|---|---|
| What decision is requested? |  |
| What evidence tier is justified? |  |
| What is the strongest supporting evidence? |  |
| What is the strongest weakening evidence? |  |
| What claim is prohibited? |  |
| Controlled decision word |  |

Controlled decision words:

| Route | Allowed terms |
|---|---|
| `cramps-*` preflight | `advance_to_CRAMPS-<DOMAIN>`, `hold_coordinate_lock`, `hold_source_completeness`, `hold_dependence_or_bias`, `stop` |
| `CRAMPS-*` full release | `release`, `release_with_conditions`, `hold_for_rework`, `demote_to_exploratory`, `reject`, `stop` |
| supervisor action | `approve`, `approve_with_limits`, `hold`, `demote`, `reject`, `emergency_parallel_action` |

## 7. Trust Positioning Worksheet

| Field | Entry |
|---|---|
| This package is trustworthy for |  |
| This package is not trustworthy for |  |
| Current assurance route |  |
| Current trust state |  |
| Current evidence tier |  |
| Decision safe now |  |
| Decision unsafe now |  |
| Next trust-building action |  |

## 8. Personal Competency Check

Before claiming competency, confirm:

| Skill | I can do this |
|---|---|
| explain CRAMPS in one sentence |  |
| distinguish lowercase and uppercase routes |  |
| write a precise coordinate |  |
| identify null and non-event evidence |  |
| spot duplicate evidence |  |
| identify missing-evidence risk |  |
| interpret sidecar blockers |  |
| write restrained claim language |  |
| defend a hold or rejection |  |
