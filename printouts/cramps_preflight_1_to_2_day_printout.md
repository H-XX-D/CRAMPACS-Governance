# cramps-* 1-2 Day Preflight Printout

Use this only for the lowercase preflight route, for example `cramps-med`.
If escalated, the decision must name the matching uppercase full system, for example `CRAMPS-MED`.

## Inputs

- Domain suffix:
- Question:
- Candidate coordinate:
- Units:
- Tolerance sketch:
- Decision owner:

## Required Artifacts

| Artifact | Done | Notes |
|---|---|---|
| preflight_scope.md |  |  |
| preflight_sources.csv |  |  |
| preflight_rows.csv |  |  |
| preflight_gotchas.md |  |  |
| preflight_decision.md |  |  |
| preflight_manifest.csv |  |  |
| sidecar metrics |  |  |

## Stop Signs

- No coordinate lock.
- No nulls.
- One source family.
- Units unclear.
- Dependence unknown.
- Bias ignored.
- Team wants a full assurance claim.

## Decision

- advance_to_CRAMPS-<DOMAIN>
- hold_coordinate_lock
- hold_source_completeness
- hold_dependence_or_bias
- stop
