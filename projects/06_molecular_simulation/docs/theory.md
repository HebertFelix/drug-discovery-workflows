# Theory — trajectory analysis

## Observables in this demo

| Observable | Definition used |
|---|---|
| RMSD (CA) | After CA alignment to the minimized topology frame |
| RMSF (CA) | Fluctuation around the production reference frame |
| Rg | Radius of gyration of all atoms in the trajectory frame |
| H-bonds | Per-frame count (Wernet–Nilsson geometric criterion) |

## Dependence in time

MD frames form a time series. Treating each frame as an independent draw
underestimates uncertainty. This demo reports:

1. a simple integrated autocorrelation time for RMSD;
2. block standard errors on contiguous blocks of production frames.

Fixed length and a visually flat RMSD do **not** prove global convergence.
