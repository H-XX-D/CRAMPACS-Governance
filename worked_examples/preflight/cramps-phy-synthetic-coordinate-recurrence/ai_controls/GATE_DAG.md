# CRAMPS Gate DAG

This worked example follows the lowercase preflight gate path.

| gate | priority | phase | depends on | terms/prerequisites |
|---|---:|---|---|---|
| `G0` | 0 | package_boundary | none | package state exists and is active; package is not inside controlled source material |
| `P1` | 10 | preflight_scope | G0 | preflight scope exists; all required preflight artifacts exist |
| `P2` | 20 | source_accounting | P1 | preflight sources have at least one row; source unit diversity is accounted for |
| `P3` | 30 | row_extraction | P2 | preflight rows have at least one row; coordinate values and units are populated |
| `P4` | 40 | null_and_failure_mode_check | P3 | at least one null or non-event row exists; failure-mode worksheet exists |
| `P5` | 50 | decision_and_leak_clearance | P4 | decision record exists; sidecar blockers are clear; leak scan has no open critical finding |

Run gate accounting only after check and leak scan:

```bash
python tools/cramps_cli.py check worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
python tools/cramps_cli.py leak-scan worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence
python tools/cramps_cli.py gate worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
```
