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
python3 tools/cramps_cli.py release-check source
python3 tools/cramps_cli.py contract-audit source
python3 tools/cramps_cli.py source-audit
python3 tools/cramps_cli.py self-test
python3 tools/cramps_cli.py source-snapshot
python3 tools/cramps_cli.py init --level preflight --domain phy --study-id STUDY001
python3 tools/cramps_cli.py check ./cramps_projects/<package>
python3 tools/cramps_cli.py agent-audit ./cramps_projects/<package>
python3 tools/cramps_cli.py leak-scan ./cramps_projects/<package>
python3 tools/cramps_cli.py gate ./cramps_projects/<package>
python3 tools/cramps_cli.py contract-audit package ./cramps_projects/<package>
python3 tools/cramps_cli.py acceptance-audit ./cramps_projects/<package>
python3 tools/cramps_cli.py review-packet ./cramps_projects/<package>
python3 tools/cramps_cli.py release-check package ./cramps_projects/<package>
python3 tools/cramps_cli.py promote ./cramps_projects/<preflight_package> --study-id STUDY001-FULL
```

See `CRAMPS_CLI_AI_OPERATOR_GUIDE.md` for the AI operator loop.

`self-test` includes both positive and negative controls: it runs a temp-package
happy path, verifies reviewer handoff, confirms stale post-acceptance edits are
blocked, and tampers with a copied worked-example artifact to confirm manifest
SHA-256 drift is detected. It also corrupts a copied row/source reference to
confirm the contract audit fails closed on broken foreign keys.

## Portable Tool

`cramps_sidecar.py` uses only the Python standard library. It checks preflight or full-study package completeness, writes package metrics, and produces a hash manifest.

Examples:

```bash
python3 tools/cramps_sidecar.py domain_packs/med --level preflight --out-json /tmp/cramps-med-sidecar.json --out-md /tmp/cramps-med-sidecar.md
python3 tools/cramps_sidecar.py templates --level full --out-json /tmp/cramps-templates-sidecar.json --out-md /tmp/cramps-templates-sidecar.md
```

Use explicit `--level preflight` or `--level full` for governance audits. Auto-detection is intended for completed study package directories, not the repository root.
When reading source-kit examples or templates, write sidecar outputs to `/tmp` or another external path. Copy real packages under `cramps_projects/` before using the default package-local outputs.

## Generation Tools

`generate_domain_packs.py` regenerates domain pack Markdown and CSV starter files.

`build_printouts_and_spreadsheets.mjs` regenerates printouts and XLSX workbooks.

`verify_workbooks.mjs` imports representative XLSX workbooks and inspects key ranges.

The JavaScript workbook tools require the Codex bundled spreadsheet runtime and `@oai/artifact-tool`. In this workspace, create or reuse a local `node_modules` symlink to the bundled package directory before running them.

The generated XLSX files are committed release artifacts. The local `node_modules` symlink is intentionally ignored.
