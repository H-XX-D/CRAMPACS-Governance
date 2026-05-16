# CRAMPS Domain Overlays

These overlays adapt CRAMPS to specific evidence ecosystems.

Core policies:

- `../policies/CRAMPS_PROGRAM_SOP_2026-05-15.md`
- `../policies/CRAMPS_STANDARDS_AND_PRACTICES_POLICY_2026-05-15.md`
- `../policies/CRAMPS_METHODOLOGY_POLICY_2026-05-15.md`
- `../policies/CRAMPS_CROSS_UNIT_EXPERIMENT_CHECKSUM_GUIDELINES_2026-05-15.md`

Domain overlays:

| Lightweight preflight | Full assurance overlay | Domain | File |
|---|---|---|---|
| `cramps-med` | `CRAMPS-MED` | Medicine and clinical evidence | `CRAMPS_MED_MEDICINE_OVERLAY.md` |
| `cramps-gen` | `CRAMPS-GEN` | Genomics and omics | `CRAMPS_GEN_GENOMICS_OVERLAY.md` |
| `cramps-clim` | `CRAMPS-CLIM` | Climate and Earth systems | `CRAMPS_CLIM_CLIMATE_OVERLAY.md` |
| `cramps-mat` | `CRAMPS-MAT` | Materials science | `CRAMPS_MAT_MATERIALS_OVERLAY.md` |
| `cramps-eng` | `CRAMPS-ENG` | Engineering reliability | `CRAMPS_ENG_ENGINEERING_OVERLAY.md` |
| `cramps-fin` | `CRAMPS-FIN` | Finance, fraud, and risk | `CRAMPS_FIN_FINANCE_OVERLAY.md` |
| `cramps-cyb` | `CRAMPS-CYB` | Cybersecurity | `CRAMPS_CYB_CYBERSECURITY_OVERLAY.md` |
| `cramps-ast` | `CRAMPS-AST` | Astronomy and astrophysics | `CRAMPS_AST_ASTRONOMY_OVERLAY.md` |
| `cramps-phy` | `CRAMPS-PHY` | Physics and physical anomaly catalogs | `CRAMPS_PHY_PHYSICS_OVERLAY.md` |

Each overlay defines:

- Coordinate families.
- Eligible evidence rows.
- Null and non-event definitions.
- Dependence hazards.
- Bias hazards.
- Null-model requirements.
- Checksum additions.
- Standards anchors.
- Claim-language limits.

For practitioner-ready field packets, use `../domain_packs/<domain>/`.

Lowercase `cramps-*` packets are preflight only. Uppercase `CRAMPS-*` addenda are for full assurance studies.
