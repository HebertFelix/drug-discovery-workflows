# Theory — target evidence

## Question

Which evidence supports target choice, and which experimental structure is
adequate for a declared computational study?

## Layers of evidence

1. **Identity** — accession, isoform/canonical sequence, organism, gene symbol.
2. **Annotation** — domains, active/binding sites, variants (with source dates).
3. **Comparative** — conservation across orthologs (method-dependent).
4. **Structural** — experimental method, resolution, ligands, partners, completeness.

## Conservation score used here

Each ortholog is globally aligned to the human reference (Needleman–Wunsch with
a simple match/mismatch/gap scheme). At each reference position, conservation is
the fraction of orthologs that align a residue identical to the reference.
Gaps in the ortholog do not count as matches.

This is a **teaching statistic**, not a substitute for a curated MSA + rate model.

## Structure selection

Scores are intent-dependent. Example: `ligand_pose_reference` rewards
target-matching X-ray entries with non-trivial ligands and better resolution.
The score is a transparent heuristic for ranking a curated catalog — not a
global optimality claim over the PDB.
