# CRAMPACS-CYB Cybersecurity Overlay

**Domain:** Cybersecurity, threat intelligence, vulnerability management, detection engineering, incident response, and fraud-adjacent security telemetry

## Definition

CRAMPACS-CYB tests whether weak security indicators, alerts, exploit traces, vulnerabilities, or behavioral anomalies recur at pre-specified cyber coordinates more often than expected under a registered infrastructure and threat-activity null model.

## Coordinate Families

- CVE, CWE, CVSS vector, exploit maturity.
- MITRE ATT&CK tactic, technique, procedure.
- Port, protocol, service, endpoint class, identity type.
- Time-to-exploit, patch age, exposure window.
- Domain, ASN, IP range, certificate, file hash, process lineage.
- Detection rule, SIEM field, EDR sensor, cloud control plane.

## Eligible Rows

- Low-confidence alerts.
- Honeypot hits.
- Vulnerability scan signals.
- Exploit attempts.
- Incident near-misses.
- Threat intel sightings.
- Detection-rule residuals.
- Null detections from monitored assets.
- Closed false-positive cases.

## Null and Non-Events

Nulls include:

- Exposed assets not exploited.
- Alert rules with no hits.
- Vulnerabilities scanned but not observed exploited.
- Similar tenants or networks without recurrence.
- False positives after investigation.

## Dependence Hazards

- Same sensor fleet.
- Same SIEM parser.
- Same EDR vendor.
- Same detection rule.
- Same threat-intel feed.
- Same honeypot network.
- Same cloud region.
- Same asset inventory.
- Same incident response playbook.

## Bias Hazards

- Sensor coverage gaps.
- Alert suppression.
- Vendor feed amplification.
- Base-rate neglect.
- Duplicate indicator sharing.
- Honeypot selection bias.
- Survivorship bias from remediated systems.
- Adversary adaptation.
- Reporting bias toward high-profile CVEs.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve asset exposure, sensor coverage, network segment, time window, vulnerability population, and alert opportunity.

Preferred null:

- Threat-informed generative null using ATT&CK behavior, exploitability, exposure, and patch state.

## Standards Anchors

- NIST Cybersecurity Framework 2.0.
- NIST AI RMF where AI detection systems are used.
- MITRE ATT&CK for adversary behavior taxonomy.
- CISA Known Exploited Vulnerabilities catalog for exploitation status.
- FIRST CVSS v4.0 for vulnerability severity scoring.
- ISO/IEC 27001 for security management controls.
- STIX/TAXII where threat intelligence exchange is used.

## Checksum Additions

- ATT&CK version.
- CVE/CVSS version.
- Detection rule hash.
- Log parser version.
- Sensor ID.
- Asset inventory snapshot.
- Threat-intel feed snapshot.
- Evidence chain hash.

## Claim Limits

CRAMPACS-CYB can prioritize threat, vulnerability, or detection coordinates. It cannot establish attribution, compromise, exploitability, or legal responsibility without incident response and forensic validation.

