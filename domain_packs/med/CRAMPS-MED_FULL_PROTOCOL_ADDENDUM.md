# CRAMPS-MED Full Protocol Addendum

**Domain:** Medicine and clinical evidence

Use this addendum with `../../templates/CRAMPS_PROTOCOL_TEMPLATE.md`.

## Domain Coordinate Families

dose, exposure window, biomarker threshold, adverse-event onset, phenotype, care setting

## Domain Nulls and Non-Events

negative safety analyses, monitored adverse events not elevated, failed replications, cohorts with exposure but no event

## Domain Dependence Hazards

List the source families, instruments, vendors, sites, pipelines, datasets, or reporting systems that could make rows non-independent.

## Domain Bias Hazards

Primary gotcha: confounding by indication, differential coding, missing nulls, surveillance bias

Add domain-specific publication, reporting, measurement, selection, and survivorship biases.

## Required Negative Controls

Define at least one coordinate, source class, or row family expected not to recur.

## Domain Checksum Additions

List required hashes for domain-specific source systems, units, transforms, vocabularies, reference systems, or vendor snapshots.

## Domain Standards Anchors

PRISMA, STROBE/RECORD/CONSORT/STARD, FDA RWE, ICH GCP, HIPAA, 21 CFR Part 11

## Claim Limits

This `CRAMPS-MED` study can produce a full CRAMPS evidence package only after protocol lock, full source flow, null inclusion, independence review, bias review, null-model analysis, sensitivity tests, checksum reproduction, and signoff.
