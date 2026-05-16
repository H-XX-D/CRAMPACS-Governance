# CRAMPS First Pilot Runbook

**Document ID:** CRAMPS-PILOT-RUNBOOK-001
**Status:** Draft operating runbook
**Applies to:** first organizational `cramps-*` preflight and first `CRAMPS-*` pilot

## 1. Purpose

This runbook is the short path from "we want to try CRAMPS" to a bounded first pilot.

It is designed for a team that has read the program documents but needs a concrete operating sequence. It does not replace the SOP, the deployment playbook, or the release checklist.

## 2. Pilot Principle

The first pilot should prove the process, not the domain.

Choose a pilot that is:

- narrow enough to finish
- important enough to reveal useful failure modes
- low enough risk that a hold or stop is acceptable
- rich enough to include nulls, non-events, dependence, and bias
- bounded enough that source accounting can be inspected

Do not choose the team's most politically important, legally sensitive, public, or safety-critical decision as the first pilot.

## 3. What A Good First Pilot Looks Like

| Dimension | Good first pilot | Bad first pilot |
|---|---|---|
| Coordinate | one coordinate family, 3 to 5 candidate values | broad open-ended search |
| Source set | bounded and inspectable | undefined literature or log universe |
| Nulls | known places to look for nulls and non-events | only positive or interesting cases |
| Dependence | likely but mappable | unknown shared source process everywhere |
| Risk | useful internal prioritization | immediate public, legal, clinical, safety, or financial action |
| Time | 1 to 2 day preflight, 1 to 4 week pilot | indefinite research program |
| Claim | prioritization or method demonstration | discovery, compliance, or causality |

## 4. Required Roles

Minimum preflight roles:

- decision owner
- domain reviewer
- preflight operator

Minimum full-pilot roles:

- program owner
- protocol steward
- domain lead
- statistical lead
- independence auditor
- bias auditor
- data steward
- reproducibility lead
- red-team reviewer

In a pilot, one person may hold multiple roles. Before external release or regulated use, role separation must follow the operating manual.

## 5. Pilot Intake

Before kickoff, fill this intake:

| Question | Required answer |
|---|---|
| What decision could this pilot affect? | |
| What decision is explicitly out of scope? | |
| What coordinate family is being inspected? | |
| What candidate values or ranges are known before scoring? | |
| What source universe is feasible to inspect? | |
| Where will nulls, non-events, exclusions, or failed replications come from? | |
| What source families may be dependent? | |
| What bias could create apparent recurrence? | |
| What data is private, restricted, regulated, or source-contaminating? | |
| Who can place a release hold? | |

If the team cannot answer the coordinate, source universe, null evidence, and decision-boundary questions, do not start a full pilot. Start with a `cramps-*` preflight only.

## 6. Pilot Sequence

### Step 0: Select Candidate Pilot

Use `PILOT_SELECTION_SCORECARD.md`.

Decision:

- `select_for_preflight`
- `hold_for_scoping`
- `reject_as_first_pilot`

### Step 1: Create Lowercase Preflight

Run:

```bash
python tools/cramps_cli.py init --level preflight --domain <domain> --study-id <study_id>
```

Fill:

- `preflight_scope.md`
- `preflight_sources.csv`
- `preflight_rows.csv`
- `preflight_gotchas.md`
- `preflight_decision.md`

Run:

```bash
python tools/cramps_cli.py check <package> --level preflight
python tools/cramps_cli.py agent-audit <package> --level preflight
python tools/cramps_cli.py leak-scan <package>
python tools/cramps_cli.py gate <package> --level preflight
python tools/cramps_cli.py acceptance-audit <package> --level preflight
```

Run `check`, then `agent-audit`, then `leak-scan`, then `gate`, then `acceptance-audit` in that order. The acceptance audit depends on the latest sidecar, agent-control, leak-scan, and gate status.

Preflight output must be one of:

- advance to full `CRAMPS-*`
- hold coordinate lock
- hold source completeness
- hold dependence or bias
- stop

### Step 2: Escalation Review

Escalate only if:

- preflight gate path clears
- leak scan has no open critical finding
- null or non-event evidence exists
- dependence and bias concerns are visible
- the decision owner accepts the claim boundary

Do not escalate if the team wants the preflight to serve as a final answer.

### Step 3: Create Full Pilot Package

Run:

```bash
python tools/cramps_cli.py promote <preflight_package> --study-id <full_study_id>
```

Then:

- review preflight import disposition
- quarantine synthetic, weak, or unapproved preflight rows
- lock the full protocol
- assign full-system roles
- re-extract or approve rows under full data contracts

### Step 4: Run Full Pilot Gates

Work through:

- G0/F1 charter
- F2 protocol lock
- F3 source and raw signal rows
- F4 coordinate normalization
- F5 dependence and bias
- F6 statistics
- F7 reproducibility
- F8 trust and release

Run after material work:

```bash
python tools/cramps_cli.py check <full_package> --level full
python tools/cramps_cli.py agent-audit <full_package> --level full
python tools/cramps_cli.py leak-scan <full_package>
python tools/cramps_cli.py gate <full_package> --level full
python tools/cramps_cli.py acceptance-audit <full_package> --level full
```

Run these commands sequentially. Do not evaluate acceptance from stale or missing sidecar, agent-audit, leak-scan, or gate output.

### Step 5: Closeout

The first pilot must close with one of:

- release as limited internal prioritization
- demote to exploratory
- hold for rework
- reject
- stop and open CAPA

Every closeout must include:

- decision memo
- trust status summary
- failure-mode review
- lessons learned
- template or training changes
- next-pilot recommendation or stop rationale

## 7. Meeting Cadence

| Meeting | Timing | Required output |
|---|---|---|
| Pilot selection review | before preflight | scorecard decision |
| Preflight kickoff | hour 0 | scope and operator assignment |
| Preflight decision review | after sidecar/gate/leak scan | advance, hold, stop, or re-scope |
| Full protocol lock review | before scoring | locked protocol and candidate registry |
| Dependence/bias review | before statistics | weights, holds, or demotion |
| Statistical review | before report drafting | null model, global correction, sensitivities |
| Release review | before any use | evidence tier, decision memo, claim language |
| Retrospective | after closeout | lessons, CAPA, next action |

## 8. Sponsor Language

Use:

> This first pilot tests whether CRAMPS can produce a controlled evidence package for a bounded recurrence question.

Do not use:

> This first pilot will prove whether the underlying domain claim is true.

## 9. Immediate Stop Rules

Stop or hold if:

- the coordinate changes after rows are seen
- nulls cannot be found or searched
- source rights, privacy, or security are unclear
- one source family drives the case
- the team asks for a public or regulated claim from a preflight
- the leak scan reports an open critical finding
- the package cannot state what it is trustworthy for and not trustworthy for

## 10. First Pilot Definition Of Done

A first pilot is done when:

- the package reaches release review, is demoted, or is stopped for documented reasons
- all Critical findings are closed or the package is stopped
- trust debt is recorded
- lessons learned are written
- sponsor decision is documented
- no unsupported domain claim is made
