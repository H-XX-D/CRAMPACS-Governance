# Reviewer Walkthrough

**Example:** `cramps-phy` synthetic coordinate recurrence
**Purpose:** teach how to review a completed lowercase preflight
**Reviewer posture:** skeptical, bounded, non-confirmatory

## 1. Start With The Boundary

Confirm:

- this is lowercase `cramps-phy`
- the data are synthetic
- the target full system is `CRAMPS-PHY`
- only one preflight operator is assigned
- no full-system claim is made

Immediate stop if any reader treats this as real evidence.

## 2. Read The Scope

Open `preflight_scope.md`.

Pass:

- coordinate is stated as `42 GeV/c^2`
- tolerance is visible and labeled preflight only
- inclusion and exclusion boundaries are explicit
- claim boundary says this is not confirmatory

Hold:

- tolerance is not yet a full protocol tolerance
- real source universe has not been searched

## 3. Review Sources

Open `preflight_sources.csv`.

Pass:

- five synthetic sources exist
- positive-like and null/non-event source roles are both present
- source unit diversity exists

Hold:

- `SRC-SYN-002` and `SRC-SYN-004` share a synthetic detector family
- real source search would need replacement, not reuse

## 4. Review Rows

Open `preflight_rows.csv`.

Pass:

- five rows exist
- all rows have coordinate values
- all rows use `GeV/c^2`
- three rows are null, exclusion, non-event, or failed replication

Hold:

- dependence and bias concerns are visible
- synthetic rows must be quarantined from any full-system scoring

## 5. Review Failure Modes

Open `preflight_gotchas.md`.

Pass:

- nulls and non-events are acknowledged
- dependence and tolerance holds are not hidden
- negative control is identified as a full-system need

Hold:

- independence is not fully resolved
- full checksum reproduction is not performed at preflight level

## 6. Review Decision

Open `preflight_decision.md`.

Acceptable decision:

- `advance_to_CRAMPS-PHY` as a teaching disposition only

Required interpretation:

- the preflight may seed a full package
- the preflight does not clear a full package
- full-system rows must be re-extracted or formally quarantined

## 7. Review Agent Boundary

Open `agent_registry.csv` and `FULL_SYSTEM_HANDOFF.md`.

Pass:

- one preflight operator is assigned
- extra agents are prohibited during preflight
- full-system roles begin only after uppercase package creation, import disposition, protocol lock, and role approval

## 8. Run Checks

Run from the repository root:

```bash
python tools/cramps_cli.py check worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
python tools/cramps_cli.py leak-scan worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence
python tools/cramps_cli.py gate worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
```

Expected:

- readiness score: `100.0`
- recommendation: `candidate_for_CRAMPS_upgrade`
- leak findings: `0`
- highest cleared gate priority: `50`
- all clear: `true`

## 9. Reviewer Decision

The correct reviewer decision is:

> Accept this as a worked preflight example. It is structurally ready to teach escalation mechanics. It is not evidence and must not be used for scoring.

## 10. Teaching Points

Use this example to teach:

- how a coordinate is made explicit
- why nulls and non-events matter
- how dependence concerns can coexist with escalation
- how a preflight can advance without becoming a full claim
- where one-agent preflight work stops
- where full-system agent deployment begins
