# Limitations — Project 04

1. ChEMBL snapshot is the first 400 IC50 rows returned by the API, not a complete CDK2 extract.
2. Assay protocols are heterogeneous; pIC50 values are not fully cross-calibrated.
3. Descriptor set is minimal; no physicochemical ionization states or 3D fields.
4. AD via max Tanimoto is a heuristic, not a calibrated coverage guarantee.
5. Scaffold definition follows RDKit Murcko helpers; edge cases (empty scaffolds) are isolated.
6. Modest R² on scaffold split is expected and informative — not a failure mode by itself.
