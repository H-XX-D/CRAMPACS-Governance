# Full-System Handoff and Agent Deployment Position

**Preflight ID:** EX-PHY-001
**Target full system:** `CRAMPS-PHY`
**Status:** teaching handoff only

## Handoff Rule

The lowercase preflight used one operator: `single_preflight_operator`.

If the work escalates, the full package must be created as a separate uppercase `CRAMPS-PHY` package. The preflight artifacts may seed the package, but they do not carry full assurance status.

The package-local deployment controls are in:

- `ai_controls/AGENT_DEPLOYMENT_HELPER.md`
- `ai_controls/agent_deployment_plan.csv`
- `ai_controls/agent_handoff_checklist.csv`
- `ai_controls/agent_registry.csv`

## Where Expanded Agent Deployment Starts

Expanded agent deployment starts after:

1. a separate `CRAMPS-PHY` package is created
2. the preflight import log is opened
3. a protocol steward accepts or rejects each preflight artifact
4. the full protocol is locked
5. release authority approves role assignments

## Full-System Agent Positions

| Position | Can do | Cannot do |
|---|---|---|
| Protocol steward | Maintain protocol lock and amendment log | Score rows or tune results |
| Source search agent | Build source catalog and source flow | Exclude adverse evidence |
| Extraction agent | Extract row values with provenance | Treat summaries as source data |
| Independence auditor | Grade dependence and evidence families | Select favorable rows |
| Bias auditor | Assess missing evidence and source-process bias | Approve release alone |
| Statistical lead | Lock statistic, null model, and global correction | Change methods after seeing results |
| Reproducibility lead | Build checksum and clean-run records | Edit evidence to pass reproduction |
| Red-team reviewer | Attempt to break the claim | Rewrite the claim to make it stronger |

## Import Disposition For This Example

Because all rows are synthetic:

- `preflight_scope.md` may be accepted as training background
- `preflight_sources.csv` must be replaced by a real source search
- `preflight_rows.csv` must be quarantined from scoring
- `preflight_gotchas.md` may seed the failure-mode checklist
- `preflight_decision.md` may seed the escalation rationale only

## Claim Boundary

The full system may not claim anything until the uppercase package clears its own gates. This handoff does not clear any `CRAMPS-PHY` gate.
