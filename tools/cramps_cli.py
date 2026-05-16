#!/usr/bin/env python3
"""End-to-end CRAMPS package CLI.

The CLI treats this repository as a sanitized source kit. New studies are
created as isolated package directories, and all operator state, gate status,
leak-watch findings, and quarantine records live inside those package
directories.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import cramps_sidecar as sidecar  # noqa: E402
import scaffold_cramps_package as full_scaffold  # noqa: E402


CLI_VERSION = "0.1.0"
STATE_FILE = "cramps_project.json"

CONTROLLED_SOURCE_DIRS = {
    "brand",
    "domain_overlays",
    "domain_packs",
    "policies",
    "printouts",
    "program",
    "research",
    "spreadsheets",
    "templates",
    "tools",
    "training",
}

SOURCE_TREE_PACKAGE_ROOTS = {
    "cramps_projects",
}

PACKAGE_RUNTIME_DIRS = [
    "ai_controls",
    "intake",
    "exports",
    "logs",
    "quarantine",
]

AI_LOG_FIELDS = [
    "timestamp",
    "actor_id",
    "action",
    "artifact_path",
    "gate_id",
    "decision_impact",
    "notes",
]

LEAK_LOG_FIELDS = [
    "timestamp",
    "finding_id",
    "severity",
    "surface",
    "artifact_path",
    "line",
    "pattern_id",
    "status",
    "quarantine_required",
    "notes",
]

QUARANTINE_LOG_FIELDS = [
    "timestamp",
    "event",
    "status",
    "reason",
    "scope",
    "actor_id",
    "release_hold",
    "notes",
]

TERM_FIELDS = [
    "gate_id",
    "phase",
    "priority",
    "term_id",
    "term_or_prerequisite",
    "status",
    "evidence_artifact",
    "missing_or_blocker",
    "cleared_at",
    "notes",
]

AGENT_DEPLOYMENT_PLAN_FIELDS = [
    "study_id",
    "package_level",
    "deployment_mode",
    "agent_id",
    "agent_role",
    "assigned_scope",
    "allowed_inputs",
    "prohibited_inputs",
    "required_outputs",
    "reviewer_id",
    "gate_start",
    "gate_stop",
    "can_write",
    "can_export",
    "human_review_required",
    "status",
    "notes",
]

AGENT_HANDOFF_FIELDS = [
    "handoff_id",
    "study_id",
    "from_agent_id",
    "to_agent_id",
    "artifact_path",
    "artifact_state",
    "gate_context",
    "open_blockers",
    "quarantine_status",
    "reviewer_id",
    "accepted_timestamp",
    "notes",
]

AGENT_REGISTRY_FIELDS = [
    "agent_id",
    "agent_name",
    "agent_type",
    "purpose",
    "allowed_inputs",
    "prohibited_inputs",
    "output_schema",
    "model_or_tool_version",
    "prompt_or_sop_version",
    "human_review_required",
    "audit_log_path",
    "status",
]

REVIEW_PACKET_MANIFEST_FIELDS = [
    "artifact_path",
    "bytes",
    "sha256",
    "modified_utc",
    "included_in_zip",
    "notes",
]

SOURCE_SNAPSHOT_MANIFEST_FIELDS = [
    "artifact_path",
    "bytes",
    "sha256",
    "modified_utc",
    "included_in_zip",
]

RELEASE_CHECK_FIELDS = [
    "check_id",
    "scope",
    "status",
    "severity",
    "evidence",
    "exit_code",
    "message",
]

CONTRACT_AUDIT_FIELDS = [
    "check_id",
    "scope",
    "artifact_path",
    "status",
    "severity",
    "message",
]

SOURCE_AUDIT_SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "cramps_projects",
    "dist",
}

SOURCE_AUDIT_SKIP_SUFFIXES = {
    ".xlsx",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".zip",
    ".pyc",
}

SOURCE_AUDIT_SKIP_NAMES = {
    ".DS_Store",
    "cramps_sidecar_metrics.json",
    "cramps_sidecar_metrics.md",
    "gate_status.json",
    "gate_status.md",
    "leak_scan_status.json",
    "leak_scan_report.md",
    "acceptance_audit_status.json",
    "acceptance_audit_report.md",
    "review_packet_status.json",
}

STALE_NAME_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        "CRAMP" + "ACS",
        "CRAMP" + "AS",
        "CRAMP" + "aS",
        "cramp" + "acs",
        "cramp" + "as",
    ]
]

EXPECTED_DOMAIN_PACK_FILES = [
    "README.md",
    "{full}_DOMAIN_GOVERNANCE_PRINTABLE.md",
    "{full}_FULL_PROTOCOL_ADDENDUM.md",
    "{full}_RELEASE_GATE_PRINTABLE.md",
    "{light}_PREFLIGHT_DECISION.md",
    "{light}_PREFLIGHT_GOTCHAS_PRINTABLE.md",
    "{light}_PREFLIGHT_ROWS.csv",
    "{light}_PREFLIGHT_SCOPE.md",
    "{light}_PREFLIGHT_SOURCES.csv",
]

AGENT_PLAN_REQUIRED_FIELDS = [
    "study_id",
    "package_level",
    "deployment_mode",
    "agent_id",
    "agent_role",
    "assigned_scope",
    "allowed_inputs",
    "prohibited_inputs",
    "required_outputs",
    "gate_start",
    "gate_stop",
    "can_write",
    "can_export",
    "human_review_required",
    "status",
]

AGENT_REGISTRY_REQUIRED_FIELDS = [
    "agent_id",
    "agent_name",
    "agent_type",
    "purpose",
    "allowed_inputs",
    "prohibited_inputs",
    "output_schema",
    "model_or_tool_version",
    "prompt_or_sop_version",
    "human_review_required",
    "audit_log_path",
    "status",
]

AGENT_HANDOFF_REQUIRED_FIELDS = [
    "handoff_id",
    "study_id",
    "from_agent_id",
    "to_agent_id",
    "artifact_path",
    "artifact_state",
    "gate_context",
    "open_blockers",
    "quarantine_status",
    "reviewer_id",
    "accepted_timestamp",
]

AGENT_ALLOWED_STATUSES = {"planned", "active", "complete", "deferred", "canceled", "cancelled"}
AGENT_CLOSED_STATUSES = {"deferred", "canceled", "cancelled"}
AGENT_REGISTRY_REQUIRED_STATUSES = {"active", "complete"}
EMPTY_FIELD_VALUES = {"", "[fill]", "fill", "tbd", "todo", "placeholder"}

FULL_AGENT_ROLES = (
    "protocol_steward",
    "source_search",
    "row_extraction",
    "coordinate_normalization",
    "dependence_mapping",
    "bias_and_missing_evidence",
    "null_model_and_statistics",
    "reproducibility",
    "bounded_reporting",
    "red_team_review",
)


LEAK_PATTERNS = [
    ("openai_api_key", "critical", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("github_token", "critical", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", "critical", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", "critical", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b")),
    ("slack_token", "critical", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
    ("private_key", "critical", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----")),
    ("ssn_like", "major", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("card_like", "major", re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
    ("email_address", "watch", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]

OVERCLAIM_PATTERNS = [
    ("proof_claim", re.compile(r"\b(proves?|proven|proof of|guarantees?|confirmed discovery)\b", re.I)),
    ("causal_claim", re.compile(r"\b(causes?|causally establishes|establishes causality)\b", re.I)),
    ("safety_claim", re.compile(r"\b(safe and effective|clinically proven|fraud proven)\b", re.I)),
]


@dataclass(frozen=True)
class GateSpec:
    gate_id: str
    phase: str
    title: str
    priority: int
    level: str
    depends_on: tuple[str, ...]
    terms: tuple[tuple[str, str, Callable[[Path, dict, dict], tuple[bool, str, str]]], ...]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return cleaned or "untitled"


def load_domains() -> list[dict]:
    return json.loads((ROOT / "tools" / "cramps_domains.json").read_text(encoding="utf-8"))


def load_domain(slug: str) -> dict:
    for domain in load_domains():
        if domain["slug"] == slug:
            return domain
    valid = ", ".join(sorted(domain["slug"] for domain in load_domains()))
    raise SystemExit(f"Unknown domain '{slug}'. Valid domains: {valid}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_csv_header(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def template_header(name: str) -> list[str]:
    return read_csv_header(ROOT / "templates" / name)


def register_header(name: str) -> list[str]:
    return read_csv_header(ROOT / "program" / "registers" / name)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]], force: bool = True) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_csv(path: Path, fieldnames: list[str], row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_text(path: Path, text: str, force: bool = True) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def copy_file(src: Path, dst: Path, force: bool = True) -> None:
    if dst.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def git_value(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def source_dirty() -> bool:
    status = git_value("status", "--short")
    return bool(status and status != "unknown")


def default_output_dir(level: str, domain: dict, study_id: str, title: str | None) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    label = domain["light"] if level == "preflight" else domain["full"]
    suffix = slugify(title or study_id)
    return ROOT / "cramps_projects" / f"{stamp}_{study_id}_{label}_{suffix}"


def guard_output_path(out_dir: Path, force: bool) -> Path:
    resolved = out_dir.expanduser().resolve()
    if resolved == ROOT:
        raise SystemExit("Refusing to create a project in the sanitized source repository root.")
    for dirname in CONTROLLED_SOURCE_DIRS:
        controlled = (ROOT / dirname).resolve()
        if resolved == controlled or is_relative_to(resolved, controlled):
            raise SystemExit(
                f"Refusing to create a project inside controlled source material: {controlled}"
            )
    if resolved.exists() and any(resolved.iterdir()) and not force:
        raise SystemExit(f"Output directory is not empty. Re-run with --force if intentional: {resolved}")
    return resolved


def package_level(package: Path, explicit: str = "auto") -> str:
    if explicit != "auto":
        return explicit
    state = load_state(package, required=False)
    if state.get("level") in {"preflight", "full"}:
        return state["level"]
    preflight_present = sum(1 for name in sidecar.PREFLIGHT_REQUIRED if sidecar.find_file(package, name))
    full_present = sum(1 for name in sidecar.FULL_REQUIRED if sidecar.find_file(package, name))
    if preflight_present and not full_present:
        return "preflight"
    return "full"


def state_path(package: Path) -> Path:
    return package / STATE_FILE


def load_state(package: Path, required: bool = True) -> dict:
    path = state_path(package)
    if not path.exists():
        if required:
            raise SystemExit(f"Missing package state file: {path}")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(package: Path, state: dict) -> None:
    state_path(package).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_history(package: Path, event: str, details: dict | None = None) -> None:
    state = load_state(package, required=False)
    if not state:
        return
    state.setdefault("history", []).append(
        {
            "timestamp": utc_now(),
            "event": event,
            "details": details or {},
        }
    )
    write_state(package, state)


def relative_artifact(package: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(package.resolve()).as_posix()
    except ValueError:
        return str(path)


def render_package_readme(domain: dict, level: str, study_id: str, title: str) -> str:
    label = domain["light"] if level == "preflight" else domain["full"]
    check_level = "preflight" if level == "preflight" else "full"
    return f"""
# {label} Package

**Study ID:** {study_id}  
**Title:** {title}  
**Domain:** {domain["label"]}  
**Package level:** {level}  

This directory is the working package. The sanitized CRAMPS source kit stays
outside the package and must not be edited during package operation.

## Required Operator Loop

1. Work only inside this package directory unless a human explicitly authorizes source-kit maintenance.
2. Record material AI actions in `logs/ai_activity_log.csv`.
3. Run `python {ROOT / "tools" / "cramps_cli.py"} check . --level {check_level}` after material edits.
4. Run `python {ROOT / "tools" / "cramps_cli.py"} agent-audit . --level {check_level}` after agent-plan, registry, or handoff changes.
5. Run `python {ROOT / "tools" / "cramps_cli.py"} leak-scan .` before sharing, exporting, escalation, release, or gate evaluation.
6. Run `python {ROOT / "tools" / "cramps_cli.py"} gate . --level {check_level}` before phase progress.
7. Run `python {ROOT / "tools" / "cramps_cli.py"} contract-audit package . --level {check_level}` before acceptance.
8. Run `python {ROOT / "tools" / "cramps_cli.py"} acceptance-audit . --level {check_level}` before reliance changes.
9. Run `python {ROOT / "tools" / "cramps_cli.py"} review-packet . --level {check_level}` before reviewer handoff.
10. Run `python {ROOT / "tools" / "cramps_cli.py"} release-check package . --level {check_level}` before promotion, closeout, or release review.
11. If a critical leak, source-boundary breach, fabricated field, or prohibited claim is found, run quarantine.

## Claim Boundary

This package can support structured inspection and prioritization claims only
after the relevant gates clear. It does not prove causality, safety, efficacy,
fraud, exploitability, physical discovery, or regulatory compliance by itself.
"""


def render_domain_reference(domain: dict) -> str:
    return f"""
# {domain["light"]} / {domain["full"]} Domain Reference

**Domain:** {domain["label"]}

## Coordinate Families

{chr(10).join(f"- {item}" for item in domain["coordinates"])}

## Nulls And Non-Events To Seek

{chr(10).join(f"- {item}" for item in domain["nulls"])}

## Domain Failure Modes

{chr(10).join(f"- {item}" for item in domain["gotchas"])}

## Relevant Standards And Practices

{chr(10).join(f"- {item}" for item in domain["standards"])}
"""


def render_ai_operator_brief(domain: dict, level: str, study_id: str, title: str) -> str:
    label = domain["light"] if level == "preflight" else domain["full"]
    return f"""
# AI Operator Brief

**Package:** {label}
**Study ID:** {study_id}
**Title:** {title}
**Trust posture:** bounded, inspected, non-confirmatory until gates clear.

## Prime Directive

Operate inside this package as a controlled evidence-building assistant. The
sanitized source kit is reusable program infrastructure. Do not edit source-kit
templates, policies, program files, domain packs, printouts, or training files
while performing package work.

## Required Loop

1. Read `cramps_project.json`, this brief, `ai_controls/AGENT_DEPLOYMENT_HELPER.md`, and `ai_controls/GATE_DAG.md`.
2. Before adding evidence, state the current phase and blocked gate.
3. Add or revise only package artifacts.
4. Record material actions in `logs/ai_activity_log.csv`.
5. Run sidecar checks with `cramps_cli.py check`.
6. Run agent-control checks with `cramps_cli.py agent-audit`.
7. Run leak scanning with `cramps_cli.py leak-scan`.
8. Run DAG accounting with `cramps_cli.py gate`.
9. Run CSV contract checks with `cramps_cli.py contract-audit package`.
10. Run acceptance synthesis with `cramps_cli.py acceptance-audit`.
11. Run reviewer packet synthesis with `cramps_cli.py review-packet` before handoff.
12. Run executable package acceptance with `cramps_cli.py release-check package` before promotion, closeout, or release review.
13. Stop and quarantine if a critical leak, contamination event, fabricated field, or prohibited claim appears.

## Non-Negotiables

- Do not remove nulls, non-events, failed replications, exclusions, or negative controls to improve a score.
- Do not invent unknown values. Leave unknowns blank and log the uncertainty.
- Do not upgrade lowercase `cramps-*` language into uppercase `CRAMPS-*` assurance.
- Do not claim proof, discovery, safety, efficacy, compliance, causality, fraud, or exploitability from CRAMPS alone.
- Do not export restricted, private, sensitive, or source-contaminated material.
- Do not clear a gate manually. Gates clear only through the CLI accounting output plus human review when required.

## Release Rule

The package may progress only when the next gate's prerequisites are met,
leak-scan has no open critical findings, quarantine status is clear, and the
claim language matches the package level.
"""


def agent_deployment_plan_rows(domain: dict, level: str, study_id: str) -> list[dict[str, str]]:
    def row(
        deployment_mode: str,
        agent_id: str,
        agent_role: str,
        assigned_scope: str,
        allowed_inputs: str,
        prohibited_inputs: str,
        required_outputs: str,
        gate_start: str,
        gate_stop: str,
        can_write: str,
        can_export: str,
        review: str,
        notes: str,
    ) -> dict[str, str]:
        return {
            "study_id": study_id,
            "package_level": level,
            "deployment_mode": deployment_mode,
            "agent_id": agent_id,
            "agent_role": agent_role,
            "assigned_scope": assigned_scope,
            "allowed_inputs": allowed_inputs,
            "prohibited_inputs": prohibited_inputs,
            "required_outputs": required_outputs,
            "reviewer_id": "",
            "gate_start": gate_start,
            "gate_stop": gate_stop,
            "can_write": can_write,
            "can_export": can_export,
            "human_review_required": review,
            "status": "planned",
            "notes": notes,
        }

    if level == "preflight":
        return [
            row(
                "single_operator_preflight",
                "single_preflight_operator",
                "preflight_operator",
                "Complete the bounded one to two day preflight and prepare an escalation, hold, stop, or rescope decision.",
                "Package files; public or authorized sources; domain reference; preflight templates.",
                "Source-kit edits; restricted data without authorization; full-system assurance claims; unlogged external outputs.",
                "preflight_scope.md; preflight_sources.csv; preflight_rows.csv; preflight_gotchas.md; preflight_decision.md; logs/ai_activity_log.csv.",
                "G0",
                "P5",
                "yes-package-only",
                "no-before-P5",
                "yes-before-promotion",
                f"Default for {domain['light']}: do not deploy extra agents unless a documented deviation approves the scope.",
            )
        ]

    common_allowed = "Package files; locked protocol; authorized source materials; package-local AI controls."
    common_prohibited = "Unapproved source-kit edits; private or restricted data without authorization; post-hoc coordinate tuning; final release signoff."
    return [
        row(
            "full_system_role_agents",
            "protocol_agent",
            "protocol_steward",
            "Maintain protocol, amendment path, candidate-coordinate lock, and role boundaries.",
            "Charter, preflight import log, domain reference, reviewer instructions.",
            "Source-kit edits; scoring results; changing methods after seeing results; approving release alone.",
            "01_protocol_lock/protocol.md; 01_protocol_lock/candidate_coordinate_registry.csv; 01_protocol_lock/amendment_log.csv.",
            "F1",
            "F2",
            "yes-package-only",
            "no",
            "yes",
            "Can block downstream agents until candidate coordinates and amendment rules are locked.",
        ),
        row(
            "full_system_role_agents",
            "source_search_agent",
            "source_search",
            "Execute registered searches, record source universe, and preserve exclusions, nulls, and non-events.",
            "Locked protocol, search strategy, public or authorized databases.",
            "Source-kit edits; dropping adverse evidence; adding unregistered search criteria without amendment.",
            "02_sources/source_catalog.csv; 02_sources/search_strategy.md; 02_sources/source_flow.md.",
            "F2",
            "F3",
            "yes-package-only",
            "no",
            "yes",
            "Search records must include unavailable, duplicate, null, and excluded sources.",
        ),
        row(
            "full_system_role_agents",
            "extraction_agent",
            "row_extraction",
            "Extract raw coordinate, uncertainty, residual, source, and reviewer fields without normalization.",
            common_allowed,
            f"{common_prohibited}; inferred values presented as source values.",
            "03_extraction/anomaly_rows_raw.csv; 03_extraction/extraction_notes.md.",
            "F3",
            "F3",
            "yes-package-only",
            "no",
            "yes-sampled-or-dual-review",
            "Raw values stay raw; uncertain values remain blank or flagged.",
        ),
        row(
            "full_system_role_agents",
            "normalization_agent",
            "coordinate_normalization",
            "Apply locked transforms and keep raw and normalized coordinate values separated.",
            common_allowed,
            f"{common_prohibited}; undocumented unit conversions.",
            "04_coordinate_normalization/normalized_rows.csv; 04_coordinate_normalization/coordinate_transform_registry.csv; 04_coordinate_normalization/unit_conversion_audit.md.",
            "F3",
            "F4",
            "yes-package-only",
            "no",
            "yes",
            "Every transform must be reproducible from raw values.",
        ),
        row(
            "full_system_role_agents",
            "independence_agent",
            "dependence_mapping",
            "Assign evidence-family, shared-instrument, shared-dataset, and shared-pipeline dependence groups.",
            common_allowed,
            f"{common_prohibited}; treating duplicate analyses as independent rows.",
            "05_dependence_bias/independence_groups.csv.",
            "F4",
            "F5",
            "yes-package-only",
            "no",
            "yes",
            "Dependence grades can reduce but must not inflate evidentiary weight.",
        ),
        row(
            "full_system_role_agents",
            "bias_agent",
            "bias_and_missing_evidence",
            "Assess missing evidence, selective reporting, source-process bias, and domain-specific blind spots.",
            common_allowed,
            f"{common_prohibited}; removing inconvenient missing-evidence findings.",
            "05_dependence_bias/bias_assessment.csv; 05_dependence_bias/missing_evidence_assessment.md.",
            "F4",
            "F5",
            "yes-package-only",
            "no",
            "yes",
            "Bias findings are gate inputs, not narrative decoration.",
        ),
        row(
            "full_system_role_agents",
            "statistics_agent",
            "null_model_and_statistics",
            "Run registered null models, correction accounting, negative controls, and sensitivity summaries.",
            "Locked protocol, normalized rows, dependence map, bias assessment, approved analysis environment.",
            "Source-kit edits; changing nulls after seeing results; release language; unregistered favorable reruns.",
            "06_statistics/null_model_runs.csv; 06_statistics/analysis_result.csv; 06_statistics/negative_controls.md; 06_statistics/sensitivity_results.md.",
            "F5",
            "F6",
            "yes-package-only",
            "no",
            "yes-statistical-lead",
            "All runs need seed, code version, and correction-scope accounting.",
        ),
        row(
            "full_system_role_agents",
            "reproducibility_agent",
            "reproducibility",
            "Rebuild the package outputs from frozen inputs and record environment, hashes, and clean-run issues.",
            "Frozen package snapshot, analysis code, environment instructions.",
            "Source-kit edits; editing evidence to make reproduction pass; omitting failed rebuild notes.",
            "07_reproducibility/checksum_manifest.csv; 07_reproducibility/environment_record.md; 07_reproducibility/clean_run_report.md.",
            "F6",
            "F7",
            "yes-package-only",
            "no",
            "yes",
            "Reproduction failures stay visible until resolved or accepted as residual risk.",
        ),
        row(
            "full_system_role_agents",
            "reporting_agent",
            "bounded_reporting",
            "Draft claim-limited reports, decision memo text, and claim trace entries from reviewed evidence.",
            common_allowed,
            "Source-kit edits; proof, discovery, safety, efficacy, compliance, causality, fraud, or exploitability claims from CRAMPS alone.",
            "09_review_and_release/decision_memo.md; 10_trust_maintenance/claim_trace_matrix.csv; exports/.",
            "F7",
            "F8",
            "yes-package-only",
            "hold-until-release-review",
            "yes-release-authority",
            "Reports must cite gate status and unresolved trust debt.",
        ),
        row(
            "full_system_role_agents",
            "red_team_agent",
            "red_team_review",
            "Attempt to break the package through dependence, leakage, null-model, missing-evidence, and claim-boundary attacks.",
            "Complete package, gate status, leak reports, sidecar metrics, claim drafts.",
            "Source-kit edits; rewriting the claim to hide a defect; closing findings without reviewer basis.",
            "09_review_and_release/audit_report.md; 10_trust_maintenance/trust_debt_register.csv; logs/ai_activity_log.csv.",
            "F6",
            "F8",
            "yes-package-only",
            "no",
            "yes-release-authority",
            "Red-team findings block release until accepted, resolved, or formally dispositioned.",
        ),
    ]


def render_agent_deployment_helper(domain: dict, level: str, study_id: str, title: str) -> str:
    label = domain["light"] if level == "preflight" else domain["full"]
    rows = agent_deployment_plan_rows(domain, level, study_id)
    role_lines = [
        "| agent_id | role | gate span | writes | required review |",
        "|---|---|---|---|---|",
    ]
    for item in rows:
        role_lines.append(
            f"| `{item['agent_id']}` | {item['agent_role']} | `{item['gate_start']}` to `{item['gate_stop']}` | {item['can_write']} | {item['human_review_required']} |"
        )

    if level == "preflight":
        level_rule = f"""
## Preflight Deployment Rule

`{label}` defaults to one operator only: `single_preflight_operator`.

The preflight is meant to be fast, bounded, and cheap. Do not split the work
across multiple agents unless the package owner records a deviation explaining
why the preflight cannot be completed with one operator. If additional help is
approved, the helper may gather source candidates or formatting checks only;
the single preflight operator remains accountable for the decision record.
"""
    else:
        level_rule = f"""
## Full-System Deployment Rule

`{label}` may use role-specific agents after the charter, role assignment, and
protocol-lock path are in place. The deployment plan is not permission to run
unbounded parallel work. Each role must stay within its assigned gate span and
must hand off artifacts through `ai_controls/agent_handoff_checklist.csv`.
"""

    return f"""
# Agent Deployment Helper

**Package:** {label}
**Study ID:** {study_id}
**Title:** {title}

This helper controls when human, software, or AI agents can be used inside this
package. It is a deployment aid, not a release authority.

{level_rule}

## Required Files

- `ai_controls/agent_deployment_plan.csv` records who can work, on what scope,
  with which inputs, and under which gate span.
- `ai_controls/agent_handoff_checklist.csv` records artifact handoffs between
  agents or reviewers.
- `ai_controls/agent_registry.csv` records model, tool, prompt, SOP, review,
  and audit-log details for agents used in the package.
- `logs/ai_activity_log.csv` records material actions.

## Deployment Preconditions

Before deploying any agent beyond the default operator:

1. Confirm the package is active and outside controlled source material.
2. Confirm the agent has a row in `agent_deployment_plan.csv`.
3. Confirm allowed inputs and prohibited inputs are explicit.
4. Confirm the agent's write scope is package-only.
5. Run `cramps_cli.py check`, then `cramps_cli.py agent-audit`, then
   `cramps_cli.py leak-scan`, then `cramps_cli.py gate`.
6. Do not start work if the current gate or a dependency gate is blocked for a
   reason the agent would bypass rather than fix.

## Role Cards

{chr(10).join(role_lines)}

## Handoff Rule

An artifact is not handed off by conversation alone. Record the path, state,
gate context, open blockers, quarantine status, reviewer, and acceptance time
in `ai_controls/agent_handoff_checklist.csv`.

## Stop Conditions

Stop and quarantine when an agent encounters a critical leak, source-kit
contamination, fabricated value, untraceable source field, hidden deletion of
null/non-event evidence, blocked-gate bypass, or claim language above the
package assurance level.

## Command Order

```bash
python {ROOT / "tools" / "cramps_cli.py"} check .
python {ROOT / "tools" / "cramps_cli.py"} agent-audit .
python {ROOT / "tools" / "cramps_cli.py"} leak-scan .
python {ROOT / "tools" / "cramps_cli.py"} gate . --level {level}
python {ROOT / "tools" / "cramps_cli.py"} contract-audit package . --level {level}
python {ROOT / "tools" / "cramps_cli.py"} acceptance-audit . --level {level}
python {ROOT / "tools" / "cramps_cli.py"} review-packet . --level {level}
python {ROOT / "tools" / "cramps_cli.py"} release-check package . --level {level}
python {ROOT / "tools" / "cramps_cli.py"} status .
```
"""


def is_blank_field(value: str | None) -> bool:
    normalized = (value or "").strip().lower()
    return normalized in EMPTY_FIELD_VALUES


def add_agent_issue(
    issues: list[dict[str, str]],
    severity: str,
    code: str,
    artifact_path: str,
    message: str,
) -> None:
    issues.append(
        {
            "severity": severity,
            "code": code,
            "artifact_path": artifact_path,
            "message": message,
        }
    )


def validate_csv_header(
    issues: list[dict[str, str]],
    package: Path,
    rel: str,
    required_fields: list[str],
) -> None:
    path = package / rel
    if not path.exists():
        add_agent_issue(issues, "blocker", "missing_agent_control_file", rel, f"missing {rel}")
        return
    header = set(read_csv_header(path))
    missing = [field for field in required_fields if field not in header]
    if missing:
        add_agent_issue(
            issues,
            "blocker",
            "agent_control_header_missing_fields",
            rel,
            f"missing columns: {', '.join(missing)}",
        )


def validate_required_fields(
    issues: list[dict[str, str]],
    rel: str,
    row_index: int,
    row: dict[str, str],
    fields: list[str],
    severity: str = "blocker",
) -> None:
    missing = [field for field in fields if is_blank_field(row.get(field, ""))]
    if missing:
        add_agent_issue(
            issues,
            severity,
            "agent_row_missing_required_fields",
            f"{rel}:{row_index}",
            f"missing required fields: {', '.join(missing)}",
        )


def row_status(row: dict[str, str]) -> str:
    return (row.get("status") or "").strip().lower()


def agent_row_in_scope(row: dict[str, str]) -> bool:
    return row_status(row) not in AGENT_CLOSED_STATUSES


def audit_agent_controls(package: Path, level: str) -> dict:
    assert_package_output_allowed(package, "agent-audit")
    issues: list[dict[str, str]] = []
    now = utc_now()
    controls_dir = package / "ai_controls"
    helper_rel = "ai_controls/AGENT_DEPLOYMENT_HELPER.md"
    plan_rel = "ai_controls/agent_deployment_plan.csv"
    handoff_rel = "ai_controls/agent_handoff_checklist.csv"
    registry_rel = "ai_controls/agent_registry.csv"

    if not package.exists():
        raise SystemExit(f"Package not found: {package}")
    if package == ROOT or any(is_relative_to(package, ROOT / dirname) for dirname in CONTROLLED_SOURCE_DIRS):
        raise SystemExit("Refusing to write agent-audit outputs inside controlled source material.")

    if not (package / helper_rel).exists():
        add_agent_issue(issues, "blocker", "missing_agent_deployment_helper", helper_rel, f"missing {helper_rel}")

    validate_csv_header(issues, package, plan_rel, AGENT_DEPLOYMENT_PLAN_FIELDS)
    validate_csv_header(issues, package, handoff_rel, AGENT_HANDOFF_FIELDS)
    validate_csv_header(issues, package, registry_rel, AGENT_REGISTRY_FIELDS)

    plan_rows = read_csv_rows(package / plan_rel)
    registry_rows = read_csv_rows(package / registry_rel)
    handoff_rows = read_csv_rows(package / handoff_rel)

    if not plan_rows:
        add_agent_issue(issues, "blocker", "agent_deployment_plan_empty", plan_rel, "agent deployment plan has no rows")

    seen_agent_ids: set[str] = set()
    duplicate_agent_ids: set[str] = set()
    for index, row in enumerate(plan_rows, start=2):
        agent_id = (row.get("agent_id") or "").strip()
        if agent_id:
            if agent_id in seen_agent_ids:
                duplicate_agent_ids.add(agent_id)
            seen_agent_ids.add(agent_id)
        validate_required_fields(issues, plan_rel, index, row, AGENT_PLAN_REQUIRED_FIELDS)
        status = row_status(row)
        if status and status not in AGENT_ALLOWED_STATUSES:
            add_agent_issue(
                issues,
                "warning",
                "agent_plan_unknown_status",
                f"{plan_rel}:{index}",
                f"unknown status '{status}'",
            )
        if row.get("package_level") and row.get("package_level") != level:
            add_agent_issue(
                issues,
                "warning",
                "agent_plan_level_mismatch",
                f"{plan_rel}:{index}",
                f"plan row level is {row.get('package_level')} but package level is {level}",
            )
        prohibited = (row.get("prohibited_inputs") or "").lower()
        if "source-kit" not in prohibited and "source kit" not in prohibited:
            add_agent_issue(
                issues,
                "warning",
                "source_kit_boundary_not_explicit",
                f"{plan_rel}:{index}",
                "prohibited_inputs should explicitly forbid source-kit edits or source-kit contamination",
            )
        can_write = (row.get("can_write") or "").lower()
        if can_write and "package" not in can_write and can_write not in {"no", "read-only", "readonly"}:
            add_agent_issue(
                issues,
                "warning",
                "agent_write_scope_not_package_bound",
                f"{plan_rel}:{index}",
                "can_write should be package-only, no, or read-only",
            )

    for agent_id in sorted(duplicate_agent_ids):
        add_agent_issue(
            issues,
            "blocker",
            "duplicate_agent_plan_id",
            plan_rel,
            f"agent_id appears more than once: {agent_id}",
        )

    in_scope_plan_rows = [row for row in plan_rows if agent_row_in_scope(row)]
    if level == "preflight":
        single_rows = [row for row in in_scope_plan_rows if row.get("agent_id") == "single_preflight_operator"]
        if not single_rows:
            add_agent_issue(
                issues,
                "blocker",
                "missing_single_preflight_operator",
                plan_rel,
                "lowercase preflight must include single_preflight_operator",
            )
        has_deviation = any("deviation" in (row.get("notes") or "").lower() for row in in_scope_plan_rows)
        if len(in_scope_plan_rows) > 1 and not has_deviation:
            add_agent_issue(
                issues,
                "blocker",
                "preflight_multi_agent_without_deviation",
                plan_rel,
                "preflight has more than one in-scope agent without a documented deviation",
            )

    if level == "full":
        roles = {row.get("agent_role", "").strip() for row in in_scope_plan_rows}
        missing_roles = [role for role in FULL_AGENT_ROLES if role not in roles]
        if missing_roles:
            add_agent_issue(
                issues,
                "blocker",
                "full_agent_roles_missing",
                plan_rel,
                f"missing full-system role plans: {', '.join(missing_roles)}",
            )

    registry_by_id: dict[str, dict[str, str]] = {}
    for index, row in enumerate(registry_rows, start=2):
        agent_id = (row.get("agent_id") or "").strip()
        if not agent_id:
            add_agent_issue(
                issues,
                "warning",
                "agent_registry_row_missing_id",
                f"{registry_rel}:{index}",
                "registry row has no agent_id",
            )
            continue
        if agent_id in registry_by_id:
            add_agent_issue(
                issues,
                "blocker",
                "duplicate_agent_registry_id",
                f"{registry_rel}:{index}",
                f"agent_id appears more than once in registry: {agent_id}",
            )
        registry_by_id[agent_id] = row
        if row_status(row) in AGENT_REGISTRY_REQUIRED_STATUSES:
            validate_required_fields(issues, registry_rel, index, row, AGENT_REGISTRY_REQUIRED_FIELDS)
        if agent_id not in seen_agent_ids:
            add_agent_issue(
                issues,
                "warning",
                "registry_agent_not_in_plan",
                f"{registry_rel}:{index}",
                f"registry agent is not listed in deployment plan: {agent_id}",
            )

    for row in in_scope_plan_rows:
        agent_id = (row.get("agent_id") or "").strip()
        if not agent_id:
            continue
        if agent_id not in registry_by_id:
            severity = "blocker" if row_status(row) in AGENT_REGISTRY_REQUIRED_STATUSES else "warning"
            add_agent_issue(
                issues,
                severity,
                "planned_agent_missing_registry_row",
                registry_rel,
                f"agent has no registry row: {agent_id}",
            )

    for index, row in enumerate(handoff_rows, start=2):
        if not any((value or "").strip() for value in row.values()):
            continue
        validate_required_fields(issues, handoff_rel, index, row, AGENT_HANDOFF_REQUIRED_FIELDS)
        for field in ["from_agent_id", "to_agent_id"]:
            agent_id = (row.get(field) or "").strip()
            if agent_id and agent_id not in seen_agent_ids:
                add_agent_issue(
                    issues,
                    "warning",
                    "handoff_agent_not_in_plan",
                    f"{handoff_rel}:{index}",
                    f"{field} is not listed in deployment plan: {agent_id}",
                )

    blocker_count = sum(1 for issue in issues if issue["severity"] == "blocker")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    status = {
        "generated_at": now,
        "package": str(package),
        "level": level,
        "all_clear": blocker_count == 0,
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "plan_row_count": len(plan_rows),
        "registry_row_count": len(registry_rows),
        "handoff_row_count": len(handoff_rows),
        "issues": issues,
    }
    controls_dir.mkdir(parents=True, exist_ok=True)
    (controls_dir / "agent_audit_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(controls_dir / "agent_audit_report.md", render_agent_audit_report(status))
    return status


def render_agent_audit_report(status: dict) -> str:
    lines = [
        "# CRAMPS Agent Audit Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Level: `{status['level']}`",
        f"All clear: `{status['all_clear']}`",
        f"Blockers: `{status['blocker_count']}`",
        f"Warnings: `{status['warning_count']}`",
        f"Deployment plan rows: `{status['plan_row_count']}`",
        f"Registry rows: `{status['registry_row_count']}`",
        f"Handoff rows: `{status['handoff_row_count']}`",
        "",
        "| severity | code | artifact | message |",
        "|---|---|---|---|",
    ]
    if status["issues"]:
        for issue in status["issues"]:
            lines.append(
                f"| `{issue['severity']}` | `{issue['code']}` | `{issue['artifact_path']}` | {issue['message']} |"
            )
    else:
        lines.append("| none | none | none | no agent-control issues detected |")
    lines.append("")
    return "\n".join(lines)


def load_json_artifact(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def add_acceptance_check(
    checks: list[dict[str, str]],
    check_id: str,
    status: str,
    evidence: str,
    message: str,
    severity: str = "blocker",
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": status,
            "severity": severity,
            "evidence": evidence,
            "message": message,
        }
    )


def add_contract_check(
    checks: list[dict[str, str]],
    check_id: str,
    scope: str,
    artifact_path: str,
    status: str,
    severity: str,
    message: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "scope": scope,
            "artifact_path": artifact_path,
            "status": status,
            "severity": severity,
            "message": message,
        }
    )


def header_shape_message(header: list[str]) -> str:
    if not header:
        return "missing or empty CSV header"
    if any(not item.strip() for item in header):
        return "CSV header contains a blank field"
    duplicates = sorted({item for item in header if header.count(item) > 1})
    if duplicates:
        return f"CSV header has duplicate fields: {', '.join(duplicates)}"
    return ""


def audit_csv_header(
    checks: list[dict[str, str]],
    scope: str,
    base: Path,
    rel: str,
    expected: list[str],
    required: bool = True,
    check_id_prefix: str = "csv_header",
) -> None:
    path = base / rel
    if not path.exists():
        add_contract_check(
            checks,
            f"{check_id_prefix}:{rel}",
            scope,
            rel,
            "fail" if required else "warn",
            "blocker" if required else "warning",
            "required CSV contract artifact is missing" if required else "optional CSV contract artifact is missing",
        )
        return
    header = read_csv_header(path)
    shape_issue = header_shape_message(header)
    if shape_issue:
        add_contract_check(checks, f"{check_id_prefix}:{rel}", scope, rel, "fail", "blocker", shape_issue)
        return
    if expected and header != expected:
        add_contract_check(
            checks,
            f"{check_id_prefix}:{rel}",
            scope,
            rel,
            "fail",
            "blocker",
            f"header mismatch; expected {','.join(expected)}",
        )
        return
    add_contract_check(checks, f"{check_id_prefix}:{rel}", scope, rel, "pass", "blocker", "CSV header matches contract")


def audit_required_fields(
    checks: list[dict[str, str]],
    scope: str,
    base: Path,
    rel: str,
    required_fields: list[str],
    id_field: str,
) -> list[dict[str, str]]:
    path = base / rel
    rows = read_csv_rows(path)
    if not path.exists() or not rows:
        return rows
    bad_rows = []
    for index, row in enumerate(rows, start=2):
        missing = [field for field in required_fields if is_blank_field(row.get(field, ""))]
        if missing:
            row_id = row.get(id_field, "") or f"line {index}"
            bad_rows.append(f"{row_id} missing {', '.join(missing)}")
    add_contract_check(
        checks,
        f"required_fields:{rel}",
        scope,
        rel,
        "pass" if not bad_rows else "fail",
        "blocker",
        "required populated-row fields are present" if not bad_rows else "; ".join(bad_rows[:8]),
    )
    return rows


def audit_reference_integrity(
    checks: list[dict[str, str]],
    scope: str,
    artifact_path: str,
    source_ids: set[str],
    rows: list[dict[str, str]],
    row_field: str,
    ref_field: str,
) -> None:
    missing = []
    for row in rows:
        row_id = row.get(row_field, "") or "unidentified_row"
        ref = (row.get(ref_field, "") or "").strip()
        if ref and ref not in source_ids:
            missing.append(f"{row_id}->{ref}")
    add_contract_check(
        checks,
        f"reference_integrity:{artifact_path}:{ref_field}",
        scope,
        artifact_path,
        "pass" if not missing else "fail",
        "blocker",
        "foreign-key references resolve" if not missing else f"unresolved references: {', '.join(missing[:10])}",
    )


def source_contract_checks() -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    template_contracts = {
        "agent_deployment_plan.csv": AGENT_DEPLOYMENT_PLAN_FIELDS,
        "agent_handoff_checklist.csv": AGENT_HANDOFF_FIELDS,
        "agent_registry.csv": AGENT_REGISTRY_FIELDS,
        "preflight_sources.csv": template_header("preflight_sources.csv"),
        "preflight_rows.csv": template_header("preflight_rows.csv"),
        "preflight_manifest.csv": template_header("preflight_manifest.csv"),
        "preflight_import_log.csv": template_header("preflight_import_log.csv"),
        "source_catalog.csv": template_header("source_catalog.csv"),
        "anomaly_rows_raw.csv": template_header("anomaly_rows_raw.csv"),
        "normalized_rows.csv": template_header("normalized_rows.csv"),
        "candidate_coordinate_registry.csv": template_header("candidate_coordinate_registry.csv"),
        "coordinate_transform_registry.csv": template_header("coordinate_transform_registry.csv"),
        "independence_groups.csv": template_header("independence_groups.csv"),
        "bias_assessment.csv": template_header("bias_assessment.csv"),
        "null_model_runs.csv": template_header("null_model_runs.csv"),
        "analysis_result.csv": template_header("analysis_result.csv"),
        "amendment_log.csv": template_header("amendment_log.csv"),
        "role_assignment.csv": template_header("role_assignment.csv"),
        "build_ledger.csv": template_header("build_ledger.csv"),
        "checkpoint_reviews.csv": template_header("checkpoint_reviews.csv"),
        "assumption_uncertainty_log.csv": template_header("assumption_uncertainty_log.csv"),
        "claim_trace_matrix.csv": template_header("claim_trace_matrix.csv"),
        "trust_debt_register.csv": template_header("trust_debt_register.csv"),
    }
    for rel, expected in template_contracts.items():
        audit_csv_header(checks, "source", ROOT, f"templates/{rel}", expected)

    for rel in sorted((ROOT / "program" / "registers").glob("*.csv")):
        audit_csv_header(checks, "source", ROOT, f"program/registers/{rel.name}", read_csv_header(rel))

    for domain in load_domains():
        audit_csv_header(
            checks,
            "source",
            ROOT,
            f"domain_packs/{domain['slug']}/{domain['light']}_PREFLIGHT_SOURCES.csv",
            template_header("preflight_sources.csv"),
        )
        audit_csv_header(
            checks,
            "source",
            ROOT,
            f"domain_packs/{domain['slug']}/{domain['light']}_PREFLIGHT_ROWS.csv",
            template_header("preflight_rows.csv"),
        )
    return checks


def package_contract_checks(package: Path, level: str) -> list[dict[str, str]]:
    assert_package_output_allowed(package, "contract-audit")
    checks: list[dict[str, str]] = []
    common_contracts = {
        "ai_controls/agent_deployment_plan.csv": AGENT_DEPLOYMENT_PLAN_FIELDS,
        "ai_controls/agent_handoff_checklist.csv": AGENT_HANDOFF_FIELDS,
        "ai_controls/agent_registry.csv": AGENT_REGISTRY_FIELDS,
    }
    for rel, expected in common_contracts.items():
        audit_csv_header(checks, "package", package, rel, expected)

    if level == "preflight":
        audit_csv_header(checks, "package", package, "preflight_sources.csv", template_header("preflight_sources.csv"))
        audit_csv_header(checks, "package", package, "preflight_rows.csv", template_header("preflight_rows.csv"))
        audit_csv_header(checks, "package", package, "preflight_manifest.csv", template_header("preflight_manifest.csv"), required=False)
        source_rows = audit_required_fields(
            checks,
            "package",
            package,
            "preflight_sources.csv",
            ["source_id", "citation_or_label", "source_role", "unit_or_site"],
            "source_id",
        )
        row_rows = audit_required_fields(
            checks,
            "package",
            package,
            "preflight_rows.csv",
            ["row_id", "source_id", "coordinate_value", "coordinate_units", "row_type"],
            "row_id",
        )
        audit_reference_integrity(
            checks,
            "package",
            "preflight_rows.csv",
            {row.get("source_id", "") for row in source_rows if row.get("source_id")},
            row_rows,
            "row_id",
            "source_id",
        )
    else:
        full_contracts = {
            "00_charter/role_assignment.csv": template_header("role_assignment.csv"),
            "01_protocol_lock/candidate_coordinate_registry.csv": template_header("candidate_coordinate_registry.csv"),
            "01_protocol_lock/amendment_log.csv": template_header("amendment_log.csv"),
            "02_sources/source_catalog.csv": template_header("source_catalog.csv"),
            "03_extraction/anomaly_rows_raw.csv": template_header("anomaly_rows_raw.csv"),
            "04_coordinate_normalization/coordinate_transform_registry.csv": template_header("coordinate_transform_registry.csv"),
            "04_coordinate_normalization/normalized_rows.csv": template_header("normalized_rows.csv"),
            "05_dependence_bias/independence_groups.csv": template_header("independence_groups.csv"),
            "05_dependence_bias/bias_assessment.csv": template_header("bias_assessment.csv"),
            "06_statistics/null_model_runs.csv": template_header("null_model_runs.csv"),
            "06_statistics/analysis_result.csv": template_header("analysis_result.csv"),
            "09_review_and_release/gate_review_record.csv": register_header("gate_review_record.csv"),
            "10_trust_maintenance/build_ledger.csv": template_header("build_ledger.csv"),
            "10_trust_maintenance/checkpoint_reviews.csv": template_header("checkpoint_reviews.csv"),
            "10_trust_maintenance/assumption_uncertainty_log.csv": template_header("assumption_uncertainty_log.csv"),
            "10_trust_maintenance/claim_trace_matrix.csv": template_header("claim_trace_matrix.csv"),
            "10_trust_maintenance/trust_debt_register.csv": template_header("trust_debt_register.csv"),
        }
        for rel, expected in full_contracts.items():
            audit_csv_header(checks, "package", package, rel, expected)
        for register in sorted((ROOT / "program" / "registers").glob("*.csv")):
            audit_csv_header(checks, "package", package, f"registers/{register.name}", read_csv_header(register))

        sources = audit_required_fields(
            checks,
            "package",
            package,
            "02_sources/source_catalog.csv",
            ["source_id", "citation", "source_type", "domain", "screening_status"],
            "source_id",
        )
        raw_rows = audit_required_fields(
            checks,
            "package",
            package,
            "03_extraction/anomaly_rows_raw.csv",
            ["row_id", "source_id", "result_type", "raw_coordinate_value", "raw_coordinate_units"],
            "row_id",
        )
        normalized = audit_required_fields(
            checks,
            "package",
            package,
            "04_coordinate_normalization/normalized_rows.csv",
            ["row_id", "canonical_coordinate_family", "canonical_coordinate_value", "canonical_coordinate_units"],
            "row_id",
        )
        candidates = audit_required_fields(
            checks,
            "package",
            package,
            "01_protocol_lock/candidate_coordinate_registry.csv",
            ["candidate_id", "coordinate_family", "value", "units", "lock_timestamp", "status"],
            "candidate_id",
        )
        audit_reference_integrity(
            checks,
            "package",
            "03_extraction/anomaly_rows_raw.csv",
            {row.get("source_id", "") for row in sources if row.get("source_id")},
            raw_rows,
            "row_id",
            "source_id",
        )
        raw_ids = {row.get("row_id", "") for row in raw_rows if row.get("row_id")}
        audit_reference_integrity(checks, "package", "04_coordinate_normalization/normalized_rows.csv", raw_ids, normalized, "row_id", "row_id")
        audit_reference_integrity(
            checks,
            "package",
            "06_statistics/analysis_result.csv",
            {row.get("candidate_id", "") for row in candidates if row.get("candidate_id")},
            read_csv_rows(package / "06_statistics" / "analysis_result.csv"),
            "result_id",
            "candidate_id",
        )
    return checks


def contract_audit_status(scope: str, package: Path | None, level: str) -> dict:
    if scope == "source":
        checks = source_contract_checks()
        package_path = ""
        resolved_level = ""
    else:
        if package is None:
            raise SystemExit("Package path is required for package contract audit.")
        package = package.resolve()
        resolved_level = package_level(package, level)
        checks = package_contract_checks(package, resolved_level)
        package_path = str(package)

    blockers = [check for check in checks if check["severity"] == "blocker" and check["status"] != "pass"]
    warnings = [check for check in checks if check["severity"] == "warning" and check["status"] != "pass"]
    return {
        "generated_at": utc_now(),
        "scope": scope,
        "package": package_path,
        "level": resolved_level,
        "decision": "contract_audit_passed" if not blockers else "hold_contract_audit",
        "all_clear": not blockers,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
    }


def render_contract_audit_report(status: dict) -> str:
    lines = [
        "# CRAMPS Contract Audit Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Scope: `{status['scope']}`",
        f"Decision: `{status['decision']}`",
        f"All clear: `{status['all_clear']}`",
        f"Blockers: `{status['blocker_count']}`",
        f"Warnings: `{status['warning_count']}`",
        f"Output directory: `{status.get('output_dir', '')}`",
        "",
    ]
    if status.get("package"):
        lines.extend([f"Package: `{status['package']}`", f"Level: `{status['level']}`", ""])
    lines.extend(["| check | artifact | status | severity | message |", "|---|---|---|---|---|"])
    for check in status["checks"]:
        lines.append(
            f"| `{check['check_id']}` | `{check['artifact_path']}` | `{check['status']}` | `{check['severity']}` | {check['message']} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_contract_audit_outputs(status: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "CONTRACT_AUDIT_RESULTS.csv", CONTRACT_AUDIT_FIELDS, status["checks"])
    (output_dir / "contract_audit_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(output_dir / "contract_audit_report.md", render_contract_audit_report(status))


def acceptance_audit(package: Path, level: str) -> dict:
    assert_package_output_allowed(package, "acceptance-audit")

    checks: list[dict[str, str]] = []
    now = utc_now()
    controls_dir = package / "ai_controls"
    state = load_state(package, required=False)

    metrics_path = package / "cramps_sidecar_metrics.json"
    agent_path = package / "ai_controls" / "agent_audit_status.json"
    leak_path = package / "ai_controls" / "leak_scan_status.json"
    gate_path = package / "ai_controls" / "gate_status.json"
    contract_path = package / "ai_controls" / "contract_audit_status.json"

    metrics = load_json_artifact(metrics_path)
    agent = load_json_artifact(agent_path)
    leak = load_json_artifact(leak_path)
    gate = load_json_artifact(gate_path)
    contract = load_json_artifact(contract_path)

    state_status = state.get("status", "missing")
    add_acceptance_check(
        checks,
        "state_active",
        "pass" if state_status == "active" else "fail",
        STATE_FILE if state else "",
        "package state is active" if state_status == "active" else f"package state is {state_status}",
    )

    boundary_clear = not (
        package == ROOT or any(is_relative_to(package, ROOT / dirname) for dirname in CONTROLLED_SOURCE_DIRS)
    )
    add_acceptance_check(
        checks,
        "source_boundary",
        "pass" if boundary_clear else "fail",
        STATE_FILE if boundary_clear else "",
        "package is outside controlled source material" if boundary_clear else "package is inside controlled source material",
    )

    if not metrics:
        add_acceptance_check(checks, "sidecar_metrics_present", "fail", "", "sidecar metrics have not been run")
    else:
        expected_metrics_level = "cramps_preflight" if level == "preflight" else "CRAMPS_full"
        metrics_level = metrics.get("level", "")
        add_acceptance_check(
            checks,
            "sidecar_level_matches",
            "pass" if metrics_level == expected_metrics_level else "fail",
            "cramps_sidecar_metrics.json",
            "sidecar level matches acceptance level"
            if metrics_level == expected_metrics_level
            else f"sidecar level is {metrics_level}; expected {expected_metrics_level}",
        )
        sidecar_blockers = metrics.get("blockers", [])
        add_acceptance_check(
            checks,
            "sidecar_blockers",
            "pass" if not sidecar_blockers else "fail",
            "cramps_sidecar_metrics.json",
            "sidecar has no blockers" if not sidecar_blockers else f"sidecar blockers: {', '.join(sidecar_blockers)}",
        )
        add_acceptance_check(
            checks,
            "readiness_score",
            "pass" if float(metrics.get("readiness_score", 0) or 0) >= (80 if level == "preflight" else 90) else "warn",
            "cramps_sidecar_metrics.json",
            f"readiness score is {metrics.get('readiness_score', 0)}",
            "warning",
        )

    if not agent:
        add_acceptance_check(checks, "agent_audit_present", "fail", "", "agent audit has not been run")
    else:
        agent_level = agent.get("level", "")
        add_acceptance_check(
            checks,
            "agent_audit_level_matches",
            "pass" if agent_level == level else "fail",
            "ai_controls/agent_audit_status.json",
            "agent audit level matches acceptance level"
            if agent_level == level
            else f"agent audit level is {agent_level}; expected {level}",
        )
        agent_blockers = int(agent.get("blocker_count", 0) or 0)
        add_acceptance_check(
            checks,
            "agent_audit_blockers",
            "pass" if agent_blockers == 0 else "fail",
            "ai_controls/agent_audit_status.json",
            "agent audit has no blockers" if agent_blockers == 0 else f"agent audit has {agent_blockers} blockers",
        )

    if not leak:
        add_acceptance_check(checks, "leak_scan_present", "fail", "", "leak scan has not been run")
    else:
        quarantine_required = bool(leak.get("quarantine_required"))
        critical = int(leak.get("open_critical_findings", 0) or 0)
        major = int(leak.get("open_major_findings", 0) or 0)
        add_acceptance_check(
            checks,
            "leak_scan_clear",
            "pass" if not quarantine_required else "fail",
            "ai_controls/leak_scan_status.json",
            "leak scan has no quarantine-triggering findings"
            if not quarantine_required
            else f"leak scan requires quarantine: {critical} critical, {major} major",
        )

    if not gate:
        add_acceptance_check(checks, "gate_status_present", "fail", "", "gate status has not been run")
    else:
        summary = gate.get("summary", {})
        gate_level = summary.get("level", "")
        add_acceptance_check(
            checks,
            "gate_level_matches",
            "pass" if gate_level == level else "fail",
            "ai_controls/gate_status.json",
            "gate level matches acceptance level" if gate_level == level else f"gate level is {gate_level}; expected {level}",
        )
        all_clear = bool(summary.get("all_clear"))
        add_acceptance_check(
            checks,
            "gate_all_clear",
            "pass" if all_clear else "fail",
            "ai_controls/gate_status.json",
            "all gates are clear" if all_clear else f"next blocked gate: {summary.get('next_blocked_gate', 'unknown')}",
        )

    if gate and agent_path.exists() and gate_path.exists():
        gate_mtime = gate_path.stat().st_mtime
        agent_mtime = agent_path.stat().st_mtime
        add_acceptance_check(
            checks,
            "gate_after_agent_audit",
            "pass" if gate_mtime >= agent_mtime else "fail",
            "ai_controls/gate_status.json",
            "gate status was generated after agent audit"
            if gate_mtime >= agent_mtime
            else "gate status is stale relative to agent audit",
        )

    if gate and metrics_path.exists() and gate_path.exists():
        gate_mtime = gate_path.stat().st_mtime
        metrics_mtime = metrics_path.stat().st_mtime
        add_acceptance_check(
            checks,
            "gate_after_sidecar_metrics",
            "pass" if gate_mtime >= metrics_mtime else "fail",
            "ai_controls/gate_status.json",
            "gate status was generated after sidecar metrics"
            if gate_mtime >= metrics_mtime
            else "gate status is stale relative to sidecar metrics",
        )

    if gate and leak_path.exists() and gate_path.exists():
        gate_mtime = gate_path.stat().st_mtime
        leak_mtime = leak_path.stat().st_mtime
        add_acceptance_check(
            checks,
            "gate_after_leak_scan",
            "pass" if gate_mtime >= leak_mtime else "fail",
            "ai_controls/gate_status.json",
            "gate status was generated after leak scan"
            if gate_mtime >= leak_mtime
            else "gate status is stale relative to leak scan",
        )

    if not contract:
        add_acceptance_check(
            checks,
            "contract_audit_present",
            "fail",
            "ai_controls/contract_audit_status.json",
            "contract audit is missing",
        )
    else:
        add_acceptance_check(
            checks,
            "contract_audit_clear",
            "pass" if contract.get("all_clear") else "fail",
            "ai_controls/contract_audit_status.json",
            "contract audit has no blockers"
            if contract.get("all_clear")
            else f"contract blockers={contract.get('blocker_count', 'unknown')}",
        )
        if gate_path.exists() and contract_path.exists():
            contract_mtime = contract_path.stat().st_mtime
            gate_mtime = gate_path.stat().st_mtime
            add_acceptance_check(
                checks,
                "contract_after_gate",
                "pass" if contract_mtime >= gate_mtime else "fail",
                "ai_controls/contract_audit_status.json",
                "contract audit was generated after gate status"
                if contract_mtime >= gate_mtime
                else "contract audit is stale relative to gate status",
            )

    blockers = [check for check in checks if check["severity"] == "blocker" and check["status"] != "pass"]
    warnings = [check for check in checks if check["severity"] == "warning" and check["status"] != "pass"]
    all_clear = not blockers
    if level == "preflight":
        decision = "accepted_for_preflight_decision" if all_clear else "hold_preflight"
        reliance = "preflight decision only; no uppercase assurance"
    else:
        decision = "ready_for_release_review" if all_clear else "hold_release_review"
        reliance = "release review only; no domain confirmation by itself"

    status = {
        "generated_at": now,
        "package": str(package),
        "level": level,
        "decision": decision,
        "reliance": reliance,
        "all_clear": all_clear,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
    }
    controls_dir.mkdir(parents=True, exist_ok=True)
    (controls_dir / "acceptance_audit_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(controls_dir / "acceptance_audit_report.md", render_acceptance_audit_report(status))
    return status


def render_acceptance_audit_report(status: dict) -> str:
    lines = [
        "# CRAMPS Acceptance Audit Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Level: `{status['level']}`",
        f"Decision: `{status['decision']}`",
        f"Reliance: {status['reliance']}",
        f"All clear: `{status['all_clear']}`",
        f"Blockers: `{status['blocker_count']}`",
        f"Warnings: `{status['warning_count']}`",
        "",
        "| check | status | severity | evidence | message |",
        "|---|---|---|---|---|",
    ]
    for check in status["checks"]:
        lines.append(
            f"| `{check['check_id']}` | `{check['status']}` | `{check['severity']}` | `{check['evidence']}` | {check['message']} |"
        )
    lines.append("")
    return "\n".join(lines)


def package_path_inside_sanitized_source(package: Path) -> bool:
    resolved = package.resolve()
    if not is_relative_to(resolved, ROOT):
        return False
    for dirname in SOURCE_TREE_PACKAGE_ROOTS:
        allowed_root = (ROOT / dirname).resolve()
        if resolved != allowed_root and is_relative_to(resolved, allowed_root):
            return False
    return True


def assert_package_output_allowed(package: Path, action: str) -> None:
    if not package.exists():
        raise SystemExit(f"Package not found: {package}")
    if package_path_inside_sanitized_source(package):
        raise SystemExit(
            f"Refusing to write {action} outputs inside sanitized source material. "
            "Create or copy the package under cramps_projects/ or outside this repository."
        )


def packet_output_dir(package: Path, out: Path | None) -> Path:
    output = out.resolve() if out else package / "exports" / "review_packet"
    if output == ROOT or (is_relative_to(output, ROOT) and not is_relative_to(output, package.resolve())):
        raise SystemExit(f"Refusing to write review-packet outputs inside controlled source material: {output}")
    return output


def path_modified_utc(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def iter_package_manifest_files(package: Path, output_dir: Path | None = None) -> list[Path]:
    files: list[Path] = []
    output_resolved = output_dir.resolve() if output_dir and output_dir.exists() else None
    for path in sorted(package.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if output_resolved and (path.resolve() == output_resolved or is_relative_to(path.resolve(), output_resolved)):
            continue
        files.append(path)
    return files


def material_changes_after_acceptance(package: Path, acceptance_path: Path, output_dir: Path) -> list[str]:
    if not acceptance_path.exists():
        return []
    acceptance_mtime = acceptance_path.stat().st_mtime
    allowed_exact = {
        STATE_FILE,
        "ai_controls/acceptance_audit_status.json",
        "ai_controls/acceptance_audit_report.md",
    }
    allowed_prefixes = ("exports/",)
    changed = []
    for path in iter_package_manifest_files(package, output_dir):
        rel = relative_artifact(package, path)
        if rel in allowed_exact or rel.startswith(allowed_prefixes):
            continue
        if path.stat().st_mtime > acceptance_mtime + 0.001:
            changed.append(rel)
    return changed


def build_review_manifest(package: Path, output_dir: Path, include_package_files: bool) -> list[dict[str, str]]:
    rows = []
    for path in iter_package_manifest_files(package, output_dir):
        rel = relative_artifact(package, path)
        rows.append(
            {
                "artifact_path": rel,
                "bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
                "modified_utc": path_modified_utc(path),
                "included_in_zip": "yes" if include_package_files else "no",
                "notes": "source package artifact",
            }
        )
    return rows


def add_review_packet_check(
    checks: list[dict[str, str]],
    check_id: str,
    status: str,
    severity: str,
    evidence: str,
    message: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": status,
            "severity": severity,
            "evidence": evidence,
            "message": message,
        }
    )


def review_packet_status(package: Path, level: str, output_dir: Path, include_package_files: bool) -> dict:
    state = load_state(package, required=False)
    metrics = load_json_artifact(package / "cramps_sidecar_metrics.json")
    agent = load_json_artifact(package / "ai_controls" / "agent_audit_status.json")
    leak = load_json_artifact(package / "ai_controls" / "leak_scan_status.json")
    gate = load_json_artifact(package / "ai_controls" / "gate_status.json")
    acceptance = load_json_artifact(package / "ai_controls" / "acceptance_audit_status.json")

    checks: list[dict[str, str]] = []
    add_review_packet_check(
        checks,
        "state_active",
        "pass" if state.get("status") == "active" else "fail",
        "blocker",
        STATE_FILE if state else "",
        "package state is active" if state.get("status") == "active" else f"package state is {state.get('status', 'missing')}",
    )

    acceptance_path = package / "ai_controls" / "acceptance_audit_status.json"
    if not acceptance:
        add_review_packet_check(checks, "acceptance_present", "fail", "blocker", "", "acceptance audit has not been run")
    else:
        add_review_packet_check(
            checks,
            "acceptance_level_matches",
            "pass" if acceptance.get("level") == level else "fail",
            "blocker",
            "ai_controls/acceptance_audit_status.json",
            "acceptance level matches review packet level"
            if acceptance.get("level") == level
            else f"acceptance level is {acceptance.get('level')}; expected {level}",
        )
        add_review_packet_check(
            checks,
            "acceptance_all_clear",
            "pass" if acceptance.get("all_clear") else "fail",
            "blocker",
            "ai_controls/acceptance_audit_status.json",
            "acceptance audit is clear"
            if acceptance.get("all_clear")
            else f"acceptance decision is {acceptance.get('decision', 'missing')}",
        )
        changed = material_changes_after_acceptance(package, acceptance_path, output_dir)
        add_review_packet_check(
            checks,
            "no_material_changes_after_acceptance",
            "pass" if not changed else "fail",
            "blocker",
            "ai_controls/acceptance_audit_status.json",
            "no material package artifacts changed after acceptance"
            if not changed
            else f"material artifacts changed after acceptance: {', '.join(changed[:10])}",
        )

    if leak:
        quarantine_required = bool(leak.get("quarantine_required"))
        add_review_packet_check(
            checks,
            "leak_scan_clear",
            "pass" if not quarantine_required else "fail",
            "blocker",
            "ai_controls/leak_scan_status.json",
            "leak scan has no quarantine-triggering findings"
            if not quarantine_required
            else "leak scan requires quarantine",
        )
    else:
        add_review_packet_check(checks, "leak_scan_present", "fail", "blocker", "", "leak scan has not been run")

    if gate:
        all_clear = bool(gate.get("summary", {}).get("all_clear"))
        add_review_packet_check(
            checks,
            "gate_all_clear",
            "pass" if all_clear else "fail",
            "blocker",
            "ai_controls/gate_status.json",
            "gate status is all clear"
            if all_clear
            else f"next blocked gate is {gate.get('summary', {}).get('next_blocked_gate', 'unknown')}",
        )
    else:
        add_review_packet_check(checks, "gate_present", "fail", "blocker", "", "gate status has not been run")

    blockers = [check for check in checks if check["severity"] == "blocker" and check["status"] != "pass"]
    decision = "ready_for_review_handoff" if not blockers else "hold_review_packet"
    return {
        "generated_at": utc_now(),
        "package": str(package),
        "level": level,
        "output_dir": str(output_dir),
        "decision": decision,
        "all_clear": not blockers,
        "blocker_count": len(blockers),
        "checks": checks,
        "include_package_files": include_package_files,
        "source": {
            "source_repo": state.get("source_repo", ""),
            "source_commit_at_package_creation": state.get("source_commit", ""),
            "source_dirty_at_creation": state.get("source_dirty_at_creation", ""),
            "current_source_commit": git_value("rev-parse", "HEAD"),
            "current_source_dirty": source_dirty(),
        },
        "controls": {
            "sidecar_recommendation": (metrics or {}).get("recommendation", ""),
            "sidecar_readiness_score": (metrics or {}).get("readiness_score", ""),
            "agent_audit_all_clear": (agent or {}).get("all_clear", ""),
            "leak_quarantine_required": (leak or {}).get("quarantine_required", ""),
            "gate_all_clear": ((gate or {}).get("summary") or {}).get("all_clear", ""),
            "acceptance_decision": (acceptance or {}).get("decision", ""),
            "acceptance_reliance": (acceptance or {}).get("reliance", ""),
        },
    }


def render_review_packet_summary(status: dict, manifest_rows: list[dict[str, str]]) -> str:
    lines = [
        "# CRAMPS Review Packet Summary",
        "",
        f"Generated: {status['generated_at']}",
        f"Level: `{status['level']}`",
        f"Decision: `{status['decision']}`",
        f"All clear: `{status['all_clear']}`",
        f"Blockers: `{status['blocker_count']}`",
        f"Package: `{status['package']}`",
        "",
        "## Reliance Boundary",
        "",
        "This packet is a reviewer handoff. It does not prove the domain claim, replace release authority, or override CRAMPS gate decisions.",
        "",
        "## Control Snapshot",
        "",
        "| control | value |",
        "|---|---|",
    ]
    for key, value in status["controls"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Packet Checks",
            "",
            "| check | status | severity | evidence | message |",
            "|---|---|---|---|---|",
        ]
    )
    for check in status["checks"]:
        lines.append(
            f"| `{check['check_id']}` | `{check['status']}` | `{check['severity']}` | `{check['evidence']}` | {check['message']} |"
        )
    lines.extend(
        [
            "",
            "## Manifest",
            "",
            f"Package artifact count: `{len(manifest_rows)}`",
            "",
            "Use `REVIEW_PACKET_MANIFEST.csv` for file-level hashes. By default, the ZIP contains only the packet index, not the package evidence files.",
        ]
    )
    return "\n".join(lines)


def render_reviewer_handoff(status: dict) -> str:
    return f"""
# Reviewer Handoff

## First Checks

1. Confirm `review_packet_status.json` has `decision` = `{status['decision']}`.
2. Confirm `REVIEW_PACKET_MANIFEST.csv` matches the package files being reviewed.
3. Read `ai_controls/acceptance_audit_report.md`, `ai_controls/gate_status.md`, `cramps_sidecar_metrics.md`, and `ai_controls/leak_scan_report.md` in the source package.
4. Do not treat this packet as release approval. It is a handoff index for review.

## If Blocked

If `decision` is `hold_review_packet`, resolve or formally accept the listed blockers, then rerun `check`, `agent-audit`, `leak-scan`, `gate`, `acceptance-audit`, and `review-packet` in that order.
"""


def write_review_packet_zip(output_dir: Path, manifest_rows: list[dict[str, str]], package: Path, include_package_files: bool) -> Path:
    zip_path = output_dir / "review_packet.zip"
    packet_files = [
        output_dir / "review_packet_status.json",
        output_dir / "REVIEW_PACKET_SUMMARY.md",
        output_dir / "REVIEWER_HANDOFF.md",
        output_dir / "REVIEW_PACKET_MANIFEST.csv",
    ]
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in packet_files:
            archive.write(path, path.name)
        if include_package_files:
            for row in manifest_rows:
                artifact = package / row["artifact_path"]
                if artifact.exists() and artifact.is_file():
                    archive.write(artifact, f"package/{row['artifact_path']}")
    return zip_path


def build_review_packet(package: Path, level: str, out: Path | None, allow_hold: bool, include_package_files: bool, create_zip: bool) -> dict:
    assert_package_output_allowed(package, "review-packet")
    output_dir = packet_output_dir(package, out)
    output_dir.mkdir(parents=True, exist_ok=True)
    status = review_packet_status(package, level, output_dir, include_package_files)
    manifest_rows = build_review_manifest(package, output_dir, include_package_files)
    write_csv(output_dir / "REVIEW_PACKET_MANIFEST.csv", REVIEW_PACKET_MANIFEST_FIELDS, manifest_rows)
    (output_dir / "review_packet_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(output_dir / "REVIEW_PACKET_SUMMARY.md", render_review_packet_summary(status, manifest_rows))
    write_text(output_dir / "REVIEWER_HANDOFF.md", render_reviewer_handoff(status))

    if create_zip:
        zip_path = write_review_packet_zip(output_dir, manifest_rows, package, include_package_files)
        status["zip_path"] = str(zip_path)
        status["zip_sha256"] = sha256_file(zip_path)
        (output_dir / "review_packet_status.json").write_text(
            json.dumps(status, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if status["blocker_count"] and not allow_hold:
        status["exit_code"] = 1
    else:
        status["exit_code"] = 0
    return status


def add_source_audit_check(
    checks: list[dict[str, str]],
    check_id: str,
    status: str,
    severity: str,
    evidence: str,
    message: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": status,
            "severity": severity,
            "evidence": evidence,
            "message": message,
        }
    )


def iter_source_text_files() -> list[Path]:
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SOURCE_AUDIT_SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in SOURCE_AUDIT_SKIP_SUFFIXES:
            continue
        if path.name in SOURCE_AUDIT_SKIP_NAMES:
            continue
        files.append(path)
    return files


def find_stale_source_names() -> list[str]:
    hits = []
    for path in iter_source_text_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(pattern.search(line) for pattern in STALE_NAME_PATTERNS):
                hits.append(f"{relative_artifact(ROOT, path)}:{line_number}")
                break
    return hits


def worked_example_mutation_guidance_hits() -> list[str]:
    hits = []
    commands = [
        "check",
        "agent-audit",
        "leak-scan",
        "gate",
        "acceptance-audit",
        "review-packet",
        "quarantine",
        "release-check package",
    ]
    needles = ["cramps_cli.py " + command + " worked_examples/" for command in commands]
    for path in iter_source_text_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(needle in line for needle in needles):
                hits.append(f"{relative_artifact(ROOT, path)}:{line_number}")
                break
    return hits


def source_junk_files() -> list[str]:
    return [
        relative_artifact(ROOT, path)
        for path in sorted(ROOT.rglob(".DS_Store"))
        if ".git" not in path.parts
    ]


def controlled_source_contamination() -> list[str]:
    contamination = []
    runtime_names = {
        STATE_FILE,
        "cramps_sidecar_metrics.json",
        "cramps_sidecar_metrics.md",
        "gate_status.json",
        "gate_status.md",
        "leak_scan_status.json",
        "acceptance_audit_status.json",
        "review_packet_status.json",
    }
    runtime_dirs = {"ai_controls", "exports", "quarantine"}
    for dirname in CONTROLLED_SOURCE_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            rel = relative_artifact(ROOT, path)
            if path.is_dir() and path.name in runtime_dirs:
                contamination.append(rel)
            elif path.is_file() and path.name in runtime_names:
                contamination.append(rel)
    return contamination


def worked_example_runtime_outputs() -> list[str]:
    runtime_names = {
        "cramps_sidecar_metrics.json",
        "cramps_sidecar_metrics.md",
        "gate_status.json",
        "gate_status.md",
        "leak_scan_status.json",
        "leak_scan_report.md",
        "acceptance_audit_status.json",
        "acceptance_audit_report.md",
        "review_packet_status.json",
        "contract_audit_status.json",
        "contract_audit_report.md",
    }
    runtime_dirs = {"exports", "quarantine"}
    base = ROOT / "worked_examples"
    if not base.exists():
        return []
    contamination = []
    for path in sorted(base.rglob("*")):
        rel = relative_artifact(ROOT, path)
        if path.is_dir() and path.name in runtime_dirs:
            contamination.append(rel)
        elif path.is_file() and path.name in runtime_names:
            contamination.append(rel)
    return contamination


def worked_example_manifest_hash_issues(base: Path | None = None, report_root: Path | None = None) -> list[str]:
    base = base or ROOT / "worked_examples"
    report_root = report_root or ROOT
    if not base.exists():
        return []
    expected_header = template_header("preflight_manifest.csv")
    issues = []
    for manifest in sorted(base.rglob("preflight_manifest.csv")):
        manifest_rel = relative_artifact(report_root, manifest)
        header = read_csv_header(manifest)
        if header != expected_header:
            issues.append(f"{manifest_rel} header mismatch")
            continue
        rows = read_csv_rows(manifest)
        if not rows:
            issues.append(f"{manifest_rel} has no manifest rows")
            continue
        manifest_dir = manifest.parent.resolve()
        for index, row in enumerate(rows, start=2):
            artifact_rel = (row.get("artifact_path") or "").strip()
            expected_digest = (row.get("sha256") or "").strip().lower()
            row_label = f"{manifest_rel}:line {index}"
            if not artifact_rel:
                issues.append(f"{row_label} missing artifact_path")
                continue
            if Path(artifact_rel).is_absolute() or ".." in Path(artifact_rel).parts:
                issues.append(f"{row_label} unsafe artifact_path {artifact_rel}")
                continue
            artifact = (manifest.parent / artifact_rel).resolve()
            if not is_relative_to(artifact, manifest_dir):
                issues.append(f"{row_label} artifact escapes worked example: {artifact_rel}")
                continue
            if not artifact.exists() or not artifact.is_file():
                issues.append(f"{row_label} missing artifact {artifact_rel}")
                continue
            if not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
                issues.append(f"{row_label} invalid sha256 for {artifact_rel}")
                continue
            actual_digest = sha256_file(artifact)
            if actual_digest != expected_digest:
                issues.append(f"{row_label} sha256 mismatch for {artifact_rel}")
    return issues


def missing_domain_artifacts(domains: list[dict]) -> list[str]:
    missing = []
    for domain in domains:
        pack_dir = ROOT / "domain_packs" / domain["slug"]
        for pattern in EXPECTED_DOMAIN_PACK_FILES:
            expected = pattern.format(full=domain["full"], light=domain["light"])
            path = pack_dir / expected
            if not path.exists():
                missing.append(relative_artifact(ROOT, path))
        overlay_matches = list((ROOT / "domain_overlays").glob(f"CRAMPS_{domain['slug'].upper()}_*_OVERLAY.md"))
        if not overlay_matches:
            missing.append(f"domain_overlays/CRAMPS_{domain['slug'].upper()}_*_OVERLAY.md")
        workbook = ROOT / "spreadsheets" / "domains" / f"{domain['light']}_{domain['full']}_Workbook.xlsx"
        if not workbook.exists():
            missing.append(relative_artifact(ROOT, workbook))
        printout = ROOT / "printouts" / f"{domain['slug']}_field_printout.md"
        if not printout.exists():
            missing.append(relative_artifact(ROOT, printout))
    return missing


def template_header_issues() -> list[str]:
    checks = {
        "templates/agent_deployment_plan.csv": AGENT_DEPLOYMENT_PLAN_FIELDS,
        "templates/agent_handoff_checklist.csv": AGENT_HANDOFF_FIELDS,
        "templates/agent_registry.csv": AGENT_REGISTRY_FIELDS,
    }
    issues = []
    for rel, expected in checks.items():
        header = read_csv_header(ROOT / rel)
        if header != expected:
            issues.append(f"{rel} header mismatch")
    return issues


def source_audit_status() -> dict:
    checks: list[dict[str, str]] = []
    domains = load_domains()
    gitignore = ROOT / ".gitignore"
    gitignore_text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    required_gitignore = [".DS_Store", "cramps_projects/", "dist/", "node_modules", "__pycache__/"]
    missing_gitignore = [item for item in required_gitignore if item not in gitignore_text]
    add_source_audit_check(
        checks,
        "gitignore_release_hygiene",
        "pass" if not missing_gitignore else "fail",
        "blocker",
        ".gitignore",
        "gitignore covers generated and local runtime artifacts"
        if not missing_gitignore
        else f"missing gitignore entries: {', '.join(missing_gitignore)}",
    )

    required_paths = [
        "README.md",
        "tools/cramps_cli.py",
        "tools/cramps_sidecar.py",
        "tools/cramps_domains.json",
        "program/README.md",
        "program/RELEASE_ACCEPTANCE_CHECKLIST.md",
        "program/AUDIT_AND_INSPECTION_PACKET.md",
        "policies/CRAMPS_NAMING_AND_ASSURANCE_LEVELS_2026-05-15.md",
        "templates/README.md",
        "spreadsheets/CRAMPS_Governance_Master.xlsx",
    ]
    missing_required = [rel for rel in required_paths if not (ROOT / rel).exists()]
    add_source_audit_check(
        checks,
        "required_source_documents",
        "pass" if not missing_required else "fail",
        "blocker",
        "source tree",
        "required source-kit documents are present"
        if not missing_required
        else f"missing required paths: {', '.join(missing_required)}",
    )

    stale_hits = find_stale_source_names()
    add_source_audit_check(
        checks,
        "stale_name_scan",
        "pass" if not stale_hits else "fail",
        "blocker",
        "source text scan",
        "no stale legacy project names found"
        if not stale_hits
        else f"stale names found at: {', '.join(stale_hits[:10])}",
    )

    worked_example_guidance_hits = worked_example_mutation_guidance_hits()
    add_source_audit_check(
        checks,
        "worked_example_mutation_guidance",
        "pass" if not worked_example_guidance_hits else "fail",
        "blocker",
        "source text scan",
        "worked-example docs route mutating CLI checks through isolated copies"
        if not worked_example_guidance_hits
        else f"direct worked-example mutation commands found at: {', '.join(worked_example_guidance_hits[:10])}",
    )

    contamination = controlled_source_contamination()
    add_source_audit_check(
        checks,
        "controlled_source_contamination",
        "pass" if not contamination else "fail",
        "blocker",
        "controlled source directories",
        "no package runtime outputs found inside controlled source material"
        if not contamination
        else f"package runtime artifacts found: {', '.join(contamination[:10])}",
    )

    worked_runtime = worked_example_runtime_outputs()
    add_source_audit_check(
        checks,
        "worked_example_runtime_outputs",
        "pass" if not worked_runtime else "fail",
        "blocker",
        "worked_examples/",
        "worked examples contain no committed runtime outputs"
        if not worked_runtime
        else f"worked example runtime artifacts found: {', '.join(worked_runtime[:10])}",
    )

    manifest_issues = worked_example_manifest_hash_issues()
    add_source_audit_check(
        checks,
        "worked_example_manifest_hashes",
        "pass" if not manifest_issues else "fail",
        "blocker",
        "worked_examples/**/preflight_manifest.csv",
        "worked-example manifest checksums match current artifacts"
        if not manifest_issues
        else f"worked-example manifest issues: {', '.join(manifest_issues[:10])}",
    )

    missing_domains = missing_domain_artifacts(domains)
    add_source_audit_check(
        checks,
        "domain_artifact_matrix",
        "pass" if not missing_domains else "fail",
        "blocker",
        "domain packs, overlays, printouts, workbooks",
        f"all {len(domains)} configured domains have expected artifacts"
        if not missing_domains
        else f"missing domain artifacts: {', '.join(missing_domains[:12])}",
    )

    header_issues = template_header_issues()
    add_source_audit_check(
        checks,
        "template_header_contracts",
        "pass" if not header_issues else "fail",
        "blocker",
        "templates/*.csv",
        "agent template headers match CLI contracts"
        if not header_issues
        else f"template header issues: {', '.join(header_issues)}",
    )

    contract_status = contract_audit_status("source", None, "auto")
    add_source_audit_check(
        checks,
        "source_csv_contracts",
        "pass" if contract_status["blocker_count"] == 0 else "fail",
        "blocker",
        "contract-audit source",
        "source CSV contracts are internally consistent"
        if contract_status["blocker_count"] == 0
        else f"source CSV contract blockers: {contract_status['blocker_count']}",
    )

    junk = source_junk_files()
    add_source_audit_check(
        checks,
        "local_junk_files",
        "pass" if not junk else "warn",
        "warning",
        "source tree",
        "no local .DS_Store files outside .git"
        if not junk
        else f"local junk files present: {', '.join(junk[:10])}",
    )

    generated_projects = [relative_artifact(ROOT, path) for path in sorted((ROOT / "cramps_projects").glob("*"))] if (ROOT / "cramps_projects").exists() else []
    add_source_audit_check(
        checks,
        "local_generated_projects",
        "pass" if not generated_projects else "warn",
        "warning",
        "cramps_projects/",
        "no local generated package directories present"
        if not generated_projects
        else f"local generated packages are present but ignored: {', '.join(generated_projects[:8])}",
    )

    add_source_audit_check(
        checks,
        "git_worktree_clean",
        "pass" if not source_dirty() else "warn",
        "warning",
        "git status --short",
        "git worktree is clean" if not source_dirty() else "git worktree has uncommitted source changes",
    )

    blockers = [check for check in checks if check["severity"] == "blocker" and check["status"] != "pass"]
    warnings = [check for check in checks if check["severity"] == "warning" and check["status"] != "pass"]
    return {
        "generated_at": utc_now(),
        "source_repo": str(ROOT),
        "source_commit": git_value("rev-parse", "HEAD"),
        "source_dirty": source_dirty(),
        "domain_count": len(domains),
        "decision": "source_kit_release_candidate" if not blockers else "hold_source_kit_release",
        "all_clear": not blockers,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
    }


def render_source_audit_report(status: dict) -> str:
    lines = [
        "# CRAMPS Source Kit Audit Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Decision: `{status['decision']}`",
        f"Source commit: `{status['source_commit']}`",
        f"Source dirty: `{status['source_dirty']}`",
        f"Domain count: `{status['domain_count']}`",
        f"Blockers: `{status['blocker_count']}`",
        f"Warnings: `{status['warning_count']}`",
        "",
        "This audit checks the reusable source kit, not a study package. It does not replace package `check`, `agent-audit`, `leak-scan`, `gate`, `acceptance-audit`, or `review-packet`.",
        "",
        "| check | status | severity | evidence | message |",
        "|---|---|---|---|---|",
    ]
    for check in status["checks"]:
        lines.append(
            f"| `{check['check_id']}` | `{check['status']}` | `{check['severity']}` | `{check['evidence']}` | {check['message']} |"
        )
    lines.append("")
    return "\n".join(lines)


def default_source_snapshot_dir() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    commit = git_value("rev-parse", "--short", "HEAD") or "unknown"
    return ROOT / "dist" / "source_snapshots" / f"{stamp}_{commit}"


def source_snapshot_output_dir(out: Path | None, force: bool) -> Path:
    output = (out or default_source_snapshot_dir()).expanduser().resolve()
    if output == ROOT:
        raise SystemExit("Refusing to write source snapshot into the source repository root.")
    dist_root = (ROOT / "dist").resolve()
    if is_relative_to(output, ROOT) and not is_relative_to(output, dist_root):
        raise SystemExit(f"Refusing to write source snapshot inside the source repository outside dist/: {output}")
    for dirname in CONTROLLED_SOURCE_DIRS:
        controlled = (ROOT / dirname).resolve()
        if output == controlled or is_relative_to(output, controlled):
            raise SystemExit(f"Refusing to write source snapshot inside controlled source material: {controlled}")
    if output.exists() and any(output.iterdir()) and not force:
        raise SystemExit(f"Snapshot output directory is not empty. Re-run with --force if intentional: {output}")
    return output


def iter_source_snapshot_files(output_dir: Path) -> list[Path]:
    files = []
    output_resolved = output_dir.resolve()
    skip_names = {".DS_Store"}
    skip_suffixes = {".pyc"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SOURCE_AUDIT_SKIP_DIRS for part in path.parts):
            continue
        if path.name in skip_names or path.suffix.lower() in skip_suffixes:
            continue
        if path.resolve() == output_resolved or is_relative_to(path.resolve(), output_resolved):
            continue
        files.append(path)
    return files


def build_source_snapshot_manifest(output_dir: Path) -> list[dict[str, str]]:
    rows = []
    for path in iter_source_snapshot_files(output_dir):
        rows.append(
            {
                "artifact_path": relative_artifact(ROOT, path),
                "bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
                "modified_utc": path_modified_utc(path),
                "included_in_zip": "yes",
            }
        )
    return rows


def source_snapshot_digest(rows: list[dict[str, str]]) -> str:
    stable = [
        {
            "artifact_path": row["artifact_path"],
            "bytes": row["bytes"],
            "sha256": row["sha256"],
        }
        for row in rows
    ]
    return hashlib.sha256(json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def render_source_snapshot_summary(status: dict, manifest_rows: list[dict[str, str]]) -> str:
    lines = [
        "# CRAMPS Source Snapshot Summary",
        "",
        f"Generated: {status['generated_at']}",
        f"Decision: `{status['decision']}`",
        f"Source commit: `{status['source_commit']}`",
        f"Source dirty: `{status['source_dirty']}`",
        f"Source audit blockers: `{status['source_audit_blockers']}`",
        f"Source audit warnings: `{status['source_audit_warnings']}`",
        f"Snapshot digest: `{status['snapshot_sha256']}`",
        f"Artifact count: `{len(manifest_rows)}`",
        "",
        "This snapshot is a source-kit handoff record. It does not certify any study package or domain claim.",
        "",
        "## Checks",
        "",
        "| check | status | message |",
        "|---|---|---|",
    ]
    for check in status["checks"]:
        lines.append(f"| `{check['check_id']}` | `{check['status']}` | {check['message']} |")
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            "- `source_snapshot_status.json`",
            "- `SOURCE_SNAPSHOT_SUMMARY.md`",
            "- `SOURCE_SNAPSHOT_MANIFEST.csv`",
            "- `source_snapshot.zip` when ZIP creation is enabled",
        ]
    )
    return "\n".join(lines)


def write_source_snapshot_zip(output_dir: Path, manifest_rows: list[dict[str, str]]) -> Path:
    zip_path = output_dir / "source_snapshot.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for row in manifest_rows:
            artifact = ROOT / row["artifact_path"]
            if artifact.exists() and artifact.is_file():
                archive.write(artifact, f"CRAMPS-Governance/{row['artifact_path']}")
        for packet_file in [
            output_dir / "source_snapshot_status.json",
            output_dir / "SOURCE_SNAPSHOT_SUMMARY.md",
            output_dir / "SOURCE_SNAPSHOT_MANIFEST.csv",
        ]:
            if packet_file.exists():
                archive.write(packet_file, f"CRAMPS-Governance/{packet_file.name}")
    return zip_path


def build_source_snapshot(
    out: Path | None,
    force: bool,
    allow_dirty: bool,
    allow_warning: bool,
    create_zip: bool,
) -> dict:
    output_dir = source_snapshot_output_dir(out, force)
    audit = source_audit_status()
    manifest_rows = build_source_snapshot_manifest(output_dir)
    checks: list[dict[str, str]] = []

    def add_check(check_id: str, ok: bool, message: str) -> None:
        checks.append({"check_id": check_id, "status": "pass" if ok else "fail", "message": message})

    add_check(
        "source_audit_blockers",
        audit["blocker_count"] == 0,
        f"source audit blockers={audit['blocker_count']}",
    )
    add_check(
        "source_audit_warnings",
        allow_warning or audit["warning_count"] == 0,
        f"source audit warnings={audit['warning_count']}",
    )
    add_check(
        "source_dirty",
        allow_dirty or not audit["source_dirty"],
        f"source dirty={audit['source_dirty']}",
    )
    add_check(
        "manifest_nonempty",
        bool(manifest_rows),
        f"manifest artifact count={len(manifest_rows)}",
    )

    failed = [check for check in checks if check["status"] != "pass"]
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "SOURCE_SNAPSHOT_MANIFEST.csv", SOURCE_SNAPSHOT_MANIFEST_FIELDS, manifest_rows)
    status = {
        "generated_at": utc_now(),
        "decision": "source_snapshot_ready" if not failed else "hold_source_snapshot",
        "source_repo": str(ROOT),
        "source_commit": audit["source_commit"],
        "source_dirty": audit["source_dirty"],
        "source_audit_blockers": audit["blocker_count"],
        "source_audit_warnings": audit["warning_count"],
        "output_dir": str(output_dir),
        "artifact_count": len(manifest_rows),
        "snapshot_sha256": source_snapshot_digest(manifest_rows),
        "zip_path": "",
        "zip_sha256": "",
        "checks": checks,
    }
    (output_dir / "source_snapshot_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(output_dir / "SOURCE_SNAPSHOT_SUMMARY.md", render_source_snapshot_summary(status, manifest_rows))
    if create_zip and not failed:
        zip_path = write_source_snapshot_zip(output_dir, manifest_rows)
        status["zip_path"] = str(zip_path)
        status["zip_sha256"] = sha256_file(zip_path)
        (output_dir / "source_snapshot_status.json").write_text(
            json.dumps(status, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    status["exit_code"] = 0 if not failed else 1
    return status


def default_release_check_dir(scope: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    commit = git_value("rev-parse", "--short", "HEAD") or "unknown"
    return ROOT / "dist" / "release_checks" / f"{stamp}_{commit}_{scope}"


def release_check_output_dir(scope: str, out: Path | None, force: bool, package: Path | None = None) -> Path:
    if out:
        output = out.expanduser().resolve()
    elif scope == "package" and package is not None:
        output = package / "exports" / "release_check"
    else:
        output = default_release_check_dir(scope)

    if output == ROOT:
        raise SystemExit("Refusing to write release-check outputs into the source repository root.")
    dist_root = (ROOT / "dist").resolve()
    if scope == "source" and is_relative_to(output, ROOT) and not is_relative_to(output, dist_root):
        raise SystemExit(f"Refusing to write source release-check outputs inside the source repository outside dist/: {output}")
    if scope == "package" and is_relative_to(output, ROOT):
        if package is None or not is_relative_to(output, package.resolve()):
            raise SystemExit(f"Refusing to write package release-check outputs inside sanitized source material: {output}")
    if any(output == (ROOT / dirname).resolve() or is_relative_to(output, (ROOT / dirname).resolve()) for dirname in CONTROLLED_SOURCE_DIRS):
        raise SystemExit(f"Refusing to write release-check outputs inside controlled source material: {output}")
    if output.exists() and any(output.iterdir()) and not force:
        raise SystemExit(f"Release-check output directory is not empty. Re-run with --force if intentional: {output}")
    return output


def compact_command_message(result: subprocess.CompletedProcess[str]) -> str:
    text = (result.stdout or result.stderr or "").strip()
    if not text:
        return "command completed" if result.returncode == 0 else "command failed without output"
    text = " ".join(text.split())
    if len(text) > 240:
        return text[:237] + "..."
    return text


def run_release_command(
    check_id: str,
    scope: str,
    command: list[str],
    output_dir: Path,
    severity: str = "blocker",
    pass_codes: tuple[int, ...] = (0,),
) -> dict[str, str]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / f"{check_id}.log"
    log_path.write_text(
        "\n".join(
            [
                f"$ {shlex.join(command)}",
                f"exit_code={result.returncode}",
                "",
                "## stdout",
                result.stdout.rstrip(),
                "",
                "## stderr",
                result.stderr.rstrip(),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "check_id": check_id,
        "scope": scope,
        "status": "pass" if result.returncode in pass_codes else "fail",
        "severity": severity,
        "evidence": relative_artifact(output_dir, log_path),
        "exit_code": str(result.returncode),
        "message": compact_command_message(result),
    }


def render_release_check_report(status: dict) -> str:
    lines = [
        "# CRAMPS Release Check Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Scope: `{status['scope']}`",
        f"Decision: `{status['decision']}`",
        f"All clear: `{status['all_clear']}`",
        f"Blockers: `{status['blocker_count']}`",
        f"Warnings: `{status['warning_count']}`",
        f"Output directory: `{status['output_dir']}`",
        "",
    ]
    if status["scope"] == "source":
        lines.extend(
            [
                f"Source commit: `{status['source_commit']}`",
                f"Source dirty: `{status['source_dirty']}`",
                "",
            ]
        )
    else:
        lines.extend(
            [
                f"Package: `{status['package']}`",
                f"Level: `{status['level']}`",
                "",
            ]
        )
    lines.extend(
        [
            "| check | status | severity | exit | evidence | message |",
            "|---|---|---|---:|---|---|",
        ]
    )
    for check in status["checks"]:
        lines.append(
            f"| `{check['check_id']}` | `{check['status']}` | `{check['severity']}` | {check['exit_code']} | `{check['evidence']}` | {check['message']} |"
        )
    lines.append("")
    if status["blocker_count"]:
        lines.extend(
            [
                "## Release Hold",
                "",
                "Do not push, hand off, publish, or rely on this artifact until the failed blocker checks are corrected or formally documented as an approved deviation.",
                "",
            ]
        )
    return "\n".join(lines)


def write_release_check_outputs(output_dir: Path, status: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "RELEASE_CHECK_RESULTS.csv", RELEASE_CHECK_FIELDS, status["checks"])
    (output_dir / "release_check_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(output_dir / "RELEASE_CHECK_REPORT.md", render_release_check_report(status))


def build_source_release_check(
    out: Path | None,
    force: bool,
    allow_dirty: bool,
    allow_warning: bool,
    skip_workbooks: bool,
    no_snapshot: bool,
) -> dict:
    output_dir = release_check_output_dir("source", out, force)
    script = str(Path(__file__).resolve())
    checks: list[dict[str, str]] = []
    checks.append(
        run_release_command(
            "python_compile",
            "source",
            [
                sys.executable,
                "-m",
                "py_compile",
                "tools/cramps_cli.py",
                "tools/cramps_sidecar.py",
                "tools/scaffold_cramps_package.py",
                "tools/generate_domain_packs.py",
            ],
            output_dir,
        )
    )
    checks.append(run_release_command("doctor", "source", [sys.executable, script, "doctor"], output_dir))
    checks.append(
        run_release_command(
            "contract_audit",
            "source",
            [sys.executable, script, "contract-audit", "source", "--out", str(output_dir / "contract_audit"), "--force"],
            output_dir,
        )
    )
    source_audit_cmd = [sys.executable, script, "source-audit"]
    if not allow_warning:
        source_audit_cmd.append("--fail-on-warning")
    checks.append(run_release_command("source_audit", "source", source_audit_cmd, output_dir))

    self_test_cmd = [sys.executable, script, "self-test"]
    if not allow_dirty and not allow_warning:
        self_test_cmd.append("--strict-source")
    checks.append(run_release_command("self_test", "source", self_test_cmd, output_dir))

    if not skip_workbooks:
        checks.append(run_release_command("workbook_verify", "source", ["node", "tools/verify_workbooks.mjs"], output_dir))

    checks.append(run_release_command("whitespace_diff_check", "source", ["git", "diff", "--check"], output_dir))

    if not no_snapshot:
        snapshot_cmd = [
            sys.executable,
            script,
            "source-snapshot",
            "--out",
            str(output_dir / "source_snapshot"),
            "--force",
        ]
        if allow_dirty:
            snapshot_cmd.append("--allow-dirty")
        if allow_warning:
            snapshot_cmd.append("--allow-warning")
        checks.append(run_release_command("source_snapshot", "source", snapshot_cmd, output_dir))

    blockers = [check for check in checks if check["severity"] == "blocker" and check["status"] != "pass"]
    warnings = [check for check in checks if check["severity"] == "warning" and check["status"] != "pass"]
    status = {
        "generated_at": utc_now(),
        "scope": "source",
        "decision": "source_release_ready" if not blockers else "hold_source_release",
        "all_clear": not blockers and not warnings,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "source_repo": str(ROOT),
        "source_commit": git_value("rev-parse", "HEAD"),
        "source_dirty": source_dirty(),
        "output_dir": str(output_dir),
        "checks": checks,
    }
    write_release_check_outputs(output_dir, status)
    return status


def build_package_release_check(
    package: Path,
    level: str,
    out: Path | None,
    force: bool,
    include_package_files: bool,
    fail_on_warning: bool,
) -> dict:
    package = package.resolve()
    assert_package_output_allowed(package, "release-check")
    level = package_level(package, level)
    output_dir = release_check_output_dir("package", out, force, package)
    script = str(Path(__file__).resolve())
    checks: list[dict[str, str]] = []
    checks.append(run_release_command("check", "package", [sys.executable, script, "check", str(package), "--level", level], output_dir))
    agent_cmd = [sys.executable, script, "agent-audit", str(package), "--level", level]
    if fail_on_warning:
        agent_cmd.append("--fail-on-warning")
    checks.append(run_release_command("agent_audit", "package", agent_cmd, output_dir))
    checks.append(run_release_command("leak_scan", "package", [sys.executable, script, "leak-scan", str(package), "--fail-on-quarantine"], output_dir))
    checks.append(run_release_command("gate", "package", [sys.executable, script, "gate", str(package), "--level", level], output_dir))
    checks.append(run_release_command("contract_audit", "package", [sys.executable, script, "contract-audit", "package", str(package), "--level", level], output_dir))
    acceptance_cmd = [sys.executable, script, "acceptance-audit", str(package), "--level", level]
    if fail_on_warning:
        acceptance_cmd.append("--fail-on-warning")
    checks.append(run_release_command("acceptance_audit", "package", acceptance_cmd, output_dir))
    review_cmd = [
        sys.executable,
        script,
        "review-packet",
        str(package),
        "--level",
        level,
        "--out",
        str(output_dir / "review_packet"),
    ]
    if include_package_files:
        review_cmd.append("--include-package-files")
    checks.append(run_release_command("review_packet", "package", review_cmd, output_dir))

    blockers = [check for check in checks if check["severity"] == "blocker" and check["status"] != "pass"]
    warnings = [check for check in checks if check["severity"] == "warning" and check["status"] != "pass"]
    status = {
        "generated_at": utc_now(),
        "scope": "package",
        "decision": "package_release_ready" if not blockers else "hold_package_release",
        "all_clear": not blockers and not warnings,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "package": str(package),
        "level": level,
        "output_dir": str(output_dir),
        "checks": checks,
    }
    write_release_check_outputs(output_dir, status)
    return status


def add_self_test_check(
    checks: list[dict[str, str]],
    check_id: str,
    status: str,
    message: str,
    evidence: str = "",
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": status,
            "message": message,
            "evidence": evidence,
        }
    )


def run_cli_subprocess(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_json_stdout(result: subprocess.CompletedProcess[str]) -> dict:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def render_self_test_report(status: dict) -> str:
    lines = [
        "# CRAMPS Self-Test Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Decision: `{status['decision']}`",
        f"Temp directory: `{status['temp_dir']}`",
        f"Checks passed: `{status['passed_count']}`",
        f"Checks failed: `{status['failed_count']}`",
        "",
        "| check | status | evidence | message |",
        "|---|---|---|---|",
    ]
    for check in status["checks"]:
        lines.append(f"| `{check['check_id']}` | `{check['status']}` | `{check['evidence']}` | {check['message']} |")
    lines.append("")
    return "\n".join(lines)


def run_self_test(strict_source: bool, keep_temp: bool) -> dict:
    checks: list[dict[str, str]] = []
    temp_path = Path(tempfile.mkdtemp(prefix="cramps-selftest-"))
    try:
        source_status = source_audit_status()
        source_ok = source_status["blocker_count"] == 0 and (not strict_source or source_status["warning_count"] == 0)
        add_self_test_check(
            checks,
            "source_audit",
            "pass" if source_ok else "fail",
            f"source audit blockers={source_status['blocker_count']}, warnings={source_status['warning_count']}",
            "source-audit",
        )

        snapshot_command = ["source-snapshot", "--out", str(temp_path / "source-snapshot")]
        if not strict_source:
            snapshot_command.extend(["--allow-dirty", "--allow-warning"])
        snapshot_result = run_cli_subprocess(snapshot_command)
        snapshot_json = parse_json_stdout(snapshot_result)
        snapshot_zip = Path(snapshot_json.get("zip_path", ""))
        snapshot_ok = snapshot_result.returncode == 0 and snapshot_json.get("decision") == "source_snapshot_ready" and snapshot_zip.exists()
        add_self_test_check(
            checks,
            "source_snapshot",
            "pass" if snapshot_ok else "fail",
            "source snapshot created with manifest and ZIP"
            if snapshot_ok
            else f"source snapshot failed: exit={snapshot_result.returncode}, decision={snapshot_json.get('decision', 'missing')}",
            " ".join(snapshot_command),
        )

        package = temp_path / "worked-preflight"
        shutil.copytree(ROOT / "worked_examples" / "preflight" / "cramps-phy-synthetic-coordinate-recurrence", package)
        add_self_test_check(checks, "temp_package_copy", "pass", "worked example copied into temp package", str(package))

        manifest_clean_issues = worked_example_manifest_hash_issues(package, temp_path)
        add_self_test_check(
            checks,
            "worked_manifest_hash_clean",
            "pass" if not manifest_clean_issues else "fail",
            "worked-example manifest hashes are current in temp copy"
            if not manifest_clean_issues
            else f"manifest issues: {', '.join(manifest_clean_issues[:6])}",
            "worked-example manifest clean check",
        )

        tampered = temp_path / "tampered-worked-preflight"
        shutil.copytree(ROOT / "worked_examples" / "preflight" / "cramps-phy-synthetic-coordinate-recurrence", tampered)
        tampered_scope = tampered / "preflight_scope.md"
        tampered_scope.write_text(tampered_scope.read_text(encoding="utf-8") + "\nSelf-test tamper line.\n", encoding="utf-8")
        tamper_issues = worked_example_manifest_hash_issues(tampered, temp_path)
        tamper_detected = any("sha256 mismatch" in issue and "preflight_scope.md" in issue for issue in tamper_issues)
        add_self_test_check(
            checks,
            "worked_manifest_hash_tamper_trap",
            "pass" if tamper_detected else "fail",
            "worked-example manifest detected a modified custody artifact"
            if tamper_detected
            else f"expected sha256 mismatch for preflight_scope.md; got: {', '.join(tamper_issues[:6])}",
            "worked-example manifest tamper check",
        )

        broken_contract = temp_path / "broken-contract-preflight"
        shutil.copytree(ROOT / "worked_examples" / "preflight" / "cramps-phy-synthetic-coordinate-recurrence", broken_contract)
        row_path = broken_contract / "preflight_rows.csv"
        row_header = read_csv_header(row_path)
        row_rows = read_csv_rows(row_path)
        if row_rows:
            row_rows[0]["source_id"] = "SRC-MISSING-SELFTEST"
            write_csv(row_path, row_header, row_rows)
        broken_contract_result = run_cli_subprocess(["contract-audit", "package", str(broken_contract), "--level", "preflight"])
        broken_contract_json = parse_json_stdout(broken_contract_result)
        contract_trap_blocked = (
            broken_contract_result.returncode == 1
            and broken_contract_json.get("decision") == "hold_contract_audit"
            and broken_contract_json.get("blocker_count", 0) > 0
        )
        add_self_test_check(
            checks,
            "contract_reference_tamper_trap",
            "pass" if contract_trap_blocked else "fail",
            "contract audit detected a row referencing a missing source"
            if contract_trap_blocked
            else (
                "expected hold_contract_audit for missing source reference; "
                f"got exit={broken_contract_result.returncode}, "
                f"decision={broken_contract_json.get('decision', 'missing')}"
            ),
            "contract-audit package broken-contract-preflight",
        )

        multi_agent = temp_path / "multi-agent-preflight"
        shutil.copytree(ROOT / "worked_examples" / "preflight" / "cramps-phy-synthetic-coordinate-recurrence", multi_agent)
        plan_path = multi_agent / "ai_controls" / "agent_deployment_plan.csv"
        plan_rows = read_csv_rows(plan_path)
        plan_rows.append(
            {
                "study_id": "EX-PHY-001",
                "package_level": "preflight",
                "deployment_mode": "extra_preflight_operator",
                "agent_id": "second_preflight_operator",
                "agent_role": "preflight_operator",
                "assigned_scope": "Second active operator injected by self-test",
                "allowed_inputs": "Package files; synthetic teaching sources",
                "prohibited_inputs": "Source-kit edits; restricted data; uppercase assurance claims",
                "required_outputs": "preflight review notes",
                "reviewer_id": "",
                "gate_start": "G0",
                "gate_stop": "P5",
                "can_write": "yes-package-only",
                "can_export": "no-before-P5",
                "human_review_required": "yes-before-promotion",
                "status": "active",
                "notes": "Self-test injected second active row.",
            }
        )
        write_csv(plan_path, AGENT_DEPLOYMENT_PLAN_FIELDS, plan_rows)
        registry_path = multi_agent / "ai_controls" / "agent_registry.csv"
        registry_rows = read_csv_rows(registry_path)
        registry_rows.append(
            {
                "agent_id": "second_preflight_operator",
                "agent_name": "Second preflight operator",
                "agent_type": "human_or_ai",
                "purpose": "Injected self-test operator",
                "allowed_inputs": "Package files; synthetic teaching sources",
                "prohibited_inputs": "Source-kit edits; restricted data; uppercase assurance claims",
                "output_schema": "preflight review notes",
                "model_or_tool_version": "not_applicable",
                "prompt_or_sop_version": "self-test",
                "human_review_required": "yes-before-promotion",
                "audit_log_path": "logs/ai_activity_log.csv",
                "status": "active",
            }
        )
        write_csv(registry_path, AGENT_REGISTRY_FIELDS, registry_rows)
        multi_agent_result = run_cli_subprocess(["agent-audit", str(multi_agent), "--level", "preflight"])
        multi_agent_status = load_json_artifact(multi_agent / "ai_controls" / "agent_audit_status.json") or {}
        multi_agent_codes = {issue.get("code", "") for issue in multi_agent_status.get("issues", [])}
        multi_agent_blocked = (
            multi_agent_result.returncode == 1
            and "preflight_multi_agent_without_deviation" in multi_agent_codes
        )
        add_self_test_check(
            checks,
            "preflight_multi_agent_tamper_trap",
            "pass" if multi_agent_blocked else "fail",
            "agent audit blocked an undeclared second preflight operator"
            if multi_agent_blocked
            else (
                "expected preflight_multi_agent_without_deviation; "
                f"got exit={multi_agent_result.returncode}, codes={', '.join(sorted(multi_agent_codes))}"
            ),
            "agent-audit package multi-agent-preflight",
        )

        leak_package = temp_path / "leak-preflight"
        shutil.copytree(ROOT / "worked_examples" / "preflight" / "cramps-phy-synthetic-coordinate-recurrence", leak_package)
        write_text(
            leak_package / "intake" / "selftest_leak_fixture.txt",
            "Synthetic leak fixture for self-test only.\n-----BEGIN PRIVATE KEY-----",
        )
        leak_trap_result = run_cli_subprocess(["leak-scan", str(leak_package), "--fail-on-quarantine"])
        leak_trap_json = parse_json_stdout(leak_trap_result)
        leak_trap_blocked = (
            leak_trap_result.returncode == 2
            and leak_trap_json.get("quarantine_required") is True
            and leak_trap_json.get("open_critical_findings", 0) > 0
        )
        add_self_test_check(
            checks,
            "leak_quarantine_tamper_trap",
            "pass" if leak_trap_blocked else "fail",
            "leak scan required quarantine for a synthetic critical pattern"
            if leak_trap_blocked
            else (
                "expected quarantine_required with exit=2; "
                f"got exit={leak_trap_result.returncode}, "
                f"quarantine_required={leak_trap_json.get('quarantine_required', 'missing')}"
            ),
            "leak-scan --fail-on-quarantine leak-preflight",
        )

        sequence = [
            ("check", ["check", str(package), "--level", "preflight"]),
            ("agent_audit", ["agent-audit", str(package), "--level", "preflight"]),
            ("leak_scan", ["leak-scan", str(package)]),
            ("gate", ["gate", str(package), "--level", "preflight"]),
            ("contract_audit", ["contract-audit", "package", str(package), "--level", "preflight"]),
            ("acceptance_audit", ["acceptance-audit", str(package), "--level", "preflight"]),
            ("review_packet", ["review-packet", str(package), "--level", "preflight"]),
        ]
        for check_id, command in sequence:
            result = run_cli_subprocess(command)
            add_self_test_check(
                checks,
                check_id,
                "pass" if result.returncode == 0 else "fail",
                result.stdout.strip().replace("\n", " ")[:400] if result.returncode == 0 else result.stderr.strip()[:400],
                " ".join(command),
            )

        review_status_path = package / "exports" / "review_packet" / "review_packet_status.json"
        review_status = load_json_artifact(review_status_path) or {}
        ready = review_status.get("decision") == "ready_for_review_handoff"
        add_self_test_check(
            checks,
            "review_packet_decision",
            "pass" if ready else "fail",
            f"review-packet decision={review_status.get('decision', 'missing')}",
            relative_artifact(package, review_status_path),
        )

        zip_path = package / "exports" / "review_packet" / "review_packet.zip"
        if zip_path.exists():
            with zipfile.ZipFile(zip_path) as archive:
                names = archive.namelist()
            bounded = names and not any(name.startswith("package/") for name in names)
            add_self_test_check(
                checks,
                "bounded_review_zip",
                "pass" if bounded else "fail",
                "default review ZIP contains only packet index files" if bounded else "default review ZIP included package evidence files",
                relative_artifact(package, zip_path),
            )
        else:
            add_self_test_check(checks, "bounded_review_zip", "fail", "review ZIP was not created", relative_artifact(package, zip_path))

        status_result = run_cli_subprocess(["status", str(package)])
        status_json = parse_json_stdout(status_result)
        status_ok = (
            status_result.returncode == 0
            and status_json.get("review_packet", {}).get("decision") == "ready_for_review_handoff"
        )
        add_self_test_check(
            checks,
            "status_reports_review_packet",
            "pass" if status_ok else "fail",
            "status includes ready review-packet decision" if status_ok else "status did not include ready review-packet decision",
            "status",
        )

        time.sleep(1.05)
        (package / "preflight_decision.md").touch()
        stale_result = run_cli_subprocess(["review-packet", str(package), "--level", "preflight"])
        stale_json = parse_json_stdout(stale_result)
        stale_blocked = stale_result.returncode == 1 and stale_json.get("decision") == "hold_review_packet"
        add_self_test_check(
            checks,
            "stale_change_trap",
            "pass" if stale_blocked else "fail",
            "post-acceptance material edit blocked review-packet"
            if stale_blocked
            else f"expected hold_review_packet exit=1; got exit={stale_result.returncode}, decision={stale_json.get('decision', 'missing')}",
            "review-packet after touched preflight_decision.md",
        )

        source_root_result = run_cli_subprocess(["review-packet", str(ROOT), "--level", "preflight"])
        add_self_test_check(
            checks,
            "source_root_refusal",
            "pass" if source_root_result.returncode != 0 else "fail",
            "review-packet refused to write into source root"
            if source_root_result.returncode != 0
            else "review-packet unexpectedly allowed source root",
            "review-packet source-root",
        )

        source_example = ROOT / "worked_examples" / "preflight" / "cramps-phy-synthetic-coordinate-recurrence"
        source_example_result = run_cli_subprocess(["release-check", "package", str(source_example), "--level", "preflight"])
        add_self_test_check(
            checks,
            "source_example_package_refusal",
            "pass" if source_example_result.returncode != 0 else "fail",
            "release-check package refused to write into source worked example"
            if source_example_result.returncode != 0
            else "release-check package unexpectedly wrote into source worked example",
            "release-check package worked-example source",
        )
    finally:
        if not keep_temp:
            shutil.rmtree(temp_path, ignore_errors=True)

    failed = [check for check in checks if check["status"] != "pass"]
    return {
        "generated_at": utc_now(),
        "decision": "self_test_passed" if not failed else "self_test_failed",
        "temp_dir": str(temp_path) if keep_temp else "removed",
        "passed_count": sum(1 for check in checks if check["status"] == "pass"),
        "failed_count": len(failed),
        "checks": checks,
    }


def render_gate_dag_doc(level: str) -> str:
    specs = gate_specs(level)
    lines = [
        "# CRAMPS Gate DAG",
        "",
        "Gates clear in dependency order. A gate is blocked if one of its own prerequisites is unmet or if a dependency gate remains blocked.",
        "",
        "| gate | priority | phase | depends on | terms/prerequisites |",
        "|---|---:|---|---|---|",
    ]
    for spec in specs:
        terms = "<br>".join(f"{term_id}: {desc}" for term_id, desc, _ in spec.terms)
        deps = ", ".join(spec.depends_on) if spec.depends_on else "none"
        lines.append(f"| `{spec.gate_id}` | {spec.priority} | {spec.phase} | {deps} | {terms} |")
    lines.extend(
        [
            "",
            "Run:",
            "",
            f"```bash\npython {ROOT / 'tools' / 'cramps_cli.py'} gate <package_dir> --level {level}\n```",
            "",
            "Run gate evaluation after `check`, `agent-audit`, and `leak-scan` so the DAG sees current package metrics, agent-control status, and leak status.",
            "",
            "The command writes `ai_controls/gate_status.json`, `ai_controls/gate_status.md`, and `ai_controls/term_prereq_ledger.csv`.",
        ]
    )
    return "\n".join(lines)


def render_leak_watch_doc() -> str:
    return """
# Leak Watch Surfaces

Leak watching is a package-safety control, not a substitute for domain privacy,
security, legal, or regulatory review.

## Watched Surfaces

| surface | watch condition | required response |
|---|---|---|
| source-kit boundary | package work appears inside controlled source directories | quarantine and move work into package |
| intake | raw PDFs, exports, dumps, logs, or private files added without provenance | record source and classify sensitivity |
| evidence tables | secrets, private identifiers, fabricated values, or unreviewed sensitive rows | quarantine affected artifact |
| AI prompts/logs | sensitive content copied into prompts, notes, or summaries | quarantine and redact before reuse |
| exports | uncontrolled claim language or restricted data in shareable outputs | hold export and run claim review |
| metrics/manifests | checksums reveal wrong artifact set or contaminated source material | hold gate and rebuild manifest |
| quarantine | unresolved critical finding or release hold | no phase progress or release |

## Critical Leak Examples

- API keys, access tokens, private keys, passwords, or credentials.
- Regulated personal identifiers where the package is not authorized for them.
- Source-kit mutation during package work.
- Fabricated or backfilled evidence values not explicitly marked as synthetic.
- CRAMPS overclaims presented as proof, discovery, safety, efficacy, compliance, or causality.
"""


def render_quarantine_protocol() -> str:
    return """
# Package Quarantine Protocol

Quarantine is a no-release, no-escalation state for a CRAMPS package. It
contains the risk while preserving evidence for review. It does not delete,
rewrite, or hide the underlying issue.

## Trigger Conditions

- Critical leak detected by `leak-scan`.
- Evidence appears in the sanitized source kit instead of the package.
- A package contains fabricated, untraceable, or materially altered evidence.
- Gate accounting shows a blocked prerequisite was bypassed.
- Claim language exceeds the package assurance level.
- Restricted data appears in exports, prompts, summaries, or logs without authorization.

## Operator Response

1. Stop package progress.
2. Run `cramps_cli.py quarantine <package_dir> --reason "<reason>"`.
3. Identify affected artifacts in `logs/quarantine_log.csv`.
4. Add containment notes and required reviewer.
5. Do not release, export, promote, or reuse affected artifacts until cleared.

## Clearance

Clearance requires documented reviewer action, a clean leak scan, gate status
re-run, and a note explaining why the affected reliance is now permitted.
"""


def render_next_actions(level: str) -> str:
    if level == "preflight":
        actions = [
            "Complete `preflight_scope.md` with the question, coordinate sketch, inclusion boundary, exclusion boundary, and intended decision.",
            "Add searched and included sources to `preflight_sources.csv`.",
            "Extract weak observation, residual, null, non-event, exclusion, and near-miss rows into `preflight_rows.csv`.",
            "Complete `preflight_gotchas.md` as the failure-mode worksheet before making an escalation decision.",
            "Run `check`, `agent-audit`, `leak-scan`, `gate`, `contract-audit package`, `acceptance-audit`, and `review-packet` before deciding whether to promote.",
        ]
    else:
        actions = [
            "Complete the charter, role assignment, and protocol lock binder.",
            "Lock candidate coordinates before scoring.",
            "Populate source, raw row, normalized row, independence, bias, null model, and result contracts.",
            "Maintain build ledger, checkpoint reviews, claim trace matrix, trust debt, and trust status summary.",
            "Run `check`, `agent-audit`, `leak-scan`, `gate`, `contract-audit package`, `acceptance-audit`, and `review-packet` before release review.",
        ]
    return "# Next Actions\n\n" + "\n".join(f"- {item}" for item in actions)


def create_common_package_controls(package: Path, domain: dict, level: str, study_id: str, title: str) -> None:
    for dirname in PACKAGE_RUNTIME_DIRS:
        (package / dirname).mkdir(parents=True, exist_ok=True)

    state = {
        "schema": "cramps.package.v1",
        "cli_version": CLI_VERSION,
        "package_id": study_id,
        "study_id": study_id,
        "title": title,
        "level": level,
        "domain_slug": domain["slug"],
        "lightweight_name": domain["light"],
        "full_name": domain["full"],
        "created_at": utc_now(),
        "source_repo": str(ROOT),
        "source_commit": git_value("rev-parse", "HEAD"),
        "source_dirty_at_creation": source_dirty(),
        "status": "active",
        "sanitized_source_rule": "Package operators write inside this package. Source-kit files are reusable controlled materials.",
        "history": [
            {
                "timestamp": utc_now(),
                "event": "package_created",
                "details": {"level": level, "domain": domain["slug"]},
            }
        ],
    }
    write_state(package, state)

    write_text(package / "PACKAGE_README.md", render_package_readme(domain, level, study_id, title))
    write_text(package / "domain_context" / "DOMAIN_REFERENCE.md", render_domain_reference(domain))
    write_text(package / "ai_controls" / "AI_OPERATOR_BRIEF.md", render_ai_operator_brief(domain, level, study_id, title))
    write_text(package / "ai_controls" / "AGENT_DEPLOYMENT_HELPER.md", render_agent_deployment_helper(domain, level, study_id, title))
    write_text(package / "ai_controls" / "GATE_DAG.md", render_gate_dag_doc(level))
    write_text(package / "ai_controls" / "LEAK_WATCH_SURFACES.md", render_leak_watch_doc())
    write_text(package / "ai_controls" / "QUARANTINE_PROTOCOL.md", render_quarantine_protocol())
    write_text(package / "NEXT_ACTIONS.md", render_next_actions(level))
    agent_registry = package / "ai_controls" / "agent_registry.csv"
    if not agent_registry.exists():
        copy_file(ROOT / "templates" / "agent_registry.csv", agent_registry)

    for path, fields in [
        (package / "logs" / "ai_activity_log.csv", AI_LOG_FIELDS),
        (package / "logs" / "leak_watch_log.csv", LEAK_LOG_FIELDS),
        (package / "logs" / "quarantine_log.csv", QUARANTINE_LOG_FIELDS),
        (package / "ai_controls" / "term_prereq_ledger.csv", TERM_FIELDS),
        (
            package / "ai_controls" / "agent_deployment_plan.csv",
            AGENT_DEPLOYMENT_PLAN_FIELDS,
        ),
        (
            package / "ai_controls" / "agent_handoff_checklist.csv",
            AGENT_HANDOFF_FIELDS,
        ),
    ]:
        if not path.exists():
            rows = agent_deployment_plan_rows(domain, level, study_id) if fields == AGENT_DEPLOYMENT_PLAN_FIELDS else []
            write_csv(path, fields, rows)


def scaffold_preflight(package: Path, domain: dict, study_id: str, title: str, force: bool) -> None:
    package.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date().isoformat()
    scope = (ROOT / "templates" / "preflight_scope.md").read_text(encoding="utf-8")
    scope = scope.replace("**Preflight ID:**  ", f"**Preflight ID:** {study_id}  ")
    scope = scope.replace("**Domain suffix:**  ", f"**Domain suffix:** {domain['slug']}  ")
    scope = scope.replace("**Date:**  ", f"**Date:** {today}  ")
    scope = scope.replace("**Target full system if escalated:** CRAMPS-", f"**Target full system if escalated:** {domain['full']}")
    write_text(package / "preflight_scope.md", scope, force)

    for name in ["preflight_sources.csv", "preflight_rows.csv", "preflight_manifest.csv"]:
        copy_file(ROOT / "templates" / name, package / name, force)

    for name in ["preflight_gotchas.md", "preflight_decision.md"]:
        content = (ROOT / "templates" / name).read_text(encoding="utf-8")
        content = content.replace("**Preflight ID:**  ", f"**Preflight ID:** {study_id}  ")
        content = content.replace("**Date:**  ", f"**Date:** {today}  ")
        write_text(package / name, content, force)


def scaffold_full(package: Path, domain: dict, study_id: str, force: bool) -> None:
    full_scaffold.scaffold(package, domain, study_id, force)


def command_init(args: argparse.Namespace) -> int:
    domain = load_domain(args.domain)
    out_dir = args.out or default_output_dir(args.level, domain, args.study_id, args.title or args.study_id)
    package = guard_output_path(out_dir, args.force)
    title = args.title or args.study_id

    if args.level == "preflight":
        scaffold_preflight(package, domain, args.study_id, title, args.force)
    else:
        scaffold_full(package, domain, args.study_id, args.force)

    create_common_package_controls(package, domain, args.level, args.study_id, title)
    append_csv(
        package / "logs" / "ai_activity_log.csv",
        AI_LOG_FIELDS,
        {
            "timestamp": utc_now(),
            "actor_id": args.actor_id,
            "action": "init_package",
            "artifact_path": ".",
            "gate_id": "G0",
            "decision_impact": "package_created",
            "notes": f"{args.level} package initialized from sanitized source kit",
        },
    )
    print(json.dumps({"package": str(package), "level": args.level, "status": "created"}, indent=2))
    return 0


def command_promote(args: argparse.Namespace) -> int:
    preflight = args.preflight.resolve()
    if not preflight.exists():
        raise SystemExit(f"Preflight package not found: {preflight}")

    preflight_state = load_state(preflight, required=False)
    domain = load_domain(args.domain or preflight_state.get("domain_slug", ""))
    study_id = args.study_id or f"{preflight_state.get('study_id', 'STUDY')}-FULL"
    title = args.title or preflight_state.get("title", study_id)
    out_dir = args.out or default_output_dir("full", domain, study_id, title)
    full_package = guard_output_path(out_dir, args.force)

    scaffold_full(full_package, domain, study_id, args.force)
    create_common_package_controls(full_package, domain, "full", study_id, title)

    import_dir = full_package / "00_charter" / "preflight_import"
    import_rows = []
    for artifact in sidecar.PREFLIGHT_REQUIRED:
        src = sidecar.find_file(preflight, artifact)
        if not src:
            continue
        dst = import_dir / artifact
        copy_file(src, dst, args.force)
        import_rows.append(
            {
                "full_study_id": study_id,
                "preflight_id": preflight_state.get("study_id", preflight.name),
                "artifact_path": relative_artifact(full_package, dst),
                "artifact_sha256": sha256_file(dst),
                "imported_as": artifact,
                "reviewer_id": "",
                "review_disposition": "pending_full_review",
                "decision_timestamp": utc_now(),
                "notes": "Copied from lowercase preflight; not full assurance until reviewed.",
            }
        )

    write_csv(
        full_package / "02_sources" / "preflight_import_log.csv",
        [
            "full_study_id",
            "preflight_id",
            "artifact_path",
            "artifact_sha256",
            "imported_as",
            "reviewer_id",
            "review_disposition",
            "decision_timestamp",
            "notes",
        ],
        import_rows,
    )
    write_text(
        full_package / "00_charter" / "preflight_import" / "IMPORT_NOTE.md",
        f"""
# Preflight Import Note

Imported from: `{preflight}`  
Imported at: {utc_now()}  

The imported lowercase preflight artifacts are seed material only. They must be
accepted, reworked, rejected, or quarantined inside the full package before
they can support any uppercase `{domain["full"]}` claim.
""",
    )
    append_history(full_package, "promoted_from_preflight", {"preflight": str(preflight)})
    print(json.dumps({"package": str(full_package), "status": "promoted", "imported_artifacts": len(import_rows)}, indent=2))
    return 0


def run_sidecar(package: Path, level: str) -> dict:
    assert_package_output_allowed(package, "check")
    metrics = sidecar.score_preflight(package) if level == "preflight" else sidecar.score_full(package)
    metrics["generated_at"] = utc_now()
    metrics["package_path"] = str(package)
    manifest = sidecar.make_manifest(package)
    metrics["manifest"] = manifest
    metrics["package_sha256"] = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    (package / "cramps_sidecar_metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (package / "cramps_sidecar_metrics.md").write_text(
        sidecar.render_markdown(metrics, manifest),
        encoding="utf-8",
    )
    return metrics


def command_check(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    level = package_level(package, args.level)
    metrics = run_sidecar(package, level)
    append_history(package, "sidecar_check", {"level": level, "recommendation": metrics["recommendation"]})
    print(
        json.dumps(
            {
                "level": metrics["level"],
                "readiness_score": metrics["readiness_score"],
                "recommendation": metrics["recommendation"],
                "blockers": metrics["blockers"],
                "package_sha256": metrics["package_sha256"],
            },
            indent=2,
        )
    )
    return 0


def file_exists(rel: str) -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(package: Path, _metrics: dict, _state: dict) -> tuple[bool, str, str]:
        path = package / rel
        return path.exists(), rel if path.exists() else "", "" if path.exists() else f"missing {rel}"

    return check


def csv_min_rows(rel: str, minimum: int) -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(package: Path, _metrics: dict, _state: dict) -> tuple[bool, str, str]:
        rows = read_csv_rows(package / rel)
        ok = len(rows) >= minimum
        return ok, rel if ok else "", "" if ok else f"{rel} has {len(rows)} rows; needs {minimum}"

    return check


def metric_at_least(metric: str, minimum: float) -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(_package: Path, metrics: dict, _state: dict) -> tuple[bool, str, str]:
        value = float(metrics.get(metric, 0) or 0)
        ok = value >= minimum
        return ok, "cramps_sidecar_metrics.json" if ok else "", "" if ok else f"{metric}={value}; needs >= {minimum}"

    return check


def no_sidecar_blocker(blocker: str) -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(_package: Path, metrics: dict, _state: dict) -> tuple[bool, str, str]:
        blockers = set(metrics.get("blockers", []))
        ok = blocker not in blockers
        return ok, "cramps_sidecar_metrics.json" if ok else "", "" if ok else f"sidecar blocker: {blocker}"

    return check


def package_state_active() -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(package: Path, _metrics: dict, state: dict) -> tuple[bool, str, str]:
        status = state.get("status", "missing")
        ok = status == "active"
        return ok, STATE_FILE if ok else "", "" if ok else f"package status is {status}"

    return check


def leak_scan_clear() -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(package: Path, _metrics: dict, _state: dict) -> tuple[bool, str, str]:
        status_path = package / "ai_controls" / "leak_scan_status.json"
        if not status_path.exists():
            return False, "", "leak scan has not been run"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        critical_open = int(status.get("open_critical_findings", 0))
        ok = critical_open == 0
        return (
            ok,
            "ai_controls/leak_scan_status.json" if ok else "",
            "" if ok else f"{critical_open} open critical leak findings",
        )

    return check


def agent_audit_clear() -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(package: Path, _metrics: dict, _state: dict) -> tuple[bool, str, str]:
        status_path = package / "ai_controls" / "agent_audit_status.json"
        if not status_path.exists():
            return False, "", "agent audit has not been run"
        status_mtime = status_path.stat().st_mtime
        watched = [
            ("ai_controls/AGENT_DEPLOYMENT_HELPER.md", package / "ai_controls" / "AGENT_DEPLOYMENT_HELPER.md"),
            ("ai_controls/agent_deployment_plan.csv", package / "ai_controls" / "agent_deployment_plan.csv"),
            ("ai_controls/agent_handoff_checklist.csv", package / "ai_controls" / "agent_handoff_checklist.csv"),
            ("ai_controls/agent_registry.csv", package / "ai_controls" / "agent_registry.csv"),
        ]
        newer = [rel for rel, path in watched if path.exists() and path.stat().st_mtime > status_mtime]
        if newer:
            return False, "", f"agent audit is stale relative to: {', '.join(newer)}"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        blockers = int(status.get("blocker_count", 0))
        ok = blockers == 0
        return (
            ok,
            "ai_controls/agent_audit_status.json" if ok else "",
            "" if ok else f"{blockers} open agent-audit blockers",
        )

    return check


def boundary_ok() -> Callable[[Path, dict, dict], tuple[bool, str, str]]:
    def check(package: Path, _metrics: dict, _state: dict) -> tuple[bool, str, str]:
        resolved = package.resolve()
        for dirname in CONTROLLED_SOURCE_DIRS:
            controlled = (ROOT / dirname).resolve()
            if resolved == controlled or is_relative_to(resolved, controlled):
                return False, "", f"package is inside controlled source directory {controlled}"
        return True, STATE_FILE, ""

    return check


def gate_specs(level: str) -> list[GateSpec]:
    common = [
        GateSpec(
            "G0",
            "package_boundary",
            "Package boundary and active state",
            0,
            "both",
            (),
            (
                ("G0.T1", "package state exists and is active", package_state_active()),
                ("G0.T2", "package is not inside controlled source material", boundary_ok()),
                ("G0.T3", "agent audit has no blockers", agent_audit_clear()),
            ),
        ),
    ]
    if level == "preflight":
        return common + [
            GateSpec(
                "P1",
                "preflight_scope",
                "Scope and coordinate sketch",
                10,
                "preflight",
                ("G0",),
                (
                    ("P1.T1", "preflight scope exists", file_exists("preflight_scope.md")),
                    ("P1.T2", "all required preflight artifacts exist", metric_at_least("required_present", 5)),
                ),
            ),
            GateSpec(
                "P2",
                "source_accounting",
                "Source accounting",
                20,
                "preflight",
                ("P1",),
                (
                    ("P2.T1", "preflight sources have at least one row", csv_min_rows("preflight_sources.csv", 1)),
                    ("P2.T2", "source unit diversity is accounted for", metric_at_least("source_unit_count", 1)),
                ),
            ),
            GateSpec(
                "P3",
                "row_extraction",
                "Row extraction",
                30,
                "preflight",
                ("P2",),
                (
                    ("P3.T1", "preflight rows have at least one row", csv_min_rows("preflight_rows.csv", 1)),
                    ("P3.T2", "coordinate values are populated", metric_at_least("coordinate_coverage", 1.0)),
                    ("P3.T3", "coordinate units are populated", metric_at_least("unit_coverage", 1.0)),
                ),
            ),
            GateSpec(
                "P4",
                "null_and_failure_mode_check",
                "Nulls, non-events, and failure modes",
                40,
                "preflight",
                ("P3",),
                (
                    ("P4.T1", "at least one null or non-event row exists", metric_at_least("null_or_non_event_rows", 1)),
                    ("P4.T2", "failure-mode worksheet exists", file_exists("preflight_gotchas.md")),
                ),
            ),
            GateSpec(
                "P5",
                "decision_and_leak_clearance",
                "Decision and leak clearance",
                50,
                "preflight",
                ("P4",),
                (
                    ("P5.T1", "preflight decision record exists", file_exists("preflight_decision.md")),
                    ("P5.T2", "sidecar has no required-artifact blocker", no_sidecar_blocker("missing_required_preflight_artifacts")),
                    ("P5.T3", "leak scan has no open critical finding", leak_scan_clear()),
                ),
            ),
        ]
    return common + [
        GateSpec(
            "F1",
            "charter",
            "Charter and roles",
            10,
            "full",
            ("G0",),
            (
                ("F1.T1", "study charter exists", file_exists("00_charter/study_charter.md")),
                ("F1.T2", "role assignment exists", file_exists("00_charter/role_assignment.csv")),
                ("F1.T3", "all binders exist", metric_at_least("binder_present", len(sidecar.FULL_BINDERS))),
            ),
        ),
        GateSpec(
            "F2",
            "protocol_lock",
            "Protocol and coordinate lock",
            20,
            "full",
            ("F1",),
            (
                ("F2.T1", "protocol exists", file_exists("01_protocol_lock/protocol.md")),
                ("F2.T2", "candidate coordinates entered", metric_at_least("candidate_count", 1)),
                ("F2.T3", "candidate coordinates are fully locked", metric_at_least("candidate_lock_coverage", 1.0)),
            ),
        ),
        GateSpec(
            "F3",
            "source_and_raw_rows",
            "Source and raw-row accounting",
            30,
            "full",
            ("F2",),
            (
                ("F3.T1", "source catalog has at least one row", csv_min_rows("02_sources/source_catalog.csv", 1)),
                ("F3.T2", "raw signal rows entered", metric_at_least("raw_row_count", 1)),
                ("F3.T3", "nulls or non-events included", metric_at_least("null_or_non_event_rows", 1)),
            ),
        ),
        GateSpec(
            "F4",
            "coordinate_normalization",
            "Coordinate normalization",
            40,
            "full",
            ("F3",),
            (
                ("F4.T1", "normalized rows entered", metric_at_least("normalized_row_count", 1)),
                ("F4.T2", "transform registry exists", file_exists("04_coordinate_normalization/coordinate_transform_registry.csv")),
                ("F4.T3", "unit conversion audit exists", file_exists("04_coordinate_normalization/unit_conversion_audit.md")),
            ),
        ),
        GateSpec(
            "F5",
            "dependence_bias",
            "Dependence and bias accounting",
            50,
            "full",
            ("F4",),
            (
                ("F5.T1", "independence coverage complete", metric_at_least("independence_coverage", 1.0)),
                ("F5.T2", "bias coverage complete", metric_at_least("bias_coverage", 1.0)),
                ("F5.T3", "missing evidence assessment exists", file_exists("05_dependence_bias/missing_evidence_assessment.md")),
            ),
        ),
        GateSpec(
            "F6",
            "statistics",
            "Null model and result accounting",
            60,
            "full",
            ("F5",),
            (
                ("F6.T1", "statistical analysis plan exists", file_exists("06_statistics/statistical_analysis_plan.md")),
                ("F6.T2", "null model runs exist", metric_at_least("null_model_run_count", 1)),
                ("F6.T3", "global result fields are populated", no_sidecar_blocker("no_global_result_fields")),
                ("F6.T4", "negative controls exist", file_exists("06_statistics/negative_controls.md")),
            ),
        ),
        GateSpec(
            "F7",
            "reproducibility",
            "Reproducibility and checksums",
            70,
            "full",
            ("F6",),
            (
                ("F7.T1", "checksum manifest exists", file_exists("07_reproducibility/checksum_manifest.csv")),
                ("F7.T2", "environment record exists", file_exists("07_reproducibility/environment_record.md")),
                ("F7.T3", "clean run report exists", file_exists("07_reproducibility/clean_run_report.md")),
            ),
        ),
        GateSpec(
            "F8",
            "trust_and_release",
            "Trust maintenance and release review",
            80,
            "full",
            ("F7",),
            (
                ("F8.T1", "build ledger has at least one row", metric_at_least("build_ledger_record_count", 1)),
                ("F8.T2", "checkpoint reviews have at least one row", metric_at_least("trust_checkpoint_record_count", 1)),
                ("F8.T3", "claim trace records have at least one row", metric_at_least("claim_trace_record_count", 1)),
                ("F8.T4", "decision records have at least one row", metric_at_least("decision_record_count", 1)),
                ("F8.T5", "leak scan has no open critical finding", leak_scan_clear()),
            ),
        ),
    ]


def evaluate_gates(package: Path, level: str) -> tuple[list[dict], list[dict], dict]:
    metrics = run_sidecar(package, level)
    state = load_state(package, required=False)
    gate_status: dict[str, str] = {}
    gates = []
    terms = []
    now = utc_now()

    for spec in gate_specs(level):
        dependency_blockers = [dep for dep in spec.depends_on if gate_status.get(dep) != "clear"]
        term_results = []
        for term_id, term_desc, check in spec.terms:
            ok, evidence, missing = check(package, metrics, state)
            status = "met" if ok else "not_met"
            term_row = {
                "gate_id": spec.gate_id,
                "phase": spec.phase,
                "priority": str(spec.priority),
                "term_id": term_id,
                "term_or_prerequisite": term_desc,
                "status": status,
                "evidence_artifact": evidence,
                "missing_or_blocker": missing,
                "cleared_at": now if ok else "",
                "notes": "",
            }
            term_results.append(term_row)
            terms.append(term_row)

        own_clear = all(row["status"] == "met" for row in term_results)
        clear = own_clear and not dependency_blockers
        gate_status[spec.gate_id] = "clear" if clear else "blocked"
        gates.append(
            {
                "gate_id": spec.gate_id,
                "phase": spec.phase,
                "title": spec.title,
                "priority": spec.priority,
                "depends_on": list(spec.depends_on),
                "dependency_blockers": dependency_blockers,
                "status": gate_status[spec.gate_id],
                "terms_met": sum(1 for row in term_results if row["status"] == "met"),
                "terms_total": len(term_results),
                "blocked_terms": [
                    row["term_id"] for row in term_results if row["status"] != "met"
                ],
            }
        )

    summary = {
        "generated_at": now,
        "level": level,
        "package": str(package),
        "highest_cleared_priority": max((g["priority"] for g in gates if g["status"] == "clear"), default=-1),
        "next_blocked_gate": next((g["gate_id"] for g in gates if g["status"] != "clear"), ""),
        "all_clear": all(g["status"] == "clear" for g in gates),
    }
    return gates, terms, summary


def render_gate_status(gates: list[dict], terms: list[dict], summary: dict) -> str:
    lines = [
        "# CRAMPS Gate Status",
        "",
        f"Generated: {summary['generated_at']}",
        f"Level: `{summary['level']}`",
        f"All clear: `{summary['all_clear']}`",
        f"Next blocked gate: `{summary['next_blocked_gate'] or 'none'}`",
        "",
        "## Gates",
        "",
        "| gate | priority | phase | status | terms | dependency blockers |",
        "|---|---:|---|---|---:|---|",
    ]
    for gate in gates:
        deps = ", ".join(gate["dependency_blockers"]) if gate["dependency_blockers"] else "none"
        lines.append(
            f"| `{gate['gate_id']}` | {gate['priority']} | {gate['phase']} | `{gate['status']}` | {gate['terms_met']}/{gate['terms_total']} | {deps} |"
        )
    lines.extend(["", "## Blocked Terms", ""])
    blocked = [term for term in terms if term["status"] != "met"]
    if not blocked:
        lines.append("No blocked terms.")
    else:
        lines.extend(["| gate | term | missing/blocker |", "|---|---|---|"])
        for term in blocked:
            lines.append(
                f"| `{term['gate_id']}` | `{term['term_id']}` {term['term_or_prerequisite']} | {term['missing_or_blocker']} |"
            )
    lines.append("")
    return "\n".join(lines)


def command_gate(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    level = package_level(package, args.level)
    gates, terms, summary = evaluate_gates(package, level)
    write_text(package / "ai_controls" / "gate_status.md", render_gate_status(gates, terms, summary))
    (package / "ai_controls" / "gate_status.json").write_text(
        json.dumps({"summary": summary, "gates": gates, "terms": terms}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(package / "ai_controls" / "term_prereq_ledger.csv", TERM_FIELDS, terms)
    append_history(package, "gate_evaluation", summary)
    print(json.dumps(summary, indent=2))
    return 0


def iter_scannable_files(package: Path) -> list[Path]:
    skip_names = {
        "cramps_sidecar_metrics.json",
        "cramps_sidecar_metrics.md",
        "gate_status.json",
        "gate_status.md",
        "leak_scan_status.json",
        "leak_scan_report.md",
    }
    files = []
    for path in sorted(package.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts or path.name in skip_names:
            continue
        if path.stat().st_size > 5 * 1024 * 1024:
            continue
        files.append(path)
    return files


def scan_text_file(package: Path, path: Path) -> list[dict]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    rel = relative_artifact(package, path)
    lines = text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        for pattern_id, severity, pattern in LEAK_PATTERNS:
            if pattern.search(line):
                if pattern_id == "email_address" and rel.startswith("ai_controls/"):
                    continue
                findings.append(
                    {
                        "severity": severity,
                        "surface": surface_for_path(rel),
                        "artifact_path": rel,
                        "line": str(line_number),
                        "pattern_id": pattern_id,
                        "status": "open",
                        "quarantine_required": "yes" if severity in {"critical", "major"} else "no",
                        "notes": "potential sensitive data or credential pattern",
                    }
                )
        for pattern_id, pattern in OVERCLAIM_PATTERNS:
            prior_window = " ".join(lines[max(0, line_number - 4) : line_number]).lower()
            claim_context = f"{prior_window} {line.lower()}"
            if pattern.search(line) and not re.search(r"\b(not|does not|cannot|must not|prohibited)\b", claim_context):
                findings.append(
                    {
                        "severity": "watch",
                        "surface": surface_for_path(rel),
                        "artifact_path": rel,
                        "line": str(line_number),
                        "pattern_id": pattern_id,
                        "status": "open",
                        "quarantine_required": "no",
                        "notes": "possible overclaim language; requires claim-boundary review",
                    }
                )
    return findings


def surface_for_path(rel: str) -> str:
    if rel.startswith("intake/"):
        return "intake"
    if rel.startswith("exports/"):
        return "exports"
    if rel.startswith("logs/"):
        return "ai_logs"
    if rel.startswith("ai_controls/"):
        return "ai_controls"
    if rel.startswith("quarantine/"):
        return "quarantine"
    if rel.endswith(".csv"):
        return "evidence_tables"
    return "package_documents"


def command_leak_scan(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    if not package.exists():
        raise SystemExit(f"Package not found: {package}")
    assert_package_output_allowed(package, "leak-scan")

    findings = []

    for path in iter_scannable_files(package):
        findings.extend(scan_text_file(package, path))

    now = utc_now()
    logged_rows = []
    for index, finding in enumerate(findings, start=1):
        row = {
            "timestamp": now,
            "finding_id": f"LF-{index:04d}",
            **finding,
        }
        logged_rows.append(row)
        append_csv(package / "logs" / "leak_watch_log.csv", LEAK_LOG_FIELDS, row)

    open_critical = sum(1 for item in findings if item["severity"] == "critical")
    open_major = sum(1 for item in findings if item["severity"] == "major")
    open_watch = sum(1 for item in findings if item["severity"] == "watch")
    status = {
        "generated_at": now,
        "package": str(package),
        "finding_count": len(findings),
        "open_critical_findings": open_critical,
        "open_major_findings": open_major,
        "open_watch_findings": open_watch,
        "quarantine_required": open_critical > 0 or open_major > 0,
        "findings": logged_rows,
    }
    (package / "ai_controls" / "leak_scan_status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_text(package / "ai_controls" / "leak_scan_report.md", render_leak_report(status))
    append_history(package, "leak_scan", {k: status[k] for k in ["finding_count", "open_critical_findings", "open_major_findings"]})
    print(json.dumps({k: status[k] for k in ["finding_count", "open_critical_findings", "open_major_findings", "open_watch_findings", "quarantine_required"]}, indent=2))
    return 2 if status["quarantine_required"] and args.fail_on_quarantine else 0


def command_agent_audit(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    level = package_level(package, args.level)
    status = audit_agent_controls(package, level)
    append_history(
        package,
        "agent_audit",
        {
            "level": level,
            "all_clear": status["all_clear"],
            "blocker_count": status["blocker_count"],
            "warning_count": status["warning_count"],
        },
    )
    print(
        json.dumps(
            {
                "level": status["level"],
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "warning_count": status["warning_count"],
                "plan_row_count": status["plan_row_count"],
                "registry_row_count": status["registry_row_count"],
                "handoff_row_count": status["handoff_row_count"],
            },
            indent=2,
        )
    )
    if status["blocker_count"]:
        return 1
    if args.fail_on_warning and status["warning_count"]:
        return 2
    return 0


def command_acceptance_audit(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    level = package_level(package, args.level)
    status = acceptance_audit(package, level)
    append_history(
        package,
        "acceptance_audit",
        {
            "level": level,
            "decision": status["decision"],
            "all_clear": status["all_clear"],
            "blocker_count": status["blocker_count"],
            "warning_count": status["warning_count"],
        },
    )
    print(
        json.dumps(
            {
                "level": status["level"],
                "decision": status["decision"],
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "warning_count": status["warning_count"],
                "reliance": status["reliance"],
            },
            indent=2,
        )
    )
    if status["blocker_count"]:
        return 1
    if args.fail_on_warning and status["warning_count"]:
        return 2
    return 0


def command_review_packet(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    level = package_level(package, args.level)
    status = build_review_packet(
        package,
        level,
        args.out,
        args.allow_hold,
        args.include_package_files,
        not args.no_zip,
    )
    print(
        json.dumps(
            {
                "level": status["level"],
                "decision": status["decision"],
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "output_dir": status["output_dir"],
                "zip_path": status.get("zip_path", ""),
                "zip_sha256": status.get("zip_sha256", ""),
            },
            indent=2,
        )
    )
    return int(status["exit_code"])


def command_source_audit(args: argparse.Namespace) -> int:
    status = source_audit_status()
    if args.report:
        write_text(args.report.resolve(), render_source_audit_report(status))
    print(
        json.dumps(
            {
                "decision": status["decision"],
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "warning_count": status["warning_count"],
                "source_commit": status["source_commit"],
                "source_dirty": status["source_dirty"],
            },
            indent=2,
        )
    )
    if args.verbose:
        print(json.dumps(status, indent=2, sort_keys=True))
    if status["blocker_count"]:
        return 1
    if args.fail_on_warning and status["warning_count"]:
        return 2
    return 0


def command_source_snapshot(args: argparse.Namespace) -> int:
    status = build_source_snapshot(
        args.out,
        args.force,
        args.allow_dirty,
        args.allow_warning,
        not args.no_zip,
    )
    print(
        json.dumps(
            {
                "decision": status["decision"],
                "artifact_count": status["artifact_count"],
                "snapshot_sha256": status["snapshot_sha256"],
                "output_dir": status["output_dir"],
                "zip_path": status.get("zip_path", ""),
                "zip_sha256": status.get("zip_sha256", ""),
            },
            indent=2,
        )
    )
    return int(status["exit_code"])


def command_release_check(args: argparse.Namespace) -> int:
    if args.release_scope == "source":
        status = build_source_release_check(
            args.out,
            args.force,
            args.allow_dirty,
            args.allow_warning,
            args.skip_workbooks,
            args.no_snapshot,
        )
    else:
        status = build_package_release_check(
            args.package,
            args.level,
            args.out,
            args.force,
            args.include_package_files,
            args.fail_on_warning,
        )
    print(
        json.dumps(
            {
                "scope": status["scope"],
                "decision": status["decision"],
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "warning_count": status["warning_count"],
                "output_dir": status["output_dir"],
            },
            indent=2,
        )
    )
    if args.verbose:
        print(json.dumps(status, indent=2, sort_keys=True))
    return 0 if status["blocker_count"] == 0 and status["warning_count"] == 0 else 1


def command_contract_audit(args: argparse.Namespace) -> int:
    if args.contract_scope == "source":
        status = contract_audit_status("source", None, "auto")
        output_dir = (args.out or default_release_check_dir("contract_audit")).expanduser().resolve()
        if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
            raise SystemExit(f"Contract-audit output directory is not empty. Re-run with --force if intentional: {output_dir}")
        if is_relative_to(output_dir, ROOT) and not is_relative_to(output_dir, (ROOT / "dist").resolve()):
            raise SystemExit(f"Refusing to write source contract-audit outputs inside the source repository outside dist/: {output_dir}")
        status["output_dir"] = str(output_dir)
        write_contract_audit_outputs(status, output_dir)
    else:
        package = args.package.resolve()
        level = package_level(package, args.level)
        status = contract_audit_status("package", package, level)
        output_dir = package / "ai_controls"
        status["output_dir"] = str(output_dir)
        write_contract_audit_outputs(status, output_dir)
        append_history(
            package,
            "contract_audit",
            {
                "level": level,
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "warning_count": status["warning_count"],
            },
        )
    print(
        json.dumps(
            {
                "scope": status["scope"],
                "decision": status["decision"],
                "all_clear": status["all_clear"],
                "blocker_count": status["blocker_count"],
                "warning_count": status["warning_count"],
                "output_dir": status["output_dir"],
            },
            indent=2,
        )
    )
    if args.verbose:
        print(json.dumps(status, indent=2, sort_keys=True))
    if status["blocker_count"]:
        return 1
    if args.fail_on_warning and status["warning_count"]:
        return 2
    return 0


def command_self_test(args: argparse.Namespace) -> int:
    status = run_self_test(args.strict_source, args.keep_temp)
    if args.report:
        write_text(args.report.resolve(), render_self_test_report(status))
    print(
        json.dumps(
            {
                "decision": status["decision"],
                "passed_count": status["passed_count"],
                "failed_count": status["failed_count"],
                "temp_dir": status["temp_dir"],
            },
            indent=2,
        )
    )
    if args.verbose:
        print(json.dumps(status, indent=2, sort_keys=True))
    return 0 if status["failed_count"] == 0 else 1


def render_leak_report(status: dict) -> str:
    lines = [
        "# CRAMPS Leak Scan Report",
        "",
        f"Generated: {status['generated_at']}",
        f"Quarantine required: `{status['quarantine_required']}`",
        f"Open critical findings: `{status['open_critical_findings']}`",
        f"Open major findings: `{status['open_major_findings']}`",
        f"Open watch findings: `{status['open_watch_findings']}`",
        "",
        "| finding | severity | surface | artifact | line | pattern | quarantine |",
        "|---|---|---|---|---:|---|---|",
    ]
    for finding in status["findings"]:
        lines.append(
            f"| `{finding['finding_id']}` | `{finding['severity']}` | {finding['surface']} | `{finding['artifact_path']}` | {finding['line']} | `{finding['pattern_id']}` | {finding['quarantine_required']} |"
        )
    if not status["findings"]:
        lines.append("| none | none | none | none |  | none | no |")
    lines.append("")
    return "\n".join(lines)


def command_quarantine(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    if not package.exists():
        raise SystemExit(f"Package not found: {package}")
    assert_package_output_allowed(package, "quarantine")
    state = load_state(package, required=False)
    previous = state.get("status", "unknown")
    state["status"] = "quarantined"
    state.setdefault("history", []).append(
        {
            "timestamp": utc_now(),
            "event": "quarantine",
            "details": {"reason": args.reason, "scope": args.scope, "previous_status": previous},
        }
    )
    write_state(package, state)
    append_csv(
        package / "logs" / "quarantine_log.csv",
        QUARANTINE_LOG_FIELDS,
        {
            "timestamp": utc_now(),
            "event": "quarantine",
            "status": "quarantined",
            "reason": args.reason,
            "scope": args.scope or ".",
            "actor_id": args.actor_id,
            "release_hold": "yes",
            "notes": args.notes or "",
        },
    )
    write_text(
        package / "quarantine" / "QUARANTINE_NOTICE.md",
        f"""
# Quarantine Notice

**Status:** quarantined  
**Timestamp:** {utc_now()}  
**Reason:** {args.reason}  
**Scope:** {args.scope or "."}  
**Actor:** {args.actor_id}  

No release, export, promotion, or reliance upgrade is allowed until this
quarantine is cleared by documented review, a clean leak scan, and a new gate
evaluation.
""",
    )
    print(json.dumps({"package": str(package), "status": "quarantined", "reason": args.reason}, indent=2))
    return 0


def command_clear_quarantine(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    assert_package_output_allowed(package, "clear-quarantine")
    state = load_state(package, required=True)
    state["status"] = "active"
    state.setdefault("history", []).append(
        {
            "timestamp": utc_now(),
            "event": "clear_quarantine",
            "details": {"reviewer": args.reviewer_id, "basis": args.basis},
        }
    )
    write_state(package, state)
    append_csv(
        package / "logs" / "quarantine_log.csv",
        QUARANTINE_LOG_FIELDS,
        {
            "timestamp": utc_now(),
            "event": "clear_quarantine",
            "status": "active",
            "reason": args.basis,
            "scope": args.scope or ".",
            "actor_id": args.reviewer_id,
            "release_hold": "no",
            "notes": "Quarantine cleared; rerun leak-scan and gate before phase progress.",
        },
    )
    print(json.dumps({"package": str(package), "status": "active"}, indent=2))
    return 0


def command_status(args: argparse.Namespace) -> int:
    package = args.package.resolve()
    state = load_state(package, required=False)
    metrics_path = package / "cramps_sidecar_metrics.json"
    gate_path = package / "ai_controls" / "gate_status.json"
    leak_path = package / "ai_controls" / "leak_scan_status.json"
    agent_audit_path = package / "ai_controls" / "agent_audit_status.json"
    contract_audit_path = package / "ai_controls" / "contract_audit_status.json"
    acceptance_audit_path = package / "ai_controls" / "acceptance_audit_status.json"
    review_packet_path = package / "exports" / "review_packet" / "review_packet_status.json"
    result = {
        "package": str(package),
        "state": {
            "status": state.get("status", "missing"),
            "level": state.get("level", package_level(package, "auto")),
            "study_id": state.get("study_id", ""),
            "domain_slug": state.get("domain_slug", ""),
        },
        "sidecar": json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else None,
        "gate": json.loads(gate_path.read_text(encoding="utf-8"))["summary"] if gate_path.exists() else None,
        "leak_scan": json.loads(leak_path.read_text(encoding="utf-8")) if leak_path.exists() else None,
        "agent_audit": json.loads(agent_audit_path.read_text(encoding="utf-8")) if agent_audit_path.exists() else None,
        "contract_audit": json.loads(contract_audit_path.read_text(encoding="utf-8")) if contract_audit_path.exists() else None,
        "acceptance_audit": json.loads(acceptance_audit_path.read_text(encoding="utf-8")) if acceptance_audit_path.exists() else None,
        "review_packet": json.loads(review_packet_path.read_text(encoding="utf-8")) if review_packet_path.exists() else None,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def command_domains(_args: argparse.Namespace) -> int:
    rows = [
        {
            "slug": d["slug"],
            "lightweight": d["light"],
            "full": d["full"],
            "domain": d["label"],
        }
        for d in load_domains()
    ]
    print(json.dumps(rows, indent=2))
    return 0


def command_doctor(_args: argparse.Namespace) -> int:
    required = [
        ROOT / "templates",
        ROOT / "program",
        ROOT / "domain_packs",
        ROOT / "tools" / "cramps_sidecar.py",
        ROOT / "tools" / "scaffold_cramps_package.py",
    ]
    issues = [str(path) for path in required if not path.exists()]
    gitignore = ROOT / ".gitignore"
    ignored_project_root = "cramps_projects/" in gitignore.read_text(encoding="utf-8") if gitignore.exists() else False
    if not ignored_project_root:
        issues.append(".gitignore does not include cramps_projects/")
    result = {
        "source_repo": str(ROOT),
        "source_commit": git_value("rev-parse", "HEAD"),
        "source_dirty": source_dirty(),
        "domain_count": len(load_domains()),
        "issues": issues,
        "ok": not issues,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cramps",
        description="Create, operate, check, audit, gate, leak-scan, contract-audit, accept, packet, quarantine, source-audit, source-snapshot, release-check, and self-test CRAMPS packages.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an isolated CRAMPS package.")
    init.add_argument("--level", choices=["preflight", "full"], default="preflight")
    init.add_argument("--domain", required=True, help="Domain slug, for example med, fin, phy, cyb.")
    init.add_argument("--study-id", required=True)
    init.add_argument("--title", default="")
    init.add_argument("--out", type=Path, default=None)
    init.add_argument("--force", action="store_true")
    init.add_argument("--actor-id", default="ai_operator")
    init.set_defaults(func=command_init)

    promote = sub.add_parser("promote", help="Create a full package seeded from a lowercase preflight.")
    promote.add_argument("preflight", type=Path)
    promote.add_argument("--domain", default="")
    promote.add_argument("--study-id", default="")
    promote.add_argument("--title", default="")
    promote.add_argument("--out", type=Path, default=None)
    promote.add_argument("--force", action="store_true")
    promote.set_defaults(func=command_promote)

    check = sub.add_parser("check", help="Run sidecar metrics and package checksum.")
    check.add_argument("package", type=Path)
    check.add_argument("--level", choices=["preflight", "full", "auto"], default="auto")
    check.set_defaults(func=command_check)

    gate = sub.add_parser("gate", help="Evaluate DAG gates and term/prerequisite accounting.")
    gate.add_argument("package", type=Path)
    gate.add_argument("--level", choices=["preflight", "full", "auto"], default="auto")
    gate.set_defaults(func=command_gate)

    leak_scan = sub.add_parser("leak-scan", help="Scan package leak surfaces.")
    leak_scan.add_argument("package", type=Path)
    leak_scan.add_argument("--fail-on-quarantine", action="store_true")
    leak_scan.set_defaults(func=command_leak_scan)

    agent_audit = sub.add_parser("agent-audit", help="Audit agent deployment plan, registry, and handoffs.")
    agent_audit.add_argument("package", type=Path)
    agent_audit.add_argument("--level", choices=["preflight", "full", "auto"], default="auto")
    agent_audit.add_argument("--fail-on-warning", action="store_true")
    agent_audit.set_defaults(func=command_agent_audit)

    acceptance_audit_parser = sub.add_parser("acceptance-audit", help="Synthesize package readiness into an acceptance decision.")
    acceptance_audit_parser.add_argument("package", type=Path)
    acceptance_audit_parser.add_argument("--level", choices=["preflight", "full", "auto"], default="auto")
    acceptance_audit_parser.add_argument("--fail-on-warning", action="store_true")
    acceptance_audit_parser.set_defaults(func=command_acceptance_audit)

    review_packet = sub.add_parser("review-packet", help="Build a bounded reviewer handoff packet.")
    review_packet.add_argument("package", type=Path)
    review_packet.add_argument("--level", choices=["preflight", "full", "auto"], default="auto")
    review_packet.add_argument("--out", type=Path, default=None)
    review_packet.add_argument("--allow-hold", action="store_true", help="Write a packet even when acceptance is blocked.")
    review_packet.add_argument(
        "--include-package-files",
        action="store_true",
        help="Include package artifacts in the ZIP. Default ZIP contains only packet index files.",
    )
    review_packet.add_argument("--no-zip", action="store_true")
    review_packet.set_defaults(func=command_review_packet)

    quarantine = sub.add_parser("quarantine", help="Place a package into no-release quarantine.")
    quarantine.add_argument("package", type=Path)
    quarantine.add_argument("--reason", required=True)
    quarantine.add_argument("--scope", default="")
    quarantine.add_argument("--actor-id", default="ai_operator")
    quarantine.add_argument("--notes", default="")
    quarantine.set_defaults(func=command_quarantine)

    clear = sub.add_parser("clear-quarantine", help="Clear quarantine after documented review.")
    clear.add_argument("package", type=Path)
    clear.add_argument("--reviewer-id", required=True)
    clear.add_argument("--basis", required=True)
    clear.add_argument("--scope", default="")
    clear.set_defaults(func=command_clear_quarantine)

    status = sub.add_parser("status", help="Print package state, sidecar, agent, gate, leak, acceptance, and packet summaries.")
    status.add_argument("package", type=Path)
    status.set_defaults(func=command_status)

    domains = sub.add_parser("domains", help="List configured CRAMPS domains.")
    domains.set_defaults(func=command_domains)

    contract_audit = sub.add_parser("contract-audit", help="Audit CSV data-contract headers, required fields, and references.")
    contract_scopes = contract_audit.add_subparsers(dest="contract_scope", required=True)
    contract_source = contract_scopes.add_parser("source", help="Audit source-kit templates, registers, and domain-pack CSV contracts.")
    contract_source.add_argument("--out", type=Path, default=None)
    contract_source.add_argument("--force", action="store_true")
    contract_source.add_argument("--fail-on-warning", action="store_true")
    contract_source.add_argument("--verbose", action="store_true")
    contract_source.set_defaults(func=command_contract_audit)
    contract_package = contract_scopes.add_parser("package", help="Audit a package's CSV contracts and cross-table references.")
    contract_package.add_argument("package", type=Path)
    contract_package.add_argument("--level", choices=["auto", "preflight", "full"], default="auto")
    contract_package.add_argument("--fail-on-warning", action="store_true")
    contract_package.add_argument("--verbose", action="store_true")
    contract_package.set_defaults(func=command_contract_audit)

    release_check = sub.add_parser("release-check", help="Run executable source-kit or package release acceptance checks.")
    release_scopes = release_check.add_subparsers(dest="release_scope", required=True)
    release_source = release_scopes.add_parser("source", help="Run source-kit release checks and write a release-check report.")
    release_source.add_argument("--out", type=Path, default=None)
    release_source.add_argument("--force", action="store_true")
    release_source.add_argument("--allow-dirty", action="store_true", help="Allow source release check to run non-strict self-test and snapshot dirty source.")
    release_source.add_argument("--allow-warning", action="store_true", help="Allow source-audit warnings during source release check.")
    release_source.add_argument("--skip-workbooks", action="store_true", help="Skip XLSX workbook import verification.")
    release_source.add_argument("--no-snapshot", action="store_true", help="Skip source snapshot creation.")
    release_source.add_argument("--verbose", action="store_true")
    release_source.set_defaults(func=command_release_check)

    release_package = release_scopes.add_parser("package", help="Run package acceptance sequence and write a release-check report.")
    release_package.add_argument("package", type=Path)
    release_package.add_argument("--level", choices=["auto", "preflight", "full"], default="auto")
    release_package.add_argument("--out", type=Path, default=None)
    release_package.add_argument("--force", action="store_true")
    release_package.add_argument("--include-package-files", action="store_true")
    release_package.add_argument("--fail-on-warning", action="store_true")
    release_package.add_argument("--verbose", action="store_true")
    release_package.set_defaults(func=command_release_check)

    source_audit = sub.add_parser("source-audit", help="Audit the reusable CRAMPS source kit before handoff or push.")
    source_audit.add_argument("--fail-on-warning", action="store_true")
    source_audit.add_argument("--report", type=Path, default=None, help="Optional Markdown report output path.")
    source_audit.add_argument("--verbose", action="store_true", help="Print full check details after the summary.")
    source_audit.set_defaults(func=command_source_audit)

    source_snapshot = sub.add_parser("source-snapshot", help="Build a source-kit handoff snapshot with hashes and ZIP.")
    source_snapshot.add_argument("--out", type=Path, default=None)
    source_snapshot.add_argument("--force", action="store_true")
    source_snapshot.add_argument("--allow-dirty", action="store_true", help="Allow snapshot creation when the worktree is dirty.")
    source_snapshot.add_argument("--allow-warning", action="store_true", help="Allow snapshot creation when source-audit has warnings.")
    source_snapshot.add_argument("--no-zip", action="store_true")
    source_snapshot.set_defaults(func=command_source_snapshot)

    self_test = sub.add_parser("self-test", help="Run an end-to-end temp-package CRAMPS smoke test.")
    self_test.add_argument("--strict-source", action="store_true", help="Fail when source-audit reports warnings.")
    self_test.add_argument("--keep-temp", action="store_true", help="Keep the temporary package for debugging.")
    self_test.add_argument("--report", type=Path, default=None, help="Optional Markdown report output path.")
    self_test.add_argument("--verbose", action="store_true", help="Print full check details after the summary.")
    self_test.set_defaults(func=command_self_test)

    doctor = sub.add_parser("doctor", help="Check source-kit readiness for CLI operation.")
    doctor.set_defaults(func=command_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
