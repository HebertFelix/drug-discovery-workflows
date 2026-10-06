"""Docking validation report."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_Empty._"
    header = "| " + " | ".join(map(str, df.columns)) + " |"
    sep = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = []
    for _, row in df.iterrows():
        cells = [f"{v:.4g}" if isinstance(v, float) else str(v) for v in row.tolist()]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def write_docking_report(
    path: Path,
    *,
    protocol: dict,
    redock: dict,
    ranks: pd.DataFrame,
    enrichment: dict,
) -> Path:
    path = Path(path)
    lines = [
        "# Docking protocol validation report — CDK2 / 1AQ1 / STU",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Question",
        "",
        "Does the protocol recover a plausible pose for the co-crystallized ligand,",
        "and does ranking on a tiny labeled set look useful?",
        "",
        "## Protocol (documented)",
        "",
        f"- Receptor: {protocol.get('receptor_source')} (chain A; waters/other HETs removed)",
        f"- Ligand reference: {protocol.get('ligand_resname')} from the same crystal entry",
        f"- Protonation: Open Babel `-p {protocol.get('ph')}` for ligands",
        f"- Engine: AutoDock Vina {protocol.get('vina_version')}",
        f"- Box: center=({protocol.get('center')}), size=({protocol.get('size')})",
        f"- Exhaustiveness: {protocol.get('exhaustiveness')}; seed: {protocol.get('seed')}",
        "",
        "## Pose recovery (redocking)",
        "",
        f"- Best-mode affinity: **{redock.get('affinity')}** kcal/mol",
        f"- Hungarian heavy-atom RMSD to crystal: **{redock.get('rmsd_A'):.3f} Å**",
        f"- Success criterion (demo): RMSD ≤ 2.0 Å → **{redock.get('success')}**",
        "",
        "> Successful redocking does **not** alone validate a virtual-screening campaign.",
        "> Vina scores are model estimates — not experimental affinity, efficacy or safety.",
        "",
        "## Tiny screen (actives vs constructed decoys)",
        "",
        "Decoys are **constructed examples** for teaching ranking metrics; they may be",
        "chemically/physically biased relative to property-matched DUD-E style sets.",
        "",
        _md_table(ranks),
        "",
        "### Enrichment (early fraction)",
        "",
        _md_table(pd.DataFrame([enrichment])),
        "",
        "## Separation of claims",
        "",
        "| Claim type | Status in this demo |",
        "|---|---|",
        "| Pose recovery for STU in 1AQ1 pocket | Evaluated via RMSD |",
        "| Ranking usefulness on a tiny set | Evaluated via EF; not general |",
        "| Experimental binding affinity | **Not claimed** |",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
