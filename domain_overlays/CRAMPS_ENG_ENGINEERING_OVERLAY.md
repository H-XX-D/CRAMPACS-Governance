# CRAMPS-ENG Engineering Reliability Overlay

**Domain:** Engineering systems, reliability, manufacturing quality, safety, operations, and field failures

## Definition

CRAMPS-ENG tests whether weak defects, failures, near-misses, sensor residuals, or operational anomalies recur at pre-specified engineering coordinates more often than expected under a registered reliability or process-control null model.

## Coordinate Families

- Load, torque, vibration frequency, temperature, pressure, humidity.
- Firmware or software version.
- Supplier, batch, lot, serial range, manufacturing line.
- Operating hours, cycle count, maintenance interval.
- Sensor channel, part geometry, tolerance band.
- Failure mode, fault code, component class.
- Field environment or duty cycle.

## Eligible Rows

- Field returns.
- Warranty claims.
- Near-miss safety events.
- Process-control excursions.
- Sensor residuals.
- Test-bench anomalies.
- Failure-analysis reports.
- Null reliability tests.
- Passed stress tests.

## Null and Non-Events

Nulls include:

- Units exposed to the same condition without failure.
- Passed qualification tests.
- Lots with no reported anomaly.
- Maintenance intervals with no event.
- Sensor streams without recurrence.

## Dependence Hazards

- Same supplier lot.
- Same manufacturing line.
- Same test bench.
- Same firmware.
- Same maintenance team.
- Same sensor calibration.
- Same failure reporting system.
- Same operating fleet.

## Bias Hazards

- Underreporting of near-misses.
- Warranty selection effects.
- Fleet exposure imbalance.
- Maintenance-induced censoring.
- Sensor drift.
- Survivorship bias.
- Root-cause narrative bias.
- Retrospective threshold selection.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve exposure hours, duty cycle, lot, operating environment, maintenance window, and failure mode taxonomy.

Preferred null:

- Reliability model with censoring, competing risks, batch effects, and exposure offsets.

## Standards Anchors

- NIST/SEMATECH Engineering Statistics Handbook for measurement and process characterization.
- ISO 9001 for quality management.
- ISO 31000 for risk management.
- ISO/IEC 17025 for test lab traceability.
- IEC 61508 where safety-related E/E/PE systems are involved.
- ASME V&V and uncertainty quantification concepts where simulation evidence is used.

## Checksum Additions

- Sensor calibration hash.
- Firmware version.
- Test bench configuration hash.
- Load profile hash.
- Maintenance record snapshot.
- Failure taxonomy version.
- Supplier lot manifest.

## Claim Limits

CRAMPS-ENG can prioritize failure coordinates for engineering investigation. It cannot establish root cause, safety compliance, recall necessity, or product qualification without engineering validation.

