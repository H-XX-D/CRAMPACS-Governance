# CRAMPACS Evidence Package Specification

**Document ID:** CRAMPACS-EPS-001

## 1. Purpose

This specification defines what a complete CRAMPACS evidence package must contain.

## 2. Package Layout

```text
CRAMPACS_<domain>_<study_id>/
  00_charter/
  01_protocol_lock/
  02_sources/
  03_extraction/
  04_coordinate_normalization/
  05_dependence_bias/
  06_statistics/
  07_reproducibility/
  08_assurance_case/
  09_review_and_release/
  10_trust_maintenance/
  registers/
```

## 3. Required Binders

### Binder 00: Charter

Required:

- decision statement
- assurance level
- roles and authorities
- domain constraints
- intended use
- prohibited use

### Binder 01: Protocol Lock

Required:

- protocol
- candidate registry
- coordinate ontology
- statistical analysis plan
- null model specification
- protocol hash
- amendment log

### Binder 02: Sources

Required:

- search strategy
- source catalog
- source flow
- exclusion reasons
- source snapshots or pointers

### Binder 03: Extraction

Required:

- raw anomaly rows
- extraction notes
- extraction reviewer status
- plot digitization logs if applicable
- AI agent logs if applicable

### Binder 04: Coordinate Normalization

Required:

- transform registry
- normalized rows
- unit conversion audit
- reference system notes

### Binder 05: Dependence and Bias

Required:

- independence groups
- evidence-family map
- bias assessment
- missing-evidence assessment
- analysis weights

### Binder 06: Statistics

Required:

- primary statistic code or formula
- null model runs
- primary result
- global correction
- sensitivity results
- negative control results

### Binder 07: Reproducibility

Required:

- checksum manifest
- environment record
- run script
- output hashes
- clean-run report

### Binder 08: Assurance Case

Required:

- assurance claim register
- claim evidence map
- rebuttal log
- residual risk register

### Binder 09: Review and Release

Required:

- red-team report
- reviewer comments
- response to findings
- evidence tier approval
- claim-language approval
- decision memo

### Binder 10: Trust Maintenance

Required:

- build ledger
- checkpoint reviews
- assumption and uncertainty log
- claim trace matrix
- trust debt register
- trust status summary
- open questions

## 4. Completeness Rule

An evidence package is complete only when:

- every required binder exists
- every applicable control has evidence
- every Critical finding is closed
- release authority signs the decision memo

## 5. Minimum File Contract

The scaffold tool creates the minimum file structure. Teams may add files, but they may not remove or rename these without updating the sidecar and register references.

| Binder | Minimum records |
|---|---|
| `00_charter` | `study_charter.md`, `role_assignment.csv` |
| `01_protocol_lock` | `protocol.md`, `candidate_coordinate_registry.csv`, `amendment_log.csv` |
| `02_sources` | `search_strategy.md`, `source_catalog.csv`, `source_flow.md` |
| `03_extraction` | `anomaly_rows_raw.csv`, `extraction_notes.md` |
| `04_coordinate_normalization` | `coordinate_transform_registry.csv`, `normalized_rows.csv`, `unit_conversion_audit.md` |
| `05_dependence_bias` | `independence_groups.csv`, `bias_assessment.csv`, `missing_evidence_assessment.md` |
| `06_statistics` | `statistical_analysis_plan.md`, `null_model_runs.csv`, `analysis_result.csv`, `negative_controls.md`, `sensitivity_results.md` |
| `07_reproducibility` | `checksum_manifest.csv`, `environment_record.md`, `run_instructions.md`, `clean_run_report.md` |
| `08_assurance_case` | `assurance_case.md`, `assurance_case_register.csv`, `risk_register.csv` |
| `09_review_and_release` | `gate_review_record.csv`, `audit_report.md`, `decision_memo.md`, `claim_language_approval.md`, `release_signoff.md` |
| `10_trust_maintenance` | `build_ledger.csv`, `checkpoint_reviews.csv`, `assumption_uncertainty_log.csv`, `claim_trace_matrix.csv`, `trust_debt_register.csv`, `trust_status_summary.md`, `open_questions.md` |
| `registers` | document, control evidence, gate review, assurance case, CAPA, decision, risk, and training registers |

## 6. Sidecar Expectation

The full-system sidecar treats missing binders or minimum records as structural blockers. A package can be in progress with blockers, but it cannot be released while structural blockers or unresolved Critical findings remain.
