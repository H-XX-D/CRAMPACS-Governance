# CRAMPS Deployment Playbook

**Document ID:** CRAMPS-DPLY-001

## 1. Deployment Modes

| Mode | Use when | Typical duration | Output |
|---|---|---:|---|
| `cramps-*` preflight | Team needs fast triage | 1-2 days | proceed, hold, stop |
| CRAMPS pilot | Narrow question, limited sources | 1-4 weeks | limited evidence package |
| CRAMPS standard | Serious internal decision or publication support | 1-3 months | full evidence package |
| CRAMPS regulated | Safety/security/regulated operating environment | project-specific | audit-ready decision package |

## 2. Preflight Deployment

Day 1:

1. Appoint decision owner and reviewer.
2. State the coordinate in one sentence.
3. Collect a bounded source set, including nulls.
4. Fill preflight rows.
5. Run gotcha checklist.

Day 2:

1. Run sidecar.
2. Review dependence and bias.
3. Write decision memo.
4. Decide: advance, hold, stop, or re-scope.

Preflight stop conditions:

- no nulls
- no stable coordinate
- one-source collapse
- severe unit ambiguity
- team wants a full assurance claim

## 3. Full Deployment

Phase 1, charter and lock:

- assign roles
- define assurance level
- lock protocol
- lock candidate registry

Phase 2, evidence:

- run source search
- extract rows
- normalize coordinates
- log exclusions

Phase 3, review:

- grade independence
- assess bias
- review missing evidence
- approve weights

Phase 4, analysis:

- run null model
- run sensitivity tests
- run negative controls
- report local and global results

Phase 5, assurance:

- build assurance case
- run clean reproduction
- red-team package
- close findings
- issue decision memo

## 4. Regulated Deployment Additions

Use `REGULATED_DEPLOYMENT_ADDENDUM.md` before CRAMPS supports a safety, security, regulated research, public agency, financial, clinical, or operational decision.

Add:

- data classification
- privacy/security review
- legal or compliance review
- domain-specific standards mapping
- training records
- change-control board
- CAPA process
- retention policy
- external audit readiness review

## 5. Team Minimums

Preflight:

- decision owner
- domain reviewer
- analyst

Full standard:

- program owner
- domain lead
- statistical lead
- independence auditor
- bias auditor
- data steward
- reproducibility lead
- red-team reviewer

Regulated:

- all full-standard roles
- safety/compliance authority
- privacy/security officer where applicable
- records owner
