# 2026-10-06 — Independent reproduction of Project 01 (agent dry-run)

## Asked

Can a clean environment reproduce the Project 01 quick start from the README
without hidden local state?

## Tried

1. Recreated/activated `projects/01_experimental_data/.venv`.
2. Ran `python -m src.run_demo`.
3. Ran `pytest tests/ -q`.

## Result

- Demo completed; outputs rewritten under `results/example/`.
- QC messages identical to the reference run: P01 Z′ ≈ 0.85 PASS; P02 Z′ raw ≈ 0.007 → after edge QC ≈ 0.85 PASS; four edge-control exclusions on P02; one missing readout on P01 H11.
- **10 passed** in ~0.5 s.
- Fitted IC50 values: CMP-A ≈ 76.6 nM (truth 80); CMP-B ≈ 362 nM (truth 350); CMP-C ≈ 2903 nM (truth 8000, incomplete curve).

## Limitations

This reproduction was executed by the same automation that authored the module,
not by an independent human. Friction points for Windows/WSL2 remain unverified.

## Decision

Mark the automated reproduction checklist item as done; keep the human
external dry-run open until a second person logs their run here.
