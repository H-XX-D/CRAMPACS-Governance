# Trust Positioning and Reliance Levels

**Document ID:** CRAMPS-TRUST-POS-001  
**Version:** 0.1  
**Status:** Draft positioning standard  
**Applies to:** all CRAMPS communication, training, preflights, full packages, and releases

## 1. Core Rule

Never say a CRAMPS package is simply "trustworthy."

Always say what it is trustworthy for.

Trustworthy positioning requires four parts:

1. assurance route
2. trust state
3. permitted reliance
4. prohibited reliance

Example:

> This `cramps-med` preflight is trustworthy for deciding whether to invest in a full `CRAMPS-MED` study. It is not trustworthy for clinical action, causal inference, or public safety claims.

## 2. Trustworthy For What?

| Package state | Trustworthy for | Not trustworthy for |
|---|---|---|
| idea sketch | conversation and scoping | CRAMPS claim, preflight decision, operational decision |
| `cramps-*` draft | internal triage work | escalation, publication, safety action |
| `cramps-*` checked | deciding continue, hold, stop, or full-study escalation | domain conclusion, full assurance, external claim |
| `CRAMPS-*` scaffold | organizing work | evidence reliance or release |
| `CRAMPS-*` gate-accepted | advancing to the next gate | release unless G7 is complete |
| `CRAMPS-*` release-ready | decision support within assigned evidence tier | proof of causality or regulatory compliance by itself |
| externally validated | stronger prioritization and confidence in process reproducibility | domain proof unless domain-standard confirmation is complete |

## 3. Positioning Ladder

Use this ladder in reports, training, and supervisor decisions.

| Level | Name | Positioning language |
|---|---|---|
| P0 | not positioned | "This is not a CRAMPS output." |
| P1 | exploration | "This is an exploratory observation." |
| P2 | preflight | "This is a lowercase `cramps-*` triage result." |
| P3 | full package in progress | "This is a full `CRAMPS-*` package under construction and is not release-ready." |
| P4 | gate accepted | "This package has passed specified gates but is not yet a release result." |
| P5 | release result | "This package is approved for the stated decision within the assigned evidence tier." |
| P6 | externally validated | "This package has independent reproduction or external audit support." |

## 4. Required Positioning Sentence

Every decision memo, supervisor packet, and release-facing report must include:

```text
This package is trustworthy for: [specific reliance].
This package is not trustworthy for: [specific prohibited reliance].
Current assurance route: [cramps-* or CRAMPS-*].
Current trust state: [draft / unchecked / checked_with_limits / accepted / blocked / superseded / quarantined].
Current evidence tier: [0-4].
```

## 5. Mispositioning Failures

Mispositioning is a release defect.

| Failure | Why it matters | Required action |
|---|---|---|
| calling preflight full assurance | creates false confidence | hold, correct language, log deviation |
| calling recurrence proof | overstates method | hold, rewrite claim, reviewer approval |
| omitting prohibited reliance | lets users infer too much | hold release memo |
| hiding open blockers | breaks trust state | hold and update trust summary |
| using "validated" for internal-only review | overstates independence | demote or correct |
| describing compliance without domain mapping | creates regulatory risk | legal/compliance review |

## 6. Trust Is Scoped

Trust can be local.

An artifact may be trustworthy for one purpose and not another:

- a source catalog may be trustworthy for screening but not final inclusion
- raw signal rows may be trustworthy for extraction review but not normalized analysis
- a null model may be trustworthy for sensitivity exploration but not release inference
- a preflight may be trustworthy for budget scoping but not operational action

The trust status summary must preserve these scopes.

## 7. Supervisor Translation

When briefing a supervisor, use this structure:

1. What is the package route?
2. What has been checked?
3. What remains untrusted?
4. What decision is safe now?
5. What decision is unsafe now?
6. What would move the package to the next trust state?

## 8. Release Language Examples

Preflight:

> This `cramps-*` preflight is trustworthy for deciding whether a full CRAMPS package is worth funding. It is not trustworthy for domain action or external claims.

Full package in progress:

> This `CRAMPS-*` package is under construction. It may be useful for internal review, but it is not trustworthy for release until G7, sidecar, trust summary, and decision memo are complete.

Release-ready:

> This `CRAMPS-*` package is trustworthy for the decision named in the decision memo, within the assigned evidence tier and stated limitations. It does not establish domain causality or compliance by itself.

Externally validated:

> This CRAMPS result has additional process confidence from independent reproduction or external audit. Domain-standard confirmation is still required for domain proof.
