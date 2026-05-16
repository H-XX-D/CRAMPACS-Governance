# CRAMPACS Templates

These templates implement the data contracts defined in `../CRAMPACS_PROGRAM_SOP_2026-05-15.md`.

Use them by copying this directory into a study workspace such as:

```text
crampacs/CRAMPACS_<domain>_<YYYY-MM-DD>/
```

Rules:

- Do not remove columns during a study.
- Add new columns only through `amendment_log.csv`.
- Preserve raw source values in `anomaly_rows_raw.csv`.
- Write normalized values only in `normalized_rows.csv`.
- Leave unknown values blank rather than inventing placeholders.
- Keep all IDs stable after the protocol lock.

