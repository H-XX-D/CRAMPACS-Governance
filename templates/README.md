# CRAMPS Templates

These templates implement the data contracts defined in `../policies/CRAMPS_PROGRAM_SOP_2026-05-15.md`.

Use them by copying this directory into a study workspace such as:

```text
cramps/CRAMPS_<domain>_<YYYY-MM-DD>/
```

Rules:

- Do not remove columns during a study.
- Add new columns only through `amendment_log.csv`.
- Preserve raw source values in `anomaly_rows_raw.csv`. The filename is a stable data-contract name; the table may contain anomaly-like rows, residuals, failures, nulls, non-events, exclusions, or near-misses.
- Write normalized values only in `normalized_rows.csv`.
- Leave unknown values blank rather than inventing placeholders.
- Keep all IDs stable after the protocol lock.

## Lowercase Preflight Templates

Use these for a one to two day `cramps-*` preflight:

- `preflight_scope.md`
- `preflight_sources.csv`
- `preflight_rows.csv`
- `preflight_gotchas.md`
- `preflight_decision.md`
- `preflight_manifest.csv`

If the preflight escalates, use `preflight_import_log.csv` in the uppercase `CRAMPS-*` package to record which preflight artifacts were accepted, reworked, rejected, or quarantined. It is a conversion/full-system artifact, not a required preflight artifact.

## Uppercase Full-System Templates

Use the remaining CSV templates and `CRAMPS_PROTOCOL_TEMPLATE.md` for a full `CRAMPS-*` study.

Lowercase templates can seed uppercase templates, but they do not carry full assurance until reviewed under the full protocol.

Core full-system narrative templates:

- `coordinate_ontology.md`
- `statistical_analysis_plan.md`
- `null_model_specification.md`
- `independence_policy.md`
- `bias_assessment_policy.md`
