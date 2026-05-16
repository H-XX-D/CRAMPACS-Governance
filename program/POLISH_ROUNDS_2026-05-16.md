# CRAMPS Polish Rounds

**Document ID:** CRAMPS-POLISH-2026-05-16  
**Version:** 0.1  
**Status:** Completed polish log  
**Date:** 2026-05-16

## Purpose

This log records ten rounds of aesthetic, teaching, and system polish applied to the CRAMPS package.

## Round 1: Brand identity

Focus:

- make CRAMPS feel like a controlled technical method
- define voice, visual roles, color roles, and message architecture

Artifacts:

- `brand/CRAMPS_BRAND_SYSTEM.md`
- `brand/CRAMPS_MESSAGE_ARCHITECTURE.md`

Outcome:

- CRAMPS now has a consistent identity and claim boundary.

## Round 2: Document style

Focus:

- make policies, printouts, training material, and supervisor packets easier to scan
- standardize decision words, severity words, and page patterns

Artifacts:

- `brand/CRAMPS_DOCUMENT_STYLE_GUIDE.md`

Outcome:

- future documents have a style rule set and release checklist.

## Round 3: Research-backed framework design

Focus:

- benchmark CRAMPS against mature reporting, evidence, quality, risk, and systems-engineering frameworks

Artifacts:

- `research/SUCCESSFUL_FRAMEWORK_PATTERNS.md`

Outcome:

- framework design choices now trace to source-backed patterns.

## Round 4: Training architecture

Focus:

- create teachable adoption paths for executives, supervisors, analysts, practitioners, and instructors

Artifacts:

- `training/CRAMPS_TRAINING_GUIDE.md`
- `training/SLIDE_OUTLINE.md`

Outcome:

- CRAMPS can be taught as a 60 minute briefing, 2 hour orientation, 1 day workshop, or 3 day practitioner course.

## Round 5: Instructor enablement

Focus:

- let an internal trainer teach the method without improvising

Artifacts:

- `training/INSTRUCTOR_GUIDE.md`

Outcome:

- instructors have facilitation notes, debrief scripts, and correction patterns for common learner mistakes.

## Round 6: Learner practice

Focus:

- make learners practice the artifacts, not just hear the theory

Artifacts:

- `training/LEARNER_WORKBOOK.md`
- `training/EXERCISE_PACKETS.md`

Outcome:

- training includes coordinate lock, source universe, row integrity, sidecar, and decision exercises.

## Round 7: Competency and training records

Focus:

- prevent attendance from being mistaken for competence

Artifacts:

- `training/COMPETENCY_RUBRIC.md`
- `program/registers/training_matrix.csv`

Outcome:

- learners can be scored by role and recorded in the training matrix.

## Round 8: Navigation and entry points

Focus:

- make the repository easier to enter from brand, training, program, domain, and tool routes

Artifacts:

- `README.md`
- `brand/README.md`
- `training/README.md`
- `research/README.md`

Outcome:

- the package reads as a teachable system rather than a file dump.

## Round 9: Generated artifacts and workbooks

Focus:

- carry brand and training concepts into generated printouts and spreadsheets

Artifacts:

- `tools/build_printouts_and_spreadsheets.mjs`
- `printouts/governance_master_printout.md`
- `spreadsheets/CRAMPS_Governance_Master.xlsx`

Outcome:

- governance workbooks now include brand controls and training paths.

## Round 10: Release hygiene

Focus:

- run naming, ASCII, syntax, workbook, and sidecar checks before commit

Checks:

- Python compile
- Node syntax checks
- workbook import verification
- sidecar preflight check
- sidecar full scaffold check
- bad naming scan
- ASCII scan
- diff whitespace check

Outcome:

- package is ready for commit and push after the verification run.

## Post-Build Round 3: Operational acceptance hardening

Focus:

- add a reviewer route for the worked example
- make acceptance criteria explicit for source-kit releases, preflights, full packages, and examples
- document the one-agent preflight boundary and full-system agent handoff point

Artifacts:

- `program/RELEASE_ACCEPTANCE_CHECKLIST.md`
- `program/ROUND_3_HARDENING_AUDIT_2026-05-16.md`
- `worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence/REVIEWER_WALKTHROUGH.md`

Outcome:

- a supervisor or AI operator can now inspect whether the source kit, worked example, or package is in a usable state without inferring acceptance rules from scattered documents.

## Post-Build Round 4: First-pilot operationalization

Focus:

- turn the program from a governed package into a first-pilot operating path
- make pilot selection explicit before teams spend time or budget
- prevent teams from choosing a first pilot that is too broad, too sensitive, or too politically loaded

Artifacts:

- `program/FIRST_PILOT_RUNBOOK.md`
- `program/PILOT_SELECTION_SCORECARD.md`

Outcome:

- a team can now choose a bounded first pilot, run a lowercase preflight, decide whether to open an uppercase package, and close the pilot without inventing the operating sequence.

## Post-Build Round 5: Agent deployment helper polish

Focus:

- make agent deployment explicit instead of implied by role names
- keep lowercase preflights to one accountable operator by default
- make uppercase role-agent deployment gated, logged, and handoff-controlled

Artifacts:

- `program/AGENT_DEPLOYMENT_HELPERS.md`
- `templates/agent_deployment_plan.csv`
- `templates/agent_handoff_checklist.csv`
- `templates/agent_task_brief.md`
- package-local `ai_controls/AGENT_DEPLOYMENT_HELPER.md`

Outcome:

- AI and human helpers can be pointed at a package with clear role spans, input limits, handoff accounting, and quarantine stop rules.

## Post-Build Round 6: Agent audit enforcement

Focus:

- make agent deployment controls machine-checkable
- detect missing deployment files, broken CSV headers, duplicate agent IDs, missing active-agent registry rows, preflight multi-agent drift, and broken handoffs
- add agent-control status to the normal package operating loop

Artifacts:

- `tools/cramps_cli.py agent-audit`
- package-local `ai_controls/agent_audit_status.json`
- package-local `ai_controls/agent_audit_report.md`
- updated operator guides, pilot runbook, and acceptance checks

Outcome:

- packages can now be inspected for agent deployment consistency before gates rely on agent-produced work.

## Post-Build Round 7: Acceptance audit synthesis

Focus:

- turn separate package checks into a single reviewer-facing acceptance decision
- distinguish preflight-decision acceptance from full release-review readiness
- make stale or missing sidecar, agent-audit, leak-scan, and gate artifacts visible before reliance

Artifacts:

- `tools/cramps_cli.py acceptance-audit`
- package-local `ai_controls/acceptance_audit_status.json`
- package-local `ai_controls/acceptance_audit_report.md`
- updated pilot runbook, release checklist, operator guides, and worked example commands

Outcome:

- operators can ask one final package-level question before promotion or release review: is this package control-complete enough for the reliance being requested?

## Post-Build Round 8: Reviewer packet hardening

Focus:

- convert accepted package state into an inspectable reviewer handoff
- prevent silent handoff after material package changes made after acceptance
- keep packet ZIPs bounded by default so raw evidence is not bundled unless explicitly requested

Artifacts:

- `tools/cramps_cli.py review-packet`
- package-local `exports/review_packet/review_packet_status.json`
- package-local `exports/review_packet/REVIEW_PACKET_MANIFEST.csv`
- package-local `exports/review_packet/REVIEW_PACKET_SUMMARY.md`
- package-local `exports/review_packet/REVIEWER_HANDOFF.md`
- updated audit packet, runbook, release checklist, operator guides, and worked example commands

Outcome:

- reviewers receive a package index with hashes, control status, reliance limits, and blocker checks instead of a loose folder handoff.

## Post-Build Round 9: Source-kit audit hardening

Focus:

- give the reusable CRAMPS source kit its own audit path, separate from study-package audits
- detect stale legacy names, missing domain artifacts, template-contract drift, controlled-source contamination, local junk files, generated package leftovers, and dirty worktrees
- make pre-push and handoff hygiene inspectable with one command

Artifacts:

- `tools/cramps_cli.py source-audit`
- updated README, program README, tools README, and release acceptance checklist

Outcome:

- a maintainer can now ask whether the source kit itself is coherent enough to publish or hand off before running package-specific controls.

## Post-Build Round 10: End-to-end self-test hardening

Focus:

- add a no-residue smoke test that proves the CLI can operate a package from source audit through review packet
- verify the default review ZIP stays bounded and does not include package evidence
- verify stale post-acceptance edits block handoff
- verify source-root review-packet writes are refused

Artifacts:

- `tools/cramps_cli.py self-test`
- optional self-test Markdown report output
- updated README, program README, tools README, and release acceptance checklist

Outcome:

- maintainers can now run one command to exercise the trust path before pushing or handing CRAMPS to another operator.

## Post-Build Round 11: Source snapshot handoff

Focus:

- create a reproducible source-kit handoff record after source audit and self-test
- generate a file-level source manifest with hashes, a summary, status JSON, and ZIP
- fail closed on dirty source or audit warnings unless explicitly allowed
- keep generated handoff artifacts under ignored `dist/`

Artifacts:

- `tools/cramps_cli.py source-snapshot`
- ignored `dist/` output path
- updated README, program README, tools README, and release acceptance checklist

Outcome:

- source-kit releases can now be handed off with a manifest and archive instead of relying only on the git commit pointer.

## Post-Build Round 12: Executable release acceptance

Focus:

- convert the release acceptance checklist from a document-only control into an executable gate
- collect command logs, CSV results, status JSON, and a Markdown release-check report in one output directory
- support both source-kit release checks and package-level release checks
- keep source-kit release outputs under ignored `dist/` by default and keep package checks package-local
- refuse mutating package checks against source-tree worked examples unless the example is copied to an isolated package path first

Artifacts:

- `tools/cramps_cli.py release-check source`
- `tools/cramps_cli.py release-check package <package>`
- source-tree package-output refusal guards in `tools/cramps_cli.py` and `tools/cramps_sidecar.py`
- `RELEASE_CHECK_RESULTS.csv`
- `release_check_status.json`
- `RELEASE_CHECK_REPORT.md`
- updated README, program README, tools README, and release acceptance checklist

Outcome:

- maintainers and AI operators can now run one acceptance command before handoff instead of manually reconstructing the release sequence from the checklist.

## Post-Build Round 13: Data-contract audit gate

Focus:

- add an explicit CSV data-contract audit instead of relying only on file presence
- check package table headers, required populated-row fields, and cross-table references
- check source templates, register headers, and domain-pack starter CSVs for internal consistency
- make acceptance depend on a current contract audit so malformed rows cannot bypass review

Artifacts:

- `tools/cramps_cli.py contract-audit source`
- `tools/cramps_cli.py contract-audit package <package>`
- `CONTRACT_AUDIT_RESULTS.csv`
- `contract_audit_status.json`
- `contract_audit_report.md`
- updated release-check, self-test, status, acceptance audit, operator guides, and release checklist

Outcome:

- CRAMPS now has a dedicated data-contract gate between DAG accounting and acceptance, making malformed package tables a release blocker rather than a hidden reviewer burden.

## Post-Build Round 14: Worked example custody polish

Focus:

- make the worked example a stronger teaching and audit artifact
- replace the informal preflight manifest with the source-kit manifest contract and SHA-256 hashes
- add a source-safe run record and guided teaching script
- remove stale committed sidecar runtime output from the source example
- add a source-audit blocker if worked examples contain runtime outputs

Artifacts:

- `worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence/RUN_RECORD.md`
- `worked_examples/preflight/cramps-phy-synthetic-coordinate-recurrence/TEACHING_SCRIPT.md`
- contract-shaped `preflight_manifest.csv`
- updated worked-example README, reviewer walkthrough, expected-output guidance, and source-audit check

Outcome:

- the worked example now teaches custody, contract audit, source-safe verification, and escalation boundaries without carrying stale generated output in the reusable source tree.

## Post-Build Round 15: Worked example manifest hardening

Focus:

- make worked-example custody hashes executable instead of decorative
- fail the source audit if a worked-example manifest path is unsafe, missing, or stale
- document how maintainers update custody hashes after reviewed artifact edits

Artifacts:

- `tools/cramps_cli.py` `worked_example_manifest_hashes` source-audit check
- updated worked-example README and run record

Outcome:

- a reviewer can now trust that the worked example's manifest represents the files actually present in the repository at audit time.

## Post-Build Round 16: Manifest tamper-trap self-test

Focus:

- prove the worked-example manifest control fails closed when a custody artifact changes
- add a clean-manifest positive check and a tampered-copy negative check to `self-test`
- make release acceptance documentation name the manifest tamper trap explicitly

Artifacts:

- `tools/cramps_cli.py` self-test manifest clean and tamper checks
- updated release checklist and tools README

Outcome:

- maintainers now test both sides of the worked-example checksum control: current manifests pass, stale manifests are detected before release.

## Post-Build Round 17: Contract-reference tamper trap

Focus:

- prove the data-contract audit catches broken row-to-source references
- add a self-test negative control that corrupts a copied preflight row source ID
- make release documentation treat contract-reference failure as a tested stop condition

Artifacts:

- `tools/cramps_cli.py` `contract_reference_tamper_trap` self-test check
- updated release checklist and tools README

Outcome:

- maintainers now test that malformed preflight rows cannot pass release hygiene simply because the happy-path worked example is valid.

## Post-Build Round 18: Preflight agent-boundary tamper trap

Focus:

- prove lowercase preflight packages remain one-operator by default
- add a self-test negative control that injects a second active preflight operator
- verify `agent-audit` raises `preflight_multi_agent_without_deviation`

Artifacts:

- `tools/cramps_cli.py` `preflight_multi_agent_tamper_trap` self-test check
- updated release checklist and tools README

Outcome:

- maintainers now test that a lightweight preflight cannot quietly become an undeclared multi-agent workflow before review.

## Post-Build Round 19: Leak-quarantine tamper trap

Focus:

- prove the leak scanner fails closed on critical disclosure patterns
- add a self-test negative control that injects a synthetic private-key header into a copied package
- verify `leak-scan --fail-on-quarantine` requires quarantine before release checks proceed

Artifacts:

- `tools/cramps_cli.py` `leak_quarantine_tamper_trap` self-test check
- updated release checklist and tools README

Outcome:

- maintainers now test that sensitive-data leakage cannot pass the package hygiene path as a quiet warning.
