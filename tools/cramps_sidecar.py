#!/usr/bin/env python3
"""CRAMPS package sidecar metrics runner.

This tool performs lightweight package checks for either:

- lowercase cramps-* preflight packages
- uppercase CRAMPS full study packages

It does not validate scientific truth. It checks whether the package has the
minimum control artifacts needed to support the claimed assurance level.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TREE_PACKAGE_ROOTS = {
    "cramps_projects",
}


NULL_TYPES = {
    "null",
    "non_event",
    "non-event",
    "exclusion",
    "upper_limit",
    "negative",
    "failed_replication",
    "false_positive",
    "cleared",
    "passed",
}


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def package_path_inside_sanitized_source(package: Path) -> bool:
    resolved = package.resolve()
    if not is_relative_to(resolved, ROOT):
        return False
    for dirname in SOURCE_TREE_PACKAGE_ROOTS:
        allowed_root = (ROOT / dirname).resolve()
        if resolved != allowed_root and is_relative_to(resolved, allowed_root):
            return False
    return True


def output_path_inside_sanitized_source(path: Path) -> bool:
    resolved = path.resolve()
    if not is_relative_to(resolved, ROOT):
        return False
    for dirname in SOURCE_TREE_PACKAGE_ROOTS:
        allowed_root = (ROOT / dirname).resolve()
        if resolved != allowed_root and is_relative_to(resolved, allowed_root):
            return False
    return True

POSITIVE_TYPES = {
    "excess",
    "deficit",
    "residual",
    "tension",
    "anomaly",
    "calibration_oddity",
    "near_miss",
    "alert",
    "failure",
}

PREFLIGHT_REQUIRED = [
    "preflight_scope.md",
    "preflight_sources.csv",
    "preflight_rows.csv",
    "preflight_gotchas.md",
    "preflight_decision.md",
]

FULL_REQUIRED = [
    "source_catalog.csv",
    "anomaly_rows_raw.csv",
    "normalized_rows.csv",
    "candidate_coordinate_registry.csv",
    "coordinate_transform_registry.csv",
    "independence_groups.csv",
    "bias_assessment.csv",
    "null_model_runs.csv",
    "analysis_result.csv",
    "amendment_log.csv",
]

FULL_BINDERS = [
    "00_charter",
    "01_protocol_lock",
    "02_sources",
    "03_extraction",
    "04_coordinate_normalization",
    "05_dependence_bias",
    "06_statistics",
    "07_reproducibility",
    "08_assurance_case",
    "09_review_and_release",
    "10_trust_maintenance",
    "registers",
]

FULL_REQUIRED_RECORDS = [
    "00_charter/study_charter.md",
    "00_charter/role_assignment.csv",
    "01_protocol_lock/protocol.md",
    "01_protocol_lock/candidate_coordinate_registry.csv",
    "01_protocol_lock/amendment_log.csv",
    "02_sources/search_strategy.md",
    "02_sources/source_catalog.csv",
    "02_sources/source_flow.md",
    "03_extraction/anomaly_rows_raw.csv",
    "03_extraction/extraction_notes.md",
    "04_coordinate_normalization/normalized_rows.csv",
    "04_coordinate_normalization/coordinate_transform_registry.csv",
    "04_coordinate_normalization/unit_conversion_audit.md",
    "05_dependence_bias/independence_groups.csv",
    "05_dependence_bias/bias_assessment.csv",
    "05_dependence_bias/missing_evidence_assessment.md",
    "06_statistics/statistical_analysis_plan.md",
    "06_statistics/null_model_runs.csv",
    "06_statistics/analysis_result.csv",
    "06_statistics/negative_controls.md",
    "06_statistics/sensitivity_results.md",
    "07_reproducibility/checksum_manifest.csv",
    "07_reproducibility/environment_record.md",
    "07_reproducibility/run_instructions.md",
    "07_reproducibility/clean_run_report.md",
    "08_assurance_case/assurance_case.md",
    "08_assurance_case/assurance_case_register.csv",
    "08_assurance_case/risk_register.csv",
    "09_review_and_release/audit_report.md",
    "09_review_and_release/decision_memo.md",
    "09_review_and_release/gate_review_record.csv",
    "09_review_and_release/claim_language_approval.md",
    "09_review_and_release/release_signoff.md",
    "10_trust_maintenance/build_ledger.csv",
    "10_trust_maintenance/checkpoint_reviews.csv",
    "10_trust_maintenance/assumption_uncertainty_log.csv",
    "10_trust_maintenance/claim_trace_matrix.csv",
    "10_trust_maintenance/trust_debt_register.csv",
    "10_trust_maintenance/trust_status_summary.md",
    "10_trust_maintenance/open_questions.md",
    "registers/assurance_case_register.csv",
    "registers/control_evidence_register.csv",
    "registers/deviation_capa_log.csv",
    "registers/decision_log.csv",
    "registers/document_register.csv",
    "registers/gate_review_record.csv",
    "registers/risk_register.csv",
    "registers/training_matrix.csv",
    "registers/trust_debt_register.csv",
]

ALIASES = {
    "preflight_scope.md": ["*PREFLIGHT_SCOPE.md"],
    "preflight_sources.csv": ["*PREFLIGHT_SOURCES.csv"],
    "preflight_rows.csv": ["*PREFLIGHT_ROWS.csv"],
    "preflight_gotchas.md": ["*PREFLIGHT_GOTCHAS_PRINTABLE.md", "*PREFLIGHT_GOTCHAS.md"],
    "preflight_decision.md": ["*PREFLIGHT_DECISION.md"],
}


@dataclass
class CsvInfo:
    path: Path
    exists: bool
    rows: int = 0
    columns: list[str] | None = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def find_file(root: Path, name: str) -> Path | None:
    direct = root / name
    if direct.exists():
        return direct
    matches = list(root.rglob(name))
    if matches:
        return matches[0]
    for pattern in ALIASES.get(name, []):
        alias_matches = sorted(root.rglob(pattern))
        if alias_matches:
            return alias_matches[0]
    return None


def relative_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def read_csv(path: Path | None) -> CsvInfo:
    if path is None or not path.exists():
        return CsvInfo(path=Path(""), exists=False, rows=0, columns=[])
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return CsvInfo(path=path, exists=True, rows=len(rows), columns=reader.fieldnames or [])


def load_csv_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def count_values(rows: Iterable[dict[str, str]], fields: Iterable[str], values: set[str]) -> int:
    count = 0
    for row in rows:
        for field in fields:
            if normalize(row.get(field)) in values:
                count += 1
                break
    return count


def nonempty_fraction(rows: list[dict[str, str]], field: str) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if normalize(row.get(field))) / len(rows)


def unique_nonempty(rows: list[dict[str, str]], field: str) -> int:
    return len({normalize(row.get(field)) for row in rows if normalize(row.get(field))})


def make_manifest(root: Path) -> list[dict[str, str]]:
    manifest = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if rel.endswith("cramps_sidecar_metrics.json") or rel.endswith("cramps_sidecar_metrics.md"):
            continue
        manifest.append(
            {
                "path": rel,
                "bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
            }
        )
    return manifest


def score_preflight(root: Path) -> dict:
    paths = {name: find_file(root, name) for name in PREFLIGHT_REQUIRED}
    rows = load_csv_rows(paths.get("preflight_rows.csv"))
    sources = load_csv_rows(paths.get("preflight_sources.csv"))

    null_count = count_values(
        rows,
        ["row_type", "result_direction", "null_or_non_event_flag"],
        NULL_TYPES | {"yes", "true", "1"},
    )
    positive_count = count_values(rows, ["row_type", "result_direction"], POSITIVE_TYPES)

    dependence_flagged = sum(1 for row in rows if normalize(row.get("dependence_concern")))
    bias_flagged = sum(1 for row in rows if normalize(row.get("bias_concern")))
    coordinate_values = sum(1 for row in rows if normalize(row.get("coordinate_value")))
    unit_values = sum(1 for row in rows if normalize(row.get("coordinate_units")))

    required_present = sum(1 for path in paths.values() if path and path.exists())
    source_units = unique_nonempty(sources, "unit_or_site")

    blockers = []
    if required_present < len(PREFLIGHT_REQUIRED):
        blockers.append("missing_required_preflight_artifacts")
    if not sources:
        blockers.append("no_preflight_sources_entered")
    if not rows:
        blockers.append("no_preflight_rows_entered")
    if rows and null_count == 0:
        blockers.append("no_null_or_non_event_rows")
    if rows and coordinate_values < len(rows):
        blockers.append("some_rows_missing_coordinate_values")
    if rows and unit_values < len(rows):
        blockers.append("some_rows_missing_units")
    if rows and source_units <= 1 and len(sources) > 2:
        blockers.append("source_unit_concentration")
    if rows and dependence_flagged / max(len(rows), 1) > 0.5:
        blockers.append("high_dependence_concern")
    if rows and bias_flagged / max(len(rows), 1) > 0.5:
        blockers.append("high_bias_concern")

    completeness = required_present / len(PREFLIGHT_REQUIRED)
    null_coverage = 1.0 if null_count > 0 else 0.0
    coordinate_coverage = coordinate_values / max(len(rows), 1)
    unit_coverage = unit_values / max(len(rows), 1)
    source_diversity = min(source_units / 3, 1.0)

    readiness = round(
        100
        * (
            0.30 * completeness
            + 0.20 * null_coverage
            + 0.20 * coordinate_coverage
            + 0.15 * unit_coverage
            + 0.15 * source_diversity
        ),
        1,
    )

    if blockers:
        recommendation = "hold"
    elif readiness >= 80:
        recommendation = "candidate_for_CRAMPS_upgrade"
    elif readiness >= 60:
        recommendation = "continue_preflight"
    else:
        recommendation = "do_not_escalate"

    return {
        "level": "cramps_preflight",
        "required_present": required_present,
        "required_total": len(PREFLIGHT_REQUIRED),
        "row_count": len(rows),
        "source_count": len(sources),
        "positive_like_rows": positive_count,
        "null_or_non_event_rows": null_count,
        "source_unit_count": source_units,
        "coordinate_coverage": round(coordinate_coverage, 3),
        "unit_coverage": round(unit_coverage, 3),
        "dependence_concern_rows": dependence_flagged,
        "bias_concern_rows": bias_flagged,
        "readiness_score": readiness,
        "blockers": blockers,
        "recommendation": recommendation,
    }


def score_full(root: Path) -> dict:
    paths = {name: find_file(root, name) for name in FULL_REQUIRED}
    raw_rows = load_csv_rows(paths.get("anomaly_rows_raw.csv"))
    normalized_rows = load_csv_rows(paths.get("normalized_rows.csv"))
    candidates = load_csv_rows(paths.get("candidate_coordinate_registry.csv"))
    independence = load_csv_rows(paths.get("independence_groups.csv"))
    bias = load_csv_rows(paths.get("bias_assessment.csv"))
    null_runs = load_csv_rows(paths.get("null_model_runs.csv"))
    results = load_csv_rows(paths.get("analysis_result.csv"))
    control_records = load_csv_rows(root / "registers" / "control_evidence_register.csv")
    gate_records = load_csv_rows(root / "registers" / "gate_review_record.csv")
    decision_records = load_csv_rows(root / "registers" / "decision_log.csv")
    build_ledger_records = load_csv_rows(root / "10_trust_maintenance" / "build_ledger.csv")
    checkpoint_records = load_csv_rows(root / "10_trust_maintenance" / "checkpoint_reviews.csv")
    claim_trace_records = load_csv_rows(root / "10_trust_maintenance" / "claim_trace_matrix.csv")
    trust_debt_records = load_csv_rows(root / "10_trust_maintenance" / "trust_debt_register.csv")

    required_present = sum(1 for path in paths.values() if path and path.exists())
    binder_present = sum(1 for binder in FULL_BINDERS if (root / binder).is_dir())
    program_record_present = sum(1 for rel in FULL_REQUIRED_RECORDS if relative_exists(root, rel))
    null_count = count_values(raw_rows, ["result_type"], NULL_TYPES)
    positive_count = count_values(raw_rows, ["result_type"], POSITIVE_TYPES)
    independence_coverage = nonempty_fraction(independence, "independence_grade")
    bias_coverage = nonempty_fraction(bias, "overall_bias_risk")
    candidate_lock_coverage = nonempty_fraction(candidates, "lock_timestamp")
    global_p_coverage = nonempty_fraction(results, "global_p_value")
    null_run_count = len(null_runs)

    blockers = []
    if required_present < len(FULL_REQUIRED):
        blockers.append("missing_required_full_artifacts")
    if binder_present < len(FULL_BINDERS):
        blockers.append("missing_required_evidence_binders")
    if program_record_present < len(FULL_REQUIRED_RECORDS):
        blockers.append("missing_required_program_records")
    if not raw_rows:
        blockers.append("no_raw_rows_entered")
    if not candidates:
        blockers.append("no_candidate_coordinates_entered")
    if not control_records:
        blockers.append("no_control_evidence_records")
    if not gate_records:
        blockers.append("no_gate_review_records")
    if not decision_records:
        blockers.append("no_decision_records")
    if not build_ledger_records:
        blockers.append("no_build_ledger_records")
    if not checkpoint_records:
        blockers.append("no_trust_checkpoint_records")
    if not claim_trace_records:
        blockers.append("no_claim_trace_records")
    if not (root / "10_trust_maintenance" / "trust_status_summary.md").exists():
        blockers.append("missing_trust_status_summary")
    if raw_rows and null_count == 0:
        blockers.append("no_null_or_non_event_rows")
    if candidates and candidate_lock_coverage < 1:
        blockers.append("candidate_registry_not_fully_locked")
    if raw_rows and len(independence) < len(raw_rows):
        blockers.append("independence_rows_less_than_raw_rows")
    if raw_rows and len(bias) < len(raw_rows):
        blockers.append("bias_rows_less_than_raw_rows")
    if null_run_count == 0:
        blockers.append("no_null_model_runs")
    if results and global_p_coverage == 0:
        blockers.append("no_global_result_fields")

    completeness = required_present / len(FULL_REQUIRED)
    binder_coverage = binder_present / len(FULL_BINDERS)
    program_record_coverage = program_record_present / len(FULL_REQUIRED_RECORDS)
    null_coverage = 1.0 if null_count > 0 else 0.0
    null_model_coverage = 1.0 if null_run_count > 0 else 0.0

    readiness = round(
        100
        * (
            0.15 * completeness
            + 0.10 * null_coverage
            + 0.12 * candidate_lock_coverage
            + 0.12 * independence_coverage
            + 0.12 * bias_coverage
            + 0.14 * null_model_coverage
            + 0.13 * binder_coverage
            + 0.12 * program_record_coverage
        ),
        1,
    )

    if blockers:
        recommendation = "hold_release"
    elif readiness >= 90:
        recommendation = "ready_for_red_team_or_release_gate"
    elif readiness >= 75:
        recommendation = "continue_full_package"
    else:
        recommendation = "not_ready"

    return {
        "level": "CRAMPS_full",
        "required_present": required_present,
        "required_total": len(FULL_REQUIRED),
        "binder_present": binder_present,
        "binder_total": len(FULL_BINDERS),
        "binder_coverage": round(binder_coverage, 3),
        "program_record_present": program_record_present,
        "program_record_total": len(FULL_REQUIRED_RECORDS),
        "program_record_coverage": round(program_record_coverage, 3),
        "raw_row_count": len(raw_rows),
        "normalized_row_count": len(normalized_rows),
        "candidate_count": len(candidates),
        "control_evidence_record_count": len(control_records),
        "gate_review_record_count": len(gate_records),
        "decision_record_count": len(decision_records),
        "build_ledger_record_count": len(build_ledger_records),
        "trust_checkpoint_record_count": len(checkpoint_records),
        "claim_trace_record_count": len(claim_trace_records),
        "trust_debt_record_count": len(trust_debt_records),
        "positive_like_rows": positive_count,
        "null_or_non_event_rows": null_count,
        "independence_coverage": round(independence_coverage, 3),
        "bias_coverage": round(bias_coverage, 3),
        "candidate_lock_coverage": round(candidate_lock_coverage, 3),
        "null_model_run_count": null_run_count,
        "readiness_score": readiness,
        "blockers": blockers,
        "recommendation": recommendation,
    }


def render_markdown(metrics: dict, manifest: list[dict[str, str]]) -> str:
    lines = [
        "# CRAMPS Sidecar Metrics",
        "",
        f"Generated: {metrics['generated_at']}",
        f"Package: `{metrics['package_path']}`",
        f"Level: `{metrics['level']}`",
        "",
        "## Summary",
        "",
        f"- Readiness score: `{metrics['readiness_score']}`",
        f"- Recommendation: `{metrics['recommendation']}`",
        f"- Blockers: `{', '.join(metrics['blockers']) if metrics['blockers'] else 'none'}`",
        "",
        "## Metrics",
        "",
    ]

    for key, value in metrics.items():
        if key in {"manifest", "generated_at", "package_path", "blockers"}:
            continue
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(
        [
            "",
            "## Manifest",
            "",
            "| path | bytes | sha256 |",
            "|---|---:|---|",
        ]
    )
    for item in manifest:
        lines.append(f"| `{item['path']}` | {item['bytes']} | `{item['sha256']}` |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CRAMPS sidecar package metrics.")
    parser.add_argument("package", type=Path, help="Study or preflight package directory.")
    parser.add_argument(
        "--level",
        choices=["preflight", "full", "auto"],
        default="auto",
        help="Package level to check.",
    )
    parser.add_argument("--out-json", type=Path, default=None, help="Metrics JSON output path.")
    parser.add_argument("--out-md", type=Path, default=None, help="Metrics Markdown output path.")
    args = parser.parse_args()

    root = args.package.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Package directory not found: {root}")

    if args.level == "auto":
        preflight_present = sum(1 for name in PREFLIGHT_REQUIRED if find_file(root, name))
        full_present = sum(1 for name in FULL_REQUIRED if find_file(root, name))
        if preflight_present and full_present:
            level = "full" if full_present >= preflight_present else "preflight"
        elif find_file(root, "preflight_rows.csv"):
            level = "preflight"
        else:
            level = "full"
    else:
        level = args.level

    metrics = score_preflight(root) if level == "preflight" else score_full(root)
    metrics["generated_at"] = datetime.now(timezone.utc).isoformat()
    metrics["package_path"] = str(root)
    manifest = make_manifest(root)
    metrics["manifest"] = manifest
    metrics["package_sha256"] = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    out_json = args.out_json or (root / "cramps_sidecar_metrics.json")
    out_md = args.out_md or (root / "cramps_sidecar_metrics.md")

    if package_path_inside_sanitized_source(root) and (args.out_json is None or args.out_md is None):
        raise SystemExit(
            "Refusing to write sidecar outputs into sanitized source material. "
            "Use --out-json and --out-md outside the repository, or copy the package under cramps_projects/ first."
        )
    if output_path_inside_sanitized_source(out_json) or output_path_inside_sanitized_source(out_md):
        raise SystemExit("Refusing to write sidecar output files inside sanitized source material.")

    out_json.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(metrics, manifest), encoding="utf-8")

    print(json.dumps({k: metrics[k] for k in ["level", "readiness_score", "recommendation", "blockers", "package_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
