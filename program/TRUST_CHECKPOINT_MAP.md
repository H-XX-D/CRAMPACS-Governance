# Trust Checkpoint Map

**Document ID:** CRAMPS-TRUST-MAP-001  
**Version:** 0.1  
**Status:** Draft checkpoint map

## 1. Purpose

This map tells teams what to check while a CRAMPS package is being built.

It complements the canonical G0-G7 gate map. Gates decide whether a package can advance. Trust checkpoints keep the work honest before each gate decision.

## 2. Checkpoint Questions

At every checkpoint, answer:

1. What changed since the last checkpoint?
2. What evidence was added, removed, revised, or quarantined?
3. What is still assumed?
4. What is still unverified?
5. What sidecar blockers exist?
6. What claim language is currently prohibited?
7. What decision can be made now?
8. What decision cannot be made yet?
9. What is the next trust-building action?

## 3. Checkpoint Map

| Checkpoint | Package point | Main honesty risk | Minimum review |
|---|---|---|---|
| T0 | package start | unclear purpose or hidden intended use | decision owner, intended use, prohibited use |
| T1 | coordinate proposed | coordinate drift or tolerance creep | coordinate, units, tolerance, forbidden changes |
| T2 | sources drafted | positive-only evidence | source roles, null search, exclusions |
| T3 | rows extracted | source trace or AI-summary drift | source links, raw values, extraction confidence |
| T4 | normalization drafted | hidden unit conversion | raw/normalized separation, transform review |
| T5 | dependence and bias drafted | duplicate evidence counted independently | evidence-family map, missing-evidence risk |
| T6 | statistics planned | statistic shopping or weak null | locked statistic, null model, multiplicity plan |
| T7 | results generated | local result overclaimed | global correction, sensitivities, negative controls |
| T8 | report drafted | claim exceeds evidence tier | claim trace matrix, prohibited claims |
| T9 | release review | unknown trust state | trust status summary, sidecar, open CAPA |

## 4. Trust Status Summary

Before G7 release, the package must include `10_trust_maintenance/trust_status_summary.md`.

Minimum sections:

- package trust state
- artifacts accepted
- artifacts checked with limits
- artifacts blocked
- artifacts quarantined
- open assumptions
- open uncertainty
- open CAPA
- sidecar blockers
- prohibited claims
- release recommendation

## 5. Checkpoint Decisions

| Decision | Meaning |
|---|---|
| `continue` | proceed, no release impact at this point |
| `continue_with_limits` | proceed with explicitly recorded limits |
| `hold` | pause promotion until trust debt is closed |
| `quarantine` | retain artifact but exclude from scoring or release |
| `demote` | lower assurance level or evidence tier |
| `stop` | terminate route or package |

## 6. Reviewer Rule

The person who created an artifact may not be the only person to promote its trust state.

For low-risk preflights, a single independent reviewer may be enough.

For full or regulated packages, promotion requires the relevant gate owner or delegated reviewer.

