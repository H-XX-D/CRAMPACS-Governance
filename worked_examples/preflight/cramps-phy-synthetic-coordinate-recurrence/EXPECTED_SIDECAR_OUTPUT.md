# Expected Check, Leak, and Gate Output

Run:

```bash
python tools/cramps_sidecar.py worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
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
python tools/cramps_cli.py leak-scan worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence
python tools/cramps_cli.py gate worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
```

Expected gate posture:

- leak scan has zero open critical findings
- highest cleared priority: `50`
- next blocked gate: blank
- all clear: `true`

The gate result clears only the worked preflight structure. It does not clear any full `CRAMPS-PHY` gate.
