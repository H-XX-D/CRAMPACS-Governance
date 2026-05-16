# cramps-phy Preflight Decision

**Preflight ID:** EX-PHY-001
**Date:** 2026-05-16 PDT
**Decision owner:** training reviewer
**Operator:** single_preflight_operator

## Decision

`advance_to_CRAMPS-PHY`

## Rationale

The synthetic preflight has a precise coordinate, a bounded source set, complete coordinate/unit fields, and both positive-like and null/non-event rows. The package is strong enough to demonstrate escalation mechanics, but not strong enough to support any domain claim.

## Strongest Evidence

`ROW-SYN-001` and `ROW-SYN-002` are positive-like rows near the pre-specified coordinate. They are useful for teaching recurrence inspection, not for claiming physical evidence.

## Strongest Null or Non-Event

`ROW-SYN-003` is a synthetic exclusion row covering the candidate coordinate. `ROW-SYN-004` and `ROW-SYN-005` add a non-event and failed replication.

## Biggest Failure Mode

Dependence and source-process bias must be reviewed before any full-system scoring. SRC-SYN-002 and SRC-SYN-004 share a source-unit family.

## What Would Change the Decision

Escalation would stop if the full-system source search found no independent null coverage, if the coordinate tolerance had to be widened after scoring, or if a negative control showed similar recurrence.

## Recommended Next Step

Create a separate uppercase `CRAMPS-PHY` package. Import this preflight as seed material only, record import disposition, lock a full protocol, assign full-system roles, and re-extract rows under the full data contracts.

## Claim Boundary

This is a lowercase `cramps-phy` preflight. It is not a confirmatory `CRAMPS-PHY` result.
