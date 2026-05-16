# cramps-med / CRAMPS-MED Domain Governance Printable

**Domain:** Medicine and clinical evidence

## Assurance Split

- `cramps-med`: one to two day preflight.
- `CRAMPS-MED`: full assurance system after protocol lock.

## Coordinates

- dose
- exposure window
- biomarker threshold
- adverse-event onset
- phenotype
- care setting

## Nulls and Non-Events

- negative safety analyses
- monitored adverse events not elevated
- failed replications
- cohorts with exposure but no event

## Failure Modes

- confounding by indication
- differential coding
- missing nulls
- surveillance bias

## Standards Anchors

- PRISMA
- STROBE/RECORD/CONSORT/STARD
- FDA RWE
- ICH GCP
- HIPAA
- 21 CFR Part 11

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
