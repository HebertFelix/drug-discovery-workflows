# 2026-10-06 — Project 05 docking protocol validation

## Asked

Validate a docking protocol on CDK2 by separating pose recovery from ranking,
using a documented Vina setup.

## Tried

- Prep 1AQ1 chain A / STU with Open Babel → PDBQT.
- Redock with AutoDock Vina 1.2.5 (seed fixed, exhaustiveness=4).
- Hungarian heavy-atom RMSD vs crystal; tiny active/decoy screen + EF.

## Results

- Redock RMSD ≈ **0.32 Å** (success ≤ 2 Å); best score ≈ −12.8 kcal/mol.
- Illustrative EF = 2.0 on the tiny constructed decoy set.
- Unit tests + integration test passed.

## Limitations

Single system; constructed decoys; low exhaustiveness; score ≠ affinity.

## Decision

Publish as executable example; next module is trajectory analysis (Project 06).
