# AI Operator Brief

**Package:** `cramps-phy` worked example
**Study ID:** EX-PHY-001
**Title:** synthetic-coordinate-recurrence
**Trust posture:** teaching example, synthetic data, non-confirmatory

## Prime Directive

Operate inside this worked-example folder only. Do not edit reusable source-kit templates, policies, program files, domain packs, printouts, training files, or tools while reviewing this example.

## One-Agent Preflight Rule

This preflight uses one operator only:

- `single_preflight_operator`

Do not spawn additional agents inside the preflight. Expanded agent deployment starts only after a separate uppercase `CRAMPS-PHY` package is created and the preflight is imported with review disposition.

## Required Loop

1. Read `cramps_project.json`, this brief, `ai_controls/AGENT_DEPLOYMENT_HELPER.md`, and `ai_controls/GATE_DAG.md`.
2. State the current level: lowercase `cramps-phy` preflight.
3. Inspect `preflight_scope.md`, `preflight_sources.csv`, `preflight_rows.csv`, `preflight_gotchas.md`, and `preflight_decision.md`.
4. Run `python tools/cramps_cli.py check worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight` from the repo root.
5. Run `python tools/cramps_cli.py agent-audit worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight`.
6. Run `python tools/cramps_cli.py leak-scan worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence`.
7. Run `python tools/cramps_cli.py gate worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight`.
8. Treat synthetic rows as quarantined from any real full-system scoring.

## Non-Negotiables

- Do not claim the synthetic coordinate is real.
- Do not treat this as a full `CRAMPS-PHY` result.
- Do not remove nulls or non-events to improve the example.
- Do not deploy additional preflight agents.
- Do not edit source-kit files while working this example.
