# Changelog

All notable changes to this portfolio are documented here.

## [0.3.0] — 2026-10-06

### Added

- Project 04 (`predictive_models`): ChEMBL CDK2 IC50 QSAR demo with mean/Ridge/RF
  models, random vs scaffold splits, applicability-domain subgroups, tests and CI.

### Changed

- Catalog marks Projects 01–04 as executable examples.

## [0.2.0] — 2026-10-06

### Added

- Project 02 (`target_evidence`): CDK2 evidence atlas with UniProt/PDB snapshots,
  ortholog conservation, intent-aware structure ranking, NGL HTML viewer and tests.
- Project 03 (`chemical_data`): RDKit curation demo with simulated CDK2-oriented
  activities, endpoint/unit policies, exclusions, descriptors and PCA.
- Unified CI workflow running demos/tests for Projects 01–03.
- Research-log entry for an automated clean reproduction of Project 01.

### Changed

- Root catalog and status tables now mark Projects 01–03 as executable examples.

## [0.1.0] — 2026-10-06

### Added

- Repository skeleton for `drug-discovery-workflows` (architecture through 2027).
- Project 01 (`experimental_data`): end-to-end demo from plate readings to
  concentration–response parameters with QC, normalization, fits and figures.
- Simulated assay dataset with a documented quality-failure scenario.
- Documentation templates, bilingual README pair, roadmap and data-source register.
- CI workflow that installs Project 01 dependencies and runs the demo tests.
