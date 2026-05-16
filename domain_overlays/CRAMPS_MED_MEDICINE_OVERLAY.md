# CRAMPS-MED Medicine Overlay

**Aliases:** CRAMPS-M, CRAMPS-MED  
**Domain:** Medicine, clinical evidence, public health, pharmacovigilance, diagnostics, and real-world evidence

## Definition

CRAMPS-MED tests whether weak clinical, safety, diagnostic, biomarker, or public-health signals recur at pre-specified medical coordinates more often than expected under a registered clinical or epidemiological null model.

## Coordinate Families

- Dose, dose intensity, cumulative exposure.
- Time since treatment, time since exposure, latency window.
- Biomarker value or threshold.
- Age band, sex, ancestry, comorbidity stratum.
- ICD/SNOMED phenotype or adverse-event code.
- Drug, device, procedure, ingredient, or mechanism class.
- Lab value unit, assay platform, or diagnostic cutoff.
- Geography, site, care setting, or calendar period.

## Eligible Rows

- Adverse-event disproportionality signals.
- Trial subgroup signals.
- Diagnostic false-positive or false-negative clusters.
- EHR or claims residuals.
- Registry signals.
- Postmarket surveillance events.
- Public-health outbreak or syndrome signals.
- Null studies, safety monitoring reports, negative diagnostic studies, and non-events.

## Null and Non-Events

Nulls include:

- Monitored adverse events not elevated.
- Negative safety analyses.
- Diagnostic studies with no threshold recurrence.
- Sites or cohorts with exposure but no event.
- Trial outcomes listed in protocol but not significant.

## Dependence Hazards

- Same health system or registry.
- Same EHR vendor or coding practice.
- Same payer claims stream.
- Same trial sponsor.
- Same drug safety database.
- Same coding dictionary version.
- Same lab assay platform.
- Same clinical guideline causing ascertainment bias.

## Bias Hazards

- Confounding by indication.
- Immortal time bias.
- Channeling bias.
- Surveillance bias.
- Selective outcome reporting.
- Differential coding.
- Site-level missingness.
- Publication bias.
- Safety signal amplification after media attention.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve exposure prevalence, outcome baseline rate, age/sex/calendar strata, site, coding vocabulary, and observation window.

Preferred null:

- Target trial emulation or causal design where the claim is comparative.
- Negative control outcomes and exposures.
- Self-controlled design where appropriate for pharmacovigilance.

## Standards Anchors

- PRISMA, PRISMA-P, STROBE, RECORD, CONSORT 2025, STARD 2015, TRIPOD+AI where applicable.
- FDA real-world evidence guidance and fit-for-purpose RWD/RWE concepts.
- ICH E6(R3) Good Clinical Practice for clinical research governance.
- HIPAA Privacy and Security Rules for protected health information.
- 21 CFR Part 11 where electronic records are used for regulated submissions.
- OMOP, HL7 FHIR, MedDRA, ICD, SNOMED CT, LOINC, RxNorm where applicable.

## Checksum Additions

- IRB or ethics status hash.
- Data-use agreement ID.
- Vocabulary versions.
- EHR extract timestamp.
- Site manifest.
- De-identification method.
- Phenotype algorithm hash.

## Claim Limits

CRAMPS-MED can prioritize a clinical signal for validation. It cannot establish clinical efficacy, safety causality, diagnostic performance, or medical guidance without domain-standard confirmation.

