# cramps-phy Preflight Scope

**Preflight ID:** EX-PHY-001
**Domain suffix:** `phy`
**Date:** 2026-05-16 PDT
**Decision owner:** training reviewer
**Target full system if escalated:** `CRAMPS-PHY`
**Synthetic status:** teaching data only

## Question

Does a bounded synthetic source set in the physics anomaly-catalog style show enough coordinate-specific recurrence near `42 GeV/c^2`, including null and non-event checks, to justify opening a full `CRAMPS-PHY` package?

## Coordinate Sketch

| coordinate_id | coordinate_family | value_or_range | units | tolerance_sketch | why_it_matters |
|---|---|---:|---|---|---|
| PHY-MASS-042 | mass | 42 | GeV/c^2 | plus or minus 2 GeV/c^2, preflight only | Demonstrates how weak observations and nulls map to one locked coordinate. |

## Inclusion Boundary

Included:

- synthetic source records created for this worked example
- records with a measurable mass coordinate
- positive-like rows, null rows, exclusions, and non-events near the candidate range

Excluded:

- real experimental claims
- external PDFs, plots, or private files
- theory-only rows without an observed or searched coordinate
- rows whose coordinate cannot be stated in canonical units

## Intended Decision

Choose one:

- advance_to_CRAMPS-PHY
- hold_coordinate_lock
- hold_source_completeness
- hold_dependence_or_bias
- stop

This worked example chooses `advance_to_CRAMPS-PHY` as a teaching disposition only. A real package would require protocol lock and full source accounting before any formal analysis.

## Claim Boundary

This is a lowercase `cramps-phy` preflight. It is not a confirmatory `CRAMPS-PHY` result.
