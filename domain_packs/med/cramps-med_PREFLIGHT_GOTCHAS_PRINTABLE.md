# cramps-med Gotchas Printable

**Domain:** Medicine and clinical evidence

## Top Domain Gotcha

confounding by indication, differential coding, missing nulls, surveillance bias

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

Escalate only if the preflight package can be imported into `CRAMPS-MED` with review disposition.
