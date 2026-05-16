import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");

const domains = [
  {
    slug: "med",
    full: "CRAMPACS-MED",
    light: "crampacs-med",
    label: "Medicine and clinical evidence",
    coordinates: ["dose", "exposure window", "biomarker threshold", "adverse-event onset", "phenotype", "care setting"],
    nulls: ["negative safety analyses", "monitored adverse events not elevated", "failed replications", "cohorts with exposure but no event"],
    gotchas: ["confounding by indication", "differential coding", "missing nulls", "surveillance bias"],
    standards: ["PRISMA", "STROBE/RECORD/CONSORT/STARD", "FDA RWE", "ICH GCP", "HIPAA", "21 CFR Part 11"],
  },
  {
    slug: "gen",
    full: "CRAMPACS-GEN",
    light: "crampacs-gen",
    label: "Genomics and omics",
    coordinates: ["locus", "variant", "gene", "pathway", "cell type", "expression threshold"],
    nulls: ["failed replications", "non-significant loci", "negative functional assays", "tested pathways not enriched"],
    gotchas: ["population stratification", "batch effects", "genome-build drift", "winner's curse"],
    standards: ["GA4GH", "ClinGen", "MIAME/MINSEQE", "STREGA", "FAIR"],
  },
  {
    slug: "clim",
    full: "CRAMPACS-CLIM",
    light: "crampacs-clim",
    label: "Climate and Earth systems",
    coordinates: ["latitude", "longitude", "depth", "pressure level", "season", "climate mode"],
    nulls: ["comparable regions without anomaly", "model runs without recurrence", "negative attribution studies"],
    gotchas: ["spatial autocorrelation", "temporal autocorrelation", "non-stationary baseline", "model-family dependence"],
    standards: ["WMO", "CF Conventions", "CMIP/ESGF", "IPCC uncertainty", "FAIR"],
  },
  {
    slug: "mat",
    full: "CRAMPACS-MAT",
    light: "crampacs-mat",
    label: "Materials science",
    coordinates: ["composition ratio", "dopant level", "phase", "lattice parameter", "processing temperature", "operating condition"],
    nulls: ["failed syntheses", "tested materials without property jump", "simulations with no predicted anomaly"],
    gotchas: ["unreported failed syntheses", "hidden processing parameters", "batch variation", "simulation convergence artifacts"],
    standards: ["OPTIMADE", "NOMAD/FAIR-DI", "Materials Project provenance", "PIF/GEMD", "ISO 17025"],
  },
  {
    slug: "eng",
    full: "CRAMPACS-ENG",
    light: "crampacs-eng",
    label: "Engineering reliability",
    coordinates: ["load", "vibration frequency", "temperature", "firmware version", "supplier lot", "cycle count"],
    nulls: ["units exposed without failure", "passed qualification tests", "lots with no anomaly", "sensor streams without recurrence"],
    gotchas: ["fleet exposure imbalance", "maintenance censoring", "supplier-lot dependence", "sensor drift"],
    standards: ["NIST Engineering Statistics", "ISO 9001", "ISO 31000", "ISO 17025", "IEC 61508", "ASME V&V"],
  },
  {
    slug: "fin",
    full: "CRAMPACS-FIN",
    light: "crampacs-fin",
    label: "Finance, fraud, and risk",
    coordinates: ["asset", "tenor", "counterparty", "time window", "transaction velocity", "network position"],
    nulls: ["cleared alerts", "comparable accounts without event", "backtests with no breach", "control portfolios"],
    gotchas: ["look-ahead bias", "backtest overfitting", "vendor revisions", "feedback loops from prior controls"],
    standards: ["SR 11-7/OCC 2011-12", "BCBS 239", "FFIEC", "SEC Regulation SCI", "GLBA/FCRA/ECOA/BSA"],
  },
  {
    slug: "cyb",
    full: "CRAMPACS-CYB",
    light: "crampacs-cyb",
    label: "Cybersecurity",
    coordinates: ["CVE", "ATT&CK technique", "port", "protocol", "endpoint class", "time-to-exploit"],
    nulls: ["exposed assets not exploited", "rules with no hits", "scanned vulnerabilities not exploited", "false positives"],
    gotchas: ["sensor coverage gaps", "duplicate intel feeds", "alert suppression", "honeypot selection bias"],
    standards: ["NIST CSF 2.0", "MITRE ATT&CK", "CISA KEV", "CVSS v4", "ISO 27001", "STIX/TAXII"],
  },
  {
    slug: "ast",
    full: "CRAMPACS-AST",
    light: "crampacs-ast",
    label: "Astronomy and astrophysics",
    coordinates: ["sky coordinate", "redshift", "wavelength", "period", "phase", "cadence"],
    nulls: ["follow-up non-detections", "survey fields with no event", "searched spectral windows with no feature"],
    gotchas: ["sky coverage bias", "cadence bias", "follow-up selection bias", "calibration drift"],
    standards: ["FITS", "IVOA", "VOEvent", "NASA ADS", "FAIR/DataCite"],
  },
  {
    slug: "phy",
    full: "CRAMPACS-PHY",
    light: "crampacs-phy",
    label: "Physics and physical anomaly catalogs",
    coordinates: ["mass", "energy", "frequency", "redshift", "coupling", "cross section"],
    nulls: ["null searches", "exclusion contours", "control regions", "sidebands", "failed replications"],
    gotchas: ["look-elsewhere effect", "theory-fashion clustering", "shared detector pipelines", "plot digitization error"],
    standards: ["PRISMA", "PDG statistics", "HEP look-elsewhere practice", "JCGM GUM", "FAIR/DataCite/PROV"],
  },
];

const layers = [
  ["0", "Concept", "Vocabulary, claim boundary, uppercase/lowercase distinction", "README, naming policy"],
  ["1", "Lightweight preflight", "1-2 day triage and seed artifacts", "preflight policy and templates"],
  ["2", "Gotchas", "Fast failure-mode checks", "gotcha guide and printouts"],
  ["3", "Standards", "Governance, quality gates, document control", "standards policy"],
  ["4", "Methodology", "Coordinate ontology, nulls, dependence, bias, claim tiers", "methodology policy"],
  ["5", "Domain overlay", "Field-specific adaptation", "domain overlays and packs"],
  ["6", "Data contracts", "Structured tables and stable IDs", "templates"],
  ["7", "Checksums", "Cross-unit reproducibility and unit integrity", "checksum policy"],
  ["8", "Sidecar metrics", "Package readiness and blockers", "sidecar runner"],
  ["9", "Full SOP", "End-to-end study execution", "program SOP and protocol template"],
  ["10", "Regulatory", "Pair with domain controls", "domain addenda"],
  ["11", "Platform", "Software workflow modules", "future product layer"],
];

const gates = [
  ["Protocol", "Study charter, role assignment, protocol, candidate registry", "Before extraction"],
  ["Extraction", "Source flow, exclusions, row provenance, extraction confidence", "Before normalization"],
  ["Normalization", "Raw values preserved, transforms registered, uncertainty assigned", "Before analysis"],
  ["Independence and bias", "Independence grades, bias review, missing evidence, weights", "Before scoring"],
  ["Statistical", "Primary statistic, null model, global correction, sensitivities", "Before reporting"],
  ["Release", "Repro capsule, red team, signoff, claim language", "Before external use"],
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
    ["CRAMPACS Governance Master", ""],
    ["Purpose", "Coordinate-resolved weak-signal recurrence governance"],
    ["Uppercase", "CRAMPACS-* = full assurance system"],
    ["Lowercase", "crampacs-* = 1-2 day preflight"],
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
    ["source_id", "citation_or_label", "url_or_path", "source_type", "source_role", "unit_or_site", "known_dependence", "screening_status", "notes"],
    ["", "", "", "", "positive_or_anomaly", "", "", "", ""],
    ["", "", "", "", "null_or_non_event", "", "", "", ""],
  ]);
  addSheet(wb, "Preflight Rows", [
    ["row_id", "source_id", "coordinate_label", "coordinate_value", "coordinate_units", "row_type", "result_direction", "uncertainty_status", "dependence_concern", "bias_concern", "null_or_non_event_flag", "notes"],
    ["", "", "", "", "", "", "", "", "", "", "", ""],
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
  addSheet(wb, "Import Log", [
    ["full_study_id", "preflight_id", "artifact_path", "artifact_sha256", "imported_as", "reviewer_id", "review_disposition", "decision_timestamp", "notes"],
    ["", "", "", "", "", "", "", "", ""],
  ]);
  return wb;
}

async function buildPrintouts() {
  const printoutDir = path.join(root, "printouts");
  await writeText(
    path.join(printoutDir, "governance_master_printout.md"),
    `
# CRAMPACS Governance Master Printout

## System Rule

- Uppercase \`CRAMPACS-*\` is the full assurance system.
- Lowercase \`crampacs-*\` is the one to two day preflight.
- A preflight can seed the full system, but only the full system can carry full assurance after protocol lock.

## Documentation Layers

${mdTable(["Layer", "Name", "Purpose", "Documents"], layers)}

## Quality Gates

${mdTable(["Gate", "Required evidence", "When checked"], gates)}
`
  );

  await writeText(
    path.join(printoutDir, "domain_matrix_printout.md"),
    `
# CRAMPACS Domain Matrix Printout

${mdTable(
  ["Preflight", "Full System", "Domain", "Coordinates", "Nulls", "Primary Gotchas"],
  domains.map((d) => [d.light, d.full, d.label, d.coordinates.join("; "), d.nulls.join("; "), d.gotchas.join("; ")])
)}
`
  );

  await writeText(
    path.join(printoutDir, "governance_gotchas_printout.md"),
    `
# CRAMPACS Governance Gotchas Printout

${mdTable(["Gotcha", "Symptom", "Fast sanity check"], gotchas)}
`
  );

  await writeText(
    path.join(printoutDir, "governance_spreadsheet_index_printout.md"),
    `
# CRAMPACS Spreadsheet Index Printout

## Master Workbook

- \`spreadsheets/CRAMPACS_Governance_Master.xlsx\`

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
  await exportWorkbook(governanceWorkbook(), path.join(root, "spreadsheets", "CRAMPACS_Governance_Master.xlsx"));
  for (const domain of domains) {
    await exportWorkbook(domainWorkbook(domain), path.join(root, "spreadsheets", "domains", `${domain.light}_${domain.full}_Workbook.xlsx`));
  }
}

await main();
