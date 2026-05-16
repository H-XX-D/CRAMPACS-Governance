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
