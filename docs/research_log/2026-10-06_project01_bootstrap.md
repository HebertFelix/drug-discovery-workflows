# 2026-10-06 — Bootstrap of Project 01

## Asked

Can we stand up the portfolio skeleton and a first reproducible path from plate
file → QC → IC50 report using clearly labeled simulated data, including one
known quality failure?

## Tried

- Modular monorepo `drug-discovery-workflows` as specified in the 2027 plan.
- Simulated two-plate 96-well assay with edge-effect inflation on P02.
- QC exclusions, percent-response normalization, 4PL fits, figures, tests, CI.

## Why this method

Simulated data removes access barriers while still exercising provenance,
exclusion logging and out-of-range IC50 flagging — the first milestone in the
plan (Oct–Dec 2026).

## Result

Executable demo under `projects/01_experimental_data/` with automated tests.

## Limitations

No independent human reproduction yet; laboratory data not included.

## Decision

Publish as **executable example**; next step is an external dry-run of the README
quick start and logging of friction points here.
