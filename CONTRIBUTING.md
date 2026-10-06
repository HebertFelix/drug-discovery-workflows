# Contributing

Thank you for considering a contribution. This portfolio prioritizes scientific
clarity, traceability and reproducible demos over feature volume.

## Before you start

1. Read the project `README.md` and `docs/limitations.md` for the module you touch.
2. Prefer a small, well-documented change over a broad rewrite.
3. Keep simulated and public/authorized data clearly labeled in `data/manifest.tsv`.

## Workflow

1. Fork or branch from `main`.
2. Work inside the relevant `projects/<module>/` tree.
3. Update documentation when behavior, assumptions or limits change.
4. Add or adjust tests that protect scientific decisions (units, identifiers,
   train/test isolation, metric definitions).
5. Run the module demo and its tests locally before opening a pull request.

## Documentation expectations

Every substantial contribution should record:

- what was asked;
- what was tried;
- why a method was chosen;
- what result appeared;
- which limitations remain;
- which decision was taken.

Negative or inconclusive results that inform the next step belong in
`docs/research_log/`.

## Code style

- Prefer small, named functions with explicit units in docstrings.
- Keep reusable logic in `src/`; notebooks are for teaching and exploration.
- Do not silently merge incompatible measurements or hide exclusions.

## Language

Top-level project presentation is bilingual (Portuguese and English). Tutorial
prose may start in Portuguese and be translated when the material stabilizes.
Code, identifiers and configuration keys remain in English.
