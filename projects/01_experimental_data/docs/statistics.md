# Statistics — Project 01

## Unit of analysis

| Layer | Unit | Independence |
|---|---|---|
| Raw QC | Well within plate | Not independent across a plate |
| Normalization | Plate | Control medians estimated per plate |
| Curve fit | Compound | Points = technical wells across plates; not biological replicates |

## Metrics

| Metric | Meaning |
|---|---|
| Z′ | Control separation / dispersion on a plate |
| RMSE | Root mean squared residual of the 4PL fit (percent-response units) |
| IC50 CI | Approximate 95% Wald interval from \(\mathrm{Var}(\widehat{L})\) on \(\log_{10}\mathrm{IC}_{50}\), transformed to nM |

## What we do **not** claim

- Mean ± SD of wells is **not** automatically a confidence interval.
- A p-value comparing compounds is **not** computed in this demo.
- Passing Z′ does **not** validate biological relevance of an IC50.

## Validation checks (automated)

See `tests/test_assay_pipeline.py`: single unit, unique well IDs, detection of the planted edge failure, normalization endpoints, 4PL midpoint identity, approximate recovery of CMP-A potency.
