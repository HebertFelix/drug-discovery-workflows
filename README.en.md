# drug-discovery-workflows

**Hebert Felix** · Scientific portfolio in drug discovery (2026–2027)

[Versão em português](README.md)

Turn biological, chemical and biophysical data into **traceable analyses**,
**interpretable visualizations** and **hypotheses that can be tested** against
experimental evidence.

This repository connects bioinformatics, cheminformatics and computational
biophysics / physical chemistry, with emphasis on reproducible methods and
teachable documentation.

## Current status

| Item | Status |
|---|---|
| Portfolio structure | Executable example |
| Projects 01–06 | Executable example |
| CDK2 integrative case study | Executable narrative |
| Integrative case study | Planned |

Catalog maturity states: **planned → prototype → executable example → validated within declared scope**.

## Quick start (Project 01)

```bash
cd projects/01_experimental_data
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r envs/requirements.txt
python -m src.run_demo
pytest tests/ -q
```

Reference outputs live in `projects/01_experimental_data/results/example/`.

## Learning map

| Level | Experience | Evidence of learning |
|---|---|---|
| Beginner | Small dataset, guided path, expected outputs | Run, interpret and explain each transformation |
| Intermediate | New data, tunable parameters, method comparison | Adapt the workflow and justify choices |
| Advanced | Uncertainty, bias, independent validation | Assess limits and investigate an original question |

## Project catalog

| Project | Question | Level | Data | Environment | Demo cost | Expected result | Maturity |
|---|---|---|---|---|---|---|---|
| [01 Experimental data](projects/01_experimental_data/) | Do assay data support a reliable comparison? | Beginner → intermediate | Simulated | Python 3.11+ | < 1 min CPU | QC report, IC50 with uncertainty, figures | Executable example |
| [02 Target evidence](projects/02_target_evidence/) | What evidence supports the target and structure? | Beginner → intermediate | UniProt/PDB snapshot | Python 3.11+ | < 1 min CPU | Brief, ranking, conservation, 3D view | Executable example |
| [03 Chemical data](projects/03_chemical_data/) | Which compounds and measurements are comparable? | Intermediate | Public structures + simulated activities | Python 3.11+ / RDKit | < 1 min CPU | Curated dataset + PCA | Executable example |
| [04 Predictive models](projects/04_predictive_models/) | Does the model generalize to dissimilar compounds? | Intermediate → advanced | ChEMBL CDK2 snapshot | Python/RDKit/sklearn | ~1–2 min CPU | Baseline+RF, random vs scaffold | Executable example |
| [05 Validated docking](projects/05_validated_docking/) | Does the protocol recover poses and rank usefully? | Intermediate → advanced | 1AQ1/STU + constructed decoys | Vina+OpenBabel | ~1–3 min CPU | Redocking RMSD + EF | Executable example |
| [06 Molecular simulation](projects/06_molecular_simulation/) | Which behaviors are consistent under the simulated conditions? | Intermediate → advanced | Trp-cage 1L2Y | OpenMM+mdtraj | ~1–2 min CPU | RMSD/RMSF/Rg + block SE | Executable example |
| [Case study CDK2](case_studies/) | How to integrate evidence without summing scores? | Intermediate | Outputs 02–05 | — | — | Prioritization brief | Executable narrative |

## Architecture

```
docs/           foundations, methods and research log
projects/       six core modules
case_studies/   studies that connect modules
extensions/     advanced variants (omics, free energy, QM/MM, …)
templates/      documentation and report templates
```

See [`ROADMAP.md`](ROADMAP.md) for priorities and milestones.

## Principles

1. Every project states an explicit **scientific question**.
2. Results preserve **provenance** to source data.
3. Limitations and known failures are documented, not hidden.
4. Demonstration (small data) and full study are distinct modes.
5. Scores from different methods are **not** summed without justification.

## Citation

See [`CITATION.cff`](CITATION.cff). Code license: [`LICENSE`](LICENSE) (MIT).
Data terms: [`DATA_SOURCES.md`](DATA_SOURCES.md).
