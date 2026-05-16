# CRAMPS Standards and Practices Policy

**Policy ID:** CRAMPS-SPP-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft governance policy  
**Parent SOP:** `CRAMPS_PROGRAM_SOP_2026-05-15.md`

## 1. Purpose

This policy defines the standards, practices, quality controls, reporting obligations, and governance requirements for CRAMPS studies.

CRAMPS exists to test whether weak anomalies, residuals, nulls, exclusions, and near-misses show statistically unusual recurrence at pre-specified coordinates. Its credibility depends on stricter-than-normal discipline around pre-specification, source completeness, independence, null models, and conservative reporting.

## 2. Authority

This policy applies to all CRAMPS work products:

- Exploratory anomaly atlases.
- Locked retrospective studies.
- Prospective holdout studies.
- Pilot method demonstrations.
- Public reports.
- Reproducibility capsules.
- AI-assisted extraction or review workflows.

No CRAMPS output may be promoted externally unless it satisfies this policy or documents a formal deviation.

## 3. Governing Standard Stack

CRAMPS uses the following standard stack as alignment targets:

| Area | Alignment target | CRAMPS use |
|---|---|---|
| Review reporting | PRISMA 2020 | Transparent source flow, eligibility, extraction, synthesis, limitations |
| Protocol reporting | PRISMA-P | Locked protocol before extraction and scoring |
| Missing evidence | Cochrane Handbook | Bias due to missing nulls, selective reporting, publication bias |
| Statistical reporting | SAMPL, ASA guidance | Clear methods, uncertainty, p-value limits, ethical inference |
| HEP/astro statistics | PDG and field practice | Nuisance parameters, trials factors, look-elsewhere handling |
| Measurement uncertainty | JCGM GUM | Coordinate uncertainty and propagation |
| Data stewardship | FAIR, DataCite | Findable, reusable, citable study objects |
| Provenance | W3C PROV | Source lineage, extraction lineage, transform lineage |
| Quality management | ISO 9001 | Document control, risk management, corrective action |
| Test competence | ISO/IEC 17025 | Method validation, traceability, impartiality, uncertainty |
| Security | ISO/IEC 27001 | Restricted-data access, secrets, audit logging |
| Repository trust | CoreTrustSeal | Preservation, metadata, continuity, fixity |
| AI governance | NIST AI RMF | Agent risk mapping, human review, failure tracking |
| Attribution | CRediT | Contributor role clarity |

These standards are not treated as badges. They define controls the program must implement.

## 4. Required Practices

### 4.1 Pre-specification

Every confirmatory CRAMPS study must lock:

- Candidate coordinates.
- Coordinate transforms.
- Inclusion and exclusion criteria.
- Source search strategy.
- Extraction fields.
- Tolerance windows.
- Independence rules.
- Bias assessment rules.
- Primary statistic.
- Null model.
- Sensitivity tests.
- Reporting language constraints.

The lock must include timestamp, protocol hash, responsible person, and amendment procedure.

### 4.2 Separation of Work Modes

CRAMPS recognizes three work modes:

| Mode | Purpose | Claim limit |
|---|---|---|
| Exploratory | Build atlas, discover possible coordinates | Hypothesis generation only |
| Confirmatory | Test locked coordinates against existing data | Cross-catalog coherence under registered null |
| Prospective | Test locked coordinates against future or held-out data | Stronger prioritization signal, still not discovery |

Exploratory findings cannot be re-labeled as confirmatory without a new blind-locked protocol.

### 4.3 Source Completeness

Source search must include:

- Anomaly papers.
- Null searches.
- Exclusion results.
- Collaboration pages.
- Public datasets.
- Relevant review bibliographies.
- Non-event searches that inspected the coordinate range.

The source flow must report identified, screened, eligible, included, excluded, and quarantined records.

### 4.4 Evidence Independence

Rows must be audited for shared:

- Detector or instrument.
- Collaboration or team.
- Raw dataset.
- Public data release.
- Calibration chain.
- Reconstruction pipeline.
- Simulation background.
- Theory-motivated scan value.
- Plot extraction source.

Duplicate or derivative rows must not be treated as independent evidence.

### 4.5 Statistical Conservatism

The statistical lead must ensure:

- Local and global results are separated.
- Look-elsewhere correction is reported.
- Multiple coordinate families are accounted for.
- Null models preserve important literature and detector structure.
- Monte Carlo uncertainty is reported.
- Sensitivity failures are visible.
- Negative controls are included.

No CRAMPS report may headline an uncorrected local result.

### 4.6 Missing Evidence

Every study must assess:

- Missing nulls.
- Unpublished non-events.
- Selective threshold reporting.
- Publication bias.
- Search-range fashion.
- Review-article amplification.
- Public-data reuse.

High missing-evidence risk requires demotion or explicit limitation.

### 4.7 Reproducibility

Every externally shared CRAMPS result must include:

- Data contract files.
- Analysis code.
- Dependency manifest.
- Checksums.
- Protocol hash.
- Run instructions.
- Expected output hashes or summary statistics.
- Reproducibility report.

If raw sources cannot be redistributed, the capsule must include source pointers, hashes where possible, and an explicit restricted-data note.

## 5. Document Control

Every policy, protocol, data contract, and report must include:

- Title.
- Version.
- Date.
- Owner.
- Status.
- Parent document or study ID.
- Change log or amendment log.

Major changes after protocol lock require amendment records.

Major changes include:

- New candidate coordinate.
- New coordinate transform.
- New primary statistic.
- New null model.
- New inclusion criterion.
- New exclusion criterion.
- New dependence weighting.
- New sensitivity test added after result inspection.

Administrative changes include:

- Typographic fixes.
- Citation formatting.
- File path correction.
- Clarifying prose that does not change analysis behavior.

## 6. Quality Gates

### Gate A: Protocol Gate

Required before extraction:

- Study charter complete.
- Roles assigned.
- Protocol complete.
- Candidate registry complete or exploratory status declared.
- Data contracts selected.
- Amendment log initialized.

### Gate B: Extraction Gate

Required before normalization:

- Source flow complete.
- Exclusion reasons complete.
- Row-level provenance complete.
- Extraction confidence assigned.
- Ambiguous rows quarantined.

### Gate C: Normalization Gate

Required before analysis:

- Raw values preserved.
- Normalized values reproducible.
- Transform registry complete.
- Uncertainty status assigned.
- Forbidden transforms excluded.

### Gate D: Independence and Bias Gate

Required before primary scoring:

- Independence grades complete.
- Bias assessment complete.
- Missing-evidence assessment complete.
- Primary weights approved.
- Non-independent duplicates collapsed or modeled.

### Gate E: Statistical Gate

Required before reporting:

- Primary statistic matches protocol.
- Null model matches protocol.
- Global correction complete.
- Negative controls run.
- Sensitivity tests run.
- Monte Carlo uncertainty reported.

### Gate F: Release Gate

Required before external release:

- Reproducibility capsule runs cleanly.
- Red-team review complete.
- Statistical lead approves language.
- Data steward approves release rights.
- Evidence tier assigned.
- Limitations explicit.

## 7. Deviations and Corrective Actions

A deviation occurs when study execution differs from the locked protocol or this policy.

Deviation records must include:

- Deviation ID.
- Date.
- Description.
- Discovery point.
- Affected files.
- Result-blind status.
- Impact assessment.
- Corrective action.
- Preventive action.
- Approval.

If a deviation affects primary inference after result inspection, the result must be demoted unless an independent reviewer determines the change is purely administrative.

## 8. Accreditation-Ready Controls

CRAMPS may claim "accreditation-ready" only when the following are present:

- Approved SOP.
- Standards and practices policy.
- Methodology policy.
- Cross-unit checksum guideline.
- Role and competency records.
- Training records.
- Internal audit record.
- Corrective action log.
- Reproducibility evidence.
- Document control.
- Data retention and security policy.
- External review trail.

CRAMPS may not claim formal accreditation without external accreditation.

## 9. Reporting Policy

Permitted language:

- "pre-specified coordinate test"
- "cross-catalog recurrence"
- "cluster coherence"
- "under the registered null model"
- "global result"
- "priority for prospective testing"

Restricted language:

- "discovery"
- "proof"
- "confirmed new physics"
- "combined weak signals prove"
- "independent evidence" without independence audit
- "sigma" without calibrated null and global correction

Every public report must state:

> CRAMPS is an anomaly synthesis and prioritization method. It does not replace direct experimental confirmation or field-specific discovery thresholds.

## 10. Ownership

Minimum owners:

- Program owner.
- Protocol steward.
- Statistical lead.
- Data steward.
- Independence auditor.
- Bias auditor.
- Reproducibility lead.

The statistical lead and data steward both hold release veto authority.

## 11. Review Cycle

This policy should be reviewed:

- Before each new confirmatory study.
- After any major deviation.
- After failed reproduction.
- After external review.
- At least every six months while CRAMPS is active.

