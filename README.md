# CRAMPACS Governance Package

CRAMPACS means **Coordinate-Resolved Anomaly Meta-analysis with Pre-specified Anomaly Cluster Statistics**.

This repository contains a domain-general governance, methodology, and data-contract package for testing whether weak signals, anomalies, residuals, nulls, exclusions, failures, or near-misses recur at pre-specified coordinates more often than expected under registered null models.

CRAMPACS is not a discovery shortcut. It is a disciplined evidence-synthesis framework for building defensible anomaly-prioritization results.

## Core Documents

- `policies/CRAMPACS_PROGRAM_SOP_2026-05-15.md`  
  End-to-end SOP from study charter to external review.
- `policies/CRAMPACS_STANDARDS_AND_PRACTICES_POLICY_2026-05-15.md`  
  Standards stack, quality gates, document control, accreditation-ready controls.
- `policies/CRAMPACS_METHODOLOGY_POLICY_2026-05-15.md`  
  Domain-general methodology rules, claim tiers, null models, sensitivity requirements.
- `policies/CRAMPACS_CROSS_UNIT_EXPERIMENT_CHECKSUM_GUIDELINES_2026-05-15.md`  
  Cross-unit, cross-site, and cross-measurement checksum rules.

## Domain Overlays

The `domain_overlays/` directory adapts CRAMPACS to:

- Medicine and clinical evidence, `CRAMPACS-MED`, alias `CRAMPACS-M`
- Genomics and omics, `CRAMPACS-GEN`
- Climate and Earth systems, `CRAMPACS-CLIM`
- Materials science, `CRAMPACS-MAT`
- Engineering reliability, `CRAMPACS-ENG`
- Finance, fraud, and risk, `CRAMPACS-FIN`, alias `CRAMPACS-F`
- Cybersecurity, `CRAMPACS-CYB`
- Astronomy and astrophysics, `CRAMPACS-AST`

## Templates

The `templates/` directory contains the protocol template and CSV data-contract headers for source catalogs, raw anomaly rows, normalized rows, candidate coordinate registries, transforms, independence groups, bias assessment, null runs, results, amendments, agents, and roles.

## Claim Boundary

CRAMPACS can support statements like:

> A pre-specified coordinate shows unusual cross-catalog recurrence under the registered null model and should be prioritized for prospective validation.

CRAMPACS cannot by itself support statements like:

> This proves a clinical, financial, physical, cyber, materials, or engineering causal claim.

Domain-standard confirmation remains required.

## Recommended First Use

Start with a narrow pilot:

1. Pick one domain overlay.
2. Lock 3 to 5 candidate coordinates.
3. Extract a bounded source universe.
4. Include nulls and non-events.
5. Grade dependence.
6. Run negative controls.
7. Reproduce from checksums.
8. Report conservatively.

