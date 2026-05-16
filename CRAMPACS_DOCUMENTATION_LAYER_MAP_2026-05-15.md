# CRAMPACS Documentation Layer Map

**Document ID:** CRAMPACS-DOCMAP-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft documentation architecture

## 1. Purpose

This document defines the documentation layers for the CRAMPACS ecosystem.

The goal is composability:

- A team can run a lowercase `crampacs-*` preflight in one to two days.
- The preflight produces seed artifacts.
- Those artifacts can be imported into the uppercase `CRAMPACS-*` full system.
- The full system adds protocol lock, full data contracts, independence, bias, null models, sensitivity, checksums, red-team review, and domain signoff.
- The same documentation layers apply across every domain.

## 2. Naming Principle

The naming distinction is an assurance boundary.

| Name style | Meaning | Output |
|---|---|---|
| lowercase `crampacs-*` | Lightweight preflight | Triage and escalation recommendation |
| uppercase `CRAMPACS-*` | Full assurance system | Defensible evidence package under registered protocol |

Included examples:

- `crampacs-med` can compose into `CRAMPACS-MED`.
- `crampacs-gen` can compose into `CRAMPACS-GEN`.
- `crampacs-clim` can compose into `CRAMPACS-CLIM`.
- `crampacs-mat` can compose into `CRAMPACS-MAT`.
- `crampacs-eng` can compose into `CRAMPACS-ENG`.
- `crampacs-fin` can compose into `CRAMPACS-FIN`.
- `crampacs-cyb` can compose into `CRAMPACS-CYB`.
- `crampacs-ast` can compose into `CRAMPACS-AST`.
- `crampacs-phy` can compose into `CRAMPACS-PHY`.

The pattern extends to any field.

## 3. Documentation Layers

### Layer 0: Concept Layer

Purpose:

- Define what CRAMPACS is and is not.
- Define the claim boundary.
- Explain the uppercase/lowercase distinction.

Documents:

- `README.md`
- `policies/CRAMPACS_NAMING_AND_ASSURANCE_LEVELS_2026-05-15.md`

Output:

- Shared vocabulary.
- Assurance boundary.
- Product and practice positioning.

### Layer 1: Lightweight Preflight Layer

Purpose:

- Run a one to two day pass.
- Determine whether deeper work is worth it.
- Produce seed artifacts for the full system.

Documents:

- `policies/crampacs_lightweight_preflight_policy_2026-05-15.md`
- `templates/preflight_scope.md`
- `templates/preflight_sources.csv`
- `templates/preflight_rows.csv`
- `templates/preflight_gotchas.md`
- `templates/preflight_decision.md`
- `templates/preflight_manifest.csv`
- Conversion artifact: `templates/preflight_import_log.csv`

Output:

- Coordinate sketch.
- Source shortlist.
- Row sketch.
- Gotcha register.
- Sidecar metrics.
- Preflight manifest.
- Escalation decision.

`preflight_import_log.csv` is created during conversion into the full system.

### Layer 2: Gotcha and Sanity Layer

Purpose:

- Catch cheap failure modes before expensive analysis.
- Give practitioners fast checks.
- Prevent obvious misuse.

Documents:

- `policies/crampacs_gotchas_and_sanity_checks_2026-05-15.md`
- `printouts/crampacs_preflight_1_to_2_day_printout.md`
- `printouts/preflight_to_full_composition_printout.md`

Output:

- Stop signs.
- Five-minute sanity score.
- Known failure-mode register.
- Printable field checklists.

### Layer 3: Core Standards Layer

Purpose:

- Define program governance, standards stack, quality gates, document control, and accreditation-ready controls.

Documents:

- `program/PROGRAM_OPERATING_MANUAL.md`
- `program/CONTROL_CATALOG.md`
- `program/DOCUMENT_CONTROL_PROCEDURE.md`
- `program/RELEASE_AUTHORITY_RACI.md`
- `program/CANONICAL_GATE_MAP.md`
- `program/DEVIATION_AND_CAPA_PROCEDURE.md`
- `policies/CRAMPACS_STANDARDS_AND_PRACTICES_POLICY_2026-05-15.md`

Output:

- Required practices.
- Quality gates.
- Deviation and corrective-action rules.
- Reporting policy.
- Auditable control evidence requirements.

### Layer 4: Core Methodology Layer

Purpose:

- Define the domain-general CRAMPACS method.
- Define coordinate ontology, nulls, dependence, bias, sensitivity, and claim tiers.

Documents:

- `policies/CRAMPACS_METHODOLOGY_POLICY_2026-05-15.md`

Output:

- Method rules.
- Claim tiers.
- Null-model ladder.
- Methodological vetoes.

### Layer 5: Domain Overlay Layer

Purpose:

- Adapt the method to a field.
- Define field-specific coordinates, nulls, dependence hazards, bias hazards, standards, and claim limits.

Documents:

- `domain_overlays/CRAMPACS_MED_MEDICINE_OVERLAY.md`
- `domain_overlays/CRAMPACS_GEN_GENOMICS_OVERLAY.md`
- `domain_overlays/CRAMPACS_CLIM_CLIMATE_OVERLAY.md`
- `domain_overlays/CRAMPACS_MAT_MATERIALS_OVERLAY.md`
- `domain_overlays/CRAMPACS_ENG_ENGINEERING_OVERLAY.md`
- `domain_overlays/CRAMPACS_FIN_FINANCE_OVERLAY.md`
- `domain_overlays/CRAMPACS_CYB_CYBERSECURITY_OVERLAY.md`
- `domain_overlays/CRAMPACS_AST_ASTRONOMY_OVERLAY.md`
- `domain_overlays/CRAMPACS_PHY_PHYSICS_OVERLAY.md`
- `domain_packs/<domain>/README.md`
- `printouts/<domain>_field_printout.md`

Output:

- Domain adapter.
- Domain-specific gotchas.
- Standards anchors.
- Domain claim limits.
- Domain-specific preflight templates.
- Domain-specific full-system addenda.

### Layer 6: Data Contract Layer

Purpose:

- Make evidence portable, reviewable, and reproducible.

Documents:

- `templates/source_catalog.csv`
- `templates/anomaly_rows_raw.csv`
- `templates/normalized_rows.csv`
- `templates/candidate_coordinate_registry.csv`
- `templates/coordinate_transform_registry.csv`
- `templates/independence_groups.csv`
- `templates/bias_assessment.csv`
- `templates/null_model_runs.csv`
- `templates/analysis_result.csv`
- `templates/amendment_log.csv`
- `templates/agent_registry.csv`
- `templates/role_assignment.csv`
- `domain_packs/<domain>/*_PREFLIGHT_SOURCES.csv`
- `domain_packs/<domain>/*_PREFLIGHT_ROWS.csv`
- `program/REGISTER_DATA_DICTIONARY.md`
- `program/registers/*.csv`
- `program/PACKAGE_SCAFFOLD_MANIFEST.md`
- `tools/scaffold_crampacs_package.py`

Output:

- Structured study tables.
- Stable IDs.
- Reusable package format.
- Field-specific printable tables that preserve the core schema.

### Layer 7: Cross-Unit Checksum Layer

Purpose:

- Verify that data, units, transforms, and outputs do not silently drift across teams, sites, instruments, vendors, or systems.

Documents:

- `policies/CRAMPACS_CROSS_UNIT_EXPERIMENT_CHECKSUM_GUIDELINES_2026-05-15.md`

Output:

- Unit manifest.
- Conversion audit.
- Analysis manifest.
- Top-level experiment checksum.

### Layer 8: Sidecar Metrics Layer

Purpose:

- Keep package metrics as the package comes together.
- Flag missing controls before release.
- Support preflight-to-full upgrade decisions.

Documents and tools:

- `tools/crampacs_sidecar.py`

Output:

- `crampacs_sidecar_metrics.json`
- `crampacs_sidecar_metrics.md`
- Package manifest with hashes.
- Readiness score.
- Blocker list.
- Recommendation.

### Layer 9: Full SOP Layer

Purpose:

- Define end-to-end execution for a full study.

Documents:

- `program/EVIDENCE_PACKAGE_SPEC.md`
- `program/PACKAGE_SCAFFOLD_MANIFEST.md`
- `program/ASSURANCE_CASE_FRAMEWORK.md`
- `program/DECISION_MEMO_TEMPLATE.md`
- `program/DEVIATION_AND_CAPA_TEMPLATE.md`
- `policies/CRAMPACS_PROGRAM_SOP_2026-05-15.md`
- `templates/CRAMPACS_PROTOCOL_TEMPLATE.md`

Output:

- Full study workflow.
- Protocol lock.
- Source search.
- Extraction.
- Normalization.
- Independence and bias review.
- Statistical analysis.
- Sensitivity.
- Reporting.
- Reproducibility capsule.
- External review.
- Assurance claim register.

### Layer 10: Regulatory and Accreditation Layer

Purpose:

- Pair CRAMPACS controls with field-specific regulatory or assurance systems.

Documents:

- `program/SAFETY_SUPERVISOR_PACKET.md`
- `program/AUDIT_AND_INSPECTION_PACKET.md`
- `program/AUDIT_PROCEDURE.md`
- `program/AUDIT_REPORT_TEMPLATE.md`
- `program/VALIDATION_AND_BENCHMARKING_PLAN.md`
- `program/VALIDATION_REPORT_TEMPLATE.md`
- `program/REGULATED_DEPLOYMENT_ADDENDUM.md`
- `program/DEPLOYMENT_PLAYBOOK.md`
- `program/TRAINING_AND_COMPETENCY_PLAN.md`
- `program/IMPLEMENTATION_ROADMAP_90_DAY.md`
- Core standards policy.
- Domain overlay.
- Organization-specific compliance addendum.

Output:

- Audit-ready decision support when paired with applicable domain controls.
- Not automatic compliance.

### Layer 11: Platform Layer

Purpose:

- Turn the documentation stack into software workflows.

Platform modules:

- Protocol builder.
- Coordinate registry.
- Source atlas.
- Extraction workbench.
- Independence graph.
- Bias register.
- Null model lab.
- Sidecar metrics dashboard.
- Checksum and reproducibility capsule.
- Claim-tier approval workflow.
- Preflight-to-full import workflow.

Output:

- Repeatable organizational operating system for weak-signal recurrence.

## 4. Composition Path

The intended path is:

```text
crampacs-* preflight
  -> gotcha scan
  -> sidecar metrics
  -> escalation decision
  -> preflight import log
  -> CRAMPACS-* full protocol
  -> full data contracts
  -> full null/dependence/bias/statistical review
  -> checksum/reproducibility capsule
  -> red-team and domain signoff
```

The preflight is not thrown away. It becomes the seed bundle for the full system.

The assurance claim starts only after the full system protocol lock.

## 5. Field Extension Pattern

To add a new field:

1. Choose a suffix.
2. Define lowercase and uppercase names.
3. Create a domain overlay.
4. Define coordinate families.
5. Define row types.
6. Define nulls and non-events.
7. Define dependence hazards.
8. Define bias hazards.
9. Define checksum additions.
10. Define standards anchors.
11. Define claim limits.

Example:

```text
crampacs-edu  -> education preflight
CRAMPACS-EDU  -> education full assurance system
```

## 6. Documentation Rule

Every new domain should have both:

- a lowercase preflight route
- an uppercase full assurance route

The same templates should be reused wherever possible. Domain-specific fields should be added through addenda, not by breaking the core data contracts.
