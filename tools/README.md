# CRAMPS Tools

## End-To-End CLI

`cramps_cli.py` is the primary operating surface for AI-assisted package work.
It creates isolated project packages, keeps the source kit sanitized, runs
sidecar checks, evaluates DAG gates, writes term/prerequisite accounting,
creates and audits agent deployment helper files, scans leak surfaces, and
records acceptance, reviewer packet, and quarantine state.

Examples:

```bash
python3 tools/cramps_cli.py domains
python3 tools/cramps_cli.py init --level preflight --domain phy --study-id STUDY001
python3 tools/cramps_cli.py check ./cramps_projects/<package>
python3 tools/cramps_cli.py agent-audit ./cramps_projects/<package>
python3 tools/cramps_cli.py leak-scan ./cramps_projects/<package>
python3 tools/cramps_cli.py gate ./cramps_projects/<package>
python3 tools/cramps_cli.py acceptance-audit ./cramps_projects/<package>
python3 tools/cramps_cli.py review-packet ./cramps_projects/<package>
python3 tools/cramps_cli.py promote ./cramps_projects/<preflight_package> --study-id STUDY001-FULL
```

See `CRAMPS_CLI_AI_OPERATOR_GUIDE.md` for the AI operator loop.

## Portable Tool

`cramps_sidecar.py` uses only the Python standard library. It checks preflight or full-study package completeness, writes package metrics, and produces a hash manifest.

Examples:

```bash
python3 tools/cramps_sidecar.py domain_packs/med --level preflight
python3 tools/cramps_sidecar.py templates --level full
```

Use explicit `--level preflight` or `--level full` for governance audits. Auto-detection is intended for completed study package directories, not the repository root.

## Generation Tools

`generate_domain_packs.py` regenerates domain pack Markdown and CSV starter files.

`build_printouts_and_spreadsheets.mjs` regenerates printouts and XLSX workbooks.

`verify_workbooks.mjs` imports representative XLSX workbooks and inspects key ranges.

The JavaScript workbook tools require the Codex bundled spreadsheet runtime and `@oai/artifact-tool`. In this workspace, create or reuse a local `node_modules` symlink to the bundled package directory before running them.

The generated XLSX files are committed release artifacts. The local `node_modules` symlink is intentionally ignored.
