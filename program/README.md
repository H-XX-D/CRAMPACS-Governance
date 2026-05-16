# CRAMPS Program Spine

This directory is the operational spine of CRAMPS.

The repository has templates, domain packs, printouts, and spreadsheets. Those are supporting artifacts. The files in this directory define the actual assurance program a team can run.

## Operating Principle

Lowercase `cramps-*` is a lightweight preflight. It answers whether a suspected coordinate recurrence deserves investment.

Uppercase `CRAMPS-*` is the full assurance system. It produces a defensible evidence package only after protocol lock, source accounting, null evidence, dependence and bias review, statistical analysis, reproducibility, and signoff.

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
11. `FIRST_PILOT_RUNBOOK.md`
12. `PILOT_SELECTION_SCORECARD.md`
13. `SAFETY_SUPERVISOR_PACKET.md`
14. `AUDIT_AND_INSPECTION_PACKET.md`
15. `AUDIT_PROCEDURE.md`
16. `VALIDATION_AND_BENCHMARKING_PLAN.md`
17. `REGULATED_DEPLOYMENT_ADDENDUM.md`
18. `REGISTER_DATA_DICTIONARY.md`
19. `POLISH_ROUNDS_2026-05-16.md`
20. `TRUST_MAINTENANCE_PROTOCOL.md`
21. `TRUST_CHECKPOINT_MAP.md`
22. `TRUST_POSITIONING_AND_RELIANCE_LEVELS.md`
23. `TRUST_STATUS_SUMMARY_TEMPLATE.md`
24. `AI_TRUSTED_USE_GATE_DAG_AND_QUARANTINE_POLICY.md`
25. `AGENT_DEPLOYMENT_HELPERS.md`
26. `RELEASE_ACCEPTANCE_CHECKLIST.md`
27. `ROUND_3_HARDENING_AUDIT_2026-05-16.md`

## Operational Templates

Use these when running a real engagement:

- `DECISION_MEMO_TEMPLATE.md`
- `DEVIATION_AND_CAPA_TEMPLATE.md`
- `AUDIT_REPORT_TEMPLATE.md`
- `VALIDATION_REPORT_TEMPLATE.md`
- `TRAINING_AND_COMPETENCY_PLAN.md`
- `IMPLEMENTATION_ROADMAP_90_DAY.md`
- `RELEASE_ACCEPTANCE_CHECKLIST.md`
- `FIRST_PILOT_RUNBOOK.md`
- `PILOT_SELECTION_SCORECARD.md`
- `AGENT_DEPLOYMENT_HELPERS.md`

## Registers

The `registers/` folder contains CSV logs for evidence, controls, risk, CAPA, gate reviews, training, decisions, and assurance claims.

These are not decorative. A CRAMPS package is not release-ready unless the relevant registers are filled and reviewed.

## Package Scaffold

Use the end-to-end CLI when an AI agent or practitioner is operating a package:

```bash
python tools/cramps_cli.py init --level preflight --domain med --study-id STUDY001
python tools/cramps_cli.py check ./cramps_projects/<package>
python tools/cramps_cli.py agent-audit ./cramps_projects/<package>
python tools/cramps_cli.py leak-scan ./cramps_projects/<package>
python tools/cramps_cli.py gate ./cramps_projects/<package>
python tools/cramps_cli.py acceptance-audit ./cramps_projects/<package>
python tools/cramps_cli.py review-packet ./cramps_projects/<package>
```

The CLI creates a package-local AI operator brief, agent deployment helper,
deployment plan, handoff checklist, DAG gate map, term/prerequisite ledger,
agent-audit report, leak-watch report, acceptance-audit report, reviewer packet,
quarantine protocol, sidecar metrics, and checksums. The source kit remains
sanitized for reuse.

For source-kit handoff, run:

```bash
python tools/cramps_cli.py source-audit
```

Use the lower-level scaffold tool only when you need the full evidence-binder
structure without the CLI operating controls:

```bash
python tools/scaffold_cramps_package.py ./packages/CRAMPS_MED_STUDY001 --domain med --study-id STUDY001
python tools/cramps_sidecar.py ./packages/CRAMPS_MED_STUDY001 --level full
```

The first command creates the binder. The second command shows what is still missing before the package can be treated as release-ready.

## Teaching and Adoption

Use the training kit when introducing CRAMPS to a team:

- `../training/CRAMPS_TRAINING_GUIDE.md`
- `../training/INSTRUCTOR_GUIDE.md`
- `../training/LEARNER_WORKBOOK.md`
- `../training/EXERCISE_PACKETS.md`
- `../training/COMPETENCY_RUBRIC.md`

Use the brand kit when writing public, internal, or platform-facing material:

- `../brand/CRAMPS_BRAND_SYSTEM.md`
- `../brand/CRAMPS_DOCUMENT_STYLE_GUIDE.md`
- `../brand/CRAMPS_MESSAGE_ARCHITECTURE.md`
