# CRAMPACS Program Spine

This directory is the operational spine of CRAMPACS.

The repository has templates, domain packs, printouts, and spreadsheets. Those are supporting artifacts. The files in this directory define the actual assurance program a team can run.

## Operating Principle

Lowercase `crampacs-*` is a lightweight preflight. It answers whether a suspected coordinate recurrence deserves investment.

Uppercase `CRAMPACS-*` is the full assurance system. It produces a defensible evidence package only after protocol lock, source accounting, null evidence, dependence and bias review, statistical analysis, reproducibility, and signoff.

## Core Program Documents

Read in this order:

1. `PROGRAM_OPERATING_MANUAL.md`
2. `CONTROL_CATALOG.md`
3. `DOCUMENT_CONTROL_PROCEDURE.md`
4. `RELEASE_AUTHORITY_RACI.md`
5. `CANONICAL_GATE_MAP.md`
6. `DEVIATION_AND_CAPA_PROCEDURE.md`
7. `ASSURANCE_CASE_FRAMEWORK.md`
8. `EVIDENCE_PACKAGE_SPEC.md`
9. `PACKAGE_SCAFFOLD_MANIFEST.md`
10. `DEPLOYMENT_PLAYBOOK.md`
11. `SAFETY_SUPERVISOR_PACKET.md`
12. `AUDIT_AND_INSPECTION_PACKET.md`
13. `AUDIT_PROCEDURE.md`
14. `VALIDATION_AND_BENCHMARKING_PLAN.md`
15. `REGULATED_DEPLOYMENT_ADDENDUM.md`
16. `REGISTER_DATA_DICTIONARY.md`

## Operational Templates

Use these when running a real engagement:

- `DECISION_MEMO_TEMPLATE.md`
- `DEVIATION_AND_CAPA_TEMPLATE.md`
- `AUDIT_REPORT_TEMPLATE.md`
- `VALIDATION_REPORT_TEMPLATE.md`
- `TRAINING_AND_COMPETENCY_PLAN.md`
- `IMPLEMENTATION_ROADMAP_90_DAY.md`

## Registers

The `registers/` folder contains CSV logs for evidence, controls, risk, CAPA, gate reviews, training, decisions, and assurance claims.

These are not decorative. A CRAMPACS package is not release-ready unless the relevant registers are filled and reviewed.

## Package Scaffold

Use the scaffold tool to create the full evidence-binder structure:

```bash
python tools/scaffold_crampacs_package.py ./packages/CRAMPACS_MED_STUDY001 --domain med --study-id STUDY001
python tools/crampacs_sidecar.py ./packages/CRAMPACS_MED_STUDY001 --level full
```

The first command creates the binder. The second command shows what is still missing before the package can be treated as release-ready.
