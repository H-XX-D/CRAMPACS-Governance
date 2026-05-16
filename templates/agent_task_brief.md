# CRAMPS Agent Task Brief

**Study ID:** `[fill]`
**Package level:** `preflight` / `full`
**Deployment mode:** `[fill]`
**Agent ID:** `[fill]`
**Agent role:** `[fill]`
**Assigned gate span:** `[fill]`
**Reviewer ID:** `[fill]`

## Assignment

State the bounded task this agent may perform.

## Allowed Inputs

- [ ]

## Prohibited Inputs

- [ ]

## Allowed Writes

- Package-local paths only:

## Required Outputs

- [ ]

## Human Review Requirement

State the reviewer, review basis, and sampling or dual-review rule.

## Command Loop

Run these after material edits and before handoff:

```bash
python tools/cramps_cli.py check <package_dir>
python tools/cramps_cli.py agent-audit <package_dir>
python tools/cramps_cli.py leak-scan <package_dir>
python tools/cramps_cli.py gate <package_dir>
python tools/cramps_cli.py acceptance-audit <package_dir>
python tools/cramps_cli.py status <package_dir>
```

## Handoff Record

Record artifact handoff in `ai_controls/agent_handoff_checklist.csv`.

## Stop Conditions

Stop and quarantine if the agent finds a critical leak, source-kit
contamination, fabricated field, untraceable source value, deleted null or
non-event evidence, blocked-gate bypass, or claim language above package level.
