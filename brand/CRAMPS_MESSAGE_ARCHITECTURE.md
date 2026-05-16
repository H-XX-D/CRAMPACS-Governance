# CRAMPS Message Architecture

**Document ID:** CRAMPS-MSG-001  
**Version:** 0.1  
**Status:** Draft messaging standard

## 1. One-Sentence Description

CRAMPS is a coordinate-resolved assurance framework for inspecting whether weak observations recur at pre-specified coordinates across independent evidence sources more often than expected under controlled null models.

## 2. Short Description

CRAMPS helps teams move from informal signal-in-noise suspicion to a controlled evidence package. It separates a fast lowercase `cramps-*` preflight from a full uppercase `CRAMPS-*` assurance study with protocol lock, source accounting, null evidence, dependence and bias review, statistical controls, reproducibility, and supervisor signoff.

## 3. Audience-Specific Messages

| Audience | Message |
|---|---|
| Research team | CRAMPS lets you inspect cross-catalog recurrence without pretending weak observations are discoveries. |
| Safety supervisor | CRAMPS gives you a structured way to approve, hold, demote, or reject weak-evidence escalation. |
| Data science team | CRAMPS is a reusable evidence-synthesis operating layer for anomaly recurrence problems. |
| Regulated team | CRAMPS creates auditable decision support, but domain compliance still requires applicable regulatory controls. |
| Executive sponsor | CRAMPS helps decide which suspected recurrences deserve deeper investment and which should stop early. |

## 4. What Makes It Different

- It treats coordinate recurrence as the evidentiary object.
- It preserves tuning context instead of flattening weak findings into anecdotes.
- It requires pre-specification before scoring.
- It treats nulls and non-events as first-class evidence.
- It grades dependence so duplicate evidence is not multiplied.
- It has a lightweight route and a full assurance route.
- It produces teachable, inspectable artifacts.

## 5. Elevator Pitch

Most anomaly reviews ask whether one result crossed a threshold. CRAMPS asks a different question: does weak evidence keep returning to the same pre-specified coordinate after nulls, non-events, dependence, bias, and look-elsewhere effects are accounted for? The method is useful only when strict controls are applied, so CRAMPS includes gates, data contracts, bias checks, sidecar metrics, and release rules.

## 6. Boilerplate

CRAMPS stands for Coordinate-Resolved Anomaly Meta-analysis with Pre-specified Statistics. It is a domain-general framework for disciplined recurrence inspection. CRAMPS can support prioritization, escalation, validation planning, and controlled decision support. It does not by itself prove causality, safety, efficacy, exploitability, compliance, fraud, or physical discovery.
