# Protocol — Project 05

1. Split 1AQ1 chain A into receptor ATOM records and STU HETATM ligand.
2. Convert receptor (`obabel -xr`) and ligand (`obabel -p 7.4`) to PDBQT.
3. Define box from ligand centroid/extent + padding.
4. Redock with Vina (fixed seed); compute Hungarian RMSD of best mode.
5. Dock a tiny library (crystal ligand + known inhibitor SMILES + constructed decoys).
6. Rank by Vina score; compute early enrichment; write report.

## Acceptance

- Redocking RMSD ≤ 2.0 Å for STU.
- Report states decoys are constructed and scores ≠ experimental affinity.
