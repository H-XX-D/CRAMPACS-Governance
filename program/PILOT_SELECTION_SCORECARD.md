# CRAMPS Pilot Selection Scorecard

**Document ID:** CRAMPS-PILOT-SCORE-001
**Status:** Draft selection tool
**Applies to:** first-pilot and next-pilot selection

## 1. Purpose

Use this scorecard before starting a CRAMPS pilot.

The goal is not to pick the most exciting question. The goal is to pick a question that can teach the method, expose failure modes, and finish without overclaiming.

## 2. Scoring Rule

Score each criterion:

- `0`: not present or unknown
- `1`: weak
- `2`: adequate
- `3`: strong

Recommended decision:

| Total | Decision |
|---:|---|
| 0-14 | reject as first pilot |
| 15-23 | hold for scoping |
| 24-30 | select for preflight |
| 31-36 | strong pilot candidate |

Any red-flag stop condition overrides the score.

## 3. Scorecard

| Criterion | 0 | 1 | 2 | 3 | Score |
|---|---|---|---|---|---:|
| Decision boundary | no decision stated | vague interest | internal decision stated | decision and prohibited use stated | |
| Coordinate clarity | no coordinate | broad family only | candidate value or range exists | coordinate, units, and tolerance sketch exist | |
| Source boundary | unknown universe | broad literature/log space | bounded source class | bounded source list or search route | |
| Null/non-event access | none known | plausible but not identified | at least one source class | multiple null/non-event routes | |
| Dependence map feasibility | unknowable | likely but hard | likely and partly mappable | source families are clear | |
| Bias map feasibility | ignored | generic bias only | domain bias named | bias and missing-evidence routes named | |
| Data rights and sensitivity | unclear/restricted | likely sensitive | manageable with controls | public or clearly authorized | |
| Team availability | no owner | owner only | owner plus reviewer | owner, reviewer, and role coverage | |
| Time box | indefinite | more than 8 weeks | 1 to 4 week full pilot | 1 to 2 day preflight plus 1 to 4 week pilot | |
| Claim discipline | wants proof | wants strong external claim | accepts prioritization | accepts explicit non-confirmatory claim boundary | |
| Reproducibility feasibility | cannot rerun | manual only | partial rerun possible | clean-run path is feasible | |
| Training value | narrow clerical task | limited learning | teaches several controls | teaches coordinate, nulls, dependence, bias, and release boundary | |

## 4. Red-Flag Stop Conditions

Reject as a first pilot if any are true:

- the sponsor wants a discovery, compliance, safety, clinical, legal, fraud, exploitability, or causality claim from the pilot
- no null or non-event evidence can be searched
- source access is illegal, unauthorized, or unclear
- private or restricted data would be exposed without controls
- the coordinate cannot be stated in one sentence
- the package must be externally released before gates can run
- the team will not accept a hold, demotion, or stop decision

## 5. Pilot Selection Decision

Choose one:

- `select_for_preflight`
- `hold_for_scoping`
- `reject_as_first_pilot`
- `defer_until_controls_exist`

Record:

| Field | Entry |
|---|---|
| Candidate pilot name | |
| Domain suffix | |
| Proposed full system | |
| Total score | |
| Red flags present | |
| Decision | |
| Decision owner | |
| Reviewer | |
| Date | |
| Conditions before start | |

## 6. Conditions To Clear Before Preflight

Typical conditions:

- define coordinate in canonical units
- identify at least one null/non-event source route
- confirm data rights and sensitivity classification
- name decision owner and reviewer
- state prohibited claims
- choose package location
- schedule preflight decision review

## 7. Conditions To Clear Before Full Pilot

Typical conditions:

- preflight gate path clears
- leak scan has no open critical findings
- preflight decision recommends escalation
- full-system roles are assigned
- protocol steward is named
- preflight import disposition is ready
- source rights and retention policy are clear
- sponsor accepts that the pilot may hold, demote, or stop
