#!/usr/bin/env python3
"""Generate domain-specific CRAMPACS starter packs and printouts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOMAINS = [
    {
        "slug": "med",
        "upper": "CRAMPACS-MED",
        "lower": "crampacs-med",
        "label": "Medicine and clinical evidence",
        "coordinates": "dose, exposure window, biomarker threshold, adverse-event onset, phenotype, care setting",
        "nulls": "negative safety analyses, monitored adverse events not elevated, failed replications, cohorts with exposure but no event",
        "gotcha": "confounding by indication, differential coding, missing nulls, surveillance bias",
    },
    {
        "slug": "gen",
        "upper": "CRAMPACS-GEN",
        "lower": "crampacs-gen",
        "label": "Genomics and omics",
        "coordinates": "locus, variant, gene, pathway, cell type, tissue, expression threshold, perturbation",
        "nulls": "failed replications, non-significant loci, negative functional assays, tested pathways not enriched",
        "gotcha": "population stratification, batch effects, genome-build drift, winner's curse",
    },
    {
        "slug": "clim",
        "upper": "CRAMPACS-CLIM",
        "lower": "crampacs-clim",
        "label": "Climate and Earth systems",
        "coordinates": "latitude, longitude, depth, pressure level, season, climate mode, threshold, basin",
        "nulls": "comparable regions without anomaly, model runs without recurrence, negative attribution studies",
        "gotcha": "spatial autocorrelation, temporal autocorrelation, non-stationary baseline, model-family dependence",
    },
    {
        "slug": "mat",
        "upper": "CRAMPACS-MAT",
        "lower": "crampacs-mat",
        "label": "Materials science",
        "coordinates": "composition ratio, dopant level, phase, lattice parameter, processing temperature, operating condition",
        "nulls": "failed syntheses, tested materials without property jump, simulations with no predicted anomaly",
        "gotcha": "unreported failed syntheses, hidden processing parameters, batch variation, simulation convergence artifacts",
    },
    {
        "slug": "eng",
        "upper": "CRAMPACS-ENG",
        "lower": "crampacs-eng",
        "label": "Engineering reliability",
        "coordinates": "load, vibration frequency, temperature, firmware version, supplier lot, cycle count, failure mode",
        "nulls": "units exposed without failure, passed qualification tests, lots with no anomaly, sensor streams without recurrence",
        "gotcha": "fleet exposure imbalance, maintenance censoring, supplier-lot dependence, sensor drift",
    },
    {
        "slug": "fin",
        "upper": "CRAMPACS-FIN",
        "lower": "crampacs-fin",
        "label": "Finance, fraud, and risk",
        "coordinates": "asset, tenor, counterparty, time window, transaction velocity, network position, model threshold",
        "nulls": "cleared alerts, comparable accounts without event, backtests with no breach, control portfolios",
        "gotcha": "look-ahead bias, backtest overfitting, vendor revisions, feedback loops from prior controls",
    },
    {
        "slug": "cyb",
        "upper": "CRAMPACS-CYB",
        "lower": "crampacs-cyb",
        "label": "Cybersecurity",
        "coordinates": "CVE, ATT&CK technique, port, protocol, endpoint class, time-to-exploit, detection rule",
        "nulls": "exposed assets not exploited, rules with no hits, scanned vulnerabilities not exploited, false positives",
        "gotcha": "sensor coverage gaps, duplicate intel feeds, alert suppression, honeypot selection bias",
    },
    {
        "slug": "ast",
        "upper": "CRAMPACS-AST",
        "lower": "crampacs-ast",
        "label": "Astronomy and astrophysics",
        "coordinates": "sky coordinate, redshift, wavelength, period, phase, cadence, source class",
        "nulls": "follow-up non-detections, survey fields with no event, searched spectral windows with no feature",
        "gotcha": "sky coverage bias, cadence bias, follow-up selection bias, calibration drift",
    },
    {
        "slug": "phy",
        "upper": "CRAMPACS-PHY",
        "lower": "crampacs-phy",
        "label": "Physics and physical anomaly catalogs",
        "coordinates": "mass, energy, frequency, redshift, coupling, cross section, decay channel, event topology",
        "nulls": "null searches, exclusion contours, control regions, sidebands, non-detections, failed replications",
        "gotcha": "look-elsewhere effect, theory-fashion clustering, shared detector pipelines, plot digitization error",
    },
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def domain_readme(domain: dict[str, str]) -> str:
    return f"""
# {domain["upper"]} / {domain["lower"]} Starter Pack

**Domain:** {domain["label"]}

This pack contains domain-specific printable templates for both:

- `{domain["lower"]}` lightweight preflight
- `{domain["upper"]}` full assurance study

Use the lowercase documents for a one to two day triage pass. Use the uppercase documents only after creating a full protocol lock and importing the preflight package with review disposition.

## Files

- `{domain["lower"]}_PREFLIGHT_SCOPE.md`
- `{domain["lower"]}_PREFLIGHT_SOURCES.csv`
- `{domain["lower"]}_PREFLIGHT_ROWS.csv`
- `{domain["lower"]}_PREFLIGHT_GOTCHAS_PRINTABLE.md`
- `{domain["lower"]}_PREFLIGHT_DECISION.md`
- `{domain["upper"]}_FULL_PROTOCOL_ADDENDUM.md`
- `{domain["upper"]}_RELEASE_GATE_PRINTABLE.md`

## Domain Coordinates

{domain["coordinates"]}

## Domain Nulls

{domain["nulls"]}

## Main Gotcha

{domain["gotcha"]}
"""


def preflight_scope(domain: dict[str, str]) -> str:
    return f"""
# {domain["lower"]} Preflight Scope

**Domain:** {domain["label"]}  
**Target full system if escalated:** {domain["upper"]}  
**Date:**  
**Decision owner:**  

## One-Sentence Question

Does weak evidence recur at a pre-specified coordinate in {domain["label"]} strongly enough to justify a full {domain["upper"]} study?

## Candidate Coordinate Sketch

Domain coordinate examples: {domain["coordinates"]}

| coordinate_id | coordinate_family | value_or_range | units | tolerance_sketch | why_it_matters |
|---|---|---|---|---|---|

## Source Boundary

Included source types:

-

Excluded source types:

-

## Minimum Null or Non-Event Search

Look for: {domain["nulls"]}

## Preflight Claim Boundary

This is `{domain["lower"]}`. It can produce a triage decision only. It is not a `{domain["upper"]}` confirmatory result.
"""


def preflight_sources(domain: dict[str, str]) -> str:
    return """source_id,citation_or_label,url_or_path,source_type,domain,source_role,publication_or_snapshot_date,unit_or_site,known_dependence,screening_status,notes"""


def preflight_rows(domain: dict[str, str]) -> str:
    return """row_id,source_id,coordinate_label,coordinate_value,coordinate_units,row_type,result_direction,uncertainty_status,extraction_confidence,dependence_concern,bias_concern,null_or_non_event_flag,notes"""


def gotchas(domain: dict[str, str]) -> str:
    return f"""
# {domain["lower"]} Gotchas Printable

**Domain:** {domain["label"]}

## Top Domain Gotcha

{domain["gotcha"]}

## Ten Fast Checks

| Check | Pass/Hold/Fail | Notes |
|---|---|---|
| Coordinate can be stated precisely |  |  |
| Coordinate was chosen before scoring |  |  |
| Nulls and non-events were found |  |  |
| Rows are not all from one source family |  |  |
| Units and transforms are clear |  |  |
| Tolerance window is justified before scoring |  |  |
| Domain-specific bias was checked |  |  |
| One-source removal would not collapse the case |  |  |
| Negative control is identified or run |  |  |
| Package hashes can reproduce the artifact set |  |  |

## Domain-Specific Stop Signs

- No null or non-event evidence can be identified.
- Coordinate units or reference systems are unclear.
- Evidence is concentrated in one source family.
- The suspected pattern depends on a post-hoc tolerance.
- The team wants a full assurance claim from this preflight.

## Escalation Note

Escalate only if the preflight package can be imported into `{domain["upper"]}` with review disposition.
"""


def decision(domain: dict[str, str]) -> str:
    return f"""
# {domain["lower"]} Preflight Decision

**Domain:** {domain["label"]}  
**Date:**  
**Decision owner:**  

## Decision

Choose one:

- advance_to_{domain["upper"]}
- hold_coordinate_lock
- hold_source_completeness
- hold_dependence_or_bias
- stop

## Rationale

## Strongest Positive Evidence

## Strongest Null or Non-Event

## Biggest Gotcha

{domain["gotcha"]}

## What Would Change the Decision

## Import Notes for Full System

If escalated, list which artifacts should seed `{domain["upper"]}` and which should be quarantined or reworked.

## Claim Boundary

This is `{domain["lower"]}`. No confirmatory claim is made.
"""


def full_addendum(domain: dict[str, str]) -> str:
    return f"""
# {domain["upper"]} Full Protocol Addendum

**Domain:** {domain["label"]}

Use this addendum with `templates/CRAMPACS_PROTOCOL_TEMPLATE.md`.

## Domain Coordinate Families

{domain["coordinates"]}

## Domain Nulls and Non-Events

{domain["nulls"]}

## Domain Dependence Hazards

List the source families, instruments, vendors, sites, pipelines, datasets, or reporting systems that could make rows non-independent.

## Domain Bias Hazards

Primary gotcha: {domain["gotcha"]}

Add domain-specific publication, reporting, measurement, selection, and survivorship biases.

## Required Negative Controls

Define at least one coordinate, source class, or row family expected not to recur.

## Domain Checksum Additions

List required hashes for domain-specific source systems, units, transforms, vocabularies, reference systems, or vendor snapshots.

## Claim Limits

This `{domain["upper"]}` study can produce a full CRAMPACS evidence package only after protocol lock, full source flow, null inclusion, independence review, bias review, null-model analysis, sensitivity tests, checksum reproduction, and signoff.
"""


def release_gate(domain: dict[str, str]) -> str:
    return f"""
# {domain["upper"]} Release Gate Printable

**Domain:** {domain["label"]}

| Gate | Pass/Hold/Fail | Evidence |
|---|---|---|
| Protocol locked |  |  |
| Preflight import disposition complete |  |  |
| Candidate registry locked |  |  |
| Source flow complete |  |  |
| Nulls and non-events included |  |  |
| Raw rows reviewed |  |  |
| Normalized rows reproducible |  |  |
| Independence grades complete |  |  |
| Bias assessment complete |  |  |
| Null model run |  |  |
| Global correction reported |  |  |
| Sensitivity tests run |  |  |
| Negative controls run |  |  |
| Sidecar metrics reviewed |  |  |
| Checksums reproduce |  |  |
| Domain lead signoff |  |  |
| Statistical lead signoff |  |  |
| Claim language approved |  |  |

## Release Decision

Choose one:

- release
- hold_for_rework
- demote_to_exploratory
- stop

## Required Boundary

CRAMPACS does not replace domain-standard confirmation.
"""


def field_printout(domain: dict[str, str]) -> str:
    return f"""
# {domain["upper"]} / {domain["lower"]} Field Printout

**Domain:** {domain["label"]}

## Use Lowercase When

Use `{domain["lower"]}` when the team needs a one to two day triage pass.

Output:

- coordinate sketch
- source shortlist
- gotcha scan
- sidecar metrics
- escalation decision

## Use Uppercase When

Use `{domain["upper"]}` when the result may support formal research, audit-ready decision support, safety/security escalation, regulated review, or external reporting.

Output:

- locked protocol
- full data contracts
- null model
- sensitivity tests
- reproducibility capsule
- evidence tier

## Main Coordinates

{domain["coordinates"]}

## Nulls to Find

{domain["nulls"]}

## Biggest Gotcha

{domain["gotcha"]}

## Practitioner Rule

Lowercase can seed uppercase. Lowercase cannot claim uppercase assurance.
"""


def main() -> int:
    for domain in DOMAINS:
        folder = ROOT / "domain_packs" / domain["slug"]
        write(folder / "README.md", domain_readme(domain))
        write(folder / f"{domain['lower']}_PREFLIGHT_SCOPE.md", preflight_scope(domain))
        write(folder / f"{domain['lower']}_PREFLIGHT_SOURCES.csv", preflight_sources(domain))
        write(folder / f"{domain['lower']}_PREFLIGHT_ROWS.csv", preflight_rows(domain))
        write(folder / f"{domain['lower']}_PREFLIGHT_GOTCHAS_PRINTABLE.md", gotchas(domain))
        write(folder / f"{domain['lower']}_PREFLIGHT_DECISION.md", decision(domain))
        write(folder / f"{domain['upper']}_FULL_PROTOCOL_ADDENDUM.md", full_addendum(domain))
        write(folder / f"{domain['upper']}_RELEASE_GATE_PRINTABLE.md", release_gate(domain))
        write(ROOT / "printouts" / f"{domain['slug']}_field_printout.md", field_printout(domain))

    write(
        ROOT / "printouts" / "crampacs_preflight_1_to_2_day_printout.md",
        """
# crampacs 1-2 Day Preflight Printout

## Inputs

- Domain suffix:
- Question:
- Candidate coordinate:
- Units:
- Tolerance sketch:
- Decision owner:

## Required Artifacts

| Artifact | Done | Notes |
|---|---|---|
| preflight_scope.md |  |  |
| preflight_sources.csv |  |  |
| preflight_rows.csv |  |  |
| preflight_gotchas.md |  |  |
| preflight_decision.md |  |  |
| sidecar metrics |  |  |

## Stop Signs

- No coordinate lock.
- No nulls.
- One source family.
- Units unclear.
- Dependence unknown.
- Bias ignored.
- Team wants a full assurance claim.

## Decision

- advance_to_CRAMPACS
- hold_coordinate_lock
- hold_source_completeness
- hold_dependence_or_bias
- stop
""",
    )

    write(
        ROOT / "printouts" / "CRAMPACS_full_assurance_gate_printout.md",
        """
# CRAMPACS Full Assurance Gate Printout

| Gate | Pass/Hold/Fail | Evidence |
|---|---|---|
| Protocol locked |  |  |
| Candidate registry locked |  |  |
| Source flow complete |  |  |
| Nulls and non-events included |  |  |
| Raw rows reviewed |  |  |
| Normalized rows reproducible |  |  |
| Independence grades complete |  |  |
| Bias assessment complete |  |  |
| Null model registered and run |  |  |
| Global correction reported |  |  |
| Sensitivity tests run |  |  |
| Negative controls run |  |  |
| Checksum package complete |  |  |
| Sidecar metrics reviewed |  |  |
| Reproducibility run complete |  |  |
| Red-team review complete |  |  |
| Domain lead signoff |  |  |
| Statistical lead signoff |  |  |
| Claim language approved |  |  |

## Release Decision

- release
- hold_for_rework
- demote_to_exploratory
- stop
""",
    )

    write(
        ROOT / "printouts" / "preflight_to_full_composition_printout.md",
        """
# Preflight to Full CRAMPACS Composition Printout

## Preflight Import

| Preflight artifact | Hash recorded | Review disposition | Notes |
|---|---|---|---|
| preflight_scope.md |  |  |  |
| preflight_sources.csv |  |  |  |
| preflight_rows.csv |  |  |  |
| preflight_gotchas.md |  |  |  |
| preflight_decision.md |  |  |  |
| sidecar metrics |  |  |  |

## Dispositions

- accepted_for_protocol
- accepted_for_background
- needs_rework
- rejected
- quarantined

## Rule

The preflight can seed the full system. The full-system claim begins only after the full protocol lock.
""",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

