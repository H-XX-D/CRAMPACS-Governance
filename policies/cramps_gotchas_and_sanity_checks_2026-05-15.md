# cramps Gotchas and Sanity Checks

**Guide ID:** cramps-GOTCHA-001  
**Version:** 0.1  
**Date:** 2026-05-15 PDT  
**Status:** Draft practitioner guide

## 1. Purpose

This guide lists the failure modes practitioners should check before trusting a CRAMPS or cramps package.

It is written for fast use. The goal is to catch obvious failure modes before time and money are spent.

## 2. The Ten Fast Questions

Ask these before doing anything expensive:

1. Can the coordinate be stated precisely?
2. Were the coordinates chosen before scoring?
3. Are nulls and non-events present?
4. Are the rows actually independent?
5. Are units and transforms locked?
6. Is the tolerance window justified before looking?
7. Could publication or reporting bias create the pattern?
8. Does one source, vendor, instrument, site, or era drive the result?
9. Does a negative control behave normally?
10. Can someone else reproduce the package from hashes?

If three or more answers are weak, stay in lowercase preflight mode.

## 3. Gotcha Catalog

### 3.1 Coordinate Drift

Symptom:

- The coordinate changes names, units, or definitions across sources.

Fast check:

- Write the coordinate formula and units on one line.
- Ask whether every row maps to that same line.

Fix:

- Lock a coordinate ontology and transform registry.

### 3.2 Tolerance Creep

Symptom:

- The window gets wider when rows are just outside it.

Fast check:

- Ask what tolerance would have been chosen before seeing the rows.

Fix:

- Use instrument resolution, domain standard, or fixed fraction chosen before scoring.

### 3.3 Null Starvation

Symptom:

- Only positive anomalies are present.

Fast check:

- Search specifically for nulls, exclusions, failed replications, passed tests, non-events, and negative controls.

Fix:

- Do not promote without null coverage.

### 3.4 Duplicate Evidence

Symptom:

- Ten rows trace back to one dataset, one vendor, one detector, one registry, or one alert feed.

Fast check:

- Draw a dependence graph from rows to raw data sources.

Fix:

- Collapse duplicates or model dependence.

### 3.5 Literature Fashion

Symptom:

- Many sources inspect the same coordinate because it was already popular.

Fast check:

- Look for theory papers, review articles, standards, or regulations that pushed everyone to the same value.

Fix:

- Add coordinate-fashion bias and use a literature-process null.

### 3.6 Time Leakage

Symptom:

- Later knowledge influenced earlier-looking candidate selection.

Fast check:

- Compare candidate lock date with source dates and analyst knowledge.

Fix:

- Use prospective holdout or restart with a clean lock.

### 3.7 Unit Trap

Symptom:

- Same coordinate appears aligned only after hidden unit conversions, calendar choices, currency conversions, genome builds, or coordinate frames.

Fast check:

- Recompute every normalized coordinate from raw values.

Fix:

- Add unit conversion audit and checksum.

### 3.8 One-Source Collapse

Symptom:

- Remove one famous source and the signal disappears.

Fast check:

- Leave-one-source-out by hand.

Fix:

- Label fragile or stop.

### 3.9 Negative Control Failure

Symptom:

- Negative controls also look significant.

Fast check:

- Run the same recurrence logic on control coordinates.

Fix:

- Null model is too weak or source process is biased.

### 3.10 AI Extraction Drift

Symptom:

- AI summaries become source data.

Fast check:

- Trace every extracted row to a source table, text span, machine-readable file, or documented digitization.

Fix:

- Human review and row hashes.

### 3.11 Denominator Missing

Symptom:

- Counts exist but opportunity counts do not.

Fast check:

- Ask, "Out of how many possible tests, subjects, assets, events, regions, or scans?"

Fix:

- Add exposure, searched range, or opportunity denominator.

### 3.12 Too-Good Match

Symptom:

- A result aligns suspiciously well across messy sources.

Fast check:

- Inspect rounding, transform choices, duplicate data, and post-hoc tolerance.

Fix:

- Red-team before promotion.

## 4. Five-Minute Sanity Score

Score each item 0, 1, or 2.

| Check | 0 | 1 | 2 |
|---|---|---|---|
| Coordinate clarity | vague | mostly clear | exact |
| Pre-specification | post-hoc | partial | locked |
| Null coverage | none | weak | adequate |
| Independence | unknown | partially mapped | mapped |
| Bias review | none | informal | documented |
| Unit control | unclear | manually checked | audited |
| Negative controls | none | planned | run |
| Reproducibility | none | partial | checksummed |

Interpretation:

- 0-6: do not escalate.
- 7-10: continue lowercase preflight only.
- 11-14: candidate for full CRAMPS.
- 15-16: strong preflight package.

## 5. Practitioner Rule

The fastest way to harden a cramps pass is not more statistics. It is finding the nulls, mapping dependence, locking the coordinate, and checking units.

