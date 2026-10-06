# Docking protocol validation report — CDK2 / 1AQ1 / STU

Generated (UTC): 2026-10-06T17:51:21+00:00

## Question

Does the protocol recover a plausible pose for the co-crystallized ligand,
and does ranking on a tiny labeled set look useful?

## Protocol (documented)

- Receptor: data/example/1AQ1_chainA.pdb (chain A; waters/other HETs removed)
- Ligand reference: STU from the same crystal entry
- Protonation: Open Babel `-p 7.4` for ligands
- Engine: AutoDock Vina AutoDock Vina v1.2.5
- Box: center=(0.52, 27.06, 8.97), size=(24.00, 24.00, 22.91)
- Exhaustiveness: 4; seed: 20261006

## Pose recovery (redocking)

- Best-mode affinity: **-12.789** kcal/mol
- Hungarian heavy-atom RMSD to crystal: **0.315 Å**
- Success criterion (demo): RMSD ≤ 2.0 Å → **True**

> Successful redocking does **not** alone validate a virtual-screening campaign.
> Vina scores are model estimates — not experimental affinity, efficacy or safety.

## Tiny screen (actives vs constructed decoys)

Decoys are **constructed examples** for teaching ranking metrics; they may be
chemically/physically biased relative to property-matched DUD-E style sets.

| name | label | score | note |
| --- | --- | --- | --- |
| staurosporine_redock | active | -12.79 | Crystal ligand STU used for redocking and as active control |
| roscovitine | active | -8.289 | Known CDK inhibitor (structure public); activity not re-measured here |
| caffeine | decoy | -5.894 | Constructed decoy example — not property-matched |
| phenol | decoy | -5.235 | Constructed decoy example |
| benzene | decoy | -4.968 | Constructed decoy example |
| hexane | decoy | -4.022 | Constructed decoy example (extreme) |

### Enrichment (early fraction)

| EF_at_fraction | top_k | actives_in_top_k | n_actives | n | EF |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 3 | 2 | 2 | 6 | 2 |

## Separation of claims

| Claim type | Status in this demo |
|---|---|
| Pose recovery for STU in 1AQ1 pocket | Evaluated via RMSD |
| Ranking usefulness on a tiny set | Evaluated via EF; not general |
| Experimental binding affinity | **Not claimed** |
