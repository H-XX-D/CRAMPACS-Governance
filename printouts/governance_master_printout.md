# CRAMPACS Governance Master Printout

## System Rule

- Uppercase `CRAMPACS-*` is the full assurance system.
- Lowercase `crampacs-*` is the one to two day preflight.
- A preflight can seed the full system, but only the full system can carry full assurance after protocol lock.

## Documentation Layers

| Layer | Name | Purpose | Documents |
| --- | --- | --- | --- |
| 0 | Concept | Vocabulary, claim boundary, uppercase/lowercase distinction | README, naming policy |
| 1 | Lightweight preflight | 1-2 day triage and seed artifacts | preflight policy and templates |
| 2 | Gotchas | Fast failure-mode checks | gotcha guide and printouts |
| 3 | Standards | Governance, quality gates, document control | standards policy |
| 4 | Methodology | Coordinate ontology, nulls, dependence, bias, claim tiers | methodology policy |
| 5 | Domain overlay | Field-specific adaptation | domain overlays and packs |
| 6 | Data contracts | Structured tables and stable IDs | templates |
| 7 | Checksums | Cross-unit reproducibility and unit integrity | checksum policy |
| 8 | Sidecar metrics | Package readiness and blockers | sidecar runner |
| 9 | Full SOP | End-to-end study execution | program SOP and protocol template |
| 10 | Regulatory | Pair with domain controls | domain addenda |
| 11 | Platform | Software workflow modules | future product layer |

## Quality Gates

| Gate | Required evidence | When checked |
| --- | --- | --- |
| Protocol | Study charter, role assignment, protocol, candidate registry | Before extraction |
| Extraction | Source flow, exclusions, row provenance, extraction confidence | Before normalization |
| Normalization | Raw values preserved, transforms registered, uncertainty assigned | Before analysis |
| Independence and bias | Independence grades, bias review, missing evidence, weights | Before scoring |
| Statistical | Primary statistic, null model, global correction, sensitivities | Before reporting |
| Release | Repro capsule, red team, signoff, claim language | Before external use |
