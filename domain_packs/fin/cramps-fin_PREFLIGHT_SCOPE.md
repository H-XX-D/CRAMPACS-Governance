# cramps-fin Preflight Scope

**Domain:** Finance, fraud, and risk  
**Target full system if escalated:** CRAMPS-FIN  
**Date:**  
**Decision owner:**  

## One-Sentence Question

Does a bounded source set in the finance, fraud, and risk domain show enough coordinate-specific recurrence, including null and non-event checks, to justify opening a full CRAMPS-FIN package?

## Candidate Coordinate Sketch

Domain coordinate examples: asset, tenor, counterparty, time window, transaction velocity, network position, model threshold

| coordinate_id | coordinate_family | value_or_range | units | tolerance_sketch | why_it_matters |
|---|---|---|---|---|---|

## Source Boundary

Included source types:

-

Excluded source types:

-

## Minimum Null or Non-Event Search

Look for: cleared alerts, comparable accounts without event, backtests with no breach, control portfolios

## Preflight Claim Boundary

This is `cramps-fin`. It can produce a triage decision only. It is not a `CRAMPS-FIN` confirmatory result.
