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
| 10 | Trust maintenance | Checkpoint honesty, reliance positioning, trust debt, claim trace | trust maintenance protocol, trust checkpoint map, trust positioning, trust status summary |
| 11 | Regulatory and deployment | Safety supervisor review, audit, validation, training, regulated deployment | supervisor packet, audit procedure, validation plan, training plan, regulated addendum, deployment playbook, 90-day roadmap |
| 12 | Platform | Software workflow modules | future product layer |

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
| TRUST-01 | Build ledger | Track material work while package is being built | build_ledger.csv |
| TRUST-02 | Trust checkpoint review | Prevent silent promotion of unchecked artifacts | checkpoint_reviews.csv |
| TRUST-03 | Assumption and uncertainty log | Prevent assumptions becoming facts | assumption_uncertainty_log.csv |
| TRUST-04 | Claim trace matrix | Tie every claim to evidence, controls, gates, and permitted reliance | claim_trace_matrix.csv |
| TRUST-05 | Trust debt register | Track unresolved trust gaps with owner, due date, and release impact | trust_debt_register.csv |
| TRUST-06 | Reliance positioning | State what the package is trustworthy for and not trustworthy for | trust status summary, decision memo |
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
| 10_trust_maintenance | build ledger, checkpoints, assumptions, claim trace, trust debt | build_ledger.csv; checkpoint_reviews.csv; assumption_uncertainty_log.csv; claim_trace_matrix.csv; trust_debt_register.csv; trust_status_summary.md; open_questions.md |
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
| trust_debt_register.csv | unresolved trust gaps and release impact |

## Brand Controls

| Control | Rule |
| --- | --- |
| Assurance boundary | Every artifact states whether it is crampacs-* or CRAMPACS-* |
| Claim boundary | Every release-facing artifact states what CRAMPACS does not prove |
| Decision language | Approve, approve_with_limits, hold, demote, reject, stop, emergency_parallel_action |
| Severity language | Critical, Major, Minor, Observation |
| Stop signs | Preflight and full package stop rules are easy to find |
| Evidence names | Required evidence uses concrete file, register, or binder names |
| Domain humility | Domain claims are restrained and require domain-standard confirmation |

## Training Paths

| Track | Audience | Duration | Output |
| --- | --- | --- | --- |
| Executive briefing | Sponsor, agency lead, director | 60 minutes | adoption decision and pilot scope |
| Supervisor orientation | Safety supervisor, risk owner, program officer | 2 hours | approval, hold, demote, reject literacy |
| Preflight workshop | Analyst, domain reviewer, project lead | 1 day | completed mock crampacs-* preflight |
| Practitioner course | Data scientist, evidence reviewer, auditor | 3 days | full package walkthrough and gate practice |
| Instructor course | Internal trainer, quality lead | 2 days after practitioner course | teach-back and scoring consistency |

## Framework Patterns

| Framework | Pattern | CRAMPACS adoption |
| --- | --- | --- |
| PRISMA | Checklist plus flow diagrams | Use checklists, printouts, and package flow |
| Cochrane | Missing-evidence risk | Treat nulls, non-events, and missing evidence as release issues |
| GRADE | Separate certainty and recommendation | Separate evidence tier from supervisor decision |
| ISO quality management | Process, evidence-based decisions, improvement | Use owners, registers, CAPA, and review cadence |
| NIST CSF | Core, examples, references, tiers | Keep a small core with implementation examples and maturity levels |
| NIST AI RMF | Framework plus playbook | Pair principles with teachable actions |
| NASA systems engineering | Lifecycle reviews | Use G0-G7 as lifecycle gates |
| FDA quality systems | Quality model plus regulatory boundary | Add regulated controls without claiming automatic compliance |

## Trust States

| Trust state | Meaning | Reliance rule |
| --- | --- | --- |
| draft | work has started but is not checked | do not rely |
| unchecked | artifact exists but no reviewer has accepted it | do not rely |
| checked_with_limits | reviewed, but known limits remain | rely only within stated limits |
| accepted | reviewed and accepted for current gate | rely within current evidence tier |
| blocked | has a defect that prevents promotion or release | do not promote |
| superseded | replaced by a newer artifact | retain but do not use |
| quarantined | retained for traceability but excluded from scoring or release | do not use as evidence |

## Reliance Levels

| Package state | Trustworthy for | Not trustworthy for |
| --- | --- | --- |
| idea sketch | conversation and scoping | CRAMPACS claim, preflight decision, operational decision |
| crampacs-* checked | continue, hold, stop, or full-study escalation | domain conclusion, full assurance, external claim |
| CRAMPACS-* scaffold | organizing work | evidence reliance or release |
| CRAMPACS-* gate-accepted | advancing to the next gate | release unless G7 is complete |
| CRAMPACS-* release-ready | decision support within assigned evidence tier | proof of causality or regulatory compliance by itself |
| externally validated | stronger prioritization and process confidence | domain proof unless domain-standard confirmation is complete |

## Trust Checkpoints

| Checkpoint | Package point | Main honesty risk | Minimum review |
| --- | --- | --- | --- |
| T0 | package start | unclear purpose or hidden intended use | decision owner, intended use, prohibited use |
| T1 | coordinate proposed | coordinate drift or tolerance creep | coordinate, units, tolerance, forbidden changes |
| T2 | sources drafted | positive-only evidence | source roles, null search, exclusions |
| T3 | rows extracted | source trace or AI-summary drift | source links, raw values, extraction confidence |
| T4 | normalization drafted | hidden unit conversion | raw/normalized separation, transform review |
| T5 | dependence and bias drafted | duplicate evidence counted independently | evidence-family map, missing-evidence risk |
| T6 | statistics planned | statistic shopping or weak null | locked statistic, null model, multiplicity plan |
| T7 | results generated | local result overclaimed | global correction, sensitivities, negative controls |
| T8 | report drafted | claim exceeds evidence tier | claim trace matrix, prohibited claims |
| T9 | release review | unknown trust state | trust status summary, sidecar, open CAPA |
