# CRAMPS-GEN Full Protocol Addendum

**Domain:** Genomics and omics

Use this addendum with `../../templates/CRAMPS_PROTOCOL_TEMPLATE.md`.

## Domain Coordinate Families

locus, variant, gene, pathway, cell type, tissue, expression threshold, perturbation

## Domain Nulls and Non-Events

failed replications, non-significant loci, negative functional assays, tested pathways not enriched

## Domain Dependence Hazards

List the source families, instruments, vendors, sites, pipelines, datasets, or reporting systems that could make rows non-independent.

## Domain Bias Hazards

Primary gotcha: population stratification, batch effects, genome-build drift, winner's curse

Add domain-specific publication, reporting, measurement, selection, and survivorship biases.

## Required Negative Controls

Define at least one coordinate, source class, or row family expected not to recur.

## Domain Checksum Additions

List required hashes for domain-specific source systems, units, transforms, vocabularies, reference systems, or vendor snapshots.

## Domain Standards Anchors

GA4GH, ClinGen, MIAME/MINSEQE, STREGA, FAIR

## Claim Limits

This `CRAMPS-GEN` study can produce a full CRAMPS evidence package only after protocol lock, full source flow, null inclusion, independence review, bias review, null-model analysis, sensitivity tests, checksum reproduction, and signoff.
