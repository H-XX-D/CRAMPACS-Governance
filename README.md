# CRAMPACS Governance Package

CRAMPACS means **Coordinate-Resolved Anomaly Meta-analysis with Pre-specified Anomaly Cluster Statistics**.

This repository contains a domain-general governance, methodology, and data-contract package for testing whether weak signals, anomalies, residuals, nulls, exclusions, failures, or near-misses recur at pre-specified coordinates more often than expected under registered null models.

CRAMPACS is not a discovery shortcut. It is a disciplined evidence-synthesis framework for building defensible anomaly-prioritization results.

## Core Documents

- `CRAMPACS_DOCUMENTATION_LAYER_MAP_2026-05-15.md`  
  Explains the documentation layers and how lowercase preflights compose into uppercase full systems.
- `policies/CRAMPACS_NAMING_AND_ASSURANCE_LEVELS_2026-05-15.md`  
  Defines uppercase `CRAMPACS-*` as full assurance and lowercase `crampacs-*` as lightweight preflight.
- `policies/CRAMPACS_PROGRAM_SOP_2026-05-15.md`  
  End-to-end SOP from study charter to external review.
- `policies/CRAMPACS_STANDARDS_AND_PRACTICES_POLICY_2026-05-15.md`  
  Standards stack, quality gates, document control, accreditation-ready controls.
- `policies/CRAMPACS_METHODOLOGY_POLICY_2026-05-15.md`  
  Domain-general methodology rules, claim tiers, null models, sensitivity requirements.
- `policies/CRAMPACS_CROSS_UNIT_EXPERIMENT_CHECKSUM_GUIDELINES_2026-05-15.md`  
  Cross-unit, cross-site, and cross-measurement checksum rules.
- `policies/crampacs_lightweight_preflight_policy_2026-05-15.md`  
  One to two day lightweight preflight system.
- `policies/crampacs_gotchas_and_sanity_checks_2026-05-15.md`  
  Failure-mode and sanity-check guide.

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
- Physics and physical anomaly catalogs, `CRAMPACS-PHY`

## Templates

The `templates/` directory contains the protocol template and CSV data-contract headers for source catalogs, raw anomaly rows, normalized rows, candidate coordinate registries, transforms, independence groups, bias assessment, null runs, results, amendments, agents, and roles.

It also contains preflight templates that compose into the full system:

- `preflight_scope.md`
- `preflight_sources.csv`
- `preflight_rows.csv`
- `preflight_gotchas.md`
- `preflight_decision.md`
- `preflight_manifest.csv`
- `preflight_import_log.csv`

## Domain Packs and Printouts

The `domain_packs/` directory contains field-specific starter packets for every included domain. Each pack has lowercase preflight documents and uppercase full-system addenda.

The `printouts/` directory contains practitioner-facing checklists:

- one to two day preflight printout
- full assurance gate printout
- preflight-to-full composition printout
- field printouts for medicine, genomics, climate, materials, engineering, finance, cybersecurity, astronomy, and physics

## Sidecar Runner

The sidecar runner keeps package metrics as a preflight or full study comes together.

```bash
python tools/crampacs_sidecar.py <package_dir> --level preflight
python tools/crampacs_sidecar.py <package_dir> --level full
```

It writes:

- `crampacs_sidecar_metrics.json`
- `crampacs_sidecar_metrics.md`

The sidecar reports readiness, blockers, null/non-event coverage, dependence coverage, bias coverage, and package checksums.

## Claim Boundary

CRAMPACS can support statements like:

> A pre-specified coordinate shows unusual cross-catalog recurrence under the registered null model and should be prioritized for prospective validation.

CRAMPACS cannot by itself support statements like:

> This proves a clinical, financial, physical, cyber, materials, or engineering causal claim.

Domain-standard confirmation remains required.

## Recommended First Use

Start with a lowercase preflight:

1. Pick a domain suffix, for example `crampacs-fin`.
2. Fill the preflight templates.
3. Run the gotcha checklist.
4. Run the sidecar metrics runner.
5. Decide whether to compose into the uppercase full system.

Then start a narrow full pilot:

1. Pick one domain overlay.
2. Lock 3 to 5 candidate coordinates.
3. Extract a bounded source universe.
4. Include nulls and non-events.
5. Grade dependence.
6. Run negative controls.
7. Reproduce from checksums.
8. Report conservatively.
