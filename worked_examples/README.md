# CRAMPS Worked Examples

These examples are sanitized teaching artifacts. They are not evidence and do not support any domain claim.

Use them to see how a small `cramps-*` preflight is supposed to look before a team opens a full `CRAMPS-*` package.

## Included Example

- `preflight/cramps-phy-synthetic-coordinate-recurrence/`
  A one-agent lowercase preflight for a synthetic physics-style coordinate recurrence question.

Start with `REVIEWER_WALKTHROUGH.md` inside the example if you are auditing or teaching it.

## Rules

- Worked examples stay separate from `templates/` so the reusable source kit remains clean.
- Copy a worked example to `/tmp`, `cramps_projects/`, or another external package directory before running mutating CLI commands such as `check`, `gate`, `acceptance-audit`, `review-packet`, or `release-check package`.
- Preflight examples use one named operator only.
- Full-system agent deployment begins only after the preflight decision recommends escalation and a separate uppercase package is created.
- Synthetic examples must never be copied into a real evidence package without changing IDs, dates, sources, and claim boundaries.
