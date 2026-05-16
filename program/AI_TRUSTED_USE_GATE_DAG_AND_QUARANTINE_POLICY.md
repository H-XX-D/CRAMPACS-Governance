# CRAMPS AI Trusted Use, Gate DAG, Leak Watch, and Quarantine Policy

## Purpose

This policy governs AI-assisted operation of CRAMPS packages. It exists to
keep the reusable source kit sanitized, make package progress inspectable, and
prevent weak-evidence inspection from turning into uncontrolled pattern claims.

The policy applies to both:

- lowercase `cramps-*` preflight packages
- uppercase `CRAMPS-*` full assurance packages

## Source-Kit Boundary

The repository is the source kit. It contains reusable templates, policies,
program files, domain packs, training material, printouts, and tools.

A study package is a separate working directory created by:

```bash
python tools/cramps_cli.py init --level preflight --domain med --study-id STUDY001
python tools/cramps_cli.py init --level full --domain med --study-id STUDY001
```

Package operators, including AI agents, write inside the package directory.
They do not edit source-kit files while running a package.

The source kit may be revised only as a controlled program-maintenance task,
not as an accidental byproduct of a study.

## AI Operator Rules

Before doing package work, an AI operator must read:

- `cramps_project.json`
- `ai_controls/AI_OPERATOR_BRIEF.md`
- `ai_controls/AGENT_DEPLOYMENT_HELPER.md`
- `ai_controls/GATE_DAG.md`
- `ai_controls/LEAK_WATCH_SURFACES.md`
- `ai_controls/QUARANTINE_PROTOCOL.md`

The AI operator must:

1. State the current package level and blocked gate before substantive work.
2. Work only inside the package directory.
3. Preserve nulls, non-events, exclusions, failed replications, and negative controls.
4. Leave unknown values blank instead of inventing values.
5. Record material actions in `logs/ai_activity_log.csv`.
6. Run sidecar checks after material edits.
7. Run agent-control audit after deployment-plan, registry, or handoff changes.
8. Run leak scanning before gate accounting, export, escalation, release, or external sharing.
9. Run gate accounting before phase progress.
10. Run acceptance audit before promotion, release review, external sharing, or reliance upgrade.
11. Quarantine the package if a critical leak, source-boundary breach, fabricated field, or overclaim appears.

The AI operator must not:

- clear gates manually
- hide or delete adverse evidence
- remove rows to improve a score
- upgrade lowercase preflight language into uppercase full-assurance claims
- claim proof, discovery, causality, safety, efficacy, fraud, exploitability, or compliance from CRAMPS alone
- export restricted, private, sensitive, or source-contaminated material

## Agent Deployment Controls

The package-local deployment plan controls how agents may be used:

- `ai_controls/AGENT_DEPLOYMENT_HELPER.md`
- `ai_controls/agent_deployment_plan.csv`
- `ai_controls/agent_handoff_checklist.csv`
- `ai_controls/agent_registry.csv`

A lowercase `cramps-*` preflight defaults to one accountable operator:
`single_preflight_operator`. Additional agents require a documented deviation
and may not turn the preflight into an uppercase assurance package.

An uppercase `CRAMPS-*` package may use role-specific agents only inside their
assigned gate spans. Material handoffs must be recorded in the handoff
checklist. Agent identity, model or tool version, prompt or SOP version, review
requirement, and audit-log path must be recorded in the agent registry.

Run:

```bash
python tools/cramps_cli.py agent-audit <package_dir>
```

The command writes `ai_controls/agent_audit_status.json` and
`ai_controls/agent_audit_report.md`. Blockers mean the agent deployment layer is
not consistent enough to support phase progress.

Before promotion or release review, run:

```bash
python tools/cramps_cli.py acceptance-audit <package_dir>
```

The command writes `ai_controls/acceptance_audit_status.json` and
`ai_controls/acceptance_audit_report.md`. It does not prove the domain claim. It
states whether the package controls are coherent enough for the requested
preflight decision or full-system release review. It also checks that sidecar,
agent-audit, and gate artifacts match the requested level and that the gate was
run after the sidecar, agent audit, and leak scan.

## DAG Gate Accounting

CRAMPS gates are dependency gates. A later phase cannot progress merely
because its own files exist. It progresses only when:

- all dependency gates are clear
- all terms and prerequisites for the current gate are met
- no open critical leak finding exists
- quarantine status is clear

The CLI writes three gate-accounting artifacts:

- `ai_controls/gate_status.json`
- `ai_controls/gate_status.md`
- `ai_controls/term_prereq_ledger.csv`

The term/prerequisite ledger is the accounting record for phase progress. Each
row identifies:

- gate ID
- phase
- priority
- term or prerequisite
- status
- evidence artifact
- missing item or blocker
- cleared timestamp when applicable

If a term is not met, the phase is blocked. If a dependency gate is blocked, the
phase is blocked even when its local terms appear complete.

## Lowercase Preflight Gate DAG

| gate | phase | progress condition |
|---|---|---|
| `G0` | package boundary | package state is active, outside controlled source material, and agent-audit has no blockers |
| `P1` | preflight scope | required preflight artifacts exist |
| `P2` | source accounting | sources exist and source-unit diversity is accounted for |
| `P3` | row extraction | rows exist with coordinate values and units |
| `P4` | null and failure-mode check | null/non-event evidence and failure-mode worksheet exist |
| `P5` | decision and leak clearance | decision record exists, sidecar required-artifact blockers are clear, and leak scan has no open critical finding |

A lowercase preflight can recommend escalation only after `P5` clears. It cannot
make an uppercase `CRAMPS-*` claim.

## Uppercase Full-System Gate DAG

| gate | phase | progress condition |
|---|---|---|
| `G0` | package boundary | package state is active, outside controlled source material, and agent-audit has no blockers |
| `F1` | charter | charter, roles, and binders exist |
| `F2` | protocol lock | protocol exists and candidate coordinates are locked |
| `F3` | source and raw signal rows | source catalog, raw signal rows, and null/non-event evidence exist |
| `F4` | coordinate normalization | normalized rows, transform registry, and unit audit exist |
| `F5` | dependence and bias | independence and bias coverage are complete |
| `F6` | statistics | statistical plan, null runs, global result fields, and negative controls exist |
| `F7` | reproducibility | checksum manifest, environment record, and clean-run report exist |
| `F8` | trust and release | trust ledger, checkpoint, claim trace, decision record, and leak clearance exist |

An uppercase full package is not release-ready until `F8` clears and the
release authority accepts the decision memo and claim language.

## Leak Watch Surfaces

Leak scanning watches surfaces where trust can fail quietly:

| surface | examples | response |
|---|---|---|
| source-kit boundary | package work appears under `templates/`, `program/`, `domain_packs/`, or other controlled source directories | quarantine and move work into a package |
| intake | raw PDFs, exports, dumps, private files, screenshots, or logs | classify sensitivity and record provenance |
| evidence tables | secrets, identifiers, fabricated values, unreviewed sensitive rows | quarantine affected artifact |
| AI prompts/logs | private data copied into prompts, notes, summaries, or action logs | quarantine and redact before reuse |
| exports | uncontrolled claims or restricted material in shareable outputs | hold export and run claim review |
| metrics/manifests | hashes show the wrong artifact set or source contamination | hold gate and rebuild |
| quarantine | unresolved release hold | no phase progress |

The CLI leak scan is a minimum control. It does not replace privacy, security,
legal, clinical, financial, classified, or regulatory review.

## Quarantine Protocol

Quarantine is a no-release and no-escalation state. It preserves the problem for
review instead of deleting or masking it.

Quarantine is required when any of the following occurs:

- critical credential, token, key, or private identifier pattern appears
- package work is written into controlled source material
- a package contains fabricated, backfilled, or untraceable evidence
- a blocked prerequisite is bypassed
- claim language exceeds the package assurance level
- restricted data appears in exports, prompts, summaries, or logs without authorization

Run:

```bash
python tools/cramps_cli.py quarantine <package_dir> --reason "<reason>"
```

Quarantine writes:

- `quarantine/QUARANTINE_NOTICE.md`
- `logs/quarantine_log.csv`
- updated `cramps_project.json`

Clearance requires:

- documented reviewer basis
- clean leak scan
- new gate evaluation
- updated affected artifacts or explicit exclusion/quarantine of those artifacts

Run:

```bash
python tools/cramps_cli.py clear-quarantine <package_dir> --reviewer-id <id> --basis "<basis>"
```

Clearing quarantine does not clear gates by itself. The gate DAG must be rerun.

## Trusted Use Statement

A CRAMPS package is trustworthy only for the reliance it has earned. Gate
clearance means prerequisites for the next phase are accounted for. It does not
mean the underlying domain claim is true, causal, safe, compliant, or externally
validated.
