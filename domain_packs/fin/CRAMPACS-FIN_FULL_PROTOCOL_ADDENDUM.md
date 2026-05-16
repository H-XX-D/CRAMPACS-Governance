# CRAMPACS-FIN Full Protocol Addendum

**Domain:** Finance, fraud, and risk

Use this addendum with `templates/CRAMPACS_PROTOCOL_TEMPLATE.md`.

## Domain Coordinate Families

asset, tenor, counterparty, time window, transaction velocity, network position, model threshold

## Domain Nulls and Non-Events

cleared alerts, comparable accounts without event, backtests with no breach, control portfolios

## Domain Dependence Hazards

List the source families, instruments, vendors, sites, pipelines, datasets, or reporting systems that could make rows non-independent.

## Domain Bias Hazards

Primary gotcha: look-ahead bias, backtest overfitting, vendor revisions, feedback loops from prior controls

Add domain-specific publication, reporting, measurement, selection, and survivorship biases.

## Required Negative Controls

Define at least one coordinate, source class, or row family expected not to recur.

## Domain Checksum Additions

List required hashes for domain-specific source systems, units, transforms, vocabularies, reference systems, or vendor snapshots.

## Claim Limits

This `CRAMPACS-FIN` study can produce a full CRAMPACS evidence package only after protocol lock, full source flow, null inclusion, independence review, bias review, null-model analysis, sensitivity tests, checksum reproduction, and signoff.
