# CRAMPS Training Guide

**Document ID:** CRAMPS-TRN-001  
**Version:** 0.1  
**Status:** Draft training standard  
**Applies to:** `cramps-*` preflight and `CRAMPS-*` full assurance training

## 1. Purpose

This guide defines how to teach CRAMPS so practitioners can use it safely, consistently, and defensibly.

Training is not complete when learners understand the idea. Training is complete when learners can:

- explain the assurance boundary
- run a lowercase preflight
- identify stop signs
- map a preflight into a full package
- apply G0-G7 gates
- fill core registers
- run the sidecar
- write restrained claim language
- defend a hold, demotion, or rejection

## 2. Audience Tracks

| Track | Audience | Duration | Output |
|---|---|---:|---|
| Executive briefing | sponsor, agency lead, director | 60 minutes | adoption decision and pilot scope |
| Supervisor orientation | safety supervisor, risk owner, program officer | 2 hours | approval/hold/reject literacy |
| Preflight workshop | analyst, domain reviewer, project lead | 1 day | complete `cramps-*` mock preflight |
| Practitioner course | data scientist, evidence reviewer, auditor | 3 days | full package walkthrough and gate practice |
| Instructor course | internal trainer, quality lead | 2 days after practitioner course | teach-back and scoring consistency |

## 3. Learning Objectives

By the end of baseline training, learners can:

1. Define CRAMPS in one sentence.
2. Distinguish `cramps-*` from `CRAMPS-*`.
3. Write a pre-specified coordinate and tolerance.
4. Search for positive, null, exclusion, failed, and non-event evidence.
5. Identify dependence between rows and sources.
6. Identify missing-evidence and reporting-bias risks.
7. Explain why local recurrence is not enough without a credible null model.
8. Use sidecar output to decide hold, continue, stop, or escalate.
9. Assemble the full evidence-binder scaffold.
10. Apply claim-tier and release-language restrictions.

## 4. Recommended 3 Day Practitioner Course

### Day 1: Preflight discipline

| Time | Module | Activity |
|---|---|---|
| 09:00 | Method overview | CRAMPS purpose, boundary, lowercase/uppercase split |
| 10:00 | Coordinate lock | write candidate coordinate, units, tolerance, forbidden drift |
| 11:00 | Evidence universe | source roles, nulls, non-events, exclusions |
| 13:00 | Preflight exercise | fill scope, sources, rows, failure-mode checks |
| 15:00 | Sidecar exercise | run sidecar and interpret blockers |
| 16:00 | Decision memo | advance, hold, stop, or re-scope |

### Day 2: Full assurance package

| Time | Module | Activity |
|---|---|---|
| 09:00 | G0-G7 gates | gate map and release holds |
| 10:00 | Package scaffold | create binder and locate required records |
| 11:00 | Row integrity | source trace, raw/normalized split, extraction confidence |
| 13:00 | Dependence and bias | evidence-family map and missing-evidence assessment |
| 15:00 | Statistical method | null model, multiplicity, sensitivities, negative controls |
| 16:00 | Reproducibility | checksum manifest and clean-run report |

### Day 3: Assurance, audit, and teaching back

| Time | Module | Activity |
|---|---|---|
| 09:00 | Assurance case | claims, evidence, rebuttals, residual risks |
| 10:00 | CAPA and audit | classify findings and open CAPA |
| 11:00 | Supervisor packet | approve, hold, demote, reject, emergency action |
| 13:00 | Capstone | team presents package decision |
| 15:00 | Competency check | scored practical assessment |
| 16:00 | Debrief | common failure modes and next pilot |

## 5. One Day Preflight Workshop

This is the smallest useful training format.

Required materials:

- `templates/preflight_scope.md`
- `templates/preflight_sources.csv`
- `templates/preflight_rows.csv`
- `templates/preflight_gotchas.md`
- `templates/preflight_decision.md`
- `printouts/cramps_preflight_1_to_2_day_printout.md`
- `tools/cramps_sidecar.py`

Workshop output:

- one completed mock preflight
- one sidecar output
- one preflight decision
- one list of stop signs

## 6. Competency Requirement

Learners may be marked competent only after completing a practical exercise scored against `COMPETENCY_RUBRIC.md`.

Attendance alone is not competency.

## 7. Instructor Requirements

Instructors should be able to:

- explain all G0-G7 gates
- score a preflight exercise
- recognize overclaiming
- explain null/non-event evidence
- explain dependence collapse
- interpret sidecar blockers
- run a debrief without turning weak evidence into a discovery claim

## 8. Training Records

Record training in:

- `program/registers/training_matrix.csv`

Minimum fields:

- person
- role
- module
- training version
- completion date
- competency method
- reviewer
- renewal due

## 9. Renewal

Recommended renewal:

| Role | Renewal interval |
|---|---:|
| Preflight analyst | 12 months |
| Domain reviewer | 12 months |
| Statistical lead | 12 months |
| Bias or independence auditor | 12 months |
| Safety supervisor | 12 months |
| Instructor | 6 months |
