# Protocol — Project 02

## Inputs

Snapshots under `data/example/` with access date **2026-10-06**:

- `target_card.json` — compact UniProt P24941 fields
- `target_sequence.fasta` / `orthologs.fasta`
- `structures_catalog.tsv` — curated PDB metadata via RCSB GraphQL
- `1AQ1_chainA.pdb` — offline viewer coordinates (chain A)

## Procedure

1. Load target card and reference sequence.
2. Align each ortholog to the reference; write per-position conservation.
3. Score structures for `study_intent` from `configs/demo.yaml`.
4. Record top choice with explicit caveats.
5. Audit bundled PDB residues/HETs.
6. Emit brief, CSV tables, conservation figure, NGL HTML, run manifest.

## Decisions

| Decision | Choice | Alternative |
|---|---|---|
| Target for demo | CDK2 (P24941) | EGFR / other kinases |
| Conservation | Pairwise NW to reference | Full MSA (Clustal/MUSCLE) |
| Ranking | Intent heuristics on curated set | Exhaustive PDB API harvest |
| 3D view | Bundled 1AQ1 chain A + NGL CDN | Requires network for the viewer library |

## Acceptance

- Apo entry loses `ligand_pose_reference`.
- `apo_reference` selects 4EK3.
- Brief distinguishes observation / prediction / hypothesis.
