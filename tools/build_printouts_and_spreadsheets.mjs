import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");

const domains = JSON.parse(await fs.readFile(path.join(root, "tools", "cramps_domains.json"), "utf8"));

const layers = [
  ["0", "Concept", "Vocabulary, claim boundary, uppercase/lowercase distinction", "README, naming policy"],
  ["1", "Lightweight preflight", "1-2 day triage and seed artifacts", "preflight policy, preflight templates, domain packs"],
  ["2", "Gotchas", "Fast failure-mode checks and stop signs", "gotcha guide, field printouts"],
  ["3", "Program standards", "Governance, quality gates, document control, release authority, CAPA", "program operating manual, control catalog, document control, release RACI, gate map, CAPA procedure"],
  ["4", "Methodology", "Coordinate ontology, nulls, dependence, bias, claim tiers", "methodology policy, protocol template"],
  ["5", "Domain overlay", "Field-specific adaptation", "domain overlays, domain packs, field printouts"],
  ["6", "Data contracts", "Structured tables, stable IDs, register schemas", "templates, register data dictionary, package scaffold"],
  ["7", "Checksums", "Cross-unit reproducibility and unit integrity", "checksum policy, reproducibility binder"],
  ["8", "Sidecar metrics", "Package readiness, binder coverage, blockers", "sidecar runner"],
  ["9", "Full SOP", "End-to-end study execution and evidence package assembly", "program SOP, evidence package spec, assurance case, decision memo"],
  ["10", "Trust maintenance", "Checkpoint honesty, reliance positioning, trust debt, claim trace", "trust maintenance protocol, trust checkpoint map, trust positioning, trust status summary"],
  ["11", "Regulatory and deployment", "Safety supervisor review, audit, validation, training, regulated deployment", "supervisor packet, audit procedure, validation plan, training plan, regulated addendum, deployment playbook, 90-day roadmap"],
  ["12", "Platform", "Software workflow modules", "future product layer"],
];

const gates = [
  ["G0 Charter", "decision statement, assurance level, roles, intended use, prohibited use", "Before protocol lock"],
  ["G1 Coordinate Lock", "coordinate ontology, candidate registry, tolerance basis, transform rules, negative controls", "Before source scoring"],
  ["G2 Source Universe", "search strategy, source catalog, source flow, exclusions, null search", "Before extraction closeout"],
  ["G3 Row Integrity", "raw rows, source trace, extraction confidence, review status, quarantine log", "Before normalization closeout"],
  ["G4 Dependence and Bias", "evidence-family map, independence grades, bias table, missing-evidence memo, weights", "Before analysis"],
  ["G5 Statistical Method", "primary statistic, null model, multiplicity correction, negative controls, sensitivity plan", "Before reporting"],
  ["G6 Reproducibility", "checksums, environment, run script, output hashes, clean-run report", "Before release review"],
  ["G7 Release", "assurance case, red-team findings, decision memo, evidence tier, claim-language approval", "Before external or operational use"],
];

const controls = [
  ["GOV-01", "Decision authority assigned", "Prevent ownerless decisions", "charter, role assignment, decision memo"],
  ["GOV-02", "Assurance level declared", "Prevent lowercase work being treated as full assurance", "charter, report title"],
  ["DOC-02", "Protocol lock", "Prevent post-hoc method changes", "protocol hash, lock timestamp"],
  ["COORD-01", "Coordinate definition", "Prevent vague or mobile target coordinates", "coordinate ontology"],
  ["COORD-02", "Tolerance justification", "Prevent tolerance creep", "candidate registry"],
  ["SRC-02", "Null/non-event search", "Prevent positive-only evidence", "source catalog, null row count"],
  ["ROW-01", "Row provenance", "Ensure every row traces to source", "raw row table"],
  ["ROW-02", "Raw/normalized separation", "Prevent unit and transform overwrites", "raw and normalized tables"],
  ["IND-01", "Evidence-family map", "Prevent duplicate evidence multiplication", "independence groups"],
  ["BIAS-01", "Missing-evidence assessment", "Identify inaccessible or unpublished nulls", "missing-evidence memo"],
  ["STAT-02", "Null model specification", "Make the test basis explicit", "null model spec"],
  ["STAT-03", "Global correction", "Control look-elsewhere and multiplicity", "result table"],
  ["STAT-04", "Sensitivity tests", "Identify fragility", "sensitivity results"],
  ["REPRO-01", "Checksum manifest", "Detect silent file drift", "manifest and hashes"],
  ["REPRO-03", "Clean reproduction", "Verify package can be rerun", "reproducibility report"],
  ["REL-01", "Evidence tier assignment", "Prevent overclaiming", "evidence tier table"],
  ["REL-02", "Claim language approval", "Prevent unsupported conclusions", "signed report review"],
  ["CAPA-01", "Deviation handling", "Track failures and repairs", "deviation/CAPA log"],
  ["TRUST-01", "Build ledger", "Track material work while package is being built", "build_ledger.csv"],
  ["TRUST-02", "Trust checkpoint review", "Prevent silent promotion of unchecked artifacts", "checkpoint_reviews.csv"],
  ["TRUST-03", "Assumption and uncertainty log", "Prevent assumptions becoming facts", "assumption_uncertainty_log.csv"],
  ["TRUST-04", "Claim trace matrix", "Tie every claim to evidence, controls, gates, and permitted reliance", "claim_trace_matrix.csv"],
  ["TRUST-05", "Trust debt register", "Track unresolved trust gaps with owner, due date, and release impact", "trust_debt_register.csv"],
  ["TRUST-06", "Reliance positioning", "State what the package is trustworthy for and not trustworthy for", "trust status summary, decision memo"],
  ["TRAIN-01", "Role training", "Ensure operators know controls", "training matrix"],
];

const assuranceClaims = [
  ["AC-01", "Coordinate was pre-specified", "protocol hash, candidate registry", "coordinate moved after rows were known"],
  ["AC-02", "Source universe was not cherry-picked", "search log, source flow", "null sources omitted"],
  ["AC-03", "Rows are traceable and correctly extracted", "row table, source references", "AI or analyst inferred values incorrectly"],
  ["AC-04", "Units and transforms are controlled", "raw/normalized split, transform registry", "hidden conversion created cluster"],
  ["AC-05", "Dependence is modeled or controlled", "evidence-family map, weights", "duplicate evidence counted independently"],
  ["AC-06", "Missing evidence and bias are assessed", "bias table, missing-evidence memo", "reporting bias explains cluster"],
  ["AC-07", "Null model is fit for purpose", "null spec, negative controls", "null is too weak"],
  ["AC-08", "Multiple testing is addressed", "global correction", "local result is look-elsewhere artifact"],
  ["AC-09", "Result is robust enough for tier", "sensitivity tests", "one source drives result"],
  ["AC-10", "Package is reproducible", "checksums, clean run", "output cannot be recreated"],
  ["AC-11", "Claim language matches evidence", "evidence tier, approved report", "report overstates causality"],
];

const validationBatteries = [
  ["A", "Known negative", "Recurrence should not exist", "No false high-confidence recurrence"],
  ["B", "Synthetic planted cluster", "Known recurrence is injected", "Detects planted recurrence under registered statistic"],
  ["C", "Duplicate-evidence trap", "Many rows derive from one source family", "Down-weights or collapses duplicates"],
  ["D", "Missing-null trap", "Nulls are hidden until audit", "Flags missing evidence and demotes/holds"],
  ["E", "Unit-conversion trap", "Mixed units/reference systems", "Raw/normalized audit catches drift"],
  ["F", "Inter-rater reliability", "Independent reviewers grade same sample", "Disagreements measured and adjudicated"],
];

const packageScaffold = [
  ["00_charter", "decision, roles, intended use, prohibited use, constraints", "study_charter.md; role_assignment.csv"],
  ["01_protocol_lock", "protocol, candidate registry, amendment control", "protocol.md; candidate_coordinate_registry.csv; amendment_log.csv"],
  ["02_sources", "search strategy, source catalog, source flow", "search_strategy.md; source_catalog.csv; source_flow.md"],
  ["03_extraction", "raw rows and extraction review", "anomaly_rows_raw.csv; extraction_notes.md"],
  ["04_coordinate_normalization", "transforms, normalized rows, unit audit", "coordinate_transform_registry.csv; normalized_rows.csv; unit_conversion_audit.md"],
  ["05_dependence_bias", "independence, bias, missing evidence", "independence_groups.csv; bias_assessment.csv; missing_evidence_assessment.md"],
  ["06_statistics", "analysis plan, null model, result, controls, sensitivities", "statistical_analysis_plan.md; null_model_runs.csv; analysis_result.csv; negative_controls.md; sensitivity_results.md"],
  ["07_reproducibility", "checksums, environment, run instructions, clean run", "checksum_manifest.csv; environment_record.md; run_instructions.md; clean_run_report.md"],
  ["08_assurance_case", "claims, rebuttals, residual risk", "assurance_case.md; assurance_case_register.csv; risk_register.csv"],
  ["09_review_and_release", "gate review, audit, decision, release signoff", "gate_review_record.csv; audit_report.md; decision_memo.md; claim_language_approval.md; release_signoff.md"],
  ["10_trust_maintenance", "build ledger, checkpoints, assumptions, claim trace, trust debt", "build_ledger.csv; checkpoint_reviews.csv; assumption_uncertainty_log.csv; claim_trace_matrix.csv; trust_debt_register.csv; trust_status_summary.md; open_questions.md"],
  ["registers", "package-level governance registers", "document; control; gate; assurance; CAPA; decision; risk; training"],
];

const programRegisters = [
  ["document_register.csv", "document control, version, status, approval"],
  ["control_evidence_register.csv", "control-by-control evidence map"],
  ["gate_review_record.csv", "gate decisions, blockers, release holds"],
  ["assurance_case_register.csv", "claim, evidence, rebuttal, residual risk"],
  ["deviation_capa_log.csv", "deviation, containment, CAPA, effectiveness"],
  ["decision_log.csv", "authorized decision, tier, conditions, prohibited claims"],
  ["risk_register.csv", "active and residual risks"],
  ["training_matrix.csv", "role training and competency"],
  ["trust_debt_register.csv", "unresolved trust gaps and release impact"],
];

const brandControls = [
  ["Assurance boundary", "Every artifact states whether it is cramps-* or CRAMPS-*"],
  ["Claim boundary", "Every release-facing artifact states what CRAMPS does not prove"],
  ["Decision language", "Approve, approve_with_limits, hold, demote, reject, stop, emergency_parallel_action"],
  ["Severity language", "Critical, Major, Minor, Observation"],
  ["Stop signs", "Preflight and full package stop rules are easy to find"],
  ["Evidence names", "Required evidence uses concrete file, register, or binder names"],
  ["Domain humility", "Domain claims are restrained and require domain-standard confirmation"],
];

const trainingPaths = [
  ["Executive briefing", "Sponsor, agency lead, director", "60 minutes", "adoption decision and pilot scope"],
  ["Supervisor orientation", "Safety supervisor, risk owner, program officer", "2 hours", "approval, hold, demote, reject literacy"],
  ["Preflight workshop", "Analyst, domain reviewer, project lead", "1 day", "completed mock cramps-* preflight"],
  ["Practitioner course", "Data scientist, evidence reviewer, auditor", "3 days", "full package walkthrough and gate practice"],
  ["Instructor course", "Internal trainer, quality lead", "2 days after practitioner course", "teach-back and scoring consistency"],
];

const frameworkPatterns = [
  ["PRISMA", "Checklist plus flow diagrams", "Use checklists, printouts, and package flow"],
  ["Cochrane", "Missing-evidence risk", "Treat nulls, non-events, and missing evidence as release issues"],
  ["GRADE", "Separate certainty and recommendation", "Separate evidence tier from supervisor decision"],
  ["ISO quality management", "Process, evidence-based decisions, improvement", "Use owners, registers, CAPA, and review cadence"],
  ["NIST CSF", "Core, examples, references, tiers", "Keep a small core with implementation examples and maturity levels"],
  ["NIST AI RMF", "Framework plus playbook", "Pair principles with teachable actions"],
  ["NASA systems engineering", "Lifecycle reviews", "Use G0-G7 as lifecycle gates"],
  ["FDA quality systems", "Quality model plus regulatory boundary", "Add regulated controls without claiming automatic compliance"],
];

const trustStates = [
  ["draft", "work has started but is not checked", "do not rely"],
  ["unchecked", "artifact exists but no reviewer has accepted it", "do not rely"],
  ["checked_with_limits", "reviewed, but known limits remain", "rely only within stated limits"],
  ["accepted", "reviewed and accepted for current gate", "rely within current evidence tier"],
  ["blocked", "has a defect that prevents promotion or release", "do not promote"],
  ["superseded", "replaced by a newer artifact", "retain but do not use"],
  ["quarantined", "retained for traceability but excluded from scoring or release", "do not use as evidence"],
];

const relianceLevels = [
  ["idea sketch", "conversation and scoping", "CRAMPS claim, preflight decision, operational decision"],
  ["cramps-* checked", "continue, hold, stop, or full-study escalation", "domain conclusion, full assurance, external claim"],
  ["CRAMPS-* scaffold", "organizing work", "evidence reliance or release"],
  ["CRAMPS-* gate-accepted", "advancing to the next gate", "release unless G7 is complete"],
  ["CRAMPS-* release-ready", "decision support within assigned evidence tier", "proof of causality or regulatory compliance by itself"],
  ["externally validated", "stronger prioritization and process confidence", "domain proof unless domain-standard confirmation is complete"],
];

const trustCheckpoints = [
  ["T0", "package start", "unclear purpose or hidden intended use", "decision owner, intended use, prohibited use"],
  ["T1", "coordinate proposed", "coordinate drift or tolerance creep", "coordinate, units, tolerance, forbidden changes"],
  ["T2", "sources drafted", "positive-only evidence", "source roles, null search, exclusions"],
  ["T3", "rows extracted", "source trace or AI-summary drift", "source links, raw values, extraction confidence"],
  ["T4", "normalization drafted", "hidden unit conversion", "raw/normalized separation, transform review"],
  ["T5", "dependence and bias drafted", "duplicate evidence counted independently", "evidence-family map, missing-evidence risk"],
  ["T6", "statistics planned", "statistic shopping or weak null", "locked statistic, null model, multiplicity plan"],
  ["T7", "results generated", "local result overclaimed", "global correction, sensitivities, negative controls"],
  ["T8", "report drafted", "claim exceeds evidence tier", "claim trace matrix, prohibited claims"],
  ["T9", "release review", "unknown trust state", "trust status summary, sidecar, open CAPA"],
];

const supervisorQuestions = [
  ["1", "What coordinate is being tested?"],
  ["2", "Was it locked before scoring?"],
  ["3", "What nulls or non-events were included?"],
  ["4", "What evidence is duplicated or dependent?"],
  ["5", "What bias could create the pattern?"],
  ["6", "What negative control was used?"],
  ["7", "What would make us stop believing the recurrence?"],
  ["8", "Can the package be reproduced?"],
  ["9", "What action is being requested?"],
  ["10", "What claim is explicitly prohibited?"],
];

const gotchas = [
  ["Coordinate drift", "Coordinate changes names, units, or definitions across sources", "Write the coordinate formula and units on one line"],
  ["Tolerance creep", "Window widens after rows are seen", "State tolerance source before scoring"],
  ["Null starvation", "Only positive anomalies are included", "Find nulls, exclusions, failed replications, non-events"],
  ["Duplicate evidence", "Rows trace to one raw data source", "Draw source-to-row dependence graph"],
  ["Literature fashion", "Many sources inspect same coordinate because it is popular", "Add coordinate-fashion bias"],
  ["Time leakage", "Later knowledge shaped earlier-looking lock", "Compare lock date with source dates"],
  ["Unit trap", "Alignment depends on hidden conversion", "Recompute normalized values from raw values"],
  ["One-source collapse", "Remove one source and result disappears", "Leave-one-source-out"],
  ["Negative control failure", "Controls also recur", "Strengthen null model"],
  ["AI extraction drift", "AI summary becomes data", "Trace each row to source evidence"],
];

function mdTable(headers, rows) {
  return [
    `| ${headers.join(" | ")} |`,
    `| ${headers.map(() => "---").join(" | ")} |`,
    ...rows.map((row) => `| ${row.join(" | ")} |`),
  ].join("\n");
}

async function writeText(file, text) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, `${text.trim()}\n`, "utf8");
}

function setBlock(sheet, startCell, rows) {
  const end = rangeEnd(startCell, rows.length, rows[0].length);
  sheet.getRange(`${startCell}:${end}`).values = rows;
}

function colToNumber(col) {
  return col.split("").reduce((sum, ch) => sum * 26 + ch.charCodeAt(0) - 64, 0);
}

function numberToCol(num) {
  let out = "";
  while (num > 0) {
    const rem = (num - 1) % 26;
    out = String.fromCharCode(65 + rem) + out;
    num = Math.floor((num - 1) / 26);
  }
  return out;
}

function rangeEnd(startCell, rowCount, colCount) {
  const match = startCell.match(/^([A-Z]+)(\d+)$/);
  const startCol = colToNumber(match[1]);
  const startRow = Number(match[2]);
  return `${numberToCol(startCol + colCount - 1)}${startRow + rowCount - 1}`;
}

function addSheet(workbook, name, rows) {
  const sheet = workbook.worksheets.add(name);
  if (rows.length) {
    setBlock(sheet, "A1", rows);
  }
  return sheet;
}

async function exportWorkbook(workbook, file) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  const blob = await SpreadsheetFile.exportXlsx(workbook);
  await blob.save(file);
}

function governanceWorkbook() {
  const wb = Workbook.create();
  addSheet(wb, "Dashboard", [
    ["CRAMPS Governance Master", ""],
    ["Purpose", "Coordinate-resolved weak-signal recurrence governance"],
    ["Uppercase", "CRAMPS-* = full assurance system"],
    ["Lowercase", "cramps-* = 1-2 day preflight"],
    ["Domain count", domains.length],
    ["Layer count", layers.length],
    ["Core rule", "Lowercase can seed uppercase; only uppercase after full protocol lock carries assurance."],
  ]);
  addSheet(wb, "Domain Matrix", [
    ["Preflight", "Full System", "Domain", "Coordinate Examples", "Null Examples", "Primary Gotchas", "Standards"],
    ...domains.map((d) => [d.light, d.full, d.label, d.coordinates.join("; "), d.nulls.join("; "), d.gotchas.join("; "), d.standards.join("; ")]),
  ]);
  addSheet(wb, "Doc Layers", [
    ["Layer", "Name", "Purpose", "Documents"],
    ...layers,
  ]);
  addSheet(wb, "Quality Gates", [
    ["Gate", "Required evidence", "When checked"],
    ...gates,
  ]);
  addSheet(wb, "Control Catalog", [
    ["Control ID", "Control", "Objective", "Evidence"],
    ...controls,
  ]);
  addSheet(wb, "Assurance Claims", [
    ["Claim ID", "Claim", "Required evidence", "Common rebuttal"],
    ...assuranceClaims,
  ]);
  addSheet(wb, "Supervisor Questions", [
    ["No.", "Question", "Answer", "Evidence link", "Open risk"],
    ...supervisorQuestions.map((q) => [q[0], q[1], "", "", ""]),
  ]);
  addSheet(wb, "Validation Batteries", [
    ["Battery", "Name", "Test condition", "Pass condition", "Status", "Notes"],
    ...validationBatteries.map((v) => [...v, "", ""]),
  ]);
  addSheet(wb, "Package Scaffold", [
    ["Binder", "Purpose", "Minimum records"],
    ...packageScaffold,
  ]);
  addSheet(wb, "Program Registers", [
    ["Register", "Purpose", "Owner", "Review status"],
    ...programRegisters.map((r) => [...r, "", ""]),
  ]);
  addSheet(wb, "Brand Controls", [
    ["Control", "Rule", "Owner", "Status"],
    ...brandControls.map((r) => [...r, "", ""]),
  ]);
  addSheet(wb, "Training Paths", [
    ["Track", "Audience", "Duration", "Output", "Owner", "Status"],
    ...trainingPaths.map((r) => [...r, "", ""]),
  ]);
  addSheet(wb, "Framework Patterns", [
    ["Framework", "Pattern", "CRAMPS adoption"],
    ...frameworkPatterns,
  ]);
  addSheet(wb, "Trust States", [
    ["Trust state", "Meaning", "Reliance rule"],
    ...trustStates,
  ]);
  addSheet(wb, "Reliance Levels", [
    ["Package state", "Trustworthy for", "Not trustworthy for"],
    ...relianceLevels,
  ]);
  addSheet(wb, "Trust Checkpoints", [
    ["Checkpoint", "Package point", "Main honesty risk", "Minimum review"],
    ...trustCheckpoints,
  ]);
  addSheet(wb, "CAPA Log", [
    ["Deviation ID", "Study ID", "Severity", "Affected controls", "Description", "Containment", "Root cause", "Corrective action", "Preventive action", "Owner", "Due date", "Verification", "Effectiveness check date", "Effectiveness result", "Approver", "Status"],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
  ]);
  addSheet(wb, "Gotchas", [
    ["Gotcha", "Symptom", "Fast sanity check"],
    ...gotchas,
  ]);
  addSheet(wb, "Preflight Checklist", [
    ["Item", "Status", "Owner", "Notes"],
    ["Scope written", "", "", ""],
    ["Coordinate sketch complete", "", "", ""],
    ["Source shortlist complete", "", "", ""],
    ["Nulls/non-events found", "", "", ""],
    ["Dependence scan complete", "", "", ""],
    ["Bias scan complete", "", "", ""],
    ["Sidecar metrics run", "", "", ""],
    ["Decision written", "", "", ""],
  ]);
  addSheet(wb, "Full Gate Tracker", [
    ["Gate", "Status", "Owner", "Evidence link", "Notes"],
    ...gates.map((g) => [g[0], "", "", "", ""]),
  ]);
  return wb;
}

function domainWorkbook(domain) {
  const wb = Workbook.create();
  addSheet(wb, "Domain Summary", [
    [`${domain.light} / ${domain.full}`, domain.label],
    ["Lightweight preflight", domain.light],
    ["Full assurance", domain.full],
    ["Rule", "Lowercase can seed uppercase. Full assurance starts after full protocol lock."],
    ["Main coordinates", domain.coordinates.join("; ")],
    ["Nulls to find", domain.nulls.join("; ")],
    ["Gotchas", domain.gotchas.join("; ")],
    ["Standards", domain.standards.join("; ")],
  ]);
  addSheet(wb, "Preflight Scope", [
    ["Field", "Entry"],
    ["Preflight ID", ""],
    ["Question", ""],
    ["Candidate coordinate", ""],
    ["Units", ""],
    ["Tolerance sketch", ""],
    ["Decision owner", ""],
    ["Claim boundary", `This is ${domain.light}, not a ${domain.full} confirmatory result.`],
  ]);
  addSheet(wb, "Preflight Sources", [
    ["source_id", "citation_or_label", "url_or_path", "source_type", "domain", "source_role", "publication_or_snapshot_date", "unit_or_site", "known_dependence", "screening_status", "notes"],
    ["", "", "", "", domain.slug, "positive_or_anomaly", "", "", "", "", ""],
    ["", "", "", "", domain.slug, "null_or_non_event", "", "", "", "", ""],
    ...Array.from({ length: 18 }, () => ["", "", "", "", domain.slug, "", "", "", "", "", ""]),
  ]);
  addSheet(wb, "Preflight Rows", [
    ["row_id", "source_id", "coordinate_label", "coordinate_value", "coordinate_units", "row_type", "result_direction", "uncertainty_status", "extraction_confidence", "dependence_concern", "bias_concern", "null_or_non_event_flag", "notes"],
    ["", "", "", "", "", "", "", "", "", "", "", "", ""],
    ...Array.from({ length: 19 }, () => ["", "", "", "", "", "", "", "", "", "", "", "", ""]),
  ]);
  addSheet(wb, "Gotchas", [
    ["Gotcha", "Status", "Notes"],
    ...domain.gotchas.map((g) => [g, "", ""]),
    ...gotchas.slice(0, 6).map((g) => [g[0], "", g[2]]),
  ]);
  addSheet(wb, "Full Gate", [
    ["Gate", "Status", "Owner", "Evidence", "Notes"],
    ["Preflight import disposition complete", "", "", "", ""],
    ...gates.map((g) => [g[0], "", "", g[1], ""]),
  ]);
  addSheet(wb, "Full Evidence Binder", [
    ["Binder", "Status", "Owner", "Minimum records", "Notes"],
    ...packageScaffold.map((b) => [b[0], "", "", b[2], ""]),
  ]);
  addSheet(wb, "Import Log", [
    ["full_study_id", "preflight_id", "artifact_path", "artifact_sha256", "imported_as", "reviewer_id", "review_disposition", "decision_timestamp", "notes"],
    ["", "", "", "", "", "", "", "", ""],
  ]);
  addSheet(wb, "Trust Checkpoints", [
    ["Checkpoint", "Package point", "Main honesty risk", "Decision", "Reviewer", "Notes"],
    ...trustCheckpoints.map((t) => [t[0], t[1], t[2], "", "", ""]),
  ]);
  addSheet(wb, "Reliance Positioning", [
    ["Field", "Entry"],
    ["Trustworthy for", ""],
    ["Not trustworthy for", ""],
    ["Current assurance route", domain.full],
    ["Current trust state", ""],
    ["Current evidence tier", ""],
    ["Prohibited claims", ""],
  ]);
  return wb;
}

async function buildPrintouts() {
  const printoutDir = path.join(root, "printouts");
  await writeText(
    path.join(printoutDir, "governance_master_printout.md"),
    `
# CRAMPS Governance Master Printout

## System Rule

- Uppercase \`CRAMPS-*\` is the full assurance system.
- Lowercase \`cramps-*\` is the one to two day preflight.
- A preflight can seed the full system, but only the full system can carry full assurance after protocol lock.

## Documentation Layers

${mdTable(["Layer", "Name", "Purpose", "Documents"], layers)}

## Quality Gates

${mdTable(["Gate", "Required evidence", "When checked"], gates)}

## Supervisor Questions

${mdTable(["No.", "Question"], supervisorQuestions)}

## Core Controls

${mdTable(["Control ID", "Control", "Objective", "Evidence"], controls)}

## Package Scaffold

${mdTable(["Binder", "Purpose", "Minimum records"], packageScaffold)}

## Program Registers

${mdTable(["Register", "Purpose"], programRegisters)}

## Brand Controls

${mdTable(["Control", "Rule"], brandControls)}

## Training Paths

${mdTable(["Track", "Audience", "Duration", "Output"], trainingPaths)}

## Framework Patterns

${mdTable(["Framework", "Pattern", "CRAMPS adoption"], frameworkPatterns)}

## Trust States

${mdTable(["Trust state", "Meaning", "Reliance rule"], trustStates)}

## Reliance Levels

${mdTable(["Package state", "Trustworthy for", "Not trustworthy for"], relianceLevels)}

## Trust Checkpoints

${mdTable(["Checkpoint", "Package point", "Main honesty risk", "Minimum review"], trustCheckpoints)}
`
  );

  await writeText(
    path.join(printoutDir, "domain_matrix_printout.md"),
    `
# CRAMPS Domain Matrix Printout

${mdTable(
  ["Preflight", "Full System", "Domain", "Coordinates", "Nulls", "Primary Gotchas"],
  domains.map((d) => [d.light, d.full, d.label, d.coordinates.join("; "), d.nulls.join("; "), d.gotchas.join("; ")])
)}
`
  );

  await writeText(
    path.join(printoutDir, "governance_gotchas_printout.md"),
    `
# CRAMPS Governance Gotchas Printout

${mdTable(["Gotcha", "Symptom", "Fast sanity check"], gotchas)}
`
  );

  await writeText(
    path.join(printoutDir, "trust_checkpoint_printout.md"),
    `
# CRAMPS Trust Checkpoint Printout

## Required Positioning Sentence

This package is trustworthy for:  
This package is not trustworthy for:  
Current assurance route:  
Current trust state:  
Current evidence tier:  

## Checkpoint Questions

| Question | Answer |
|---|---|
| What changed since the last checkpoint? |  |
| What evidence was added, removed, revised, or quarantined? |  |
| What is still assumed? |  |
| What is still unverified? |  |
| What sidecar blockers exist? |  |
| What claim language is currently prohibited? |  |
| What decision can be made now? |  |
| What decision cannot be made yet? |  |
| What is the next trust-building action? |  |

## Checkpoint Map

${mdTable(["Checkpoint", "Package point", "Main honesty risk", "Minimum review"], trustCheckpoints)}

## Signoff

| Role | Name | Decision | Date |
|---|---|---|---|
| Reviewer |  |  |  |
| Decision owner |  |  |  |
`
  );

  await writeText(
    path.join(printoutDir, "trust_positioning_printout.md"),
    `
# CRAMPS Trust Positioning Printout

Never say a package is simply "trustworthy." State what it is trustworthy for and what it is not trustworthy for.

## Reliance Levels

${mdTable(["Package state", "Trustworthy for", "Not trustworthy for"], relianceLevels)}

## Trust States

${mdTable(["Trust state", "Meaning", "Reliance rule"], trustStates)}

## Required Positioning

| Field | Entry |
|---|---|
| Trustworthy for |  |
| Not trustworthy for |  |
| Current assurance route |  |
| Current trust state |  |
| Current evidence tier |  |
| Prohibited claims |  |
`
  );

  await writeText(
    path.join(printoutDir, "governance_spreadsheet_index_printout.md"),
    `
# CRAMPS Spreadsheet Index Printout

## Master Workbook

- \`spreadsheets/CRAMPS_Governance_Master.xlsx\`

## Domain Workbooks

${mdTable(["Preflight", "Full System", "Workbook"], domains.map((d) => [d.light, d.full, `spreadsheets/domains/${d.light}_${d.full}_Workbook.xlsx`]))}
`
  );

  for (const d of domains) {
    await writeText(
      path.join(root, "domain_packs", d.slug, `${d.full}_DOMAIN_GOVERNANCE_PRINTABLE.md`),
      `
# ${d.light} / ${d.full} Domain Governance Printable

**Domain:** ${d.label}

## Assurance Split

- \`${d.light}\`: one to two day preflight.
- \`${d.full}\`: full assurance system after protocol lock.

## Coordinates

${d.coordinates.map((x) => `- ${x}`).join("\n")}

## Nulls and Non-Events

${d.nulls.map((x) => `- ${x}`).join("\n")}

## Gotchas

${d.gotchas.map((x) => `- ${x}`).join("\n")}

## Standards Anchors

${d.standards.map((x) => `- ${x}`).join("\n")}

## Field Gate

| Gate | Pass/Hold/Fail | Notes |
|---|---|---|
| Coordinate specified |  |  |
| Nulls found |  |  |
| Dependence mapped |  |  |
| Bias reviewed |  |  |
| Units checked |  |  |
| Sidecar run |  |  |
| Escalation decision made |  |  |
`
    );
  }
}

async function main() {
  await buildPrintouts();
  await exportWorkbook(governanceWorkbook(), path.join(root, "spreadsheets", "CRAMPS_Governance_Master.xlsx"));
  for (const domain of domains) {
    await exportWorkbook(domainWorkbook(domain), path.join(root, "spreadsheets", "domains", `${domain.light}_${domain.full}_Workbook.xlsx`));
  }
}

await main();
