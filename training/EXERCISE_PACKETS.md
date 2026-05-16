# Exercise Packets

**Document ID:** CRAMPS-TRN-EX-001  
**Version:** 0.1  
**Status:** Draft exercise set

## Exercise 1: Preflight or Full?

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

A team has noticed several weak signals around the same parameter value across papers, logs, or reports. They have not locked a coordinate and have not searched nulls.

### Task

Choose the correct route:

- `cramps-*`
- `CRAMPS-*`

### Learner answer

| Field | Entry |
|---|---|
| Selected route |  |
| Rationale |  |
| Evidence tier |  |
| Prohibited claim |  |
| Artifact or form used |  |

### Expected answer

Use `cramps-*`. The team is not ready for uppercase assurance.

### Debrief

Ask what artifacts are needed before escalation.

## Exercise 2: Coordinate Drift

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

The team first says the coordinate is "around 50," then changes it to "48 to 55," then later includes values up to 60 because those rows look related.

### Task

Classify the issue and state the control.

### Learner answer

| Field | Entry |
|---|---|
| Issue classification |  |
| Gate or checkpoint |  |
| Corrective action |  |
| Prohibited reliance |  |
| Artifact or form used |  |

### Expected answer

This is tolerance creep and possible post-hoc coordinate movement. Hold at G1 Coordinate Lock.

## Exercise 3: Positive-Only Package

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

Eight rows show weak recurrence. All came from reports that discussed anomalies. No null searches or non-events were recorded.

### Task

Write the supervisor decision.

### Learner answer

| Field | Entry |
|---|---|
| Supervisor decision |  |
| Evidence tier |  |
| Missing evidence |  |
| Rationale |  |
| Prohibited claim |  |

### Expected answer

Hold or reject for full assurance. The package can continue only after null/non-event search and missing-evidence assessment.

## Exercise 4: Duplicate Evidence Trap

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

Ten rows come from four papers, but all four papers analyze the same public dataset and use the same calibration pipeline.

### Task

Identify the dependence issue and propose a correction.

### Learner answer

| Field | Entry |
|---|---|
| Dependence issue |  |
| Evidence-family correction |  |
| Analysis impact |  |
| Trust state |  |
| Artifact or form used |  |

### Expected answer

Rows are not independent. Assign a shared evidence-family ID, collapse or down-weight, and rerun sensitivity.

## Exercise 5: Missing-Null Reveal

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

After an apparent recurrence is found, an auditor identifies several unpublished or inaccessible null reports.

### Task

Classify the finding and decision impact.

### Learner answer

| Field | Entry |
|---|---|
| Finding severity |  |
| Decision impact |  |
| CAPA needed |  |
| Trust debt item |  |
| Next action |  |

### Expected answer

Open bias and possibly CAPA. Hold or demote until missing-evidence impact is assessed.

## Exercise 6: Claim Language

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

A draft report says: "CRAMPS proves this intervention causes the adverse event."

### Task

Rewrite the claim.

### Learner answer

| Field | Entry |
|---|---|
| Rewritten claim |  |
| Trustworthy for |  |
| Not trustworthy for |  |
| Evidence tier |  |
| Prohibited claim |  |

### Expected answer

"A pre-specified coordinate shows unusual recurrence under the registered CRAMPS analysis and should be prioritized for domain-standard validation."

## Exercise 7: Sidecar Blockers

**Team:**  
**Scorer:**  
**Score:**  

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

### Learner answer

| Field | Entry |
|---|---|
| Sidecar recommendation |  |
| Blockers |  |
| Trust state |  |
| Next action owner |  |
| Due date |  |

### Expected answer

Do not release. Complete null-model runs, gate review records, and decision record, then rerun sidecar.

## Exercise 8: Emergency Action

**Team:**  
**Scorer:**  
**Score:**  

### Scenario

A safety supervisor believes immediate operational action is needed before CRAMPS is complete.

### Task

State what CRAMPS permits.

### Learner answer

| Field | Entry |
|---|---|
| Emergency decision |  |
| Accountable authority |  |
| Duration |  |
| CAPA ID |  |
| Retrospective review date |  |
| Prohibited claim |  |

### Expected answer

Emergency parallel action is permitted only as an operational override. It does not upgrade evidence tier. It requires accountable approval, duration, CAPA, prohibited claims, and retrospective review.
