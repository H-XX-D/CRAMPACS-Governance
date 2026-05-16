# CRAMPS Agent Deployment Helpers

**Document ID:** CRAMPS-AGENT-HELP-001
**Status:** Operating helper
**Applies to:** human agents, software agents, and AI-assisted agents working inside `cramps-*` or `CRAMPS-*` packages

## 1. Purpose

This helper turns the CRAMPS agent system into a deployable operating layer. It
defines when agents may be used, what each role may touch, how handoffs are
recorded, and what must stop progress.

The goal is not to make agents autonomous authorities. The goal is to let a
team divide work without losing source trace, gate accountability, null
evidence, independence controls, or claim boundaries.

## 2. Deployment Principle

CRAMPS agents perform bounded work under documented contracts.

They may:

- gather source candidates under a registered strategy
- extract values into controlled tables
- normalize coordinates under locked transforms
- map dependence and bias
- run registered checks or null models
- draft claim-limited summaries from reviewed evidence
- red-team the package

They may not:

- decide that a domain claim is true
- add candidate coordinates after result inspection
- hide nulls, non-events, exclusions, or failed replications
- treat duplicate evidence as independent
- turn AI summaries into source data
- clear gates manually
- approve release alone

## 3. Deployment Modes

| Mode | Use when | Agent rule | Output |
|---|---|---|---|
| `single_operator_preflight` | one to two day lowercase `cramps-*` preflight | one accountable operator only unless a deviation is approved | preflight decision |
| `full_system_role_agents` | uppercase `CRAMPS-*` package after charter and protocol-lock path exists | role-specific agents work inside gate spans | full evidence package |
| `red_team_only` | package appears complete but needs adversarial inspection | red-team agent can read all package artifacts but cannot rewrite claims to bypass findings | findings and trust debt |
| `quarantine_recovery` | package is quarantined or contaminated | only containment, review, and repair agents may work | clearance record or rejected package |

## 4. Preconditions Before Agent Deployment

Before any agent beyond the default operator begins:

1. Package exists outside controlled source material.
2. `cramps_project.json` status is `active`.
3. `ai_controls/AGENT_DEPLOYMENT_HELPER.md` has been read.
4. `ai_controls/agent_deployment_plan.csv` has a row for the agent.
5. `ai_controls/agent_registry.csv` records agent identity, version, prompt or SOP, and audit path.
6. Allowed inputs, prohibited inputs, required outputs, and write scope are explicit.
7. `logs/ai_activity_log.csv` is available for material-action logging.
8. Current command loop has been run in this order:

```bash
python tools/cramps_cli.py check <package_dir>
python tools/cramps_cli.py agent-audit <package_dir>
python tools/cramps_cli.py leak-scan <package_dir>
python tools/cramps_cli.py gate <package_dir>
python tools/cramps_cli.py acceptance-audit <package_dir>
```

If the next blocked gate is outside the agent's assigned gate span, do not use
that agent to force progress. Reassign, amend, or hold.

## 5. Role Cards

| Role | Gate span | Main outputs | Review gate | Hard stop |
|---|---|---|---|---|
| Preflight operator | `G0-P5` | preflight scope, sources, rows, gotchas, decision | before promotion | multi-agent drift without deviation |
| Protocol agent | `F1-F2` | protocol, coordinate registry, amendment log | protocol steward | result-informed coordinate change |
| Source search agent | `F2-F3` | source catalog, search strategy, source flow | search lead | adverse source removal |
| Extraction agent | `F3` | `anomaly_rows_raw.csv`, extraction notes | sampled or dual review | inferred value entered as source value |
| Normalization agent | `F3-F4` | normalized rows, transform registry, unit audit | coordinate lead | undocumented conversion |
| Independence agent | `F4-F5` | independence groups | independence auditor | duplicate evidence counted as independent |
| Bias agent | `F4-F5` | bias assessment, missing-evidence assessment | bias auditor | missing evidence minimized or hidden |
| Statistics agent | `F5-F6` | null runs, result table, negative controls, sensitivities | statistical lead | post-hoc null tuning |
| Reproducibility agent | `F6-F7` | checksums, environment record, clean-run report | reproducibility lead | editing evidence to pass rebuild |
| Reporting agent | `F7-F8` | decision memo, claim trace, exports | release authority | claim exceeds evidence tier |
| Red-team agent | `F6-F8` | audit report, trust debt, blocker list | release authority | finding closed without basis |

## 6. Handoff Requirements

Every material handoff must be recorded in
`ai_controls/agent_handoff_checklist.csv`.

Record:

- from-agent and to-agent IDs
- artifact path
- artifact state
- gate context
- open blockers
- quarantine status
- reviewer
- acceptance timestamp

Conversation notes are not enough. A later reviewer must be able to reconstruct
which artifact was handed off, under which gate, and with what unresolved risk.

## 7. Quarantine Triggers

Stop package progress and run quarantine when an agent detects:

- credential, token, private key, or unauthorized identifier exposure
- package work written into source-kit folders
- fabricated, backfilled, or untraceable evidence fields
- hidden deletion of nulls, non-events, exclusions, or failed replications
- blocked-gate bypass
- unapproved restricted data in prompts, logs, exports, or summaries
- claim language above package assurance level

## 8. Supervisor Quick Check

Before accepting an agent-produced package, a supervisor should be able to find:

- completed deployment plan rows for each agent used
- registry rows with versions and review requirements
- activity log entries for material actions
- handoff checklist rows for material transfers
- clean leak scan or documented quarantine
- gate status generated after the latest leak scan
- claim trace showing no unsupported release language

If any item is missing, the package may still be useful as working material, but
it is not yet defensible as a CRAMPS deliverable.

## 9. Machine Audit

Run `agent-audit` whenever the deployment plan, registry, or handoff checklist
changes:

```bash
python tools/cramps_cli.py agent-audit <package_dir>
```

The command checks required files, CSV headers, required plan fields, duplicate
agent IDs, lowercase preflight one-operator discipline, full-system role
coverage, active-agent registry records, and handoff references. It writes:

- `ai_controls/agent_audit_status.json`
- `ai_controls/agent_audit_report.md`

Warnings can be acceptable during setup. Blockers must be resolved, deferred
with documented authority, or quarantined before a package relies on agent work.
Gate evaluation treats a missing or stale agent audit as blocked. Re-run
`agent-audit` after changing the helper, deployment plan, handoff checklist, or
agent registry.
