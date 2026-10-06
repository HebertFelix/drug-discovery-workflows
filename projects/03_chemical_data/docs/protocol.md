# Protocol — Project 03

1. Generate/load `raw_bioactivity.csv` (simulated activities).
2. Parse SMILES; exclude invalids.
3. Salt-strip → largest fragment → canonical SMILES + InChIKey.
4. Convert units to nM when recognized.
5. Compute pIC50 only for uncensored IC50 rows.
6. Drop duplicate InChIKey within the same assay/organism/target/relation key.
7. Compute descriptors; Morgan FP → PCA figure.
8. Write curated table, exclusions, dictionary, report.

## Acceptance

- Invalid SMILES excluded.
- Salt duplicate of staurosporine excluded.
- Ki and Kd remain distinct from IC50.
- Censored row has NA pActivity.
- Flavopiridol 0.04 uM → 40 nM.
