# Bioactivity curation report

Generated (UTC): 2026-10-06T17:45:18+00:00

> Structures may be real public molecules; **activity values in this demo are SIMULATED**
> and labeled as such. Do not treat them as experimental SAR.

## Policies applied

- Salt stripping + largest fragment → parent structure.
- Units converted to nM when recognized; originals retained.
- IC50, Ki, Kd, EC50 kept as separate assay types.
- Censored relations (`<`, `>`) preserved; pIC50 only for uncensored IC50.
- Duplicates: same InChIKey + assay + organism + target + relation → keep first.
- Lipinski counts are contextual; not automatic exclusions.

## Exclusions

| source_id | reason | detail |
| --- | --- | --- |
| SIM-007 | invalid_smiles | this_is_not_smiles |
| SIM-001b | duplicate_inchikey_same_endpoint_context | YOQDMRRYFRZGMQ-QZKZKSIZSA-N |

## Curated rows

| source_id | name | assay_type | relation | value_nM | pActivity | organism | target_uniprot | mw | lipinski_violations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SIM-001 | staurosporine | IC50 | = | 7 | 8.155 | Homo sapiens | P24941 | 642.8 | 2 |
| SIM-002 | roscovitine | IC50 | = | 700 | 6.155 | Homo sapiens | P24941 | 354.5 | 0 |
| SIM-003 | flavopiridol | IC50 | = | 40 | 7.398 | Homo sapiens | P24941 | 401.8 | 0 |
| SIM-004 | olomoucine | IC50 | > | 1e+04 | nan | Homo sapiens | P24941 | 298.4 | 0 |
| SIM-005 | ATP | Kd | = | 3e+04 | nan | Homo sapiens | P24941 | 507.2 | 3 |
| SIM-006 | dinaciclib | Ki | = | 1 | nan | Homo sapiens | P24941 | 444.5 | 0 |
| SIM-008 | mouse_cdk2_assay | IC50 | = | 500 | 6.301 | Mus musculus | P97377 | 324.4 | 0 |
| SIM-009 | SNS-032 | IC50 | = | 48 | 7.319 | Homo sapiens | P24941 | 415.5 | 0 |
| SIM-010 | caffeine | IC50 | = | 5e+05 | 3.301 | Homo sapiens | P24941 | 194.2 | 0 |

## Data dictionary

| column | definition |
| --- | --- |
| smiles_canonical | RDKit canonical SMILES after salt stripping / largest fragment |
| inchikey | InChIKey of parent mol; duplicate key with same endpoint context → exclusion |
| assay_type | IC50 / Ki / Kd / EC50 kept separate; never silently fused |
| relation | Qualifiers =, <, >; censored rows keep relation and skip pIC50 |
| value_nM | Activity converted to nM; original unit preserved |
| pActivity | pIC50 only for uncensored IC50; else NA |
| lipinski_violations | Contextual count; not an automatic exclusion rule |

## Interpretation limits

- PCA/UMAP projections are exploratory; they do not prove mechanisms or natural classes.
- Organism/target mismatches remain in the table when structurally valid — filter explicitly for modeling.
