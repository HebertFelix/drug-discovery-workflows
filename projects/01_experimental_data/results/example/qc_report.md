# Assay QC and concentration–response report

Generated (UTC): 2026-10-06T17:39:02+00:00

> Data origin: **SIMULATED**. Ground-truth parameters in
> `sample_metadata.csv` are for simulation audit only and are not used for fitting.

## Messages

- Missing readings: 1 (0.52%)
- Plate P01: Z′ raw = 0.850; after edge QC = 0.850 (PASS)
- Plate P02: Z′ raw = 0.007; after edge QC = 0.847 (PASS)

## Plate summary

| plate_id | n_wells | n_missing | zprime_raw | zprime_after_qc | edge_controls_excluded | neg_median | pos_median | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P01 | 96 | 1 | 0.8505 | 0.8505 | 0 | 1.173 | 0.249 | PASS |
| P02 | 96 | 0 | 0.00684 | 0.8468 | 4 | 1.202 | 0.2578 | PASS |

## Exclusions

| plate_id | well | sample_id | reason | keep_for_fit |
| --- | --- | --- | --- | --- |
| P01 | H11 | P01-BUF-H11 | missing_readout | False |
| P02 | A01 | P02-NEG-A | edge_control_outlier | False |
| P02 | H01 | P02-NEG-H | edge_control_outlier | False |
| P02 | A12 | P02-POS-A | edge_control_outlier | False |
| P02 | H12 | P02-POS-H | edge_control_outlier | False |

## Fit parameters

**IC50 definition:** concentration at mid-response of the fitted model

Estimates flagged `flag_outside_range=True` lie outside the tested
concentration window and must not be quoted with unwarranted precision.

| compound_id | n_points | top | bottom | hill | ic50_M | ic50_nM | ic50_nM_ci_low | ic50_nM_ci_high | rmse | flag_outside_range | conc_min_nM | conc_max_nM | status | message |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP-A | 48 | 102.3 | 5.322 | 1.07 | 7.66e-08 | 76.6 | 69.47 | 84.46 | 2.644 | False | 3 | 1e+04 | OK | ok |
| CMP-B | 48 | 98.85 | 10.74 | 1.507 | 3.622e-07 | 362.2 | 339.9 | 386 | 2.274 | False | 3 | 1e+04 | OK | ok |
| CMP-C | 32 | 100.4 | 58.49 | 1.368 | 2.903e-06 | 2903 | 2002 | 4209 | 2.08 | False | 3 | 1e+04 | OK | ok |

## Interpretation notes

- Technical replicates on the same plate are not independent biological experiments.
- Plate-to-plate differences are summarized via control medians and Z′.
- Mean ± SD of raw wells describes dispersion; the IC50 CI below is an
  approximate Wald interval from the nonlinear fit covariance, not a
  biological confidence interval across independent experiments.
