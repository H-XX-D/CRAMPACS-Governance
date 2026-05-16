# CRAMPS Release Acceptance Checklist

**Document ID:** CRAMPS-REL-CHECK-001
**Status:** Draft operating checklist
**Applies to:** `cramps-*` preflights, `CRAMPS-*` full packages, worked examples, and source-kit releases

## 1. Purpose

This checklist defines the minimum acceptance checks before a CRAMPS artifact is treated as usable.

It is not a substitute for the SOP. It is the short inspection surface a supervisor, reviewer, or AI operator can run before trusting that the package is in the correct state.

## 2. Source-Kit Release Acceptance

Use before pushing a CRAMPS source-kit update.

| Check | Pass condition | Evidence |
|---|---|---|
| Worktree state | no unintended modified or untracked files | `git status --short` |
| Naming boundary | no stale legacy project-name or old expansion strings | repository text scan |
| Generated artifacts | domain packs, printouts, and workbooks regenerated when generators change | generator run log or commit diff |
| Python tools | CLI and sidecar compile | `python -m py_compile ...` |
| CLI health | source kit reports no doctor issues | `python tools/cramps_cli.py doctor` |
| Workbooks | master and domain workbooks import cleanly | `node tools/verify_workbooks.mjs` |
| Whitespace | no trailing whitespace or patch errors | `git diff --check` |
| Smoke path | preflight init/check/leak/gate and promote-to-full path behave as expected | smoke command output |

Do not push if any source-kit acceptance check fails unless the failure is documented as an intentional deviation.

## 3. Lowercase Preflight Acceptance

A `cramps-*` preflight may recommend escalation only when:

| Check | Pass condition |
|---|---|
| G0 boundary | package is active and outside controlled source material |
| Scope | question, coordinate, units, tolerance sketch, inclusion boundary, and claim boundary exist |
| Sources | source table has positive-like and null/non-event search evidence |
| Rows | row table has coordinate values and units for every row |
| Nulls | at least one null, exclusion, failed replication, or non-event row exists |
| Failure modes | failure-mode worksheet identifies holds and stop signs |
| Decision | decision record states advance, hold, stop, or re-scope |
| Leak scan | no open critical leak findings |
| Claim boundary | no uppercase/full assurance claim appears |

Passing preflight acceptance means only:

> The preflight is structured enough to support the stated preflight decision.

It does not mean:

> The coordinate recurrence is real, causal, safe, compliant, or confirmed.

## 4. Uppercase Full-System Acceptance

A `CRAMPS-*` package may be release-reviewed only when:

| Check | Pass condition |
|---|---|
| Protocol lock | protocol hash, candidate registry, tolerance, and primary statistic are locked before scoring |
| Source universe | search strategy, source catalog, exclusions, and null/non-event accounting are complete |
| Row integrity | every raw signal row traces to source evidence |
| Normalization | raw and normalized values are separated and reproducible |
| Dependence | evidence-family map and independence grades cover all rows |
| Bias | missing evidence and domain bias are assessed |
| Statistics | null model, global correction, negative controls, and sensitivities are complete |
| Reproducibility | checksums, environment, run instructions, and clean-run record exist |
| Trust | build ledger, checkpoint reviews, claim trace, trust debt, and trust status summary are complete |
| Release | decision memo, claim-language approval, and signoff are complete |

Passing full-system acceptance means only:

> The CRAMPS package can support a bounded evidence-tier and prioritization statement.

It does not grant domain confirmation by itself.

## 5. Worked Example Acceptance

Worked examples must satisfy:

- synthetic or public-safe data only
- explicit claim boundary
- no real private, restricted, or source-contaminated material
- sidecar check has no blockers
- leak scan has no critical findings
- gate run clears only the worked-example level
- example states what cannot be inferred
- example states whether preflight uses one operator or full-system agent deployment

## 6. Stop Conditions

Stop release or escalation if:

- a lower-case preflight is described as full assurance
- synthetic data is treated as real evidence
- nulls or non-events are removed to improve the result
- a gate is bypassed manually
- leak scan reports an open critical finding
- claim language exceeds the evidence tier
- the package cannot state what it is trustworthy for and not trustworthy for

## 7. Minimal Verification Commands

Source kit:

```bash
python -m py_compile tools/cramps_cli.py tools/cramps_sidecar.py tools/scaffold_cramps_package.py tools/generate_domain_packs.py
python tools/cramps_cli.py doctor
node tools/verify_workbooks.mjs
git diff --check
```

Worked example:

```bash
python tools/cramps_cli.py check worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
python tools/cramps_cli.py leak-scan worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence
python tools/cramps_cli.py gate worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence --level preflight
```
