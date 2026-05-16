#!/usr/bin/env python3
"""Create a full CRAMPS evidence-package binder scaffold."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BINDERS = [
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

TEMPLATE_COPIES = [
    ("templates/role_assignment.csv", "00_charter/role_assignment.csv"),
    ("templates/CRAMPS_PROTOCOL_TEMPLATE.md", "01_protocol_lock/protocol.md"),
    ("templates/candidate_coordinate_registry.csv", "01_protocol_lock/candidate_coordinate_registry.csv"),
    ("templates/amendment_log.csv", "01_protocol_lock/amendment_log.csv"),
    ("templates/source_catalog.csv", "02_sources/source_catalog.csv"),
    ("templates/anomaly_rows_raw.csv", "03_extraction/anomaly_rows_raw.csv"),
    ("templates/coordinate_transform_registry.csv", "04_coordinate_normalization/coordinate_transform_registry.csv"),
    ("templates/normalized_rows.csv", "04_coordinate_normalization/normalized_rows.csv"),
    ("templates/independence_groups.csv", "05_dependence_bias/independence_groups.csv"),
    ("templates/bias_assessment.csv", "05_dependence_bias/bias_assessment.csv"),
    ("templates/null_model_runs.csv", "06_statistics/null_model_runs.csv"),
    ("templates/analysis_result.csv", "06_statistics/analysis_result.csv"),
    ("program/ASSURANCE_CASE_FRAMEWORK.md", "08_assurance_case/assurance_case.md"),
    ("program/DECISION_MEMO_TEMPLATE.md", "09_review_and_release/decision_memo.md"),
    ("program/AUDIT_REPORT_TEMPLATE.md", "09_review_and_release/audit_report.md"),
    ("templates/build_ledger.csv", "10_trust_maintenance/build_ledger.csv"),
    ("templates/checkpoint_reviews.csv", "10_trust_maintenance/checkpoint_reviews.csv"),
    ("templates/assumption_uncertainty_log.csv", "10_trust_maintenance/assumption_uncertainty_log.csv"),
    ("templates/claim_trace_matrix.csv", "10_trust_maintenance/claim_trace_matrix.csv"),
    ("templates/trust_debt_register.csv", "10_trust_maintenance/trust_debt_register.csv"),
    ("program/TRUST_STATUS_SUMMARY_TEMPLATE.md", "10_trust_maintenance/trust_status_summary.md"),
]

REGISTER_COPIES = [
    "assurance_case_register.csv",
    "control_evidence_register.csv",
    "decision_log.csv",
    "deviation_capa_log.csv",
    "document_register.csv",
    "gate_review_record.csv",
    "risk_register.csv",
    "training_matrix.csv",
    "trust_debt_register.csv",
]


def load_domain(slug: str) -> dict:
    domains = json.loads((ROOT / "tools" / "cramps_domains.json").read_text(encoding="utf-8"))
    for domain in domains:
        if domain["slug"] == slug:
            return domain
    valid = ", ".join(sorted(domain["slug"] for domain in domains))
    raise SystemExit(f"Unknown domain '{slug}'. Valid domains: {valid}")


def write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def copy_file(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def scaffold(out_dir: Path, domain: dict, study_id: str, force: bool) -> None:
    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        raise SystemExit(f"Output directory is not empty. Re-run with --force if intentional: {out_dir}")

    for binder in BINDERS:
        (out_dir / binder).mkdir(parents=True, exist_ok=True)

    created = datetime.now(timezone.utc).isoformat()
    write(
        out_dir / "PACKAGE_README.md",
        f"""
# {domain["full"]} Evidence Package

**Study ID:** {study_id}  
**Domain:** {domain["label"]}  
**Created:** {created}  
**Assurance level:** full CRAMPS package scaffold

This package is not release-ready when created. It is a controlled binder scaffold.
Run `python tools/cramps_sidecar.py {out_dir} --level full` from the repository root during assembly and before release.

## Naming Boundary

- `{domain["light"]}` is the one to two day preflight route.
- `{domain["full"]}` is the full assurance route after protocol lock.

## Binder Rule

All required binders must be complete, all applicable controls must have evidence, and all Critical findings must be closed before release.

## Trust Positioning Rule

This package is not simply "trustworthy." It is trustworthy only for the reliance stated in the decision memo and trust status summary.

Until `10_trust_maintenance/trust_status_summary.md` is reviewed, this package is not release-ready.
""",
        force,
    )
    write(
        out_dir / "00_charter" / "study_charter.md",
        f"""
# Study Charter

**Study ID:** {study_id}  
**Domain:** {domain["label"]}  
**Preflight route:** {domain["light"]}  
**Full assurance route:** {domain["full"]}  
**Decision owner:**  
**Safety/domain supervisor:**  
**Statistical lead:**  
**Protocol steward:**  
**Data steward:**  
**Reproducibility lead:**  

## Decision To Support

State the operational, research, safety, security, financial, or scientific decision this package supports.

## Candidate Coordinate Families

{", ".join(domain["coordinates"])}

## Intended Use

## Prohibited Use

CRAMPS does not establish causality, compliance, safety, efficacy, exploitability, fraud, or physical discovery by itself.

## Constraints

Record legal, privacy, security, regulatory, ethical, data-rights, or classification constraints.
""",
        force,
    )

    for src_rel, dst_rel in TEMPLATE_COPIES:
        copy_file(ROOT / src_rel, out_dir / dst_rel, force)

    for register in REGISTER_COPIES:
        copy_file(ROOT / "program" / "registers" / register, out_dir / "registers" / register, force)

    copy_file(
        ROOT / "program" / "registers" / "gate_review_record.csv",
        out_dir / "09_review_and_release" / "gate_review_record.csv",
        force,
    )
    copy_file(
        ROOT / "program" / "registers" / "assurance_case_register.csv",
        out_dir / "08_assurance_case" / "assurance_case_register.csv",
        force,
    )
    copy_file(
        ROOT / "program" / "registers" / "risk_register.csv",
        out_dir / "08_assurance_case" / "risk_register.csv",
        force,
    )

    write(
        out_dir / "02_sources" / "search_strategy.md",
        """
# Search Strategy

Record exact search locations, dates, query strings, inclusion rules, exclusion rules, and reviewer assignments.
""",
        force,
    )
    write(
        out_dir / "02_sources" / "source_flow.md",
        """
# Source Flow

Track searched, screened, included, excluded, unavailable, duplicate, null, and non-event sources.
""",
        force,
    )
    write(
        out_dir / "03_extraction" / "extraction_notes.md",
        """
# Extraction Notes

Record extraction decisions, ambiguous rows, reviewer disagreements, plot digitization notes, and AI-assistance logs.
""",
        force,
    )
    write(
        out_dir / "04_coordinate_normalization" / "unit_conversion_audit.md",
        """
# Unit Conversion Audit

For each transform, recompute canonical values from raw values and record reviewer disposition.
""",
        force,
    )
    write(
        out_dir / "05_dependence_bias" / "missing_evidence_assessment.md",
        """
# Missing Evidence Assessment

Assess publication bias, selective reporting, inaccessible nulls, source-system censoring, and domain-specific missingness.
""",
        force,
    )
    write(
        out_dir / "06_statistics" / "statistical_analysis_plan.md",
        """
# Statistical Analysis Plan

Lock the primary statistic, null model, random seeds, multiple-testing correction, negative controls, and sensitivity tests before scoring.
""",
        force,
    )
    write(
        out_dir / "06_statistics" / "negative_controls.md",
        """
# Negative Controls

Define negative-control coordinates, source classes, or row families expected not to recur.
""",
        force,
    )
    write(
        out_dir / "06_statistics" / "sensitivity_results.md",
        """
# Sensitivity Results

Record leave-source-out, leave-family-out, leave-era-out, tolerance, bias, extraction-confidence, and null-model sensitivity results.
""",
        force,
    )
    write(
        out_dir / "07_reproducibility" / "checksum_manifest.csv",
        "artifact_path,artifact_role,bytes,sha256,created_at,created_by,review_status,notes",
        force,
    )
    write(
        out_dir / "07_reproducibility" / "environment_record.md",
        """
# Environment Record

Record operating system, language/runtime versions, package locks, container image, hardware assumptions, data locations, and restricted-data handling.
""",
        force,
    )
    write(
        out_dir / "07_reproducibility" / "run_instructions.md",
        """
# Run Instructions

List exact commands required to reproduce the analysis from the package inputs.
""",
        force,
    )
    write(
        out_dir / "07_reproducibility" / "clean_run_report.md",
        """
# Clean Run Report

Record clean-run date, operator, command, output hashes, differences, and disposition.
""",
        force,
    )
    write(
        out_dir / "09_review_and_release" / "claim_language_approval.md",
        """
# Claim Language Approval

Map each proposed claim to its evidence tier, required caveat, prohibited overclaim, and approving authority.
""",
        force,
    )
    write(
        out_dir / "09_review_and_release" / "release_signoff.md",
        """
# Release Signoff

Release is prohibited until gate review, control evidence review, reproducibility review, claim-language approval, and decision memo are complete.
""",
        force,
    )
    write(
        out_dir / "10_trust_maintenance" / "open_questions.md",
        """
# Open Questions

Track unresolved questions that could change trust state, evidence tier, decision scope, or prohibited reliance.

| question_id | question | owner | decision impact | due date | status |
|---|---|---|---|---|---|
""",
        force,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a full CRAMPS evidence-package binder.")
    parser.add_argument("output_dir", type=Path, help="Directory to create or populate.")
    parser.add_argument("--domain", required=True, help="Domain slug, for example med, fin, phy, cyb.")
    parser.add_argument("--study-id", required=True, help="Stable study identifier.")
    parser.add_argument("--force", action="store_true", help="Allow overwriting existing scaffold files.")
    args = parser.parse_args()

    domain = load_domain(args.domain)
    scaffold(args.output_dir.resolve(), domain, args.study_id, args.force)
    print(f"Created {domain['full']} scaffold at {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
