# CRAMPACS Cross-Unit Experiment Checksum Guidelines

**Guideline ID:** CRAMPACS-CHECK-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft verification guideline  
**Parent SOP:** `CRAMPACS_PROGRAM_SOP_2026-05-15.md`

## 1. Purpose

These guidelines define how CRAMPACS studies verify that evidence from different units, sites, teams, instruments, experiments, markets, repositories, or operational systems has been preserved, transformed, and analyzed consistently.

"Unit" has two meanings in this guideline:

1. **Organizational unit:** hospital, lab, experiment, trading desk, telescope, plant, supplier, SOC, dataset owner, research group.
2. **Measurement unit:** mg, mmol/L, USD, basis points, Hz, Kelvin, Celsius, coordinate reference system, time zone, genome build, software version.

Both must be controlled. Cross-unit studies fail when organizational provenance is unclear or measurement units silently drift.

## 2. Hash Standard

Default checksum:

- SHA-256 for all portable manifests.

Optional secondary checksum:

- BLAKE3 for fast large-file verification.

Every released package must include:

- Source file hashes.
- Schema hashes.
- Raw row table hashes.
- Normalized table hashes.
- Transform registry hash.
- Candidate registry hash.
- Protocol hash.
- Analysis code hash.
- Environment hash.
- Output hash.

## 3. Canonicalization Rules

Hashes must be computed over canonical files.

CSV canonicalization:

- UTF-8.
- LF line endings.
- Header row present.
- Columns in contract order.
- Rows sorted by stable ID unless row order is explicitly meaningful.
- Empty unknown values remain empty.
- No trailing spaces.
- Numeric precision fixed by data contract.
- Dates in ISO 8601.
- Time zones explicit.

JSON canonicalization:

- UTF-8.
- Sorted keys.
- No insignificant whitespace.
- ISO 8601 date strings.
- Numeric precision policy documented.

Binary files:

- Hash raw file bytes.
- Record tool used to generate any derived thumbnail, OCR, digitization, or parsed text.

## 4. Cross-Unit Manifest

Each organizational unit must produce a manifest.

Required file: `unit_manifest.csv`

Fields:

```csv
study_id,unit_id,unit_type,unit_name,data_owner,source_system,source_snapshot_time,raw_file_path,raw_sha256,schema_id,schema_sha256,timezone,coordinate_reference,measurement_unit_policy,privacy_classification,license_status,signoff_person,signoff_time
```

Unit types:

- hospital
- lab
- experiment
- instrument
- market
- desk
- plant
- supplier
- telescope
- repository
- security_system
- study_team
- other

## 5. Row-Level Hashes

Every extracted row should have a deterministic row hash.

Required formula:

```text
row_sha256 = SHA256(canonical_json({
  "row_id": ...,
  "source_id": ...,
  "raw_coordinate_value": ...,
  "raw_coordinate_units": ...,
  "reported_effect": ...,
  "reported_statistic": ...,
  "extraction_method": ...,
  "source_location": ...
}))
```

The row hash protects against silent edits to extracted evidence.

## 6. Unit Conversion Checksums

Every unit conversion must produce a conversion audit row.

Required file: `unit_conversion_audit.csv`

Fields:

```csv
conversion_id,row_id,input_value,input_unit,output_value,output_unit,conversion_formula,constants_version,rounding_policy,transform_id,transform_version,reviewer_id,conversion_sha256
```

Rules:

- Never overwrite raw units.
- Store canonical units separately.
- Store formula and constants.
- Store source coordinate reference system if spatial.
- Store genome build if genomic.
- Store currency, quote source, and timestamp if financial.
- Store time zone and calendar convention if time-based.

## 7. Cross-Site Reconciliation

When multiple units submit evidence, the reproducibility lead must run reconciliation.

Required checks:

- Same schema ID across units or approved schema mapping.
- Same candidate registry hash.
- Same transform registry hash.
- Same protocol hash.
- Same time zone policy.
- Same missing-value encoding.
- Same coordinate reference system policy.
- Same random seed policy.
- Same environment or approved equivalent.

Mismatches require a deviation record.

## 8. Analysis Reproducibility Bundle

Required file: `analysis_manifest.csv`

Fields:

```csv
study_id,run_id,protocol_sha256,candidate_registry_sha256,source_catalog_sha256,raw_rows_sha256,normalized_rows_sha256,independence_groups_sha256,bias_assessment_sha256,null_model_spec_sha256,code_sha256,environment_sha256,random_seed,output_sha256,run_timestamp,runner_id
```

The primary output is valid only when all input hashes match the locked manifest or documented amendments.

## 9. Cross-Unit Experiment Checksum

For a multi-unit study, compute a top-level checksum:

```text
experiment_sha256 = SHA256(canonical_json({
  "study_id": ...,
  "protocol_sha256": ...,
  "candidate_registry_sha256": ...,
  "transform_registry_sha256": ...,
  "unit_manifest_sha256": ...,
  "source_catalog_sha256": ...,
  "normalized_rows_sha256": ...,
  "analysis_manifest_sha256": ...,
  "result_sha256": ...
}))
```

This checksum is the compact identity of the CRAMPACS experiment.

## 10. Failure Classes

| Failure | Meaning | Required action |
|---|---|---|
| Hash mismatch | File differs from locked version | Stop and reconcile |
| Schema mismatch | Unit used different contract | Map or exclude before analysis |
| Unit mismatch | Measurement units differ silently | Re-normalize and audit |
| Time mismatch | Time zone or calendar differs | Re-normalize and audit |
| Coordinate mismatch | Reference system, genome build, or index differs | Re-map or quarantine |
| Output mismatch | Clean run does not reproduce | Block release |
| Unauthorized amendment | Locked file changed without log | Demote or restart |

## 11. Domain-Specific Checksum Additions

Medicine:

- HIPAA classification.
- IRB or ethics status.
- OMOP/FHIR mapping hash if used.
- Drug vocabulary version.
- Diagnosis vocabulary version.

Genomics:

- Genome build.
- Reference sequence digest.
- VCF/BCF hash.
- GA4GH refget identifier where available.
- Variant normalization tool version.

Climate:

- NetCDF file hash.
- CF conventions version.
- Grid definition.
- Regridding method hash.
- Scenario or experiment ID.

Materials:

- Composition parser version.
- Structure file hash.
- Processing protocol hash.
- Instrument calibration hash.
- Database/API snapshot hash.

Engineering:

- Sensor calibration hash.
- Firmware version.
- Test bench configuration hash.
- Load profile hash.
- Failure taxonomy version.

Finance:

- Market data vendor.
- Price timestamp.
- Corporate action adjustment version.
- Currency conversion source.
- Trading calendar.
- Model inventory ID.

Cybersecurity:

- ATT&CK version.
- CVE/CVSS version.
- Log parser version.
- Sensor ID.
- Detection rule hash.
- Evidence chain hash.

Astronomy:

- FITS header hash.
- Observation time standard.
- Sky coordinate frame.
- Ephemeris version.
- Instrument calibration file hash.
- Catalog crossmatch version.

## 12. Release Requirement

No CRAMPACS result may be externally described as reproduced unless:

- Top-level experiment checksum is present.
- Clean-run output checksum matches.
- All deviations are resolved or disclosed.
- Cross-unit reconciliation is complete.
- A reviewer who did not build the pipeline signs the reproducibility report.

