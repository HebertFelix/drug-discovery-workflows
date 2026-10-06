# CDK2 prioritization brief (integrative reading)

Generated (UTC): 2026-10-06T18:03:08+00:00

## Supported

- CDK2 (`P24941`) is a well-documented experimental structural target; Project 02
  selects **3QXP** for intent `ligand_pose_reference`.
- A Vina protocol can recover the 1AQ1 STU pose with RMSD ≈ **0.31 Å**
  (Project 05) — pose claim only.

## Uncertain / provisional

- QSAR RF test R² ≈ **0.80** under random split vs
  ≈ **0.52** under scaffold split (Project 04).
  Generalization outside training chemotypes remains the binding constraint.
- Tiny docking enrichment uses **constructed** decoys — not a campaign validation.

## Not claimed

- Summing Vina score + pIC50 prediction + conservation into a single priority index.
- Safety, cellular efficacy or clinical relevance.

## Compounds meriting follow-up (process, not a shopping list)

Re-rank only after: (1) single-assay experimental IC50/Ki with stated relation/units;
(2) scaffold-aware model uncertainty; (3) pose checks on the structure chosen for
the same ligand class. Prefer molecules where methods **disagree**.

## Experiment that would discriminate

Measure biochemical IC50 (or Kd) under one harmonized CDK2 assay for 5–10 molecules
spanning agreement vs disagreement between scaffold-split QSAR residuals and docking
ranks. That tests which computational channel fails, rather than reinforcing consensus.
