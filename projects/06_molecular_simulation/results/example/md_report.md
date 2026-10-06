# Molecular simulation analysis report — Trp-cage (1L2Y)

Generated (UTC): 2026-10-06T18:02:51+00:00

## Question

Which conformational observables are consistent across short independent
replicas under the declared simulation conditions?

## Protocol

- System: Trp-cage / PDB 1L2Y (waters removed), implicit solvent demo
- Force field / solvent: amber14-all.xml + implicit/obc2.xml
- Integrator: Langevin middle, T=300 K, dt=0.002 ps
- Production: 5000 steps/replica (~10.0 ps)
- Equilibration discard for analysis: first 2.0 ps
- Alignment for RMSD/RMSF: CA atoms; RMSD vs minimized topology frame
- Seeds: [20261006, 20261007]

## Replica summaries (block SE on production frames)

| replica_id | n_frames_production | rmsd_mean_nm | rmsd_block_se_nm | rg_mean_nm | rg_block_se_nm | hbonds_mean | hbonds_block_se | rmsd_tau_int_frames |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rep1 | 80 | 0.1149 | 0.01768 | 0.7585 | 0.008413 | 7.737 | 0.6496 | 25.06 |
| rep2 | 80 | 0.1565 | 0.01405 | 0.7674 | 0.003164 | 7.638 | 0.3443 | 19.59 |

## Statistical notes

- Successive frames are **time-correlated**; they are not independent experiments.
- Integrated autocorrelation time of RMSD is reported in frames as a teaching estimator.
- Block standard errors group contiguous frames; they are not a substitute for longer sampling.
- Visual RMSD 'flattening' alone does **not** prove global convergence.

## Caveats

- Implicit solvent omits explicit water structure and viscosity effects.
- Demo length is pedagogical (tens of ps), not converged conformational sampling.
- H-bond counts depend on geometric criteria (Wernet–Nilsson) and are not populations from enhanced sampling.
- This entry point emphasizes analysis discipline; full protein–ligand production MD is an advanced track.
