# Data sources

This file separates **code licensing** (see `LICENSE`) from **data access and
reuse conditions**. Every dataset used in a project must also appear in that
project's `data/manifest.tsv`.

| Dataset | Project | Origin | License / terms | Access date | Notes |
|---|---|---|---|---|---|
| `plate_readings.csv`, `plate_map.csv`, `sample_metadata.csv` | 01 | Simulated (this repository) | Same as code (MIT) | 2026-10-06 | Explicitly labeled as simulated; includes a planted QC failure. |

## Rules

1. Do not publish restricted laboratory data without written authorization.
2. Record identifiers, versions and access dates for public databases (UniProt,
   PDB, ChEMBL, PubChem, etc.) when those modules are added.
3. Prefer small demonstration subsets under version control; document how to
   obtain larger study-mode datasets separately.
4. Checksums belong in each project's `data/manifest.tsv` when files are
   downloaded or regenerated.
