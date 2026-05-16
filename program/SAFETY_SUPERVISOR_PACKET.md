# Safety Supervisor Packet

**Document ID:** CRAMPS-SSP-001  
**Audience:** safety supervisors, risk owners, government program officers, regulated operations leads

## 1. What This Lets You Decide

CRAMPS helps decide whether a weak-evidence recurrence is worth escalation, validation, mitigation, or rejection.

It does not decide causality by itself.

## 2. Supervisor Questions

Ask these before approving escalation:

1. What coordinate is being tested?
2. Was it locked before scoring?
3. What nulls or non-events were included?
4. What evidence is duplicated or dependent?
5. What bias could create the pattern?
6. What negative control was used?
7. What would make us stop believing the recurrence?
8. Can the package be reproduced?
9. What action is being requested?
10. What claim is explicitly prohibited?

## 3. Supervisor Stop Rules

Stop the package if:

- the coordinate is not precise
- no null evidence is present
- one source family drives the result
- dependencies are unresolved
- the null model is not credible
- the package cannot be reproduced
- the requested action exceeds the evidence tier
- safety or regulatory language is unsupported

## 4. Supervisor Signoff Options

| Decision | Meaning |
|---|---|
| approve_preflight_closeout | Preflight complete, no full study needed |
| approve_full_study | Preflight justifies full CRAMPS |
| approve_limited_escalation | Act only within stated evidence tier |
| hold_for_rework | Package has fixable gaps |
| reject | Package is not credible for decision support |
| emergency_parallel_action | Operational action proceeds while CRAMPS remains incomplete |

## 5. Emergency Parallel Action

Use `emergency_parallel_action` only when waiting for a complete CRAMPS package could create a material safety, security, public-interest, financial, operational, or legal harm.

Minimum requirements:

- name the immediate action being authorized
- state why delay is more harmful than acting with incomplete evidence
- state the maximum duration of the emergency authorization
- name the accountable safety, risk, or command authority
- open a deviation/CAPA record
- define what evidence would stop, narrow, or reverse the action
- prohibit public or scientific overclaiming while the CRAMPS package is incomplete
- schedule a retrospective review after the emergency interval

Emergency action does not upgrade the evidence tier. It is an operational override with documented accountability.

## 6. Required Signoff Text

> I approve this decision only within the stated CRAMPS evidence tier. I do not treat this package as proof of causality, compliance, safety, efficacy, exploitability, fraud, or physical discovery unless domain-standard confirmation is separately documented.
