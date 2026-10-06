# 2026-10-06 — Project 04 QSAR generalization demo

## Asked

Build an executable QSAR module that compares a trivial baseline with conventional
descriptor/fingerprint models and shows how split choice changes apparent
generalization (MoleculeNet lesson).

## Tried

- ChEMBL CDK2 (`CHEMBL301`) IC50 snapshot (400 rows, access 2026-10-06).
- Parent aggregation to 255 unique InChIKeys with median pIC50.
- Models: mean baseline, Ridge(descriptors), RF(Morgan FP).
- Splits: random vs Bemis–Murcko scaffold; AD via max train Tanimoto.

## Results

- Random / RF test: RMSE ≈ 0.55, R² ≈ 0.80.
- Scaffold / RF test: RMSE ≈ 0.83, R² ≈ 0.52 (clear drop vs random).
- 6 automated tests passed.

## Limitations

Snapshot is not exhaustive; assay heterogeneity remains; AD gate is heuristic.

## Decision

Publish as executable example named **QSAR with descriptors and fingerprints**.
Next: Project 05 docking validation.
