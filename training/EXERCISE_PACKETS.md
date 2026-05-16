# Exercise Packets

**Document ID:** CRAMPACS-TRN-EX-001  
**Version:** 0.1  
**Status:** Draft exercise set

## Exercise 1: Preflight or Full?

### Scenario

A team has noticed several weak signals around the same parameter value across papers, logs, or reports. They have not locked a coordinate and have not searched nulls.

### Task

Choose the correct route:

- `crampacs-*`
- `CRAMPACS-*`

### Expected answer

Use `crampacs-*`. The team is not ready for uppercase assurance.

### Debrief

Ask what artifacts are needed before escalation.

## Exercise 2: Coordinate Drift

### Scenario

The team first says the coordinate is "around 50," then changes it to "48 to 55," then later includes values up to 60 because those rows look related.

### Task

Classify the issue and state the control.

### Expected answer

This is tolerance creep and possible post-hoc coordinate movement. Hold at G1 Coordinate Lock.

## Exercise 3: Positive-Only Package

### Scenario

Eight rows show weak recurrence. All came from reports that discussed anomalies. No null searches or non-events were recorded.

### Task

Write the supervisor decision.

### Expected answer

Hold or reject for full assurance. The package can continue only after null/non-event search and missing-evidence assessment.

## Exercise 4: Duplicate Evidence Trap

### Scenario

Ten rows come from four papers, but all four papers analyze the same public dataset and use the same calibration pipeline.

### Task

Identify the dependence issue and propose a correction.

### Expected answer

Rows are not independent. Assign a shared evidence-family ID, collapse or down-weight, and rerun sensitivity.

## Exercise 5: Missing-Null Reveal

### Scenario

After an apparent recurrence is found, an auditor identifies several unpublished or inaccessible null reports.

### Task

Classify the finding and decision impact.

### Expected answer

Open bias and possibly CAPA. Hold or demote until missing-evidence impact is assessed.

## Exercise 6: Claim Language

### Scenario

A draft report says: "CRAMPACS proves this intervention causes the adverse event."

### Task

Rewrite the claim.

### Expected answer

"A pre-specified coordinate shows unusual recurrence under the registered CRAMPACS analysis and should be prioritized for domain-standard validation."

## Exercise 7: Sidecar Blockers

### Scenario

The sidecar returns:

```json
{
  "recommendation": "hold_release",
  "blockers": [
    "no_null_model_runs",
    "no_gate_review_records",
    "no_decision_records"
  ]
}
```

### Task

State the next action.

### Expected answer

Do not release. Complete null-model runs, gate review records, and decision record, then rerun sidecar.

## Exercise 8: Emergency Action

### Scenario

A safety supervisor believes immediate operational action is needed before CRAMPACS is complete.

### Task

State what CRAMPACS permits.

### Expected answer

Emergency parallel action is permitted only as an operational override. It does not upgrade evidence tier. It requires accountable approval, duration, CAPA, prohibited claims, and retrospective review.

