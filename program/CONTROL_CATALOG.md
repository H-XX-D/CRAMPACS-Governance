# CRAMPACS Control Catalog

**Document ID:** CRAMPACS-CTRL-001  
**Purpose:** Define auditable controls for CRAMPACS operation.

Controls are mandatory unless explicitly marked optional. Each full `CRAMPACS-*` study must map evidence to every applicable control.

## Control Summary

| Control ID | Control | Objective | Evidence |
|---|---|---|---|
| GOV-01 | Decision authority assigned | Prevent ownerless or informal decisions | charter, role assignment, decision memo |
| GOV-02 | Assurance level declared | Prevent lowercase work from becoming full assurance by implication | charter, report title |
| GOV-03 | Conflict and independence disclosure | Identify bias in people, sponsors, and reviewers | role register, conflict disclosures |
| GOV-04 | Release veto authority preserved | Prevent business pressure overriding controls | signoff record |
| DOC-01 | Document control | Maintain version, owner, status, and change history | document headers, amendment log |
| DOC-02 | Protocol lock | Prevent post-hoc method changes | protocol hash, lock timestamp |
| DOC-03 | Amendment control | Track all post-lock changes | amendment log |
| COORD-01 | Coordinate definition | Prevent vague or mobile target coordinates | coordinate ontology |
| COORD-02 | Tolerance justification | Prevent tolerance creep | candidate registry |
| COORD-03 | Transform registry | Prevent hidden analytical freedom | transform registry |
| COORD-04 | Negative controls | Detect null-model and selection failures | negative-control registry/results |
| SRC-01 | Source universe defined | Prevent cherry-picked literature | search strategy, source catalog |
| SRC-02 | Null/non-event search | Prevent positive-only evidence | source catalog, null row count |
| SRC-03 | Exclusion reasons | Prevent silent removal of inconvenient evidence | exclusion log |
| ROW-01 | Row provenance | Ensure every row traces to source | raw row table, source references |
| ROW-02 | Raw/normalized separation | Prevent unit and transform overwrites | raw and normalized tables |
| ROW-03 | Extraction review | Prevent extraction errors | reviewer ID, extraction confidence |
| ROW-04 | AI-output control | Prevent model hallucination becoming data | agent log, human review flag |
| IND-01 | Evidence-family map | Prevent duplicate evidence multiplication | independence groups |
| IND-02 | Independence grades | Make dependence explicit | independence grades A-E |
| IND-03 | Weighting/collapse rule | Control dependent evidence in analysis | analysis weight table |
| BIAS-01 | Missing-evidence assessment | Identify unpublished or inaccessible nulls | missing-evidence memo |
| BIAS-02 | Reporting-bias assessment | Identify publication, selective-reporting, and threshold bias | bias table |
| BIAS-03 | Domain-specific bias review | Capture field-specific hazards | domain overlay checklist |
| STAT-01 | Primary statistic lock | Prevent statistic shopping | statistical analysis plan |
| STAT-02 | Null model specification | Make test basis explicit | null model spec |
| STAT-03 | Global correction | Control look-elsewhere and multiplicity | result table |
| STAT-04 | Sensitivity tests | Identify fragility | sensitivity results |
| STAT-05 | Negative control behavior | Validate null and source process | negative-control results |
| REPRO-01 | Checksum manifest | Detect silent file drift | manifest and hashes |
| REPRO-02 | Environment record | Support rerun | environment lock |
| REPRO-03 | Clean reproduction | Verify package can be rerun | reproducibility report |
| REL-01 | Evidence tier assignment | Prevent overclaiming | evidence tier table |
| REL-02 | Claim language approval | Prevent unsupported conclusions | signed report review |
| REL-03 | Decision memo | Convert evidence to authorized action | decision memo |
| CAPA-01 | Deviation handling | Track failures and repairs | deviation/CAPA log |
| CAPA-02 | Corrective action verification | Confirm repair works | verification evidence |
| TRUST-01 | Build ledger | Track material work while package is being built | build_ledger.csv |
| TRUST-02 | Trust checkpoint review | Prevent silent promotion of unchecked artifacts | checkpoint_reviews.csv |
| TRUST-03 | Assumption and uncertainty log | Prevent assumptions becoming facts | assumption_uncertainty_log.csv |
| TRUST-04 | Claim trace matrix | Tie every claim to evidence, controls, gates, and permitted reliance | claim_trace_matrix.csv |
| TRUST-05 | Trust debt register | Track unresolved trust gaps with owner, due date, and release impact | trust_debt_register.csv |
| TRUST-06 | Reliance positioning | State what the package is trustworthy for and not trustworthy for | trust status summary, decision memo |
| TRAIN-01 | Role training | Ensure operators know controls | training matrix |
| TRAIN-02 | Competency check | Ensure reviewers can apply method | competency records |

## Minimum Control Sets

### `crampacs-*` Preflight

Required:

- GOV-01
- GOV-02
- COORD-01
- COORD-02
- SRC-01
- SRC-02
- ROW-01
- IND-01
- BIAS-01
- REPRO-01
- REL-03

Preflight controls may be satisfied at lightweight depth. Output is triage only.

### `CRAMPACS-*` Full System

Required:

- All controls in the catalog.

## Control Evidence Rule

A control is not satisfied because a document exists. It is satisfied only when the document contains the required evidence and a named reviewer accepts it.
