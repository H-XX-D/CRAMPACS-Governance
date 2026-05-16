# Canonical Gate Map

**Document ID:** CRAMPACS-GATE-001  
**Version:** 0.1  
**Status:** Draft procedure  
**Owner:** CRAMPACS method owner  

## 1. Purpose

This is the canonical gate taxonomy for CRAMPACS. Older SOP stage names and printout checklist items must map back to these gates.

## 2. Canonical Gates

| Gate ID | Gate | Required evidence | Approver | Blocker rule | Output record |
|---|---|---|---|---|---|
| G0 | Charter | decision statement, assurance level, roles, intended use, prohibited use | program owner and domain/safety supervisor | no decision owner or unclear intended use | gate_review_record.csv |
| G1 | Coordinate Lock | coordinate ontology, candidate registry, tolerance basis, transform rules, negative controls | statistical lead and domain lead | mobile/post-hoc coordinate | candidate registry and gate record |
| G2 | Source Universe | search strategy, source catalog, source flow, exclusions, null search | domain lead and bias auditor | positive-only evidence | source flow and gate record |
| G3 | Row Integrity | raw rows, source trace, extraction confidence, review status, quarantine log | data steward | untraceable rows or raw overwrite | row review record |
| G4 | Dependence and Bias | evidence-family map, grades A-E, bias table, missing-evidence memo, weights | independence auditor and bias auditor | unresolved material dependence or missing-evidence risk | dependence/bias gate record |
| G5 | Statistical Method | primary statistic, null model, multiplicity correction, negative controls, sensitivity plan | statistical lead | statistic shopping or weak null model | statistical gate record |
| G6 | Reproducibility | checksums, environment, run script, output hashes, clean-run report | reproducibility lead and data steward | unreproducible primary output | reproduction report |
| G7 | Release | assurance case, red-team findings, decision memo, evidence tier, claim-language approval | accountable release authority | Critical finding open or claim exceeds tier | signed decision memo |

## 3. Legacy Mapping

| Legacy stage | Canonical gate |
|---|---|
| Stage 0 Program Initialization | G0 |
| Stage 1 Research Question and Coordinate Ontology | G1 |
| Stage 2 Protocol and Blind Lock | G1 |
| Stage 3 Source Search and Catalog Assembly | G2 |
| Stage 4 Screening | G2 |
| Stage 5 Row Extraction | G3 |
| Stage 6 Coordinate Normalization | G3 |
| Stage 7 Independence and Bias Assessment | G4 |
| Stage 8 Statistical Analysis | G5 |
| Stage 9 Sensitivity and Negative Controls | G5 |
| Stage 10 Reporting | G7 |
| Stage 11 Reproducibility Capsule | G6 |
| Stage 12 External Review and Promotion | G7 |

## 4. Gate Review Rule

Each gate must have:

- date
- reviewer
- decision: pass, hold, fail, demote
- Critical/Major/Minor/Observation findings count
- conditions
- evidence file references
- signature or approval record

