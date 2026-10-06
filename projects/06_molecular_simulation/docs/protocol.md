# Protocol — Project 06

1. Load `1L2Y.pdb` (waters removed), build Amber14 + OBC2 implicit system.
2. Minimize; run Langevin dynamics for each seed/replica; write DCD + CSV log.
3. Load with mdtraj; compute full-series plots.
4. Discard the first `equilibration_ps` for tabulated production statistics.
5. Compute RMSD/RMSF/Rg/H-bonds; autocorrelation; block SE; write report.

## Acceptance

- Two replicas complete with production frames after eq discard.
- Report states implicit-solvent and short-timescale limits.
- Tests cover autocorrelation/block helpers; integration covers end-to-end run.
