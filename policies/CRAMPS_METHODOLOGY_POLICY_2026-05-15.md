# CRAMPS Methodology Policy

**Policy ID:** CRAMPS-MP-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft methodology policy  
**Parent SOP:** `CRAMPS_PROGRAM_SOP_2026-05-15.md`

## 1. Purpose

This policy defines the methodological rules for any CRAMPS study, regardless of domain.

CRAMPS tests whether weak signals, anomalies, non-events, exclusions, residuals, failures, or near-misses recur at pre-specified coordinates more often than expected under a registered null model.

The method is domain-general. Physics is one use case. The same structure can apply to medicine, genomics, climate, materials science, engineering reliability, finance, cybersecurity, and astronomy when the evidence can be mapped into a coordinate system.

## 2. Core Method

A CRAMPS study must define:

1. A coordinate ontology.
2. A source universe.
3. A row-level extraction contract.
4. A candidate coordinate registry.
5. A null and non-event inclusion rule.
6. A dependence model.
7. A bias and missing-evidence model.
8. A primary cluster statistic.
9. A realistic null generator.
10. A sensitivity and negative-control plan.
11. A conservative reporting tier.

If any of these are missing, the study is exploratory only.

## 3. Coordinate Ontology

Every domain overlay must define its coordinate families.

Examples:

- Physics: mass, energy, frequency, redshift, coupling, decay channel.
- Medicine: dose, biomarker value, exposure window, phenotype, adverse-event onset time.
- Finance: asset, tenor, counterparty class, transaction time, volatility regime, network position.
- Cybersecurity: CVE, attack technique, port, protocol, endpoint class, time-to-exploit.

Coordinate definitions must include:

- Canonical units.
- Allowed transforms.
- Forbidden transforms.
- Tolerance windows.
- Resolution limits.
- Known coordinate aliases.
- Negative control coordinates.

## 4. Study Modes

### 4.1 Exploratory Mode

Exploratory mode builds an atlas and proposes candidate coordinates. It may not make confirmatory claims.

Output language:

> This exploratory CRAMPS atlas identified a possible coordinate recurrence. The coordinate requires a new locked protocol before confirmatory scoring.

### 4.2 Confirmatory Mode

Confirmatory mode tests locked coordinates against existing data. It requires a locked protocol before scoring.

Output language:

> This confirmatory CRAMPS study found cross-catalog recurrence at a pre-specified coordinate under the registered null model.

### 4.3 Prospective Mode

Prospective mode tests locked coordinates against future or held-out data.

Output language:

> This prospective CRAMPS study observed recurrence at a pre-specified coordinate in held-out or future evidence.

## 5. Inclusion Method

Rows enter a study only if they satisfy:

- Source eligibility.
- Coordinate observability.
- Row-level provenance.
- Uncertainty status.
- Dependence grading.
- Bias assessment.
- Data-use rights.

Rows must not be included because they support the preferred result.

## 6. Null and Non-Event Method

Each domain overlay must define what counts as:

- A null result.
- A failed detection.
- An exclusion.
- A non-event.
- A negative control.
- A silent or missing result.

Nulls and non-events are first-class evidence. A CRAMPS analysis that includes only positive anomalies is not confirmatory.

## 7. Dependence Method

The independence auditor must map shared evidence paths.

Dependence can arise through:

- Same raw dataset.
- Same instrument.
- Same institution or collaboration.
- Same calibration process.
- Same extraction pipeline.
- Same simulation model.
- Same vendor or supplier.
- Same reporting platform.
- Same public benchmark.
- Same theory or search fashion.

Primary analysis must collapse, weight, or model dependent rows.

## 8. Bias Method

Every study must assess:

- Publication bias.
- Reporting bias.
- Availability bias.
- Selection bias.
- Survivorship bias.
- Measurement bias.
- Extraction bias.
- Model bias.
- Coordinate-fashion bias.
- Missing-evidence bias.

Domain overlays may add domain-specific bias terms.

## 9. Primary Statistics

Permitted primary statistics include:

- Dependence-adjusted count within a locked tolerance window.
- Weighted recurrence score.
- Coordinate density excess.
- Hierarchical cluster-intensity model.
- Signed residual aggregation with covariance.
- Posterior predictive tail probability under a registered Bayesian model.
- Registered risk-lift statistic for operational domains.

The primary statistic must be locked before scoring.

## 10. Null Models

Null models must preserve enough structure to make the test meaningful.

Minimum null model levels:

- Level 1: coordinate shuffling within eligible source ranges.
- Level 2: source-aware null preserving era, modality, and reporting threshold.
- Level 3: instrument or system-process null preserving measurement resolution, operational thresholds, and known background.
- Level 4: domain-specific generative null reviewed by a domain expert.

Confirmatory studies should use Level 2 or higher unless justified.

## 11. Sensitivity Requirements

Every confirmatory study must run:

- Leave-one-source-out.
- Leave-one-family-out.
- Leave-one-era-out.
- Leave-one-modality-out where applicable.
- High-bias-row exclusion.
- Low-independence-row exclusion.
- Tolerance-window sweep.
- Null-model-strength sweep.
- Negative control coordinates.
- Missing-null stress test.

If a result fails a sensitivity test, it may still be interesting, but it must be labeled fragile.

## 12. Claim Tiers

| Tier | Meaning | Claim limit |
|---|---|---|
| 0 | Exploratory atlas | Hypothesis-generating only |
| 1 | Locked retrospective | Cross-catalog recurrence under registered null |
| 2 | Independently reproduced | Reproducible recurrence under same contract |
| 3 | Prospective holdout | Recurrence observed in future or held-out data |
| 4 | Domain confirmation | Direct domain-specific confirmation under field standards |

Tier 4 is not granted by CRAMPS alone. It requires the domain's normal confirmation standard.

## 13. Domain Overlay Requirement

Each domain must have an overlay defining:

- Domain coordinates.
- Eligible source types.
- Row types.
- Null and non-event definition.
- Dependence hazards.
- Bias hazards.
- Null model requirements.
- Reporting limits.
- Standards anchors.
- Security and privacy constraints.

The overlay is part of the method contract. A generic CRAMPS SOP is not enough for a regulated or high-stakes domain.

## 14. Methodological Vetoes

The statistical lead may veto a result for:

- Post-hoc coordinate selection.
- Incomplete source universe.
- Missing null evidence.
- Unmodeled dependence.
- Unrealistic null model.
- Inadequate look-elsewhere correction.
- Sensitivity collapse.
- Data rights uncertainty.
- Overclaiming.

The domain lead may veto if the coordinate or row interpretation is not meaningful in the domain.

## 15. Methodology Review Cycle

This policy must be reviewed:

- After each pilot.
- After each failed reproduction.
- After external statistical review.
- After a new domain overlay is added.
- Before any Tier 2 or higher claim.

