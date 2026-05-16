# CRAMPS Program Operating Manual

**Document ID:** CRAMPS-POM-001  
**Status:** Operational draft  
**Applies to:** all `cramps-*` preflights and `CRAMPS-*` full assurance studies

## 1. Purpose

CRAMPS is an assurance program for deciding whether weak observations recur at pre-specified coordinates across heterogeneous evidence sources more often than expected under a registered null model.

The program is designed for teams that cannot afford informal pattern-finding:

- safety supervisors
- regulated research teams
- public agencies
- clinical safety groups
- financial risk and fraud teams
- cyber defense teams
- engineering reliability groups
- scientific research groups

CRAMPS does not make final domain claims by itself. It produces an auditable evidence package that can support prioritization, escalation, rejection, or formal follow-up.

## 2. Assurance Boundary

| Level | Name | Meaning | Permitted output |
|---|---|---|---|
| L0 | Desk sketch | Informal idea or suspected pattern | No CRAMPS output |
| L1 | `cramps-*` preflight | 1-2 day structured triage | Escalate, hold, stop, or re-scope |
| L2 | CRAMPS pilot | Narrow locked retrospective study | Limited evidence tier |
| L3 | CRAMPS standard | Full retrospective package | Defensible cross-catalog recurrence result |
| L4 | CRAMPS regulated | Full package plus domain regulatory controls | Audit-ready decision support |
| L5 | CRAMPS externally validated | Independent reproduction or external audit | Highest process assurance |

Lowercase outputs cannot be sold or described as uppercase assurance.

## 3. Decision Authority

Every study must name decision authorities before work starts.

The operating authority model is controlled by `RELEASE_AUTHORITY_RACI.md`. Gate names, IDs, inputs, outputs, and blockers are controlled by `CANONICAL_GATE_MAP.md`.

| Authority | Can approve | Can veto | Cannot do |
|---|---|---|---|
| Program owner | scope, budget, schedule | continuation if scope no longer matters | override statistical veto |
| Safety or domain supervisor | domain suitability, operational escalation | use in safety or operational decision | weaken statistical controls |
| Protocol steward | protocol lock, amendments | post-hoc scope changes | score results |
| Statistical lead | analysis plan, null model, inference language | release, claim tier, significance language | approve domain action alone |
| Independence auditor | dependence grades and evidence-family map | pooling or independence claims | select favorable rows |
| Bias auditor | missing-evidence and bias assessment | promotion when bias unresolved | decide technical causality |
| Data steward | data rights, provenance, checksums, retention | release package | change analysis plan |
| Reproducibility lead | clean run and manifest | release if reproduction fails | edit source data to pass |
| Red-team lead | adversarial findings | promotion while critical findings open | rewrite the result |

Any one of the statistical lead, data steward, reproducibility lead, or safety/domain supervisor may place a release hold.

## 4. Required Gates

### Gate 0: Charter

Pass criteria:

- Domain selected.
- Decision owner named.
- Intended decision stated.
- Assurance level selected.
- Safety, legal, privacy, or security constraints identified.
- Claim boundary written.

Failure condition:

- The team cannot state what decision the work supports.

### Gate 1: Coordinate Lock

Pass criteria:

- Candidate coordinate is stated in canonical units.
- Tolerance is justified before scoring.
- Allowed transforms are listed.
- Negative control coordinate or class is named.
- The candidate lock timestamp is recorded.

Failure condition:

- The coordinate can move after rows are seen.

### Gate 2: Source Universe

Pass criteria:

- Search scope is documented.
- Positive, null, exclusion, failed, and non-event evidence classes are searched.
- Exclusion reasons are recorded.
- Source snapshot is hashed or otherwise traceable.

Failure condition:

- The package contains only interesting anomalies.

### Gate 3: Row Integrity

Pass criteria:

- Every row maps to a source.
- Raw values and units are preserved.
- Normalized values are separately computed.
- Extraction method and confidence are recorded.
- Ambiguous rows are quarantined.

Failure condition:

- AI summary, secondary narrative, or undocumented inference becomes source data.

### Gate 4: Dependence and Bias

Pass criteria:

- Evidence-family IDs assigned.
- Dependence grades assigned.
- Bias assessment complete.
- Missing-evidence risk stated.
- Primary weights or recurrence rules approved.

Failure condition:

- Multiple rows from one dataset, vendor, detector, source system, or pipeline are counted as independent without justification.

### Gate 5: Null and Statistical Method

Pass criteria:

- Primary statistic locked.
- Null model locked.
- Multiple testing and look-elsewhere treatment defined.
- Negative controls run or scheduled.
- Sensitivity tests defined.

Failure condition:

- Local recurrence is reported without global correction or null-model validation.

### Gate 6: Reproducibility

Pass criteria:

- Data contracts complete.
- Checksums generated.
- Code/environment recorded.
- Clean run reproduces expected results.
- Output manifest matches.

Failure condition:

- A reviewer cannot reproduce the primary output from the package.

### Gate 7: Release

Pass criteria:

- Gate record complete.
- Critical and major findings closed or accepted by signoff authority.
- Evidence tier assigned.
- Claim language approved.
- Decision memo complete.

Failure condition:

- The report implies a domain conclusion that CRAMPS cannot support.

## 5. Finding Severity

| Severity | Meaning | Release impact |
|---|---|---|
| Critical | Invalidates assurance boundary, data integrity, independence, null model, or reproducibility | Stop release |
| Major | Could materially change result or interpretation | Hold until resolved or demoted |
| Minor | Documentation or traceability gap unlikely to change result | Fix or document before final release |
| Observation | Improvement opportunity | Track, does not block |

Deviation handling, CAPA due dates, effectiveness checks, and reopening rules are controlled by `DEVIATION_AND_CAPA_PROCEDURE.md`.

Controlled document approval, versioning, effective dates, and retirement are controlled by `DOCUMENT_CONTROL_PROCEDURE.md`.

## 6. Evidence Tiering

| Tier | Evidence state | Use |
|---|---|---|
| 0 | Exploratory pattern | Hypothesis generation |
| 1 | Locked retrospective recurrence | Prioritization |
| 2 | Independently reproduced package | Stronger prioritization and internal decision support |
| 3 | Prospective or holdout recurrence | Escalation to formal validation |
| 4 | Domain confirmation | Domain claim possible under field rules |

CRAMPS can support Tiers 0-3. Tier 4 requires domain-standard confirmation.

## 7. Required Release Statement

Every released package must include:

> CRAMPS is an evidence-control and recurrence-prioritization method. It does not establish clinical, legal, safety, financial, security, engineering, or scientific causality by itself. Domain-standard confirmation remains required.
