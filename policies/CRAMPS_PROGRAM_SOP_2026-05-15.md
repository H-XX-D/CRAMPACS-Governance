# CRAMPS Program Outline and End-to-End SOP

**CRAMPS:** Coordinate-Resolved Anomaly Meta-analysis with Pre-specified Statistics  
**Version:** 0.1  
**Generated:** 2026-05-15 PDT  
**Status:** Draft program standard for method development, pilot execution, and external review

## 1. Definition

CRAMPS is a coordinate-resolved assurance framework for inspecting whether weak observations from heterogeneous evidence sources recur at pre-specified parameter values more often than expected under controlled null models.

The method does not treat weak observations as discoveries. It treats recurrence at the same coordinate as an inspectable statistical object with explicit source, null, dependence, bias, and claim controls. The result of a CRAMPS study is a bounded prioritization and escalation assessment, not a domain conclusion by itself.

The core evidentiary question is:

> Given a pre-specified coordinate atlas, inclusion contract, independence model, and null model, do reported anomalies, residuals, weak excesses, near-misses, and non-events recur around candidate coordinates more often than expected?

## 2. Scientific Position

CRAMPS fills the evidentiary layer between informal pattern suspicion and domain-standard confirmation. It is designed to answer whether weak or sub-threshold observations show structured recurrence across sources, while preserving the confirmation standards of the underlying fields.

CRAMPS may support statements such as:

- "A pre-specified candidate coordinate has unusual cross-source recurrence under the registered null model."
- "The recurrence is robust to leave-family-out and leave-era-out sensitivity tests."
- "The finding should be prioritized for targeted replication or prospective search."

CRAMPS may not support statements such as:

- "This proves a new particle, field, or mechanism."
- "Many weak signals can be combined without strict independence and trial correction."
- "A visually interesting post-hoc pattern is statistically significant."

## 3. Standards Basis

CRAMPS should be built as a domain-general weak-evidence inspection standard. It borrows discipline from systematic review, statistical reporting, metrology, repository governance, and AI risk management, but adapts each to coordinate-resolved recurrence packages.

Primary standards and guidance anchors:

- PRISMA 2020 for transparent reporting of systematic reviews and meta-analyses: https://www.prisma-statement.org/prisma-2020
- PRISMA-P 2015 for protocol reporting before review completion: https://www.prisma-statement.org/protocols
- Cochrane Handbook, especially analysis, heterogeneity, and missing-evidence bias guidance: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-10 and https://www.cochrane.org/node/105
- CMS explanation of the look-elsewhere effect for bump searches: https://cms.cern/physics/cms-higgs-search/look-elsewhere-effect
- PDG statistical practice in high-energy physics, including nuisance parameters and look-elsewhere effects: https://pdg.lbl.gov
- SAMPL statistical reporting guidelines via EQUATOR: https://www.equator-network.org/reporting-guidelines/sampl/
- ASA guidance on p-values and ethical statistical practice: https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf and https://www.amstat.org/docs/default-source/amstat-documents/ethicalguidelines.pdf
- JCGM GUM for uncertainty expression where measurement uncertainty must be propagated: https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf
- FAIR data principles for findable, accessible, interoperable, reusable research objects: https://www.go-fair.org/fair-principles
- W3C PROV for provenance modeling: https://www.w3.org/ns/prov
- DataCite metadata schema for dataset citation and retrieval: https://schema.datacite.org/
- ISO 9001 for quality management system structure: https://www.iso.org/standard/62085.html
- ISO/IEC 17025 for competence requirements in testing and calibration laboratories: https://www.iso.org/standard/66912.html
- ISO/IEC 27001 for information security management when handling restricted data: https://www.iso.org/standard/27001
- CoreTrustSeal for trustworthy data repository practices: https://www.coretrustseal.org/why-certification/requirements/
- NIST AI Risk Management Framework for agentic tooling governance: https://www.nist.gov/itl/ai-risk-management-framework
- CRediT contributor roles for transparent attribution: https://credit.niso.org/

These are not copied wholesale. CRAMPS uses them as alignment targets.

## 4. Program Philosophy

1. **Pre-specification is the center of the method.** Candidate coordinates, coordinate transforms, inclusion rules, tolerance windows, weighting rules, independence rules, null models, and primary statistics are fixed before scoring.

2. **Exploration and confirmation are different products.** An exploratory atlas may identify candidate coordinates. A confirmatory CRAMPS run may only test coordinates locked before scoring.

3. **Nulls are data.** Non-events, exclusions, upper limits, searches with no excess, and negative control coordinates must be included when they satisfy the source contract.

4. **Independence is graded, not assumed.** Multiple rows from the same detector, collaboration, public dataset, calibration pipeline, simulation stack, or theory-derived search band may share evidence. CRAMPS must model this dependence.

5. **The null model must imitate the literature, not an idealized universe.** Publication bias, preferred scan ranges, detector thresholds, historical fashion, known backgrounds, and bounded search spaces can all create apparent recurrence.

6. **The result is a ranking, not a verdict.** CRAMPS can identify coordinates worth attention. It cannot replace direct replication, targeted searches, or field-specific discovery thresholds.

7. **Adversarial review is part of the method.** Each result must survive attempts to explain it by duplicate data, calibration inheritance, scan-range artifacts, theoretical popularity, rounding, and selective reporting.

## 5. Scope

### 5.1 Included Evidence Types

CRAMPS can include:

- Published anomaly claims, residuals, weak excesses, deficit features, near-threshold bumps, calibration-adjacent oddities, and unresolved tensions.
- Null searches and exclusion limits where a relevant coordinate range was examined.
- Re-analyses, public-data recasts, and collaboration notes if provenance and method metadata are adequate.
- Heterogeneous modalities, including collider, direct detection, indirect detection, atomic, astrophysical, cosmological, neutrino, gravitational, spectroscopy, timing, and precision-measurement catalogs.

### 5.2 Excluded Evidence Types

CRAMPS must exclude or quarantine:

- Anecdotal claims with no reproducible coordinate, uncertainty, and source metadata.
- Rows extracted only from plots unless extraction uncertainty is recorded.
- Theory-only predictions with no observational residual or null-search interaction, unless they define a pre-specified candidate coordinate before scoring.
- Rows whose coordinate value was chosen after seeing the CRAMPS target result.
- Duplicates of the same analysis that cannot be separated from the original evidence source.

### 5.3 Confirmatory Boundary

A confirmatory CRAMPS result requires:

- A locked protocol.
- A frozen candidate coordinate registry.
- A frozen source search strategy or documented source snapshot.
- A locked primary recurrence statistic.
- A locked null-model generator.
- A complete accounting of null and non-event evidence.
- A reproducibility capsule that re-runs the analysis from raw extracted tables.

## 6. Program Architecture

CRAMPS has three layers.

### 6.1 Foundation Layer

The foundation layer defines the coordinate ontology and statistical contract.

Artifacts:

- `coordinate_ontology.md`
- `candidate_coordinate_registry.csv`
- `coordinate_transform_registry.csv`
- `statistical_analysis_plan.md`
- `null_model_specification.md`
- `independence_policy.md`
- `bias_assessment_policy.md`

### 6.2 Runtime Layer

The runtime layer handles repeatable execution.

Artifacts:

- Source search scripts and logs.
- Extraction forms.
- Normalization code.
- Validation tests.
- Null-simulation code.
- Analysis notebooks or scripts.
- Frozen dependency manifest.
- Reproducibility report.

### 6.3 Adapter Layer

The adapter layer maps domain-specific catalogs into the common CRAMPS contract.

Examples:

- `adapter_direct_detection.md`
- `adapter_colliders.md`
- `adapter_cosmology.md`
- `adapter_neutrino.md`
- `adapter_precision_measurement.md`
- `adapter_astrophysical_spectra.md`

Each adapter defines domain-specific source classes, coordinate units, uncertainty conventions, typical dependence structures, required metadata, and standard negative controls.

## 7. Governance and Roles

Every CRAMPS study must assign named owners. A single person may hold multiple roles in a pilot, but role separation is required before external release.

| Role | Responsibility | Required independence |
|---|---|---|
| Program owner | Owns scope, schedule, final release decision | Cannot override statistical veto |
| Protocol steward | Maintains protocol, amendments, blind lock | Cannot score results before lock |
| Domain lead | Defines domain adapters and source adequacy | Must disclose theoretical commitments |
| Search lead | Runs source search and maintains PRISMA-style flow | Separate from final statistic signoff |
| Extraction lead | Maintains extraction forms and duplicate screening | Requires second reviewer sampling |
| Coordinate lead | Defines units, transforms, tolerances, uncertainty propagation | Cannot add post-hoc coordinates |
| Independence auditor | Assigns dependence groups and covariance assumptions | Independent from source extraction where possible |
| Bias auditor | Assesses missing evidence, publication bias, detector-fashion bias | Can veto pooling |
| Null model architect | Specifies and validates null generator | Cannot tune null after seeing result |
| Statistical lead | Owns primary statistic, sensitivity tests, uncertainty | Must approve all inference language |
| Reproducibility lead | Runs clean environment reproduction | Must start from published capsule |
| Red-team reviewer | Attempts to break the claim | Must be empowered to block promotion |
| Data steward | Owns data contracts, licensing, retention, repository metadata | Must approve public release |
| AI/agent steward | Governs agent use, audit logs, model versions, human review | Required if LLM agents are used |

## 8. Agent System

CRAMPS agents may be human, software, or AI-assisted workers. Agents do not decide scientific truth. They perform bounded tasks under a documented contract.

### 8.1 General Agent Contract

Every agent must have:

- A written purpose.
- Allowed inputs.
- Prohibited inputs.
- Output schema.
- Required citations or provenance.
- Confidence and uncertainty fields.
- Human review threshold.
- Version identifier.
- Audit log.
- Deployment-plan row.
- Handoff checklist row for every material artifact transfer.

No agent may:

- Add candidate coordinates after result inspection.
- Change inclusion criteria after scoring without amendment.
- Treat duplicate analyses as independent rows.
- Convert ambiguous narrative claims into quantitative anomalies without reviewer confirmation.
- Produce final statistical language without statistical lead approval.

### 8.2 Required Agents

| Agent | Purpose | Output |
|---|---|---|
| Protocol agent | Converts study intent into a PRISMA-P-like protocol draft | `protocol.md`, amendment plan |
| Source search agent | Runs source search against registered strategy | `source_search_log.csv`, flow counts |
| Deduplication agent | Identifies repeated datasets, analyses, and derived papers | `dedupe_map.csv` |
| Extraction agent | Extracts row-level coordinate, uncertainty, residual, and source metadata | `anomaly_rows_raw.csv` |
| Coordinate normalization agent | Converts raw coordinates into registered coordinate systems | `normalized_rows.csv` |
| Independence agent | Assigns dependence groups and evidence-family links | `independence_groups.csv` |
| Bias agent | Scores missing-evidence and reporting-bias risks | `bias_assessment.csv` |
| Null simulation agent | Runs registered null models | `null_model_runs.csv` |
| Sensitivity agent | Runs leave-one-family-out, leave-era-out, and tolerance sweeps | `sensitivity_results.csv` |
| Reproducibility agent | Rebuilds results from clean checkout and frozen data | `reproducibility_report.md` |
| Reporting agent | Drafts PRISMA-style report without claim inflation | `report_draft.md` |
| Red-team agent | Searches for dependence, leakage, LEE, and null-model failures | `red_team_findings.md` |

### 8.3 AI Agent Controls

If AI agents are used, the AI/agent steward must maintain:

- `agent_deployment_plan.csv`.
- `agent_handoff_checklist.csv`.
- Model name and version.
- Prompt version.
- Temperature or decoding settings where available.
- Tool access.
- Source access.
- Output hashes.
- Human adjudication status.
- Error samples.
- Hallucination checks.
- NIST AI RMF mapping across Govern, Map, Measure, and Manage.

AI outputs are never authoritative source data. They are extraction proposals until human-reviewed or mechanically verified.

## 9. End-to-End SOP

### Stage 0: Program Initialization

Objective:

Create the minimum governance and technical foundation before any study starts.

Procedure:

1. Assign roles from Section 7.
2. Create a study identifier using `CRAMPS_<domain>_<YYYY-MM-DD>`.
3. Create the study workspace.
4. Create immutable folders for raw sources, extraction forms, normalized data, analysis code, reports, logs, and review packets.
5. Record software environment, repository hash if available, and data retention policy.
6. Define whether the study is exploratory, confirmatory, or prospective.

Required outputs:

- `study_charter.md`
- `role_assignment.csv`
- `repository_manifest.md`
- `data_management_plan.md`
- `agent_registry.csv`

Gate 0 acceptance:

- Scope is documented.
- Roles are assigned.
- No scoring has occurred.
- The distinction between exploratory and confirmatory work is explicit.

### Stage 1: Research Question and Coordinate Ontology

Objective:

Define the coordinate space before looking for recurrence.

Procedure:

1. State the primary question in coordinate form.
2. Define coordinate families, such as mass, energy, frequency, redshift, coupling scale, time scale, length scale, or derived dimensionless coordinate.
3. Define allowed coordinate transforms.
4. Define the unit system and canonical unit for each coordinate.
5. Define tolerance windows and why they are physically or instrumentally justified.
6. Define negative control coordinates.
7. Define forbidden transforms that would create too much freedom.

Required outputs:

- `coordinate_ontology.md`
- `coordinate_transform_registry.csv`
- `candidate_coordinate_registry.csv`
- `negative_control_registry.csv`

Gate 1 acceptance:

- Candidate coordinates are fixed or the study is labeled exploratory.
- Tolerances are fixed before scoring.
- The effective number of candidate coordinates is documented.
- Each derived coordinate has a formula and uncertainty propagation rule.

### Stage 2: Protocol and Blind Lock

Objective:

Register the study before extraction and scoring create bias.

Procedure:

1. Draft a protocol using PRISMA-P structure adapted to CRAMPS.
2. Include rationale, objectives, eligibility criteria, information sources, search strategy, extraction fields, bias assessment, statistical analysis plan, and amendment procedure.
3. Include the candidate coordinate registry and null-model specification as protocol appendices.
4. Freeze the protocol in a timestamped location.
5. If public registration is appropriate, register on OSF or submit as a Registered Report Stage 1.
6. If embargo is necessary, store a read-only timestamped package with hash and witness.

Required outputs:

- `CRAMPS_PROTOCOL_LOCK_<YYYY-MM-DD>.md`
- `protocol_hash.txt`
- `amendment_log.csv`
- Optional external registration URL.

Gate 2 acceptance:

- The protocol hash is recorded.
- The analysis plan is complete enough to run without interpretation.
- Any later deviation requires an amendment record.

### Stage 3: Source Search and Catalog Assembly

Objective:

Build the source universe without selecting only interesting rows.

Procedure:

1. Execute registered database and archive searches.
2. Search collaboration result pages, arXiv, journal databases, public data releases, conference notes where allowed, and existing review bibliographies.
3. Record search strings, dates, sources, and result counts.
4. Deduplicate papers and identify related analyses.
5. Create PRISMA-style flow counts: identified, screened, eligible, included, excluded with reason.
6. Preserve null searches and non-events.

Required outputs:

- `source_search_log.csv`
- `source_catalog.csv`
- `screening_decisions.csv`
- `exclusion_reasons.csv`
- `source_flow_diagram.md`

Gate 3 acceptance:

- Search strategy can be repeated.
- Exclusions have reasons.
- Null and non-event sources are represented.
- Duplicates are mapped, not silently removed.

### Stage 4: Screening

Objective:

Apply inclusion and exclusion criteria consistently.

Procedure:

1. Two reviewers independently screen source titles, abstracts, and full texts when feasible.
2. Resolve disagreements by adjudication.
3. Record source eligibility independent of whether the reported result is interesting.
4. Assign source class, publication status, data-access status, and domain adapter.
5. Identify source-level dependencies, such as same detector, same dataset, same collaboration, same public data, same simulation model, or same calibration.

Required outputs:

- `screening_decisions.csv`
- `screening_disagreements.csv`
- `source_dependency_map.csv`

Gate 4 acceptance:

- Screening agreement is reported.
- Disagreements are resolved.
- Inclusion does not depend on result direction or perceived support.

### Stage 5: Row Extraction

Objective:

Extract analyzable rows with provenance and uncertainty.

Procedure:

1. Extract each anomaly, null result, exclusion, residual, or near-miss as a row.
2. Record raw coordinate, units, uncertainty, result type, residual statistic, local significance if available, sample size or exposure where relevant, and coordinate range searched.
3. Record whether values are machine-readable, table-extracted, text-extracted, plot-digitized, or inferred.
4. Record all assumptions used to convert source language into structured fields.
5. Assign extraction confidence and review status.
6. For plot digitization, record digitization tool, image source, calibration points, and extraction uncertainty.

Required outputs:

- `anomaly_rows_raw.csv`
- `extraction_notes.md`
- `plot_digitization_log.csv` if applicable
- `row_review_status.csv`

Gate 5 acceptance:

- Every row has source provenance.
- Every coordinate has units.
- Every quantitative conversion is documented.
- Ambiguous rows are quarantined or flagged.

### Stage 6: Coordinate Normalization

Objective:

Map source coordinates into the registered coordinate system.

Procedure:

1. Apply only registered transforms.
2. Convert units to canonical units.
3. Propagate uncertainty through transforms.
4. Preserve raw values and normalized values.
5. Record transform version.
6. Reject rows whose coordinate cannot be normalized without unregistered assumptions.

Required outputs:

- `normalized_rows.csv`
- `transform_audit_log.csv`
- `normalization_exclusions.csv`

Gate 6 acceptance:

- Normalized coordinates are reproducible from raw signal rows.
- Transform uncertainty is propagated.
- No post-hoc transform has been introduced.

### Stage 7: Independence and Bias Assessment

Objective:

Prevent false evidence multiplication.

Procedure:

1. Assign each row to one or more dependence groups.
2. Record shared detector, collaboration, dataset, calibration, simulation, reconstruction pipeline, theory search band, and public-data lineage.
3. Assign independence grade:
   - A: independent instrument, team, data, calibration, and analysis logic.
   - B: independent data but partially shared theory or calibration.
   - C: same facility or collaboration but distinct data/analysis channel.
   - D: same dataset or pipeline, derivative evidence only.
   - E: duplicate or non-independent, not eligible as separate evidence.
4. Assess source-level bias.
5. Assess missing-evidence risk, including unpublished nulls, non-reporting bias, and selective threshold reporting.
6. Define covariance, collapse, or recurrence weights used in analysis.

Required outputs:

- `independence_groups.csv`
- `bias_assessment.csv`
- `missing_evidence_assessment.md`
- `analysis_weight_table.csv`

Gate 7 acceptance:

- No row enters primary analysis without independence grade.
- Dependence assumptions are visible.
- Bias and missing evidence are included in interpretation.

### Stage 8: Statistical Analysis

Objective:

Compute the pre-specified recurrence statistic under calibrated null models.

Procedure:

1. Load only locked candidate coordinates.
2. Load normalized rows and analysis weights.
3. Compute the primary statistic exactly as specified.
4. Compute secondary statistics only if pre-specified or clearly labeled exploratory.
5. Run null models with recorded random seeds and simulation counts.
6. Compute local and global measures, including look-elsewhere correction across all registered coordinates and coordinate families.
7. Report uncertainty, Monte Carlo error, and sensitivity to null assumptions.

Acceptable primary statistics include:

- Weighted count of independent signal, residual, anomaly-like, null, or near-miss rows within a registered tolerance window.
- Signed or unsigned residual aggregation with dependence-adjusted covariance.
- Coordinate density excess relative to domain-specific search support.
- Hierarchical model estimating recurrence intensity above the background literature or operational process.
- Bayesian posterior predictive tail area or Bayes factor with registered priors.

Null-model tiers:

- Tier A: row-wise coordinate permutation respecting each experiment's searched range.
- Tier B: literature-process null preserving publication era, modality, scan range, and reporting threshold.
- Tier C: instrument-process null preserving detector resolution, thresholds, and known background structures.
- Tier D: generative posterior predictive null using domain-specific background and selection models.

Required outputs:

- `primary_results.csv`
- `null_model_runs.csv`
- `global_significance_report.md`
- `statistical_analysis_log.md`

Gate 8 acceptance:

- Primary result is computed without changing the locked plan.
- Global correction accounts for the registered search space.
- Null model is validated by negative controls.
- Monte Carlo uncertainty is reported.

### Stage 9: Sensitivity, Negative Controls, and Falsification Pressure

Objective:

Test whether the recurrence is robust or an artifact.

Required sensitivity tests:

- Leave-one-source-out.
- Leave-one-experiment-out.
- Leave-one-collaboration-out.
- Leave-one-modality-out.
- Leave-one-era-out.
- Exclude plot-digitized rows.
- Exclude low-independence rows.
- Exclude high-bias rows.
- Vary tolerance windows within pre-specified bounds.
- Re-run under stricter null models.
- Re-run with non-events weighted more aggressively.
- Test negative control coordinates.
- Test mirrored or shifted coordinates where physically meaningful.

Required outputs:

- `sensitivity_results.csv`
- `negative_control_results.csv`
- `falsification_pressure.md`

Gate 9 acceptance:

- The primary result is not driven by one famous source, one era, one detector, one theory paper, or one extraction convention.
- Negative controls behave as expected.
- Failures are reported, not hidden.

### Stage 10: Reporting

Objective:

Produce a transparent report that allows a skeptical reader to reproduce, criticize, and reinterpret the result.

Required report sections:

1. Title identifying the study as CRAMPS and whether it is exploratory, confirmatory, or prospective.
2. Abstract with objective, data sources, eligibility, candidate coordinates, primary statistic, null model, result, and limitations.
3. Rationale and scope.
4. Protocol registration and amendments.
5. Source search and PRISMA-style flow.
6. Inclusion and exclusion criteria.
7. Data extraction and coordinate normalization.
8. Independence and bias assessment.
9. Statistical analysis plan.
10. Null model validation.
11. Primary result.
12. Sensitivity and negative controls.
13. Missing evidence and publication bias.
14. Limitations.
15. Interpretation using evidence tiers.
16. Data, code, and reproducibility statement.
17. Conflicts of interest and funding.
18. CRediT contribution statement.

Required figures and tables:

- Source flow diagram.
- Candidate coordinate registry.
- Coordinate atlas with nulls and anomalies.
- Dependence network.
- Bias heatmap.
- Null distribution with observed statistic.
- Sensitivity tornado plot or table.
- Evidence tier table.

Gate 10 acceptance:

- The report does not imply discovery.
- Exploratory findings are labeled exploratory.
- Local and global statistics are separated.
- Missing-evidence risk is discussed.
- Data and code availability are explicit.

### Stage 11: Reproducibility Capsule

Objective:

Package the study so another team can re-run it.

Required package:

- Frozen raw extraction tables.
- Normalized tables.
- Candidate registry.
- Null model specification.
- Analysis code.
- Dependency lockfile or container.
- Run script.
- Expected checksums.
- Reproducibility report.
- License and data-use notices.
- DataCite-ready metadata.

Gate 11 acceptance:

- A clean environment reproduces the primary statistic.
- Checksums match.
- Differences are documented.
- External reviewer can run without private context unless restricted data are explicitly declared.

### Stage 12: External Review and Promotion

Objective:

Subject the result to adversarial review before public claims.

Procedure:

1. Send the protocol, data package, and report to external statistical and domain reviewers.
2. Require reviewers to inspect independence, null model realism, candidate pre-specification, and missing evidence.
3. Record reviewer criticisms and responses.
4. Promote only if the result survives pre-defined quality gates.
5. If the result fails, publish or archive the negative result with failure reason.

Evidence tiers:

- Tier 0: Exploratory atlas signal. Useful for hypothesis generation only.
- Tier 1: Locked retrospective CRAMPS signal. Candidate and scoring were pre-specified before scoring existing data.
- Tier 2: Independently reproduced CRAMPS signal. Another team re-ran the same package and obtained equivalent results.
- Tier 3: Prospective holdout confirmation. Future or held-out catalogs show the registered coordinate recurrence.
- Tier 4: Targeted experimental confirmation. A direct experiment tests the coordinate and observes a compatible effect under field standards.

Gate 12 acceptance:

- Promotion tier is justified.
- Reviewer objections are documented.
- Public language matches the tier.

## 10. Statistical Rules

### 10.1 Candidate Coordinate Rules

Each candidate coordinate must have:

- Unique ID.
- Coordinate family.
- Canonical value.
- Units.
- Tolerance window.
- Physical or methodological rationale.
- Source of pre-specification.
- Lock timestamp.
- Status: active, exploratory-only, retired, or negative control.

Coordinates generated from exploratory atlas work must be locked into a new protocol before confirmatory scoring.

### 10.2 Look-Elsewhere and Multiple Testing Rules

CRAMPS must report:

- Number of candidate coordinates.
- Number of coordinate families.
- Number of tolerance windows if multiple were tested.
- Whether the statistic scans within a coordinate range.
- Local result at each candidate.
- Global result across the full registered coordinate space.
- Sensitivity to effective-trials assumptions.

No CRAMPS report may quote a local p-value, sigma-equivalent, or posterior odds as the headline result unless the global correction is presented next to it.

### 10.3 Independence Rules

Rows are not independent merely because they appear in different papers. Dependence can arise from:

- Same detector.
- Same collaboration.
- Same raw data.
- Same public release.
- Same calibration.
- Same reconstruction pipeline.
- Same simulation background.
- Same theory-motivated scan value.
- Same review article copied across sources.
- Same plot digitized by multiple secondary authors.

Primary analysis must either collapse dependent rows, model covariance, or use conservative recurrence weights.

### 10.4 Missing-Evidence Rules

The analysis must account for sources that could have reported relevant coordinates but did not. At minimum, the missing-evidence assessment must ask:

- Were null searches in the same coordinate range identified?
- Are non-significant results less likely to be published or indexed?
- Are only prominent anomaly papers easy to find?
- Are scan ranges historically concentrated around popular coordinates?
- Are unpublished conference results likely to matter?
- Did collaborations publish exclusion contours but not residual tables?

If missing evidence risk is high, the report must demote the evidence tier or state that the result is not confirmatory.

### 10.5 Uncertainty Rules

All coordinate values require uncertainty status:

- Direct reported uncertainty.
- Derived uncertainty from reported quantities.
- Instrumental resolution proxy.
- Digitization uncertainty.
- Unknown uncertainty.

Unknown uncertainty is not zero. It requires conservative handling or exclusion from primary quantitative analysis.

### 10.6 Reporting Language Rules

Use:

- "coordinate recurrence"
- "cross-catalog recurrence"
- "pre-specified coordinate test"
- "global p-value under the registered null"
- "robustness under sensitivity tests"
- "priority for prospective test"

Avoid:

- "proof"
- "discovery"
- "confirmed new physics"
- "combined weak signals prove"
- "sigma" without calibrated null and global correction
- "independent" without dependence audit

## 11. Data Contracts

All data contracts are versioned. Field names use snake_case. Raw source fields are never overwritten by normalized fields.

### 11.1 `source_catalog.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| source_id | string | yes | Stable source identifier |
| citation | string | yes | Human-readable citation |
| doi_or_url | string | yes | DOI, arXiv URL, collaboration URL, or archive URL |
| source_type | enum | yes | journal, preprint, conference_note, collaboration_page, dataset, review, thesis, other |
| domain | enum | yes | collider, direct_detection, indirect_detection, cosmology, neutrino, precision, astrophysics, other |
| publication_date | date | no | Publication or release date |
| data_collection_period | string | no | Dates or runs covered |
| collaboration | string | no | Collaboration or team |
| facility_or_instrument | string | no | Instrument, telescope, detector, survey, or lab |
| dataset_id | string | no | Public dataset or run identifier |
| search_strategy_id | string | yes | Link to source search log |
| screening_status | enum | yes | included, excluded, pending, quarantine |
| exclusion_reason | string | no | Required if excluded |
| license_status | enum | yes | open, restricted, unclear, permission_required |
| provenance_hash | string | no | Hash of source file if locally archived |

### 11.2 `anomaly_rows_raw.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| row_id | string | yes | Stable row ID |
| source_id | string | yes | Link to source catalog |
| result_label | string | yes | Source's name for the anomaly, null, residual, or limit |
| result_type | enum | yes | excess, deficit, residual, tension, null, exclusion, upper_limit, calibration_oddity, other |
| raw_coordinate_value | number | no | Coordinate as reported |
| raw_coordinate_units | string | no | Units as reported |
| raw_coordinate_uncertainty | number | no | Uncertainty as reported |
| coordinate_range_low | number | no | Lower searched range if applicable |
| coordinate_range_high | number | no | Upper searched range if applicable |
| coordinate_range_units | string | no | Units for search range |
| reported_effect | number | no | Effect size, residual, rate, excess count, ratio, or comparable source quantity |
| reported_effect_units | string | no | Units for reported effect |
| reported_statistic | string | no | z, p, chi2, likelihood ratio, Bayes factor, CLs, residual, other |
| reported_statistic_value | number | no | Value of reported statistic |
| reported_local_significance | number | no | Local significance if source provides it |
| reported_global_significance | number | no | Global significance if source provides it |
| exposure_or_luminosity | string | no | Exposure, luminosity, survey area, sample size, or equivalent |
| extraction_method | enum | yes | table, text, machine_readable, plot_digitized, inferred |
| extraction_confidence | enum | yes | high, medium, low, quarantine |
| extractor_id | string | yes | Person or agent extracting row |
| reviewer_id | string | no | Reviewer confirming extraction |
| notes | string | no | Assumptions and caveats |

### 11.3 `normalized_rows.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| row_id | string | yes | Link to raw row |
| canonical_coordinate_family | enum | yes | mass, energy, frequency, redshift, coupling, timescale, lengthscale, dimensionless, other |
| canonical_coordinate_value | number | yes | Normalized coordinate |
| canonical_coordinate_units | string | yes | Canonical units |
| canonical_uncertainty_low | number | no | Lower uncertainty |
| canonical_uncertainty_high | number | no | Upper uncertainty |
| transform_id | string | yes | Link to transform registry |
| transform_version | string | yes | Version of transform |
| uncertainty_method | enum | yes | reported, propagated, resolution_proxy, digitization, unknown |
| normalization_status | enum | yes | primary_eligible, secondary_only, excluded, quarantine |
| normalization_notes | string | no | Notes and assumptions |

### 11.4 `candidate_coordinate_registry.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| candidate_id | string | yes | Stable candidate ID |
| coordinate_family | enum | yes | mass, energy, frequency, redshift, coupling, timescale, lengthscale, dimensionless, other |
| value | number | yes | Pre-specified coordinate |
| units | string | yes | Canonical units |
| tolerance_low | number | yes | Lower tolerance bound |
| tolerance_high | number | yes | Upper tolerance bound |
| tolerance_basis | enum | yes | instrument_resolution, theory_width, literature_standard, fixed_fraction, other |
| rationale | string | yes | Why this coordinate is eligible before scoring |
| source_of_prespecification | string | yes | Protocol, prior paper, blind lock, or external registry |
| lock_timestamp | datetime | yes | Timestamp before scoring |
| status | enum | yes | active, exploratory_only, retired, negative_control |
| multiplicity_group | string | yes | Group used for multiple-testing correction |

### 11.5 `coordinate_transform_registry.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| transform_id | string | yes | Stable transform ID |
| input_family | string | yes | Input coordinate family |
| output_family | string | yes | Output coordinate family |
| formula | string | yes | Machine-readable or plain formula |
| constants_required | string | no | Constants and versions |
| uncertainty_formula | string | yes | Propagation rule |
| validity_domain | string | yes | Conditions where transform is valid |
| forbidden_after_lock | boolean | yes | True for confirmatory studies unless already registered |
| reviewer_id | string | yes | Reviewer approving transform |

### 11.6 `independence_groups.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| row_id | string | yes | Link to normalized row |
| evidence_family_id | string | yes | Shared evidence family |
| detector_group_id | string | no | Detector or instrument group |
| dataset_group_id | string | no | Shared raw data group |
| calibration_group_id | string | no | Shared calibration group |
| theory_group_id | string | no | Shared theory-motivated scan group |
| independence_grade | enum | yes | A, B, C, D, E |
| primary_weight | number | yes | Weight used in primary analysis |
| covariance_group | string | no | Group for covariance model |
| auditor_id | string | yes | Independence auditor |
| notes | string | no | Justification |

### 11.7 `bias_assessment.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| row_id | string | yes | Link to row |
| source_id | string | yes | Link to source |
| publication_bias_risk | enum | yes | low, moderate, high, unclear |
| selective_reporting_risk | enum | yes | low, moderate, high, unclear |
| missing_null_risk | enum | yes | low, moderate, high, unclear |
| analysis_flexibility_risk | enum | yes | low, moderate, high, unclear |
| coordinate_fashion_risk | enum | yes | low, moderate, high, unclear |
| extraction_bias_risk | enum | yes | low, moderate, high, unclear |
| overall_bias_risk | enum | yes | low, moderate, high, unclear |
| assessor_id | string | yes | Bias assessor |
| rationale | string | yes | Short justification |

### 11.8 `null_model_runs.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| null_run_id | string | yes | Stable run ID |
| protocol_hash | string | yes | Protocol hash used |
| null_model_id | string | yes | Registered null model |
| null_tier | enum | yes | A, B, C, D |
| random_seed | integer | yes | Seed |
| simulation_count | integer | yes | Number of simulated datasets |
| statistic_id | string | yes | Primary or secondary statistic |
| observed_statistic | number | yes | Observed value |
| null_mean | number | no | Null mean |
| null_sd | number | no | Null standard deviation |
| local_p_value | number | no | Local p-value if applicable |
| global_p_value | number | no | Global p-value |
| monte_carlo_se | number | no | Monte Carlo standard error |
| run_timestamp | datetime | yes | Run time |
| code_version | string | yes | Code version or hash |

### 11.9 `analysis_result.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| result_id | string | yes | Stable result ID |
| candidate_id | string | yes | Candidate coordinate |
| statistic_id | string | yes | Statistic |
| observed_statistic | number | yes | Observed statistic |
| local_p_value | number | no | Local p-value |
| global_p_value | number | no | Global corrected p-value |
| effect_estimate | number | no | Estimated recurrence effect |
| effect_ci_low | number | no | Lower interval |
| effect_ci_high | number | no | Upper interval |
| evidence_tier | enum | yes | 0, 1, 2, 3, 4 |
| robustness_status | enum | yes | robust, fragile, failed, exploratory |
| interpretation | string | yes | Conservative interpretation |
| approved_by_statistical_lead | boolean | yes | Approval flag |

### 11.10 `amendment_log.csv`

| Field | Type | Required | Description |
|---|---|---|---|
| amendment_id | string | yes | Stable amendment ID |
| timestamp | datetime | yes | Amendment time |
| requested_by | string | yes | Requester |
| amendment_type | enum | yes | administrative, source, extraction, coordinate, statistic, null_model, reporting |
| before | string | yes | Prior text or config |
| after | string | yes | New text or config |
| result_blind | boolean | yes | Whether change occurred before result inspection |
| impact_assessment | string | yes | Expected impact |
| approval | string | yes | Approver and status |

## 12. Accreditation and Quality Requirements

CRAMPS should not claim formal accreditation unless an external accredited body grants it. The correct near-term target is "accreditation-ready" or "standard-aligned."

### 12.1 Minimum Quality System

Required before public release:

- Documented scope.
- Approved SOP.
- Role assignments and competency records.
- Training records for extractors and agents.
- Version-controlled protocols and data contracts.
- Change-control procedure.
- Deviation procedure.
- Internal audit record.
- Management review or program review record.
- Corrective and preventive action log.
- Reproducibility check.

### 12.2 ISO 9001 Alignment

Use ISO 9001 structure for:

- Process mapping.
- Risk-based thinking.
- Document control.
- Corrective action.
- Continual improvement.
- Stakeholder requirements.
- Management review.

### 12.3 ISO/IEC 17025 Alignment

Use ISO/IEC 17025 principles where CRAMPS behaves like a testing activity:

- Technical competence.
- Method validation.
- Measurement uncertainty.
- Traceability.
- Equipment/software validation.
- Impartiality.
- Handling of test items, here meaning source records and data rows.
- Reporting of results.

CRAMPS is not a calibration laboratory by default. The standard is useful because it forces method competence and traceability.

### 12.4 ISO/IEC 27001 Alignment

Use ISO/IEC 27001 alignment if the program handles:

- Restricted collaboration data.
- Embargoed manuscripts.
- Private reviewer comments.
- API keys.
- Non-public datasets.
- Personally identifiable contributor data.

Minimum controls:

- Access control.
- Secrets management.
- Audit logging.
- Backup and recovery.
- Incident response.
- Data classification.
- Third-party sharing policy.

### 12.5 Repository Trust

For public packages, align with FAIR, DataCite, W3C PROV, and CoreTrustSeal concepts:

- Persistent identifiers.
- Rich metadata.
- License clarity.
- Provenance.
- Fixity checks.
- Long-term preservation plan.
- Versioned releases.
- Clear withdrawal and correction policy.

### 12.6 Personnel Requirements

Minimum team for confirmatory release:

- One domain expert for each major evidence family.
- One statistician with evidence synthesis or HEP/astro statistics competence.
- One independent bias or methodology reviewer.
- One reproducibility reviewer who did not write the analysis code.
- One data steward.

Recommended credentials:

- Graduate-level statistics, physics, astronomy, or domain equivalent.
- Prior meta-analysis, systematic review, HEP statistics, astrostatistics, metrology, or reproducibility experience.
- Documented training on CRAMPS extraction and bias rules.

## 13. Risk Register

| Risk | Failure mode | Control |
|---|---|---|
| Cherry-picking | Coordinates chosen after seeing data | Blind lock, protocol hash, amendment log |
| Look-elsewhere inflation | Many coordinates searched, only best reported | Global correction, multiplicity registry |
| False independence | Duplicate or related rows treated as independent | Dependence groups, conservative weights |
| Unrealistic null | Null ignores literature and detector structure | Tiered nulls, negative controls, red-team |
| Missing nulls | Only anomaly papers included | Search strategy includes nulls and exclusions |
| Publication bias | Interesting residuals easier to find | Missing-evidence assessment, demotion rules |
| Theory-fashion clustering | Papers cluster around popular values | Coordinate-fashion risk field |
| Transform flexibility | Many derived coordinate maps create spurious alignment | Transform registry and forbidden transforms |
| Digitization error | Plot-extracted values look too precise | Digitization uncertainty and sensitivity exclusion |
| AI extraction error | Agent hallucinates or misreads source | Human review, source quotes, spot checks |
| Overclaiming | Ranking described as discovery | Reporting language gate and statistical veto |
| Reproducibility failure | External team cannot rerun | Capsule, lockfile, checksums, clean reproduction |

## 14. Pilot Program Recommendation

The first CRAMPS pilot should be narrow. A good pilot is not "all anomalies in physics." It should use one coordinate family and a bounded catalog.

Recommended pilot shape:

- Domain: dark-sector or light-mediator anomaly atlas.
- Coordinate family: mass or equivalent energy scale.
- Source classes: direct detection, collider missing-energy or resonance searches, indirect astrophysical residuals, precision constraints, and null exclusions.
- Candidate coordinates: no more than 3 to 5, locked before scoring.
- Null model: start with Tier A and Tier B, then red-team whether Tier C is required.
- Primary result: dependence-adjusted count or recurrence intensity at each locked coordinate.
- Required sensitivity: leave-modality-out, leave-era-out, nulls-only stress test, and negative control coordinates.
- Public claim: "pilot method demonstration and prioritization result," not discovery.

Minimum pilot deliverables:

- Locked protocol.
- Source flow table.
- 100 percent row-level provenance.
- One reproducibility script.
- One red-team report.
- One public-facing summary with explicit limitations.

## 15. Directory Template

Use this structure for each study:

```text
cramps/<study_id>/
  00_charter/
    study_charter.md
    role_assignment.csv
  ai_controls/
    AI_OPERATOR_BRIEF.md
    AGENT_DEPLOYMENT_HELPER.md
    agent_deployment_plan.csv
    agent_handoff_checklist.csv
    agent_registry.csv
    GATE_DAG.md
    LEAK_WATCH_SURFACES.md
    QUARANTINE_PROTOCOL.md
  01_protocol/
    CRAMPS_PROTOCOL_LOCK_<date>.md
    protocol_hash.txt
    amendment_log.csv
  02_sources/
    source_search_log.csv
    source_catalog.csv
    screening_decisions.csv
    exclusion_reasons.csv
    source_flow_diagram.md
  03_extraction/
    anomaly_rows_raw.csv
    extraction_notes.md
    plot_digitization_log.csv
  04_normalization/
    coordinate_ontology.md
    coordinate_transform_registry.csv
    normalized_rows.csv
    transform_audit_log.csv
  05_bias_independence/
    independence_groups.csv
    bias_assessment.csv
    missing_evidence_assessment.md
  06_analysis/
    candidate_coordinate_registry.csv
    null_model_specification.md
    null_model_runs.csv
    primary_results.csv
    sensitivity_results.csv
  07_reporting/
    report.md
    statistical_appendix.md
    limitations.md
  08_reproducibility/
    run_reproduce.sh
    environment.lock
    checksums.txt
    reproducibility_report.md
  09_review/
    red_team_findings.md
    reviewer_comments.csv
    response_to_reviewers.md
```

## 16. Release Checklist

Before any external release, confirm:

- Protocol is locked and hash matches.
- Candidate coordinates were locked before scoring.
- Inclusion and exclusion logs are complete.
- Nulls and non-events are represented.
- All rows have provenance.
- All normalized coordinates can be regenerated.
- Dependence grades are complete.
- Bias assessment is complete.
- Primary statistic matches the locked analysis plan.
- Global correction is reported.
- Sensitivity tests are complete.
- Negative controls are complete.
- Reproducibility capsule runs cleanly.
- Red-team findings are answered.
- Evidence tier is assigned conservatively.
- Claims avoid discovery language.
- Data rights and licenses are documented.
- Contributor roles are recorded.

## 17. Claim Templates

Approved confirmatory language:

> In a locked CRAMPS analysis, candidate coordinate X showed cross-catalog recurrence above the registered null expectation. The result remained stable under the registered sensitivity tests and is best interpreted as a prioritization signal for prospective testing.

Approved exploratory language:

> The exploratory atlas identified a possible recurrence near coordinate X. Because this coordinate was not locked before atlas inspection, the result is hypothesis-generating only and requires a new confirmatory CRAMPS protocol.

Required limitation language:

> CRAMPS does not establish a discovery claim. It tests whether structured recurrence exists under a specified evidence, dependence, and null-model contract. Direct experimental confirmation remains necessary.

## 18. Immediate Next Actions

1. Create the first CRAMPS pilot workspace.
2. Draft a one-page protocol for a bounded coordinate family.
3. Build the source and row schemas as CSV templates.
4. Select 3 to 5 candidate coordinates and lock them.
5. Run a small dry-run extraction on 10 to 20 sources without scoring.
6. Red-team the data contract before scaling extraction.
7. Only then run the first null-model analysis.

The program should start narrow and severe. A small, well-controlled CRAMPS study is more valuable than a broad anomaly story that cannot survive independence, missing-evidence, and look-elsewhere review.
