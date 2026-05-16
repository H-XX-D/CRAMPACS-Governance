# CRAMPS Governance Package

CRAMPS means **Coordinate-Resolved Anomaly Meta-analysis with Pre-specified Statistics**.

This repository contains a domain-general governance, methodology, and data-contract package for inspecting whether weak observations, anomalies, residuals, nulls, exclusions, failures, or near-misses recur at pre-specified coordinates more often than expected under registered null models.

CRAMPS is not a discovery shortcut and not a way to make weak evidence look strong. It is a disciplined inspection layer for turning signal-in-noise suspicion into a gated, reviewable evidence package.

The method is useful when a team thinks something may be hiding in noisy records but cannot yet justify a full domain claim. CRAMPS preserves the tuning context: the coordinate, source path, null evidence, dependence, bias, uncertainty, and claim limits that usually get lost when weak findings are discussed informally.

## Start Here

| Need | Use |
|---|---|
| Understand the brand and claim boundary | `brand/CRAMPS_BRAND_SYSTEM.md` |
| Teach the method to a team | `training/CRAMPS_TRAINING_GUIDE.md` |
| Run the assurance program | `program/README.md` |
| Create isolated AI-operable packages | `tools/cramps_cli.py` |
| Start a full evidence package | `tools/scaffold_cramps_package.py` |
| Run package readiness checks | `tools/cramps_sidecar.py` |
| Adapt CRAMPS to a field | `domain_packs/` and `domain_overlays/` |
| See a completed teaching preflight | `worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence/` |
| Review research-backed design choices | `research/SUCCESSFUL_FRAMEWORK_PATTERNS.md` |

## Program Spine

Start here if you are deploying CRAMPS inside an organization.

- `program/README.md`
  Entry point for the operational assurance program.
- `program/PROGRAM_OPERATING_MANUAL.md`
  Defines authority, assurance levels, gates, stop rules, evidence tiers, and release requirements.
- `program/CONTROL_CATALOG.md`
  Auditable control catalog covering governance, protocol lock, coordinates, sources, rows, independence, bias, statistics, reproducibility, release, CAPA, and training.
- `program/DOCUMENT_CONTROL_PROCEDURE.md`
  Controlled-document ownership, approval, versioning, effective-date, review, and retirement procedure.
- `program/RELEASE_AUTHORITY_RACI.md` and `program/CANONICAL_GATE_MAP.md`
  Release authority, veto rights, gate IDs, gate inputs, outputs, and blocker rules.
- `program/DEVIATION_AND_CAPA_PROCEDURE.md`
  Deviation, containment, root-cause, corrective-action, preventive-action, effectiveness-check, and reopening procedure.
- `program/ASSURANCE_CASE_FRAMEWORK.md`
  Claim, evidence, rebuttal, and residual-risk framework for defending a CRAMPS result.
- `program/EVIDENCE_PACKAGE_SPEC.md`
  Required binder structure for a complete evidence package.
- `program/PACKAGE_SCAFFOLD_MANIFEST.md`
  Exact scaffold structure and sidecar expectations for full evidence packages.
- `program/DEPLOYMENT_PLAYBOOK.md`
  Practical rollout sequence for introducing CRAMPS inside an organization.
- `program/SAFETY_SUPERVISOR_PACKET.md`
  Practical approval/hold/reject packet for safety supervisors, government program officers, and risk owners.
- `program/AUDIT_AND_INSPECTION_PACKET.md`
  Inspection plan, sampling rules, audit tests, and severity levels.
- `program/AUDIT_PROCEDURE.md` and `program/AUDIT_REPORT_TEMPLATE.md`
  Audit planning, evidence sampling, finding classification, reporting, and closure mechanics.
- `program/VALIDATION_AND_BENCHMARKING_PLAN.md`
  Validation batteries for known negatives, controlled recurrence injections, duplicate-evidence traps, missing-null traps, unit-conversion traps, and inter-rater reliability.
- `program/VALIDATION_REPORT_TEMPLATE.md`
  Standard report format for documenting validation evidence and acceptance decisions.
- `program/REGULATED_DEPLOYMENT_ADDENDUM.md`
  Added controls for safety, security, public agency, financial, clinical, or other regulated decisions.
- `program/TRAINING_AND_COMPETENCY_PLAN.md` and `program/IMPLEMENTATION_ROADMAP_90_DAY.md`
  Role competency expectations and a 90-day operational rollout plan.
- `program/POLISH_ROUNDS_2026-05-16.md`
  Ten-round aesthetic, teaching, and system polish log.
- `program/AI_TRUSTED_USE_GATE_DAG_AND_QUARANTINE_POLICY.md`
  AI operator rules, package/source boundary, gate DAGs, term/prerequisite accounting, leak watches, and quarantine protocol.

## Brand and Training

The `brand/` directory defines the CRAMPS identity, message architecture, visual roles, document style, decision language, and claim-boundary patterns.

The `training/` directory contains a teachable training kit:

- `CRAMPS_TRAINING_GUIDE.md`
- `INSTRUCTOR_GUIDE.md`
- `LEARNER_WORKBOOK.md`
- `EXERCISE_PACKETS.md`
- `COMPETENCY_RUBRIC.md`
- `SLIDE_OUTLINE.md`

The `research/` directory records source-backed design lessons from PRISMA, Cochrane, GRADE, ISO quality management, NIST risk frameworks, NASA systems engineering, and FDA quality systems.

## Supporting Documents

- `CRAMPS_DOCUMENTATION_LAYER_MAP_2026-05-15.md`
  Explains the documentation layers and how lowercase preflights compose into uppercase full systems.
- `policies/CRAMPS_NAMING_AND_ASSURANCE_LEVELS_2026-05-15.md`
  Defines uppercase `CRAMPS-*` as full assurance and lowercase `cramps-*` as lightweight preflight.
- `policies/CRAMPS_PROGRAM_SOP_2026-05-15.md`
  End-to-end SOP from study charter to external review.
- `policies/CRAMPS_STANDARDS_AND_PRACTICES_POLICY_2026-05-15.md`
  Standards stack, quality gates, document control, accreditation-ready controls.
- `policies/CRAMPS_METHODOLOGY_POLICY_2026-05-15.md`
  Domain-general methodology rules, claim tiers, null models, sensitivity requirements.
- `policies/CRAMPS_CROSS_UNIT_EXPERIMENT_CHECKSUM_GUIDELINES_2026-05-15.md`
  Cross-unit, cross-site, and cross-measurement checksum rules.
- `policies/cramps_lightweight_preflight_policy_2026-05-15.md`
  One to two day lightweight preflight system.
- `policies/cramps_gotchas_and_sanity_checks_2026-05-15.md`
  Failure-mode and fast-check guide. The filename is retained for compatibility with preflight templates.

## Domain Names

Every domain has two names. Use lowercase for the lightweight preflight and uppercase for the full assurance system.

| Lightweight preflight | Full assurance | Domain |
|---|---|---|
| `cramps-med` | `CRAMPS-MED` | Medicine and clinical evidence |
| `cramps-gen` | `CRAMPS-GEN` | Genomics and omics |
| `cramps-clim` | `CRAMPS-CLIM` | Climate and Earth systems |
| `cramps-mat` | `CRAMPS-MAT` | Materials science |
| `cramps-eng` | `CRAMPS-ENG` | Engineering reliability |
| `cramps-fin` | `CRAMPS-FIN` | Finance, fraud, and risk |
| `cramps-cyb` | `CRAMPS-CYB` | Cybersecurity |
| `cramps-ast` | `CRAMPS-AST` | Astronomy and astrophysics |
| `cramps-phy` | `CRAMPS-PHY` | Physics and physical anomaly catalogs |

The `domain_overlays/` directory adapts the full system to each domain. The `domain_packs/` directory gives each domain both lowercase preflight templates and uppercase full-system addenda.

## Templates

The `templates/` directory contains the protocol template and CSV data-contract headers for source catalogs, raw signal rows, normalized rows, candidate coordinate registries, transforms, independence groups, bias assessment, null runs, results, amendments, agents, and roles.

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

## Worked Examples

The `worked_examples/` directory contains sanitized teaching examples. The included `cramps-phy` preflight uses one operator only, then shows where expanded full-system agent deployment would begin during a separate `CRAMPS-PHY` escalation.

## End-To-End CLI

Use the CLI when an AI agent or practitioner needs to run a reusable CRAMPS
system without contaminating the sanitized source kit.

```bash
python tools/cramps_cli.py init --level preflight --domain phy --study-id STUDY001
python tools/cramps_cli.py check ./cramps_projects/<package>
python tools/cramps_cli.py leak-scan ./cramps_projects/<package>
python tools/cramps_cli.py gate ./cramps_projects/<package>
```

The CLI writes package-local AI instructions, gate DAG status, prerequisite
accounting, leak-watch reports, quarantine logs, sidecar metrics, and checksums.

To compose a lowercase preflight into an uppercase full package without changing
the original preflight:

```bash
python tools/cramps_cli.py promote <preflight_package> --study-id STUDY001-FULL
```

Package outputs created under `cramps_projects/` are ignored by git so the
source kit remains reusable.

## Sidecar Runner

The sidecar runner keeps package metrics as a preflight or full study comes together.

```bash
python tools/cramps_sidecar.py <package_dir> --level preflight
python tools/cramps_sidecar.py <package_dir> --level full
```

It writes:

- `cramps_sidecar_metrics.json`
- `cramps_sidecar_metrics.md`

The sidecar reports readiness, blockers, null/non-event coverage, dependence coverage, bias coverage, and package checksums.

For full packages, start from the evidence-binder scaffold:

```bash
python tools/scaffold_cramps_package.py <package_dir> --domain med --study-id STUDY001
```

The full-system sidecar checks both scientific data contracts and program controls: binder coverage, required records, control evidence, gate review records, decision records, row provenance, null/non-event coverage, dependence, bias, null-model runs, and checksums.

## Claim Boundary

CRAMPS can support statements like:

> A pre-specified coordinate shows unusual cross-catalog recurrence under the registered null model and should be prioritized for prospective validation.

CRAMPS cannot by itself support statements like:

> This proves a clinical, financial, physical, cyber, materials, or engineering causal claim.

Domain-standard confirmation remains required.

## Method Posture

CRAMPS should be read as an inspection and assurance layer. It asks whether the same coordinate keeps attracting weak evidence after nulls, non-events, duplicate evidence, reporting bias, unit conversions, and look-elsewhere effects are made visible.

It does not answer the final domain question. It answers whether a suspected recurrence has earned a better, more expensive test.

## Recommended First Use

Start with a lowercase preflight:

1. Pick a domain suffix, for example `cramps-fin`.
2. Fill the preflight templates.
3. Run the failure-mode checklist.
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
