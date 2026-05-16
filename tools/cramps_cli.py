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
import shutil
import subprocess
import sys
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
7. If a critical leak, source-boundary breach, fabricated field, or prohibited claim is found, run quarantine.

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
9. Stop and quarantine if a critical leak, contamination event, fabricated field, or prohibited claim appears.

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
python {ROOT / "tools" / "cramps_cli.py"} acceptance-audit . --level {level}
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


def acceptance_audit(package: Path, level: str) -> dict:
    if not package.exists():
        raise SystemExit(f"Package not found: {package}")
    if package == ROOT or any(is_relative_to(package, ROOT / dirname) for dirname in CONTROLLED_SOURCE_DIRS):
        raise SystemExit("Refusing to write acceptance-audit outputs inside controlled source material.")

    checks: list[dict[str, str]] = []
    now = utc_now()
    controls_dir = package / "ai_controls"
    state = load_state(package, required=False)

    metrics_path = package / "cramps_sidecar_metrics.json"
    agent_path = package / "ai_controls" / "agent_audit_status.json"
    leak_path = package / "ai_controls" / "leak_scan_status.json"
    gate_path = package / "ai_controls" / "gate_status.json"

    metrics = load_json_artifact(metrics_path)
    agent = load_json_artifact(agent_path)
    leak = load_json_artifact(leak_path)
    gate = load_json_artifact(gate_path)

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
            "Run `check`, `agent-audit`, `leak-scan`, `gate`, and `acceptance-audit` before deciding whether to promote.",
        ]
    else:
        actions = [
            "Complete the charter, role assignment, and protocol lock binder.",
            "Lock candidate coordinates before scoring.",
            "Populate source, raw row, normalized row, independence, bias, null model, and result contracts.",
            "Maintain build ledger, checkpoint reviews, claim trace matrix, trust debt, and trust status summary.",
            "Run `check`, `agent-audit`, `leak-scan`, `gate`, and `acceptance-audit` before release review.",
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

    findings = []
    if package == ROOT or any(is_relative_to(package, ROOT / dirname) for dirname in CONTROLLED_SOURCE_DIRS):
        findings.append(
            {
                "severity": "critical",
                "surface": "source-kit_boundary",
                "artifact_path": ".",
                "line": "",
                "pattern_id": "package_inside_controlled_source",
                "status": "open",
                "quarantine_required": "yes",
                "notes": "package path is inside sanitized source material",
            }
        )

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
    acceptance_audit_path = package / "ai_controls" / "acceptance_audit_status.json"
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
        "acceptance_audit": json.loads(acceptance_audit_path.read_text(encoding="utf-8")) if acceptance_audit_path.exists() else None,
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
        description="Create, operate, check, audit, gate, leak-scan, accept, and quarantine CRAMPS packages.",
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

    status = sub.add_parser("status", help="Print package state, sidecar, agent, gate, leak, and acceptance summaries.")
    status.add_argument("package", type=Path)
    status.set_defaults(func=command_status)

    domains = sub.add_parser("domains", help="List configured CRAMPS domains.")
    domains.set_defaults(func=command_domains)

    doctor = sub.add_parser("doctor", help="Check source-kit readiness for CLI operation.")
    doctor.set_defaults(func=command_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
