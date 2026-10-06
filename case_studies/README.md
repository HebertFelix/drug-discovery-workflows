# Case study — CDK2 prioritization across modules

**Question:** given mixed computational evidence for CDK2 ligands, which hypotheses
are supported, which are uncertain, and what experiment would discriminate them?

**Maturity:** executable narrative (reuses Projects 02–05 outputs; does not re-sum scores)

## Evidence assembled (this repository)

| Module | Evidence type | Pointer |
|---|---|---|
| [02 Target evidence](../projects/02_target_evidence/) | Target identity + structure choice | `results/example/target_brief.md` |
| [03 Chemical data](../projects/03_chemical_data/) | Curation policies (demo) | `results/example/curation_report.md` |
| [04 QSAR](../projects/04_predictive_models/) | pIC50 models; scaffold generalization | `results/example/qsar_report.md` |
| [05 Docking](../projects/05_validated_docking/) | Pose recovery vs ranking | `results/example/docking_report.md` |
| [06 MD analysis](../projects/06_molecular_simulation/) | Trajectory discipline (Trp-cage entry point) | `results/example/md_report.md` |

Project 06’s current demo uses Trp-cage to teach analysis methods; a CDK2–ligand
production MD campaign is an **advanced extension**, not silently implied here.

## Integration rule

Do **not** add Vina scores, QSAR predictions and conservation percentages onto one
scale. Any composite ranking must declare weights, sensitivity analysis and the
failure mode of each evidence channel.

## Worked reading (demo)

1. **Structure:** for ligand-pose work, Project 02 prefers an inhibitor co-crystal
   (e.g. 3QXP) over apo 4EK3; viewer coordinates may be a bundled 1AQ1 slice.
2. **Activity models:** Project 04 shows random-split metrics can look optimistic
   relative to scaffold split — treat high R² from random splits as provisional.
3. **Docking:** Project 05 recovers STU with low RMSD; that validates pose protocol
   for that ligand/pocket, not affinity ranking in general.
4. **Chemistry table:** Project 03 policies (endpoint separation, censoring) must
   be applied before any QSAR-style claim on new assays.

## Discriminating experiment

A useful next experiment would measure on-target binding (e.g. SPR/ITC or a
biochemical IC50 under a single harmonized assay) for a small set that
**disagrees** across QSAR vs docking ranks — not another incommensurable score.

See [`prioritization_brief.md`](cdk2_prioritization/prioritization_brief.md).
