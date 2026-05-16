# CRAMPACS Governance Master Printout

## System Rule

- Uppercase `CRAMPACS-*` is the full assurance system.
- Lowercase `crampacs-*` is the one to two day preflight.
- A preflight can seed the full system, but only the full system can carry full assurance after protocol lock.

## Documentation Layers

| Layer | Name | Purpose | Documents |
| --- | --- | --- | --- |
| 0 | Concept | Vocabulary, claim boundary, uppercase/lowercase distinction | README, naming policy |
| 1 | Lightweight preflight | 1-2 day triage and seed artifacts | preflight policy, preflight templates, domain packs |
| 2 | Gotchas | Fast failure-mode checks and stop signs | gotcha guide, field printouts |
| 3 | Program standards | Governance, quality gates, document control, release authority, CAPA | program operating manual, control catalog, document control, release RACI, gate map, CAPA procedure |
| 4 | Methodology | Coordinate ontology, nulls, dependence, bias, claim tiers | methodology policy, protocol template |
| 5 | Domain overlay | Field-specific adaptation | domain overlays, domain packs, field printouts |
| 6 | Data contracts | Structured tables, stable IDs, register schemas | templates, register data dictionary, package scaffold |
| 7 | Checksums | Cross-unit reproducibility and unit integrity | checksum policy, reproducibility binder |
| 8 | Sidecar metrics | Package readiness, binder coverage, blockers | sidecar runner |
| 9 | Full SOP | End-to-end study execution and evidence package assembly | program SOP, evidence package spec, assurance case, decision memo |
| 10 | Regulatory and deployment | Safety supervisor review, audit, validation, training, regulated deployment | supervisor packet, audit procedure, validation plan, training plan, regulated addendum, deployment playbook, 90-day roadmap |
| 11 | Platform | Software workflow modules | future product layer |

## Quality Gates

| Gate | Required evidence | When checked |
| --- | --- | --- |
| G0 Charter | decision statement, assurance level, roles, intended use, prohibited use | Before protocol lock |
| G1 Coordinate Lock | coordinate ontology, candidate registry, tolerance basis, transform rules, negative controls | Before source scoring |
| G2 Source Universe | search strategy, source catalog, source flow, exclusions, null search | Before extraction closeout |
| G3 Row Integrity | raw rows, source trace, extraction confidence, review status, quarantine log | Before normalization closeout |
| G4 Dependence and Bias | evidence-family map, independence grades, bias table, missing-evidence memo, weights | Before analysis |
| G5 Statistical Method | primary statistic, null model, multiplicity correction, negative controls, sensitivity plan | Before reporting |
| G6 Reproducibility | checksums, environment, run script, output hashes, clean-run report | Before release review |
| G7 Release | assurance case, red-team findings, decision memo, evidence tier, claim-language approval | Before external or operational use |

## Supervisor Questions

| No. | Question |
| --- | --- |
| 1 | What coordinate is being tested? |
| 2 | Was it locked before scoring? |
| 3 | What nulls or non-events were included? |
| 4 | What evidence is duplicated or dependent? |
| 5 | What bias could create the pattern? |
| 6 | What negative control was used? |
| 7 | What would make us stop believing the recurrence? |
| 8 | Can the package be reproduced? |
| 9 | What action is being requested? |
| 10 | What claim is explicitly prohibited? |

## Core Controls

| Control ID | Control | Objective | Evidence |
| --- | --- | --- | --- |
| GOV-01 | Decision authority assigned | Prevent ownerless decisions | charter, role assignment, decision memo |
| GOV-02 | Assurance level declared | Prevent lowercase work being treated as full assurance | charter, report title |
| DOC-02 | Protocol lock | Prevent post-hoc method changes | protocol hash, lock timestamp |
| COORD-01 | Coordinate definition | Prevent vague or mobile target coordinates | coordinate ontology |
| COORD-02 | Tolerance justification | Prevent tolerance creep | candidate registry |
| SRC-02 | Null/non-event search | Prevent positive-only evidence | source catalog, null row count |
| ROW-01 | Row provenance | Ensure every row traces to source | raw row table |
| ROW-02 | Raw/normalized separation | Prevent unit and transform overwrites | raw and normalized tables |
| IND-01 | Evidence-family map | Prevent duplicate evidence multiplication | independence groups |
| BIAS-01 | Missing-evidence assessment | Identify inaccessible or unpublished nulls | missing-evidence memo |
| STAT-02 | Null model specification | Make the test basis explicit | null model spec |
| STAT-03 | Global correction | Control look-elsewhere and multiplicity | result table |
| STAT-04 | Sensitivity tests | Identify fragility | sensitivity results |
| REPRO-01 | Checksum manifest | Detect silent file drift | manifest and hashes |
| REPRO-03 | Clean reproduction | Verify package can be rerun | reproducibility report |
| REL-01 | Evidence tier assignment | Prevent overclaiming | evidence tier table |
| REL-02 | Claim language approval | Prevent unsupported conclusions | signed report review |
| CAPA-01 | Deviation handling | Track failures and repairs | deviation/CAPA log |
| TRAIN-01 | Role training | Ensure operators know controls | training matrix |

## Package Scaffold

| Binder | Purpose | Minimum records |
| --- | --- | --- |
| 00_charter | decision, roles, intended use, prohibited use, constraints | study_charter.md; role_assignment.csv |
| 01_protocol_lock | protocol, candidate registry, amendment control | protocol.md; candidate_coordinate_registry.csv; amendment_log.csv |
| 02_sources | search strategy, source catalog, source flow | search_strategy.md; source_catalog.csv; source_flow.md |
| 03_extraction | raw rows and extraction review | anomaly_rows_raw.csv; extraction_notes.md |
| 04_coordinate_normalization | transforms, normalized rows, unit audit | coordinate_transform_registry.csv; normalized_rows.csv; unit_conversion_audit.md |
| 05_dependence_bias | independence, bias, missing evidence | independence_groups.csv; bias_assessment.csv; missing_evidence_assessment.md |
| 06_statistics | analysis plan, null model, result, controls, sensitivities | statistical_analysis_plan.md; null_model_runs.csv; analysis_result.csv; negative_controls.md; sensitivity_results.md |
| 07_reproducibility | checksums, environment, run instructions, clean run | checksum_manifest.csv; environment_record.md; run_instructions.md; clean_run_report.md |
| 08_assurance_case | claims, rebuttals, residual risk | assurance_case.md; assurance_case_register.csv; risk_register.csv |
| 09_review_and_release | gate review, audit, decision, release signoff | gate_review_record.csv; audit_report.md; decision_memo.md; claim_language_approval.md; release_signoff.md |
| registers | package-level governance registers | document; control; gate; assurance; CAPA; decision; risk; training |

## Program Registers

| Register | Purpose |
| --- | --- |
| document_register.csv | document control, version, status, approval |
| control_evidence_register.csv | control-by-control evidence map |
| gate_review_record.csv | gate decisions, blockers, release holds |
| assurance_case_register.csv | claim, evidence, rebuttal, residual risk |
| deviation_capa_log.csv | deviation, containment, CAPA, effectiveness |
| decision_log.csv | authorized decision, tier, conditions, prohibited claims |
| risk_register.csv | active and residual risks |
| training_matrix.csv | role training and competency |
