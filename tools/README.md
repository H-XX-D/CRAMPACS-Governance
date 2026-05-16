# CRAMPACS Tools

## Portable Tool

`crampacs_sidecar.py` uses only the Python standard library. It checks preflight or full-study package completeness, writes package metrics, and produces a hash manifest.

Examples:

```bash
python3 tools/crampacs_sidecar.py domain_packs/med --level preflight
python3 tools/crampacs_sidecar.py templates --level full
```

Use explicit `--level preflight` or `--level full` for governance audits. Auto-detection is intended for completed study package directories, not the repository root.

## Generation Tools

`generate_domain_packs.py` regenerates domain pack Markdown and CSV starter files.

`build_printouts_and_spreadsheets.mjs` regenerates printouts and XLSX workbooks.

`verify_workbooks.mjs` imports representative XLSX workbooks and inspects key ranges.

The JavaScript workbook tools require the Codex bundled spreadsheet runtime and `@oai/artifact-tool`. In this workspace, create or reuse a local `node_modules` symlink to the bundled package directory before running them.

The generated XLSX files are committed release artifacts. The local `node_modules` symlink is intentionally ignored.

