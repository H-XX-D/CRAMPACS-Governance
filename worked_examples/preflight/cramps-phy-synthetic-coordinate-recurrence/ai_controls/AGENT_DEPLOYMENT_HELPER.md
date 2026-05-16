# Agent Deployment Helper

**Package:** `cramps-phy`
**Study ID:** EX-PHY-001
**Title:** synthetic coordinate recurrence teaching preflight

This worked example uses the lowercase preflight deployment mode:
`single_operator_preflight`.

## Preflight Deployment Rule

The only active operator is `single_preflight_operator`.

No additional agents are deployed inside this worked preflight. Expanded role
deployment starts only after a separate uppercase `CRAMPS-PHY` package is
created and the preflight artifacts are imported, reviewed, accepted, reworked,
rejected, or quarantined.

## Required Files

- `ai_controls/agent_deployment_plan.csv`
- `ai_controls/agent_handoff_checklist.csv`
- `ai_controls/agent_registry.csv`
- `logs/ai_activity_log.csv`

## Command Order

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
python tools/cramps_cli.py release-check package /tmp/cramps-phy-worked-example --level preflight --force
```

## Handoff Rule

This example has no internal multi-agent handoff. If it is used as seed
material for a full package, the target package must record the import and
review disposition before any uppercase package gate relies on it.
