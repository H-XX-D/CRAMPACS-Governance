# cramps-phy Synthetic Coordinate Recurrence Worked Example

**Level:** `cramps-phy` lowercase preflight
**Target if escalated:** `CRAMPS-PHY`
**Status:** sanitized teaching example
**Agent rule:** one preflight operator only

This folder shows a completed one to two day preflight. The data are synthetic and exist only to demonstrate how CRAMPS artifacts fit together.

The example asks whether a synthetic set of physics-style records shows enough coordinate-specific recurrence near a pre-specified mass coordinate to justify opening a full `CRAMPS-PHY` package.

## How To Read It

1. Start with `preflight_scope.md`.
2. Review `preflight_sources.csv`.
3. Review `preflight_rows.csv`.
4. Read `preflight_gotchas.md`.
5. Read `preflight_decision.md`.
6. Check `ai_controls/agent_registry.csv` and `ai_controls/agent_deployment_plan.csv` to confirm the one-agent preflight rule.
7. Read `FULL_SYSTEM_HANDOFF.md` to see where expanded agent deployment would begin.
8. Read `RUN_RECORD.md` for source-safe verification commands.
9. Use `TEACHING_SCRIPT.md` when walking a learner through the example.

## Expected Sidecar Result

Run from the repository root without writing back into the source example:

```bash
python tools/cramps_sidecar.py worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence \
  --level preflight \
  --out-json /tmp/cramps-phy-worked-sidecar.json \
  --out-md /tmp/cramps-phy-worked-sidecar.md
```

For mutating CLI checks, copy the example first:

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
python tools/cramps_cli.py release-check package /tmp/cramps-phy-worked-example --level preflight --force
```

Expected posture:

- required preflight artifacts present
- positive-like and null/non-event rows present
- coordinate and unit coverage complete
- contract audit passes on source, row, manifest, and agent-control CSVs
- no full-system claim permitted
- decision may recommend escalation only as a preflight output

## Claim Boundary

This example does not claim that the synthetic coordinate is real, important, physical, or statistically significant. It only demonstrates a defensible preflight structure.
