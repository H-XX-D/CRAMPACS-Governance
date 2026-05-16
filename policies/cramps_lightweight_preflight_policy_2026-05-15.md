# cramps Lightweight Preflight Policy

**Policy ID:** cramps-LITE-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft lightweight preflight policy

## 1. Purpose

`cramps-*` is the lightweight one to two day version of CRAMPS.

It helps teams decide whether a suspected weak-signal recurrence deserves full `CRAMPS-*` treatment.

It is designed for limited time and budget. It is not designed to produce confirmatory claims.

## 2. Core Question

A preflight answers:

> Is this suspected coordinate recurrence specific, sourced, independent enough, and null-aware enough to justify a full CRAMPS study?

It does not answer:

> Is the coordinate recurrence real?

## 3. Minimum Inputs

A `cramps-*` preflight requires:

- Domain suffix.
- One-page scope.
- Candidate coordinate or coordinate family.
- Reason the coordinate matters.
- Bounded source list.
- At least one plausible null or non-event source.
- Initial dependence notes.
- Initial bias notes.
- Unit and transform assumptions.
- Decision owner.

## 4. One to Two Day Workflow

### Hour 0-2: Scope Lock

Write:

- Domain.
- Question.
- Candidate coordinates.
- Coordinate units.
- Inclusion boundary.
- Exclusion boundary.
- Intended decision.

Output:

- `preflight_scope.md`

### Hour 2-6: Source Sweep

Collect a bounded source set.

Minimum:

- 5 positive or anomaly-like sources where available.
- 3 null, negative, exclusion, or non-event sources where available.
- 1 review or standards source where useful.

Output:

- `preflight_sources.csv`

### Hour 6-10: Row Sketch

Extract only the fields needed for triage:

- source ID
- coordinate
- units
- row type
- result direction
- uncertainty status
- extraction confidence
- dependence concern
- bias concern

Output:

- `preflight_rows.csv`

### Hour 10-14: Gotcha Scan

Run the gotcha checklist:

- coordinate drift
- missing nulls
- duplicate evidence
- unit mismatch
- time leakage
- source overconcentration
- tolerance flexibility
- AI extraction risk
- overclaiming risk

Output:

- `preflight_gotchas.md`

### Hour 14-18: Sidecar Metrics

Run the sidecar package checker.

Output:

- `cramps_sidecar_metrics.json`
- `cramps_sidecar_metrics.md`

### Hour 18-24: Decision

Write one of five decisions:

- `advance_to_CRAMPS`
- `hold_coordinate_lock`
- `hold_source_completeness`
- `hold_dependence_or_bias`
- `stop`

Output:

- `preflight_decision.md`

## 5. Required Preflight Decision Fields

`preflight_decision.md` must contain:

- Decision.
- Rationale.
- Strongest evidence.
- Strongest null or non-event.
- Biggest gotcha.
- What would change the decision.
- Recommended next step.
- Explicit claim boundary.

Required claim boundary:

> This is a lowercase cramps-* preflight. It is not a confirmatory CRAMPS-* result.

## 6. Preflight Stop Signs

Stop or hold if:

- Candidate coordinate cannot be stated in one sentence.
- Coordinate units are unclear.
- No null or non-event source can be found.
- Evidence comes from one source family.
- Tolerance window is chosen after seeing the rows.
- Most rows share the same dataset, vendor, instrument, or pipeline.
- The result depends on one extracted plot point.
- The result would change if one source is removed.
- The team wants to make a public significance claim.

## 7. Composable Upgrade Rule

Preflight findings can justify a full CRAMPS study and should be structured so they can seed that study.

The preflight package is not discarded. It becomes the first import bundle.

Composable preflight artifacts:

- `preflight_scope.md`
- `preflight_sources.csv`
- `preflight_rows.csv`
- `preflight_gotchas.md`
- `cramps_sidecar_metrics.json`
- `cramps_sidecar_metrics.md`
- `preflight_decision.md`
- `preflight_manifest.csv`

Each imported artifact must receive review disposition in the full system:

- `accepted_for_protocol`
- `accepted_for_background`
- `needs_rework`
- `rejected`
- `quarantined`

To upgrade:

1. Start a new uppercase `CRAMPS-*` workspace.
2. Lock a full protocol.
3. Import the preflight package as seed material.
4. Review every preflight artifact and record disposition.
5. Re-extract or approve preflight rows under full data contracts.
6. Add full null/non-event coverage.
7. Grade independence formally.
8. Run a registered null model.
9. Reproduce from a checksum package.

The full system may reuse preflight work, but the full-system claim begins only after the full protocol lock.

## 8. Output Template

Recommended final paragraph:

> This cramps preflight found that the suspected recurrence is [specific / under-specified], has [adequate / inadequate] null coverage, shows [low / moderate / high] dependence risk, and has [low / moderate / high] bias risk. Recommendation: [decision]. No confirmatory claim is made.
