# Theory — docking validation

## Pose vs ranking

Recovering a crystal-like pose (low RMSD) and ranking actives above decoys are
**different** questions. A protocol can succeed at one and fail at the other.

## RMSD

This demo uses Hungarian assignment within element types on heavy atoms to
tolerate atom-order and local symmetry differences between crystal PDB and
Vina PDBQT output. A common teaching threshold is RMSD ≤ 2 Å for redocking
success — useful, not universal.

## Scores

AutoDock Vina affinities are empirical scoring-function estimates
(kcal/mol scale of the model). They are not experimental ΔG, potency, efficacy
or safety.
