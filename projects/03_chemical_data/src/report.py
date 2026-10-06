"""Markdown report for curated chemical dataset."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _md_table(df: pd.DataFrame, cols: list[str] | None = None) -> str:
    if df.empty:
        return "_Empty._"
    use = df if cols is None else df[cols]
    header = "| " + " | ".join(map(str, use.columns)) + " |"
    sep = "| " + " | ".join("---" for _ in use.columns) + " |"
    rows = []
    for _, row in use.iterrows():
        cells = []
        for c in use.columns:
            v = row[c]
            cells.append(f"{v:.4g}" if isinstance(v, float) else str(v))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def write_curation_report(
    path: Path,
    *,
    curated: pd.DataFrame,
    exclusions: pd.DataFrame,
    dictionary: pd.DataFrame,
) -> Path:
    path = Path(path)
    lines = [
        "# Bioactivity curation report",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "> Structures may be real public molecules; **activity values in this demo are SIMULATED**",
        "> and labeled as such. Do not treat them as experimental SAR.",
        "",
        "## Policies applied",
        "",
        "- Salt stripping + largest fragment → parent structure.",
        "- Units converted to nM when recognized; originals retained.",
        "- IC50, Ki, Kd, EC50 kept as separate assay types.",
        "- Censored relations (`<`, `>`) preserved; pIC50 only for uncensored IC50.",
        "- Duplicates: same InChIKey + assay + organism + target + relation → keep first.",
        "- Lipinski counts are contextual; not automatic exclusions.",
        "",
        "## Exclusions",
        "",
        _md_table(exclusions) if not exclusions.empty else "_None._",
        "",
        "## Curated rows",
        "",
        _md_table(
            curated,
            [
                "source_id",
                "name",
                "assay_type",
                "relation",
                "value_nM",
                "pActivity",
                "organism",
                "target_uniprot",
                "mw",
                "lipinski_violations",
            ],
        ),
        "",
        "## Data dictionary",
        "",
        _md_table(dictionary),
        "",
        "## Interpretation limits",
        "",
        "- PCA/UMAP projections are exploratory; they do not prove mechanisms or natural classes.",
        "- Organism/target mismatches remain in the table when structurally valid — filter explicitly for modeling.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
