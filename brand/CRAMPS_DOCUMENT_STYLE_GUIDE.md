# CRAMPS Document Style Guide

**Document ID:** CRAMPS-STYLE-001  
**Version:** 0.1  
**Status:** Draft style standard

## 1. Purpose

This guide makes CRAMPS documents consistent, teachable, and audit-friendly.

## 2. Writing Rules

Write in plain operational English.

Use:

- direct verbs
- short sections
- concrete evidence names
- controlled decision words
- stable IDs
- tables for checklists and registers

Avoid:

- unexplained acronyms
- unsupported assurance language
- decorative complexity
- vague words like robust without a control
- saying compliance unless the domain addendum proves it

## 3. Standard Decision Words

Use only these decision words unless a domain addendum defines stricter terms:

| Word | Meaning |
|---|---|
| approve | acceptable within stated evidence tier |
| approve_with_limits | acceptable only under listed constraints |
| hold | do not release until gaps are corrected |
| demote | lower the evidence tier or assurance level |
| reject | not credible for the requested decision |
| stop | terminate the package or route |
| emergency_parallel_action | operational action proceeds while CRAMPS remains incomplete |

## 4. Standard Severity Words

| Severity | Meaning |
|---|---|
| Critical | invalidates release or creates unsafe/misleading use |
| Major | could materially change interpretation |
| Minor | documentation or traceability issue unlikely to change result |
| Observation | improvement opportunity |

## 5. Page Pattern

For short printouts:

1. Title
2. Scope or assurance level
3. Required inputs
4. Checklist
5. Stop signs
6. Decision

For controlled procedures:

1. Title and document control block
2. Purpose
3. Scope
4. Roles
5. Procedure
6. Required records
7. Stop or escalation rules
8. Review cadence

For training material:

1. Learning objectives
2. Concepts
3. Demonstration
4. Exercise
5. Debrief
6. Competency check

## 6. Table Standards

Checklist tables should use:

```text
| Item | Owner | Status | Evidence | Notes |
```

Gate tables should use:

```text
| Gate ID | Gate | Required evidence | Decision | Release impact |
```

Register tables should use stable IDs and status fields.

## 7. Claim Boundary Box

Use this box in reports, training material, and supervisor packets:

```text
Claim Boundary

CRAMPS supports controlled anomaly-prioritization and evidence-tier decisions.
It does not establish domain causality or regulatory compliance by itself.
```

## 8. Lightweight vs Full Box

Use this box when both assurance levels appear:

```text
Assurance Boundary

cramps-* = 1 to 2 day preflight.
CRAMPS-* = full assurance package after protocol lock and release review.
```

## 9. Formatting Rules

- Use sentence case headings in training material.
- Use Title Case headings in policy and procedure titles.
- Use monospace for IDs, filenames, fields, and commands.
- Keep one idea per paragraph.
- Keep lists short enough to teach from.
- Prefer a checklist over a paragraph when a practitioner must act.

## 10. Review Checklist

Before release, confirm:

| Check | Pass/Hold |
|---|---|
| Assurance level named |  |
| Claim boundary visible |  |
| Required inputs listed |  |
| Outputs listed |  |
| Stop rules listed |  |
| Evidence names concrete |  |
| Decision words controlled |  |
| Domain claims restrained |  |
| Links and paths work |  |
| Document appears in register if controlled |  |

