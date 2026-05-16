# CRAMPACS CLI AI Operator Guide

This guide is for an AI agent that has been pointed at the CRAMPACS source kit.

## Operating Boundary

Treat this repository as the reusable source kit. Do not create study evidence,
case-specific rows, private data, scratch work, or project outputs inside:

- `templates/`
- `program/`
- `policies/`
- `domain_packs/`
- `domain_overlays/`
- `brand/`
- `training/`
- `research/`
- `printouts/`
- `spreadsheets/`
- `tools/`

Create an isolated package with the CLI and work inside that package.

## Start A Lowercase Preflight

```bash
python tools/crampacs_cli.py init \
  --level preflight \
  --domain phy \
  --study-id STUDY001 \
  --title "bounded coordinate recurrence preflight"
```

Then work only inside the reported package path.

## Start A Full Uppercase Package

```bash
python tools/crampacs_cli.py init \
  --level full \
  --domain phy \
  --study-id STUDY001 \
  --title "full coordinate recurrence package"
```

## Promote A Preflight Into A Full Package

```bash
python tools/crampacs_cli.py promote <preflight_package> \
  --study-id STUDY001-FULL
```

Promotion copies the lowercase preflight into the uppercase package as seed
material. It does not mutate the original preflight and does not turn preflight
evidence into full assurance without review.

## Required Work Loop

After material edits, run:

```bash
python tools/crampacs_cli.py check <package_dir>
python tools/crampacs_cli.py leak-scan <package_dir>
python tools/crampacs_cli.py gate <package_dir>
python tools/crampacs_cli.py status <package_dir>
```

Use the outputs to decide the next action:

- `crampacs_sidecar_metrics.json` gives completeness and checksum state.
- `ai_controls/leak_scan_status.json` gives leak and quarantine risk.
- `ai_controls/gate_status.json` gives DAG gate status.
- `ai_controls/term_prereq_ledger.csv` gives explicit prerequisite accounting.

## When To Quarantine

Run quarantine when you see:

- a critical credential/token/private-key finding
- private or regulated identifiers in an unauthorized package
- source-kit contamination
- fabricated or untraceable values
- hidden removal of nulls or non-events
- a blocked gate bypass
- overclaim language in exports or decision records

```bash
python tools/crampacs_cli.py quarantine <package_dir> \
  --reason "critical leak or gate bypass"
```

Do not release, export, promote, or rely on the package while quarantined.

## What The CLI Does Not Do

The CLI does not prove the domain claim. It does not replace statistical review,
domain review, legal review, privacy review, clinical review, security review,
financial model governance, or release authority.

It makes the package state inspectable so those reviewers can see what is
present, missing, blocked, contaminated, or overclaimed.
