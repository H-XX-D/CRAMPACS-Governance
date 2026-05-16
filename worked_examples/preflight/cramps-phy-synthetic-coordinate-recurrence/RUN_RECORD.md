# Worked Example Run Record

**Example:** `cramps-phy` synthetic coordinate recurrence  
**Preflight ID:** `EX-PHY-001`  
**Run posture:** source-safe; mutating checks run only on an isolated copy  
**Last source verification date:** 2026-05-16

## Purpose

This run record shows exactly how to verify the worked example without writing runtime outputs into the reusable source tree.

It is a teaching record, not evidence. Passing these checks means the example is structurally coherent enough to teach a lowercase preflight. It does not mean the synthetic coordinate is real.

## Source-Safe Read Check

```bash
python tools/cramps_sidecar.py worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence \
  --level preflight \
  --out-json /tmp/cramps-phy-worked-sidecar.json \
  --out-md /tmp/cramps-phy-worked-sidecar.md
```

Expected:

- readiness score: `100.0`
- recommendation: `candidate_for_CRAMPS_upgrade`
- blockers: none

## Isolated Release Check

```bash
rm -rf /tmp/cramps-phy-worked-example
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-worked-example
python tools/cramps_cli.py release-check package /tmp/cramps-phy-worked-example --level preflight --force
```

Expected:

- `decision`: `package_release_ready`
- `blocker_count`: `0`
- `warning_count`: `0`
- output directory: `/tmp/cramps-phy-worked-example/exports/release_check`

The release check creates package-local runtime outputs only in the isolated copy.

## Contract Audit Expectations

The isolated release check must include `contract_audit`.

Expected contract-audit posture:

- `preflight_sources.csv` header matches the source contract
- `preflight_rows.csv` header matches the row contract
- `preflight_manifest.csv` header matches the manifest contract
- populated source rows have `source_id`, `citation_or_label`, `source_role`, and `unit_or_site`
- populated preflight rows have `row_id`, `source_id`, `coordinate_value`, `coordinate_units`, and `row_type`
- all `preflight_rows.csv` `source_id` values resolve to `preflight_sources.csv`

## Failure Demonstration

Acceptance should not pass if the contract audit has not run.

```bash
rm -rf /tmp/cramps-phy-no-contract
cp -R worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence /tmp/cramps-phy-no-contract
python tools/cramps_cli.py check /tmp/cramps-phy-no-contract --level preflight
python tools/cramps_cli.py agent-audit /tmp/cramps-phy-no-contract --level preflight
python tools/cramps_cli.py leak-scan /tmp/cramps-phy-no-contract
python tools/cramps_cli.py gate /tmp/cramps-phy-no-contract --level preflight
python tools/cramps_cli.py acceptance-audit /tmp/cramps-phy-no-contract --level preflight
```

Expected:

- `decision`: `hold_preflight`
- blocker: missing `ai_controls/contract_audit_status.json`

## Reviewer Interpretation

If the isolated release check passes, the correct reviewer decision is:

> Accept this as a source-safe worked preflight example. It can teach escalation mechanics, contract checks, and claim boundaries. It cannot be reused as evidence.

