# Protocol — Project 01

## Inputs

| File | Role |
|---|---|
| `data/example/plate_readings.csv` | Raw well readouts (RFU), plate_id, well |
| `data/example/plate_map.csv` | Role, sample_id, compound, concentration, replicate, batch |
| `data/example/sample_metadata.csv` | Simulation ground truth (audit only; unused by fitting) |
| `configs/demo.yaml` | Thresholds, paths, IC50 definition |

## Procedure

1. **Validate schema** — require identifiers and a single readout unit.
2. **Merge** plate map ↔ readings on `(plate_id, well)` (1:1).
3. **Missingness** — record and exclude empty readouts; warn if fraction exceeds threshold.
4. **Edge-control screen** — on columns configured as edges, flag NEG/POS wells that deviate from the plate control median (relative deviation or robust z).
5. **Z′** — compute before and after edge exclusions; mark plate PASS/FAIL vs `min_zprime`.
6. **Normalize** — percent response from per-plate NEG/POS medians (post-QC).
7. **Fit** — 4PL per compound on SAMPLE wells that passed QC; retain technical replicates as points.
8. **Flag** — IC50 outside tested concentration range.
9. **Export** — tables, figures, Markdown report, run manifest (versions + seed).

## Decisions

| Decision | Choice | Alternative considered |
|---|---|---|
| Normalization | Per-plate percent response | Global controls (rejected: hides plate shift) |
| Edge handling | Exclude outlier edge controls | Discard entire plate (too aggressive for demo) |
| Curve model | 4PL with bounds | 3PL (less flexible for incomplete curves) |
| Uncertainty | Wald CI on log(IC50) | Bootstrap (future intermediate extension) |

## Exclusion criteria

- Missing readout.
- Edge NEG/POS well with relative deviation > `edge_control_cv_threshold` or robust z > 3.5.
- SAMPLE wells inherit plate-level warnings but are not bulk-excluded solely because Z′ failed after remediation; the report still surfaces FAIL status for review.

## Acceptance for the demo

- Planted P02 edge effect appears in `exclusions.csv`.
- CMP-A recovers an IC50 order-of-magnitude consistent with the simulation (~80 nM).
- Figures and `qc_report.md` are produced without manual edits.
