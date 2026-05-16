# CRAMPACS Domain Overlays

These overlays adapt CRAMPACS to specific evidence ecosystems.

Core policies:

- `../policies/CRAMPACS_PROGRAM_SOP_2026-05-15.md`
- `../policies/CRAMPACS_STANDARDS_AND_PRACTICES_POLICY_2026-05-15.md`
- `../policies/CRAMPACS_METHODOLOGY_POLICY_2026-05-15.md`
- `../policies/CRAMPACS_CROSS_UNIT_EXPERIMENT_CHECKSUM_GUIDELINES_2026-05-15.md`

Domain overlays:

| Lightweight preflight | Full assurance overlay | Domain | File |
|---|---|---|---|
| `crampacs-med` | `CRAMPACS-MED` | Medicine and clinical evidence | `CRAMPACS_MED_MEDICINE_OVERLAY.md` |
| `crampacs-gen` | `CRAMPACS-GEN` | Genomics and omics | `CRAMPACS_GEN_GENOMICS_OVERLAY.md` |
| `crampacs-clim` | `CRAMPACS-CLIM` | Climate and Earth systems | `CRAMPACS_CLIM_CLIMATE_OVERLAY.md` |
| `crampacs-mat` | `CRAMPACS-MAT` | Materials science | `CRAMPACS_MAT_MATERIALS_OVERLAY.md` |
| `crampacs-eng` | `CRAMPACS-ENG` | Engineering reliability | `CRAMPACS_ENG_ENGINEERING_OVERLAY.md` |
| `crampacs-fin` | `CRAMPACS-FIN` | Finance, fraud, and risk | `CRAMPACS_FIN_FINANCE_OVERLAY.md` |
| `crampacs-cyb` | `CRAMPACS-CYB` | Cybersecurity | `CRAMPACS_CYB_CYBERSECURITY_OVERLAY.md` |
| `crampacs-ast` | `CRAMPACS-AST` | Astronomy and astrophysics | `CRAMPACS_AST_ASTRONOMY_OVERLAY.md` |
| `crampacs-phy` | `CRAMPACS-PHY` | Physics and physical anomaly catalogs | `CRAMPACS_PHY_PHYSICS_OVERLAY.md` |

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

Lowercase `crampacs-*` packets are preflight only. Uppercase `CRAMPACS-*` addenda are for full assurance studies.
