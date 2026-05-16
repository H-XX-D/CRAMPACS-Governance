# Expected Check, Leak, and Gate Output

Run:

```bash
python tools/cramps_sidecar.py worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence \
  --level preflight \
  --out-json /tmp/cramps-phy-worked-sidecar.json \
  --out-md /tmp/cramps-phy-worked-sidecar.md
```

Expected result:

- recommendation: `candidate_for_CRAMPS_upgrade`
- required artifacts: present
- source count: 5
- row count: 5
- positive-like rows: 2
- null or non-event rows: 3
- blockers: none

This expected output means the example is structurally ready to demonstrate escalation. It does not mean the synthetic coordinate is real or significant.

Then run:

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
python tools/cramps_cli.py release-check package /tmp/cramps-phy-worked-example --level preflight --force
```

Expected gate posture:

- leak scan has zero open critical findings
- highest cleared priority: `50`
- next blocked gate: blank
- all clear: `true`
- review-packet decision: `ready_for_review_handoff`

The gate result clears only the worked preflight structure. It does not clear any full `CRAMPS-PHY` gate.
