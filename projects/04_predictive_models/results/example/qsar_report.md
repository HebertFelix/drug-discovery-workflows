# QSAR generalization report — CDK2 pIC50

Generated (UTC): 2026-10-06T17:48:22+00:00

## Question

Does the model predict pIC50 for compounds sufficiently unlike those used in training?

## Dataset

- Source: ChEMBL target CHEMBL301 (CDK2) IC50 snapshot
- Access date: 2026-10-06
- Modeling compounds (unique parents): 255
- pIC50 range: 3.60 – 9.48
- Endpoint definition: pIC50 = -log10(IC50[M]) from uncensored ChEMBL IC50 rows

## Models compared

| Model | Features | Role |
|---|---|---|
| mean_baseline | none | Trivial reference |
| ridge_descriptors | MW, LogP, HBD, HBA, TPSA, rotatable bonds | Simple conventional model |
| rf_morgan | Morgan FP (radius 2, 1024 bits) | Conventional nonlinear fingerprint model |

Name reserved: **QSAR with descriptors and fingerprints**. This is not 3D-QSAR.

## Split diagnostics

### random

| n_train | n_test | n_train_scaffolds | n_test_scaffolds | n_shared_scaffolds | shared_scaffold_fraction_of_test |
| --- | --- | --- | --- | --- | --- |
| 191 | 64 | 70 | 25 | 15 | 0.6 |

### scaffold

| n_train | n_test | n_train_scaffolds | n_test_scaffolds | n_shared_scaffolds | shared_scaffold_fraction_of_test |
| --- | --- | --- | --- | --- | --- |
| 181 | 74 | 77 | 3 | 0 | 0 |

## Metrics

Hyperparameters were not tuned on the held-out test set. The test set is used once per split for reporting.

| split_strategy | model | feature_set | split_eval | MAE | RMSE | R2 | n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| random | mean_baseline | none | train | 1.167 | 1.357 | 0 | 191 |
| random | mean_baseline | none | test | 1.007 | 1.229 | -0.0043 | 64 |
| random | ridge_descriptors | descriptors | train | 0.8526 | 1.044 | 0.4081 | 191 |
| random | ridge_descriptors | descriptors | test | 0.6985 | 0.8793 | 0.4861 | 64 |
| random | rf_morgan | morgan_fp | train | 0.3051 | 0.416 | 0.906 | 191 |
| random | rf_morgan | morgan_fp | test | 0.4638 | 0.552 | 0.7974 | 64 |
| scaffold | mean_baseline | none | train | 1.181 | 1.377 | 0 | 181 |
| scaffold | mean_baseline | none | test | 1.003 | 1.192 | -0 | 74 |
| scaffold | ridge_descriptors | descriptors | train | 0.8807 | 1.063 | 0.4044 | 181 |
| scaffold | ridge_descriptors | descriptors | test | 0.7036 | 0.886 | 0.4472 | 74 |
| scaffold | rf_morgan | morgan_fp | train | 0.3111 | 0.4097 | 0.9115 | 181 |
| scaffold | rf_morgan | morgan_fp | test | 0.6393 | 0.8281 | 0.5171 | 74 |

## Applicability domain (RF / scaffold split)

Max Tanimoto similarity to the nearest training fingerprint is a simple AD proxy — not a complete domain theory.

### random / rf_morgan

| subgroup | MAE | RMSE | R2 | n | mean_max_tanimoto |
| --- | --- | --- | --- | --- | --- |
| in_domain_sim>=0.35 | 0.4638 | 0.552 | 0.7974 | 64 | 0.7345 |

### scaffold / rf_morgan

| subgroup | MAE | RMSE | R2 | n | mean_max_tanimoto |
| --- | --- | --- | --- | --- | --- |
| in_domain_sim>=0.35 | 0.6393 | 0.8281 | 0.5171 | 74 | 0.594 |

## Interpretation limits

- Modest performance that is honestly reported is a valid delivery.
- Random splits can overestimate generalization when scaffolds leak across folds (MoleculeNet).
- Assay heterogeneity in ChEMBL is not fully harmonized here.
- Scores are model estimates of pIC50, not clinical efficacy or safety.
