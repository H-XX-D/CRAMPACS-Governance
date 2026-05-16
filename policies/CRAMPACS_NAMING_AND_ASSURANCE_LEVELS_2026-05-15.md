# CRAMPACS Naming and Assurance Levels

**Policy ID:** CRAMPACS-NAME-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft naming and assurance policy

## 1. Purpose

This policy defines the difference between uppercase `CRAMPACS-*` systems and lowercase `crampacs-*` systems.

The distinction prevents a lightweight preflight from being mistaken for a full assurance study.

## 2. Naming Rule

Uppercase names refer to full assurance systems.

Lowercase names refer to lightweight preflight systems.

Examples:

| Lightweight preflight | Full assurance | Domain |
|---|---|---|
| crampacs-med | CRAMPACS-MED | Medicine |
| crampacs-gen | CRAMPACS-GEN | Genomics |
| crampacs-clim | CRAMPACS-CLIM | Climate |
| crampacs-mat | CRAMPACS-MAT | Materials |
| crampacs-eng | CRAMPACS-ENG | Engineering |
| crampacs-fin | CRAMPACS-FIN | Finance |
| crampacs-cyb | CRAMPACS-CYB | Cybersecurity |
| crampacs-ast | CRAMPACS-AST | Astronomy |
| crampacs-phy | CRAMPACS-PHY | Physics |
| crampacs-genr | CRAMPACS-GENR | Generic cross-domain use |

The suffix can be extended to any field, but the uppercase/lowercase distinction must remain stable.

## 3. Uppercase System: CRAMPACS-*

`CRAMPACS-*` means the full system.

Use it when outputs may support:

- External publication.
- Regulated decision support.
- Safety review.
- Security review.
- Clinical, financial, engineering, or operational escalation.
- Formal research claims.
- Auditable management decisions.
- Cross-team or external reproducibility.

Minimum requirements:

- Locked protocol.
- Candidate coordinate registry.
- Source universe and source flow.
- Null and non-event inclusion.
- Row-level provenance.
- Coordinate normalization.
- Independence grading.
- Bias and missing-evidence assessment.
- Primary statistic.
- Registered null model.
- Sensitivity tests.
- Negative controls.
- Reproducibility capsule.
- Cross-unit checksum manifest where applicable.
- Statistical and domain signoff.

Allowed outputs:

- Evidence tier.
- Cross-catalog recurrence result under a registered null.
- Formal escalation recommendation.
- Reproducible study package.
- Regulated or audit-ready decision support when paired with domain controls.

Forbidden outputs:

- Discovery claim by CRAMPACS alone.
- Clinical, legal, safety, regulatory, or causal conclusion without domain-standard validation.

## 4. Lowercase System: crampacs-*

`crampacs-*` means lightweight preflight.

Use it when teams need a one to two day pass before committing budget, launching a full study, deploying a model, escalating an incident, or funding deeper work.

Minimum requirements:

- One-page scope.
- Coordinate sketch.
- Candidate coordinate list or suspected coordinate family.
- Small bounded source set.
- Fast null and non-event check.
- Fast dependence scan.
- Fast bias and missing-evidence scan.
- Unit and transform sanity check.
- Basic checksum manifest.
- Gotcha checklist.
- Escalation recommendation.

Allowed outputs:

- Proceed to full `CRAMPACS-*`.
- Hold until coordinate is better specified.
- Hold until nulls/non-events are found.
- Hold until dependence is resolved.
- Do not escalate.
- Run a targeted data-quality check.

Forbidden outputs:

- Confirmatory claim.
- Discovery claim.
- Regulated assurance claim.
- Safety, clinical, legal, or financial conclusion.
- Public significance language.

## 5. Assurance Level Ladder

| Level | Name | Typical time | Purpose | Output |
|---|---|---:|---|---|
| L0 | Desk sketch | Hours | Define possible coordinate and evidence class | Not a CRAMPACS output |
| L1 | crampacs preflight | 1-2 days | Decide whether deeper work is worth it | Triage and escalation recommendation |
| L2 | CRAMPACS pilot | 1-4 weeks | Narrow locked retrospective test | Limited evidence tier |
| L3 | CRAMPACS standard | 1-3 months | Full retrospective defensible package | Reproducible cross-catalog result |
| L4 | CRAMPACS regulated | Project-specific | Full system plus domain regulatory controls | Audit-ready decision support |
| L5 | CRAMPACS externally validated | Project-specific | Independent reproduction or audit | Strongest process assurance |

## 6. Composability Rule

A lowercase `crampacs-*` preflight is designed to be composable into an uppercase `CRAMPACS-*` project.

The preflight creates seed artifacts:

- initial coordinate sketch
- candidate coordinate candidates
- source shortlist
- null and non-event leads
- gotcha register
- dependence concerns
- bias concerns
- unit and transform concerns
- preliminary checksum manifest
- escalation decision

These artifacts may be imported into the full system as starting material.

They do not carry full assurance status until they are reviewed, re-locked, and completed under the full CRAMPACS protocol.

## 7. Conversion Rule

A lowercase `crampacs-*` preflight becomes an uppercase `CRAMPACS-*` project through an explicit conversion package.

Required conversion artifacts:

- Full study charter.
- Full protocol.
- Fresh candidate registry lock, informed by but not identical to the preflight sketch unless justified.
- Source strategy.
- Null and non-event plan.
- Independence plan.
- Bias plan.
- Statistical plan.
- Reproducibility plan.
- Preflight import log.
- Preflight artifact hashes.
- Review disposition for each imported preflight artifact.

Preflight findings cannot be re-labeled as confirmatory evidence. Preflight artifacts can be reused as inputs after full-system review.

## 8. Reporting Rule

Every report must identify its level in the title or first paragraph.

Permitted examples:

- `crampacs-fin preflight for merchant-risk anomaly coordinates`
- `CRAMPACS-FIN locked retrospective study of merchant-risk recurrence`
- `crampacs-cyb preflight for exploit timing recurrence`
- `CRAMPACS-CYB prospective holdout study of exploit timing recurrence`

Prohibited examples:

- Calling a preflight "validated."
- Calling a lightweight scan "CRAMPACS" without lowercase marker.
- Omitting the assurance level.
- Reporting local significance from a preflight.

## 9. Platform Implication

A platform implementing this policy should expose two separate workflows:

- `crampacs` quick-start preflight.
- `CRAMPACS` full assurance study.

The interface should make the upgrade path composable but should not blur the assurance boundary.

Recommended platform behavior:

- Preflight artifacts are marked `seed`.
- Imported artifacts are marked `under_review`.
- Reviewed artifacts are marked `accepted_for_protocol`, `accepted_for_background`, `rejected`, or `quarantined`.
- Full-system locks are created only after review disposition is complete.
