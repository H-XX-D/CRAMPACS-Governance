# CRAMPACS-GEN Genomics Overlay

**Domain:** Genomics, transcriptomics, proteomics, metabolomics, functional genomics, and multi-omics

## Definition

CRAMPACS-GEN tests whether weak omics signals recur at pre-specified genomic, molecular, pathway, cell-state, or variant coordinates more often than expected under a registered biological and technical null model.

## Coordinate Families

- Genomic locus, variant, haplotype, gene, enhancer, regulatory element.
- Genome build and reference sequence.
- Pathway, gene set, protein complex, cell type, tissue, developmental stage.
- Expression threshold, methylation site, peak coordinate, metabolite mass/charge, proteomic peptide.
- Perturbation, guide RNA, compound, dose, timepoint.

## Eligible Rows

- Weak association results.
- Replication near-misses.
- Differential expression residuals.
- Functional assay anomalies.
- Variant effect signals.
- Pathway enrichments.
- Null association scans.
- Failed replication cohorts.
- Negative perturbation results.

## Null and Non-Events

Nulls include:

- Non-significant loci in scanned regions.
- Failed replication attempts.
- Negative functional assays.
- Cohorts with adequate power and no recurrence.
- Genes/pathways tested but not enriched.

## Dependence Hazards

- Same cohort.
- Same biobank.
- Same ancestry panel.
- Same sequencing platform.
- Same genome build.
- Same imputation reference.
- Same analysis pipeline.
- Same public summary statistics.
- Same batch effects.

## Bias Hazards

- Population stratification.
- Winner's curse.
- Batch effects.
- Multiple testing and p-hacking.
- Ancestry imbalance.
- Tissue/cell-type mismatch.
- Platform-specific artifacts.
- Annotation drift.
- Publication bias toward positive loci.

## Null-Model Requirements

Minimum confirmatory null:

- Preserve linkage disequilibrium, ancestry structure, batch, platform, gene length, pathway size, and tested-region support where applicable.

Preferred null:

- Permutation or generative model that preserves cohort structure and technical covariance.
- Negative control loci, genes, pathways, and assays.

## Standards Anchors

- GA4GH standards, including Phenopackets, VRS, refget, Beacon, DRS, and DUO where applicable.
- ClinGen clinical validity framework for gene-disease evidence.
- MIAME and MINSEQE for expression and sequencing experiment metadata.
- STREGA and STROBE where genetic association reporting applies.
- FAIR and controlled vocabularies for reusable omics data.

## Checksum Additions

- Genome build.
- Reference sequence digest.
- GA4GH refget identifier where available.
- VCF/BCF hash.
- Variant normalization tool version.
- Annotation database version.
- Pipeline container hash.

## Claim Limits

CRAMPACS-GEN can rank candidate loci, genes, pathways, or molecular states for follow-up. It cannot establish clinical pathogenicity, mechanism, biomarker validity, or therapeutic relevance without domain-standard validation.

