"""Write the target evidence brief."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _md_table(df: pd.DataFrame, cols: list[str] | None = None) -> str:
    if df.empty:
        return "_Empty table._"
    use = df if cols is None else df[cols]
    header = "| " + " | ".join(str(c) for c in use.columns) + " |"
    sep = "| " + " | ".join("---" for _ in use.columns) + " |"
    rows = []
    for _, row in use.iterrows():
        cells = []
        for c in use.columns:
            val = row[c]
            if isinstance(val, float):
                cells.append(f"{val:.4g}")
            else:
                cells.append(str(val))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def write_target_brief(
    path: Path,
    *,
    card: dict,
    choice: dict,
    scored: pd.DataFrame,
    audit: dict,
    conservation_summary: dict,
) -> Path:
    path = Path(path)
    feat_rows = pd.DataFrame(card.get("features_selected") or [])
    lines = [
        f"# Target evidence brief — {card.get('uniprot_id')} ({card.get('uniprot_accession')})",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"UniProt access date: {card.get('access_date')}",
        "",
        "## Scientific question",
        "",
        "Which evidence supports choosing this target and which experimental structure",
        "is adequate for the declared study intent?",
        "",
        "## Target identity",
        "",
        f"- **Protein:** {card.get('protein_name')}",
        f"- **Gene:** {', '.join(card.get('gene_symbols') or [])}",
        f"- **Organism:** {card.get('organism')} (taxon {card.get('taxonomy_id')})",
        f"- **Length:** {card.get('sequence_length')} aa",
        f"- **UniProt PDB xrefs (full entry):** {card.get('n_pdb_xrefs_in_uniprot')}",
        "",
        "### Function (UniProt summary)",
        "",
        card.get("function_summary") or "_No function text in snapshot._",
        "",
        "## Observation vs prediction vs hypothesis",
        "",
        "| Kind | In this demo |",
        "|---|---|",
        "| Experimental observation | UniProt reviewed annotation; PDB X-ray entries in the curated catalog; chain-A coordinates of 1AQ1 |",
        "| Prediction | Ortholog conservation scores from pairwise global alignments (method choice is ours) |",
        "| Hypothesis | Structure ranking for a declared intent; any mechanistic reading of ligands/cavities |",
        "",
        "> A cavity or co-crystallized ligand is **not** by itself evidence of an allosteric",
        "> mechanism. AlphaFold models are out of scope for this demo and would require",
        "> local confidence interpretation; they are **not** general mutation-effect validators.",
        "",
        "## Selected sequence features",
        "",
        _md_table(feat_rows) if not feat_rows.empty else "_None extracted._",
        "",
        "## Conservation summary",
        "",
        f"- Ortholog sequences used: {conservation_summary.get('n_orthologs')}",
        f"- Mean positional match fraction: {conservation_summary.get('mean_conservation'):.3f}",
        f"- Active-site neighborhood mean (if annotated): {conservation_summary.get('active_site_mean')}",
        "",
        "See `conservation_by_position.csv` and `conservation_map.png`.",
        "",
        "## Structure candidates (ranked)",
        "",
        f"**Declared intent:** `{choice.get('study_intent')}`",
        "",
        _md_table(
            scored,
            [
                "pdb_id",
                "resolution_A",
                "ligand_ids",
                "uniprot_ids",
                "selection_score",
                "selection_reason",
            ],
        ),
        "",
        "## Structure choice",
        "",
        f"- **Selected:** {choice.get('selected_pdb_id')}",
        f"- **Score:** {choice.get('selection_score')}",
        f"- **Reason:** {choice.get('selection_reason')}",
        f"- **Caveat:** {choice.get('caveat')}",
        "",
        "### Coordinate audit (demo PDB slice)",
        "",
        f"- Chain: {audit.get('chain')}",
        f"- Observed residues: {audit.get('n_observed_residues')} "
        f"(span {audit.get('residue_min')}–{audit.get('residue_max')})",
        f"- Missing residue numbers inside spannable range: {len(audit.get('missing_residues_in_span') or [])}",
        f"- HET groups: {', '.join(audit.get('het_resnames') or []) or 'none'}",
        "",
        "Interactive view: `structure_view.html`.",
        "",
        "## Limits",
        "",
        "- Catalog is a **teaching subset**, not an exhaustive PDB harvest.",
        "- Conservation uses pairwise global alignments to the human reference, not a full MSA package.",
        "- Partner stoichiometry, phosphorylation state and crystal contacts are not fully modeled.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
