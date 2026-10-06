# Theory — QSAR generalization

## Endpoint

\[
\mathrm{pIC}_{50} = -\log_{10}(\mathrm{IC}_{50}[\mathrm{M}])
\]

Only uncensored IC50 rows enter the modeling table. Duplicate parents are
aggregated by median pIC50.

## Why splits matter

MoleculeNet showed that random splits can overestimate generalization when
related chemotypes appear in both train and test. Scaffold splits keep
Bemis–Murcko scaffolds together, stressing out-of-series prediction.

## Models in this demo

| Model | Features | Intent |
|---|---|---|
| Mean baseline | — | Reference floor |
| Ridge | Physicochemical descriptors | Simple linear conventional model |
| Random forest | Morgan fingerprints | Nonlinear fingerprint model |

3D-QSAR and generative chemistry are out of scope.
