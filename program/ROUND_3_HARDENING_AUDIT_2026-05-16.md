# Round 3 Hardening Audit

**Document ID:** CRAMPS-R3-AUDIT-2026-05-16
**Status:** Completed source-kit hardening note
**Scope:** post-build operational readiness

## 1. Purpose

This round checks whether CRAMPS is usable as an operating system, not merely a set of documents.

The audit asks:

- Can a practitioner find the acceptance checks?
- Can a reviewer walk through a worked example?
- Can an AI operator run checks without contaminating the reusable source kit?
- Does the repo state what the method is trustworthy for and not trustworthy for?

## 2. Findings Closed

| Finding | Risk | Closure |
|---|---|---|
| No completed worked example | Practitioners had templates but no model of a filled preflight | Added `worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence/` |
| Worked example lacked reviewer path | Teams could run files without knowing what to look for | Added reviewer walkthrough and expected output |
| Acceptance criteria were spread across documents | Supervisors had to infer release readiness | Added `RELEASE_ACCEPTANCE_CHECKLIST.md` |
| Preflight agent boundary needed explicit teaching artifact | AI operators could over-deploy during preflight | Worked example now states one-agent preflight rule and full-system handoff point |
| Generated runtime outputs could stale in examples | Timestamped check output could look authoritative after drift | Worked example stores expected-output guidance, not committed runtime output |

## 3. Verification Performed

The worked example was verified on a temporary copy so the source example stayed clean.

Checks:

- `python tools/cramps_cli.py check /tmp/cramps-worked-example-check --level preflight`
- `python tools/cramps_cli.py leak-scan /tmp/cramps-worked-example-check`
- `python tools/cramps_cli.py gate /tmp/cramps-worked-example-check --level preflight`
- `git diff --check`

Expected posture:

- preflight readiness is `100.0`
- recommendation is `candidate_for_CRAMPS_upgrade`
- no blockers
- no open leak findings
- preflight gate path clears through priority `50`

## 4. Remaining Boundaries

This round does not claim:

- external validation
- domain confirmation
- regulatory compliance
- field acceptance
- statistical proof that CRAMPS finds true recurrence in real data

Those require validation batteries, independent pilots, and domain review under the full program controls.

## 5. Round 3 Acceptance

Round 3 is acceptable when:

- the release checklist is present
- the worked example is present
- the worked example has a reviewer walkthrough
- the worked example states synthetic-data boundaries
- the worked example states the one-agent preflight rule
- verification commands pass on a temporary copy
