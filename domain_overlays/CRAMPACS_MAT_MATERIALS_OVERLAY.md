# CRAMPACS-MAT Materials Science Overlay

**Domain:** Materials science, chemistry-adjacent materials discovery, manufacturing materials data, and computational materials

## Definition

CRAMPACS-MAT tests whether weak performance, failure, synthesis, or simulation anomalies recur at pre-specified composition, structure, processing, property, or operating coordinates more often than expected under a registered materials null model.

## Coordinate Families

- Composition ratio, stoichiometry, dopant level, impurity level.
- Crystal structure, phase, defect class, lattice parameter.
- Processing temperature, pressure, atmosphere, dwell time, cooling rate.
- Mechanical, electrical, thermal, optical, catalytic, or degradation property.
- Operating condition, load, humidity, cycle count, electrolyte, substrate.
- Computational method, functional, force field, simulation cell, convergence threshold.

## Eligible Rows

- Unexpected property jumps.
- Synthesis failures.
- Reproducibility failures.
- Degradation anomalies.
- Processing-window anomalies.
- Simulation-experiment residuals.
- Negative syntheses.
- Failed replication batches.

## Null and Non-Events

Nulls include:

- Syntheses that did not produce target phase.
- Materials tested without property jump.
- Simulations with no predicted anomaly.
- Batches with no failure under same condition.
- Reported negative screens.

## Dependence Hazards

- Same lab protocol.
- Same supplier batch.
- Same instrument calibration.
- Same database entry.
- Same simulation code.
- Same exchange-correlation functional or force field.
- Same sample preparation.
- Same measurement geometry.

## Bias Hazards

- Positive-result publication bias.
- Unreported failed syntheses.
- Batch-to-batch variation.
- Hidden processing parameters.
- Unit conversion errors.
- Composition rounding.
- Simulation convergence artifacts.
- Survivorship bias in materials databases.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve composition family, processing route, property measurement type, temperature/pressure conditions, and source database or lab family.

Preferred null:

- Hierarchical model separating material family, lab, instrument, process, and measurement variance.

## Standards Anchors

- OPTIMADE for materials database interoperability.
- NOMAD and FAIR-DI concepts for FAIR computational materials data.
- Materials Project API provenance concepts where Materials Project data are used.
- PIF/GEMD-style materials process-structure-property metadata where applicable.
- ISO 9001 and ISO/IEC 17025 alignment for lab quality and traceability.

## Checksum Additions

- Composition parser version.
- Structure file hash.
- Processing protocol hash.
- Instrument calibration hash.
- Supplier batch ID.
- Simulation input hash.
- Database/API snapshot hash.

## Claim Limits

CRAMPACS-MAT can rank materials coordinates for replication or targeted synthesis. It cannot establish a material property claim, process window, or product qualification without direct testing and field-standard validation.

