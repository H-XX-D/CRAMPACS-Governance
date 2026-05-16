# CRAMPS-CYB Full Protocol Addendum

**Domain:** Cybersecurity

Use this addendum with `../../templates/CRAMPS_PROTOCOL_TEMPLATE.md`.

## Domain Coordinate Families

CVE, ATT&CK technique, port, protocol, endpoint class, time-to-exploit, detection rule

## Domain Nulls and Non-Events

exposed assets not exploited, rules with no hits, scanned vulnerabilities not exploited, false positives

## Domain Dependence Hazards

List the source families, instruments, vendors, sites, pipelines, datasets, or reporting systems that could make rows non-independent.

## Domain Bias Hazards

Primary failure modes: sensor coverage gaps, duplicate intel feeds, alert suppression, honeypot selection bias

Add domain-specific publication, reporting, measurement, selection, and survivorship biases.

## Required Negative Controls

Define at least one coordinate, source class, or row family expected not to recur.

## Domain Checksum Additions

List required hashes for domain-specific source systems, units, transforms, vocabularies, reference systems, or vendor snapshots.

## Domain Standards Anchors

NIST CSF 2.0, MITRE ATT&CK, CISA KEV, CVSS v4, ISO 27001, STIX/TAXII

## Claim Limits

Release condition: this `CRAMPS-CYB` study remains a working package until protocol lock, full source flow, null inclusion, independence review, bias review, null-model analysis, sensitivity tests, checksum reproduction, trust-state review, domain signoff, and claim-language approval are complete.
