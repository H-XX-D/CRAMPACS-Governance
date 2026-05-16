# CRAMPACS-CLIM Climate and Earth Systems Overlay

**Domain:** Climate, weather, hydrology, oceanography, geoscience, and Earth observation

## Definition

CRAMPACS-CLIM tests whether weak climate or Earth-system anomalies recur at pre-specified spatial, temporal, spectral, depth, altitude, or regime coordinates more often than expected under a registered Earth-system null model.

## Coordinate Families

- Latitude, longitude, altitude, depth.
- Time, season, ENSO phase, climate regime, return period.
- Pressure level, ocean layer, soil layer.
- Variable threshold, temperature anomaly, precipitation intensity, wind speed, humidity, radiative flux.
- Watershed, biome, ice shelf, basin, grid cell, model ensemble member.

## Eligible Rows

- Observational residuals.
- Model-data mismatches.
- Extreme event near-misses.
- Sensor-network anomalies.
- Reanalysis residuals.
- Hydrological or oceanographic departures.
- Null event attribution studies.
- Model ensembles with no anomaly at tested coordinates.

## Null and Non-Events

Nulls include:

- Comparable regions without recurrence.
- Model runs without the anomaly.
- Seasons or regimes tested but not anomalous.
- Sensor stations with coverage but no signal.
- Negative attribution studies.

## Dependence Hazards

- Same reanalysis product.
- Same satellite retrieval algorithm.
- Same station network.
- Same model family.
- Same forcing dataset.
- Same bias-correction method.
- Same gridding or regridding pipeline.
- Same observational assimilation system.

## Bias Hazards

- Spatial autocorrelation.
- Temporal autocorrelation.
- Selection of extreme events after the fact.
- Non-stationary baseline.
- Sensor drift.
- Urban heat island or land-use change.
- Data rescue gaps.
- Model-family dependence.
- Publication bias toward surprising extremes.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve spatial and temporal autocorrelation, seasonality, observational coverage, baseline period, and known regime structure.

Preferred null:

- Block bootstrap, ensemble-based null, counterfactual model ensemble, or physically informed null that preserves major climate modes.

## Standards Anchors

- WMO Unified Data Policy for Earth-system data exchange.
- NetCDF Climate and Forecast metadata conventions.
- CMIP/ESGF data reference syntax and controlled vocabularies where model data are used.
- IPCC uncertainty treatment guidance for calibrated language.
- FAIR and DataCite for reusable climate data.

## Checksum Additions

- NetCDF hash.
- CF conventions version.
- Grid definition.
- Regridding method.
- Baseline period.
- Scenario or experiment ID.
- Model ensemble member IDs.
- Observation platform calibration version.

## Claim Limits

CRAMPACS-CLIM can prioritize recurrent anomaly coordinates or regimes for attribution or monitoring. It cannot establish causal climate attribution without accepted attribution methods and domain review.

