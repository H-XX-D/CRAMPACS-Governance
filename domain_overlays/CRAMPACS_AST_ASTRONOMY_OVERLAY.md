# CRAMPACS-AST Astronomy and Astrophysics Overlay

**Domain:** Astronomy, astrophysics, planetary science, survey astronomy, time-domain astronomy, and multi-messenger observations

## Definition

CRAMPACS-AST tests whether weak astronomical residuals, transients, spectral features, timing anomalies, survey near-misses, or null observations recur at pre-specified sky, spectral, temporal, orbital, redshift, or source-class coordinates more often than expected under a registered astrophysical and survey-selection null model.

## Coordinate Families

- Right ascension, declination, Galactic coordinates.
- Redshift, distance, luminosity, magnitude, color.
- Wavelength, frequency, energy band, spectral line.
- Period, phase, cadence, transient duration.
- Orbital parameter, ephemeris, sky region.
- Source class, host type, survey field, detector band.

## Eligible Rows

- Spectral residuals.
- Weak transient candidates.
- Timing residuals.
- Survey excesses or deficits.
- Catalog crossmatch anomalies.
- Null follow-up observations.
- Non-detections.
- Candidate retractions and false positives.

## Null and Non-Events

Nulls include:

- Follow-up non-detections.
- Survey fields with comparable exposure and no event.
- Spectral windows searched without feature.
- Cataloged candidates later rejected.
- Injection-recovery misses.

## Dependence Hazards

- Same telescope or instrument.
- Same survey pipeline.
- Same calibration file.
- Same sky subtraction method.
- Same catalog crossmatch.
- Same ephemeris.
- Same alert broker.
- Same observing campaign.
- Same selection function.

## Bias Hazards

- Sky coverage bias.
- Cadence bias.
- Follow-up selection bias.
- Malmquist bias.
- Source confusion.
- Calibration drift.
- Data-release version drift.
- Publication bias toward unusual transients.
- Alert broker amplification.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve sky coverage, depth, cadence, wavelength band, source population, selection function, and known background.

Preferred null:

- Injection-recovery or survey-simulator null with instrument sensitivity and selection function.

## Standards Anchors

- FITS standard for astronomical data.
- IVOA standards for virtual observatory interoperability.
- VOEvent for sky transient alert metadata.
- NASA ADS for literature provenance.
- DataCite and FAIR for data release metadata.
- Domain-specific survey data-release documentation.

## Checksum Additions

- FITS header hash.
- Observation time standard.
- Sky coordinate frame.
- Ephemeris version.
- Instrument calibration file hash.
- Catalog crossmatch version.
- Alert packet hash.

## Claim Limits

CRAMPACS-AST can prioritize astronomical coordinates or source classes for follow-up. It cannot establish discovery, source classification, physical mechanism, or population inference without domain-standard observation and analysis.

