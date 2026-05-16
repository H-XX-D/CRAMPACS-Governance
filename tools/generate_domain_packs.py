#!/usr/bin/env python3
"""Generate domain-specific CRAMPACS starter packs and printouts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_domains() -> list[dict[str, str]]:
    raw = json.loads((ROOT / "tools" / "crampacs_domains.json").read_text(encoding="utf-8"))
    domains = []
    for item in raw:
        domains.append(
            {
                "slug": item["slug"],
                "upper": item["full"],
                "lower": item["light"],
                "label": item["label"],
                "coordinates": ", ".join(item["coordinates"]),
                "nulls": ", ".join(item["nulls"]),
                "gotcha": ", ".join(item["gotchas"]),
                "standards": ", ".join(item["standards"]),
            }
        )
    return domains


DOMAINS = load_domains()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def domain_readme(domain: dict[str, str]) -> str:
    return f"""
# {domain["lower"]} / {domain["upper"]} Starter Pack

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
- `{domain["upper"]}_DOMAIN_GOVERNANCE_PRINTABLE.md`

## Domain Coordinates

{domain["coordinates"]}

## Domain Nulls

{domain["nulls"]}

## Main Gotcha

{domain["gotcha"]}

## Standards Anchors

{domain["standards"]}
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

Use this addendum with `../../templates/CRAMPACS_PROTOCOL_TEMPLATE.md`.

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

## Domain Standards Anchors

{domain["standards"]}

## Claim Limits

This `{domain["upper"]}` study can produce a full CRAMPACS evidence package only after protocol lock, full source flow, null inclusion, independence review, bias review, null-model analysis, sensitivity tests, checksum reproduction, and signoff.
"""


def domain_governance_printable(domain: dict[str, str]) -> str:
    return f"""
# {domain["lower"]} / {domain["upper"]} Domain Governance Printable

**Domain:** {domain["label"]}

## Assurance Split

- `{domain["lower"]}`: one to two day preflight.
- `{domain["upper"]}`: full assurance system after protocol lock.

## Coordinates

{chr(10).join(f"- {x.strip()}" for x in domain["coordinates"].split(","))}

## Nulls and Non-Events

{chr(10).join(f"- {x.strip()}" for x in domain["nulls"].split(","))}

## Gotchas

{chr(10).join(f"- {x.strip()}" for x in domain["gotcha"].split(","))}

## Standards Anchors

{chr(10).join(f"- {x.strip()}" for x in domain["standards"].split(","))}

## Field Gate

| Gate | Pass/Hold/Fail | Notes |
|---|---|---|
| Coordinate specified |  |  |
| Nulls found |  |  |
| Dependence mapped |  |  |
| Bias reviewed |  |  |
| Units checked |  |  |
| Sidecar run |  |  |
| Escalation decision made |  |  |
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
# {domain["lower"]} / {domain["upper"]} Field Printout

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

## Standards Anchors

{domain["standards"]}

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
        write(folder / f"{domain['upper']}_DOMAIN_GOVERNANCE_PRINTABLE.md", domain_governance_printable(domain))
        write(ROOT / "printouts" / f"{domain['slug']}_field_printout.md", field_printout(domain))

    write(
        ROOT / "printouts" / "crampacs_preflight_1_to_2_day_printout.md",
        """
# crampacs-* 1-2 Day Preflight Printout

Use this only for the lowercase preflight route, for example `crampacs-med`.
If escalated, the decision must name the matching uppercase full system, for example `CRAMPACS-MED`.

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
| preflight_manifest.csv |  |  |
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

- advance_to_CRAMPACS-<DOMAIN>
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
| preflight_manifest.csv |  |  |  |
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
