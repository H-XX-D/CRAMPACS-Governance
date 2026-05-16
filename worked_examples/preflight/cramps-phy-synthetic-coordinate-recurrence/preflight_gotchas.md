# cramps-phy Preflight Failure Modes and Fast Checks

**Preflight ID:** EX-PHY-001
**Date:** 2026-05-16 PDT
**Operator:** single_preflight_operator

## Ten Fast Questions

| Check | Status | Notes |
|---|---|---|
| Coordinate can be stated precisely | pass | `mass = 42 GeV/c^2`, preflight tolerance plus or minus 2 GeV/c^2. |
| Coordinates were chosen before scoring | pass | Candidate is stated in `preflight_scope.md` before row review. |
| Nulls and non-events are present | pass | Three of five rows are null, exclusion, non-event, or failed replication. |
| Rows are plausibly independent | hold | SRC-SYN-002 and SRC-SYN-004 may share a background model. |
| Units and transforms are controlled | pass | All rows use `GeV/c^2`; no conversion performed. |
| Tolerance window is justified | hold | Tolerance is acceptable for preflight but needs full protocol justification. |
| Publication/reporting bias considered | hold | Two rows carry explicit bias concern. |
| No single source family drives result | pass | Five synthetic source units, with one pair needing dependence review. |
| Negative control identified or run | hold | Negative control is identified for full package, not run in preflight. |
| Package can be reproduced from hashes | hold | Preflight artifacts are present; full checksum reproduction is not performed. |

## Biggest Failure Mode

The strongest failure mode is dependence between the synthetic positive-like row `ROW-SYN-002` and the synthetic non-event row `ROW-SYN-004`, because both use `synthetic_detector_b`.

## What Would Change the Assessment

The decision would weaken if a full dependence review showed that most rows inherit the same simulated background model. The decision would strengthen if a locked full protocol found independent null coverage and a negative control behaved normally.
