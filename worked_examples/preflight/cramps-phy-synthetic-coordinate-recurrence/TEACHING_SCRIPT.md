# Teaching Script

**Audience:** new CRAMPS operators, reviewers, and supervisors  
**Duration:** 30 to 45 minutes  
**Artifact:** `cramps-phy` synthetic coordinate recurrence worked example

## Teaching Objective

By the end of this exercise, a learner should be able to explain:

- why lowercase `cramps-phy` is not uppercase `CRAMPS-PHY`
- why a preflight can recommend escalation without making a domain claim
- why nulls, exclusions, non-events, and failed replications are required
- how dependence and bias can create a hold without stopping all escalation
- why contract audit sits between gate accounting and acceptance
- why worked examples must be copied before mutating CLI checks

## Instructor Setup

From the repository root:

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
```

Keep the source example open for reading and the `/tmp` copy for CLI checks.

## Exercise Flow

### 1. Boundary

Ask the learner to identify the assurance level.

Expected answer:

- lowercase `cramps-phy`
- synthetic teaching example
- one preflight operator
- no full-system claim

Stop if the learner treats the rows as real evidence.

### 2. Coordinate

Open `preflight_scope.md`.

Ask:

- What coordinate is being inspected?
- Is the tolerance final?
- What would have to happen before full scoring?

Expected answer:

- mass near `42 GeV/c^2`
- tolerance is preflight-only
- full protocol lock and independent source search are required

### 3. Source And Row Balance

Open `preflight_sources.csv` and `preflight_rows.csv`.

Ask the learner to count:

- positive-like rows
- null, exclusion, non-event, or failed-replication rows
- source units
- dependence flags

Expected answer:

- two positive-like rows
- three null/non-event-style rows
- five source records
- one source-family dependence concern involving `synthetic_detector_b`

### 4. Failure Modes

Open `preflight_gotchas.md`.

Ask:

- Which holds remain?
- Why does a hold not automatically mean stop?

Expected answer:

- dependence, tolerance justification, publication/reporting bias, negative control, and full checksum reproduction remain open
- preflight can recommend escalation when the next step is designed to resolve the holds

### 5. Contract Audit

Run:

```bash
python tools/cramps_cli.py contract-audit package /tmp/cramps-phy-worked-example --level preflight
```

Ask:

- Which tables are checked?
- What cross-reference is checked?

Expected answer:

- source, row, manifest, and agent-control CSV headers
- row `source_id` values must resolve to the source table

### 6. Release Check

Run:

```bash
python tools/cramps_cli.py release-check package /tmp/cramps-phy-worked-example --level preflight --force
```

Ask:

- What does `package_release_ready` mean here?
- What does it not mean?

Expected answer:

- the isolated teaching package clears lowercase preflight checks
- it does not prove a physical signal or permit a `CRAMPS-PHY` claim

## Debrief

The desired learner conclusion is:

> CRAMPS is valuable because it preserves weak-signal context, null evidence, dependence, bias, and claim limits before a team spends money on a full study.

The desired reviewer conclusion is:

> This example is structurally adequate as a teaching preflight. Its synthetic rows must be quarantined from any real full-system scoring.

