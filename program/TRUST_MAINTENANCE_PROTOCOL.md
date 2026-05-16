# Trust Maintenance Protocol

**Document ID:** CRAMPACS-TRUST-001  
**Version:** 0.1  
**Status:** Draft procedure  
**Owner:** CRAMPACS program owner  
**Applies to:** `crampacs-*` preflight and `CRAMPACS-*` full assurance packages

## 1. Purpose

CRAMPACS is fragile if trust is added only at the end.

This protocol keeps trust visible while the package is being built. It requires teams to record what changed, what was checked, what remains uncertain, what was promoted, what was blocked, and what must not be relied on yet.

## 2. Trust Principle

Trust is not a mood. It is a maintained state backed by records.

Every important package element must have one of these states:

| State | Meaning | Reliance rule |
|---|---|---|
| `draft` | work has started but is not checked | do not rely |
| `unchecked` | artifact exists but no reviewer has accepted it | do not rely |
| `checked_with_limits` | reviewed, but known limits remain | rely only within stated limits |
| `accepted` | reviewed and accepted for current gate | rely within current evidence tier |
| `blocked` | has a defect that prevents promotion or release | do not promote |
| `superseded` | replaced by a newer artifact | retain but do not use |
| `quarantined` | retained for traceability but excluded from scoring or release | do not use as evidence |

## 3. Working Truth vs Release Truth

CRAMPACS separates working truth from release truth.

Working truth:

- provisional
- can contain assumptions
- can be incomplete
- must be visibly labeled
- can guide internal work

Release truth:

- gate-reviewed
- evidence-backed
- traceable to source records
- aligned with an evidence tier
- approved by release authority

No working artifact may be treated as release truth without a checkpoint review.

## 4. Trust Checkpoints

Run a trust checkpoint at:

| Point | Trigger | Record |
|---|---|---|
| Start | package created or preflight started | build ledger entry |
| Before coordinate lock | candidate coordinate proposed | checkpoint review |
| After source search | source universe drafted | checkpoint review |
| After extraction | raw rows created | checkpoint review |
| After normalization | canonical rows created | checkpoint review |
| After dependence and bias review | evidence-family and bias tables drafted | checkpoint review |
| Before statistics | statistic and null model selected | checkpoint review |
| After results | primary and sensitivity outputs generated | checkpoint review |
| Before release | decision memo drafted | checkpoint review and trust status summary |
| After any material change | artifact, protocol, data, code, or claim changes | build ledger and possible CAPA |

## 5. Required Trust Records

For full `CRAMPACS-*` packages, create binder `10_trust_maintenance/` with:

- `build_ledger.csv`
- `checkpoint_reviews.csv`
- `assumption_uncertainty_log.csv`
- `claim_trace_matrix.csv`
- `trust_debt_register.csv`
- `trust_status_summary.md`
- `open_questions.md`

For `crampacs-*` preflights, use lightweight versions:

- preflight decision notes
- sidecar output
- gotcha checklist
- explicit hold/stop/escalate rationale

## 6. Build Ledger Rule

Every material action must be logged:

- artifact created
- artifact changed
- evidence imported
- coordinate adjusted
- source excluded
- row quarantined
- analysis rerun
- claim changed
- sidecar run
- checkpoint review
- release decision

If it would matter to a skeptical reviewer later, log it now.

## 7. Assumption and Uncertainty Rule

Assumptions must not be buried in prose.

Record each assumption with:

- owner
- evidence basis
- impact if wrong
- verification path
- current status
- decision impact

Open assumptions that could change the result are release blockers unless explicitly accepted by the release authority as residual risk.

## 8. Claim Trace Rule

Every claim must trace to:

- evidence artifact
- control evidence record
- gate decision
- evidence tier
- prohibited overclaim
- reviewer

A claim with no trace is not a CRAMPACS claim.

## 9. Promotion Rule

Promotion means moving an artifact or claim to a higher trust state.

Promotion requires:

- artifact ID
- previous state
- new state
- reviewer
- evidence reviewed
- limits
- date

No artifact may move from `draft` or `unchecked` directly to release use without review.

## 10. Honesty Language

Use these phrases while building:

- "This is a working assumption."
- "This has not passed checkpoint review."
- "This is accepted only for G2 source-universe work."
- "This row is quarantined pending source trace."
- "This result is local and not release language."
- "This sidecar blocker means the package is not ready."
- "This claim is prohibited until domain confirmation."

Avoid:

- "basically proven"
- "good enough"
- "probably fine"
- "the sidecar passed so it is true"
- "we can clean it up later"

## 11. Trust Debt

Trust debt is any known gap that has not been closed:

- missing source trace
- unresolved unit ambiguity
- dependence uncertainty
- missing nulls
- unchecked extraction
- unreviewed AI output
- unclosed CAPA
- missing checkpoint review
- claim language not approved

Trust debt must have an owner, due date, and release impact.

## 12. Stop Conditions

Stop or hold if:

- the team cannot distinguish working truth from release truth
- a major artifact changed without a build ledger entry
- coordinate movement is not recorded
- sidecar blockers are ignored
- assumptions are used as facts
- claims appear without trace
- reviewers are asked to approve a package with unknown trust state
