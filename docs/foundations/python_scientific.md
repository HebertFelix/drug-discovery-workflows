# Scientific Python essentials

Minimal stack used across early portfolio modules:

| Library | Role |
|---|---|
| `numpy` | Arrays, linear algebra primitives |
| `pandas` | Tabular provenance-friendly tables |
| `scipy` | Curve fitting, stats helpers |
| `matplotlib` | Publication-oriented figures |

## Conventions

- Prefer explicit column names with units (`concentration_nM`, `readout_RFU`).
- Keep analysis code in importable modules; notebooks call those modules.
- Record seeds for any stochastic step.
- Never silently coerce incompatible measurement types.
