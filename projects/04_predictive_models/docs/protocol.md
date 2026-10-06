# Protocol — Project 04

1. Load ChEMBL CDK2 IC50 snapshot (`data/example/raw_chembl_cdk2_ic50.csv`).
2. Exclude non-IC50, censored relations, invalid SMILES, non-convertible units.
3. Salt-strip → parent → InChIKey; aggregate median pIC50.
4. Build descriptor and Morgan FP matrices (**fit/transform only after split**;
   fingerprints are computed per molecule without using test labels).
5. Run random and scaffold splits with fixed seed.
6. Fit baseline / Ridge / RF on training folds only.
7. Evaluate once on the held-out test fold; write metrics, figures, AD subgroups.

## Decisions

| Decision | Choice | Alternative |
|---|---|---|
| Target | CDK2 / CHEMBL301 | Other kinase snapshots |
| Aggregation | Median pIC50 per InChIKey | Mean / keep all assays separate |
| AD proxy | Max Tanimoto to train FP | Leverage / conformal methods |

## Acceptance

- Modeling table ≥ 50 unique parents.
- Scaffold split shares fewer scaffolds with train than random (ideally zero shared).
- Report includes baseline comparison and both splits.
