# cramps-ast Failure Modes and Fast Checks Printable

**Domain:** Astronomy and astrophysics

## Primary Domain Failure Modes

sky coverage bias, cadence bias, follow-up selection bias, calibration drift

## Ten Fast Checks

| Check | Pass/Hold/Fail | Notes |
|---|---|---|
| Coordinate can be stated precisely |  |  |
| Coordinate was chosen before scoring |  |  |
| Nulls and non-events were found |  |  |
| Rows are not all from one source family |  |  |
| Units and transforms are clear |  |  |
| Tolerance window is justified before scoring |  |  |
| Domain-specific bias was checked |  |  |
| One-source removal would not collapse the case |  |  |
| Negative control is identified or run |  |  |
| Package hashes can reproduce the artifact set |  |  |

## Domain-Specific Stop Signs

- No null or non-event evidence can be identified.
- Coordinate units or reference systems are unclear.
- Evidence is concentrated in one source family.
- The suspected pattern depends on a post-hoc tolerance.
- The team wants a full assurance claim from this preflight.

## Escalation Note

Escalate only if the preflight package can be imported into `CRAMPS-AST` with review disposition.
