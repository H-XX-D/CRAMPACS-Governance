# CRAMPACS-PHY Physics Overlay

**Domain:** Physics, high-energy physics, astrophysics-adjacent particle searches, precision measurement, detector searches, and anomaly catalogs

## Definition

CRAMPACS-PHY tests whether weak physics anomalies, residuals, excesses, deficits, null searches, exclusions, or near-misses recur at pre-specified physical coordinates more often than expected under a registered physics and literature-process null model.

## Coordinate Families

- Mass, energy, frequency, wavelength, redshift, coupling, cross section.
- Decay channel, event topology, resonance width, angular coordinate.
- Detector threshold, exposure, luminosity, energy band, spectral bin.
- Derived dimensionless coordinate or scale ratio.
- Time, phase, baseline, oscillation parameter, sky region.

## Eligible Rows

- Weak excesses.
- Residuals.
- Deficits.
- Near-threshold bumps.
- Tensions.
- Calibration-adjacent oddities.
- Null searches.
- Exclusion limits.
- Failed replications.
- Public-data recasts with adequate provenance.

## Null and Non-Events

Nulls include:

- Searches covering the coordinate range with no excess.
- Exclusion contours.
- Negative follow-up analyses.
- Control regions.
- Sideband checks.
- Non-detections.
- Retired or retracted anomaly claims.

## Dependence Hazards

- Same detector.
- Same collaboration.
- Same public dataset.
- Same simulation background.
- Same reconstruction pipeline.
- Same calibration.
- Same theoretical scan target.
- Same conference note later published as paper.
- Same review paper copied into multiple secondary sources.

## Bias Hazards

- Look-elsewhere effect.
- Publication bias toward bumps.
- Theoretical fashion around popular masses or scales.
- Selective reporting of residuals.
- Plot digitization error.
- Detector threshold pileups.
- Shared background model.
- Retrospective tolerance selection.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve searched coordinate ranges, detector resolution, modality, publication era, local/global reporting convention, and source family.

Preferred null:

- Literature-process and instrument-process nulls that preserve scan ranges, thresholds, background structures, and trials factors.

## Standards Anchors

- PRISMA and PRISMA-P for source flow and protocol lock.
- PDG statistical practice for physical measurements and particle searches.
- CMS and HEP guidance on the look-elsewhere effect.
- JCGM GUM for uncertainty propagation where physical measurement uncertainty matters.
- FAIR, DataCite, and W3C PROV for data and provenance.

## Checksum Additions

- Dataset or run ID.
- Luminosity or exposure snapshot.
- Detector calibration version.
- Simulation version.
- Analysis note or paper hash.
- Digitization log hash where plot extraction is used.
- Coordinate transform hash.

## Claim Limits

CRAMPACS-PHY can prioritize coordinates for targeted searches or prospective tests. It cannot establish discovery, new physics, model confirmation, or exclusion reinterpretation without field-standard experimental confirmation.

