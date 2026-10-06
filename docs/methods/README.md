# Methods conventions

Cross-project expectations for curation, statistics, visualization and reproduction.

## Curation

- Every table row must be traceable to a source identifier and transform.
- Exclusions are written to disk with reasons.
- Simulated vs experimental origin is always labeled.

## Statistics

- State the experimental unit and dependence structure before testing or fitting.
- Distinguish dispersion (e.g. SD) from estimate uncertainty (e.g. CI / SE).
- Do not treat p < 0.05 as a sufficient scientific conclusion.

## Visualization

- Include units, legend, accessible colors and data origin.
- Save the plotting table next to the figure when practical.
- Prefer SVG/PDF for vectors; adequate DPI for rasters.

## Reproduction

- Offer a **demo** mode (small data, reference outputs) and a **full study** mode.
- Pin environments per module when dependencies diverge.
- CI runs demos; expensive simulations keep their own run records.
