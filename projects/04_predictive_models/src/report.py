"""Markdown QSAR report."""

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


def write_qsar_report(
    path: Path,
    *,
    dataset_summary: dict,
    split_reports: dict[str, dict],
    metrics: pd.DataFrame,
    ad_tables: dict[str, pd.DataFrame],
) -> Path:
    path = Path(path)
    lines = [
        "# QSAR generalization report — CDK2 pIC50",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Question",
        "",
        "Does the model predict pIC50 for compounds sufficiently unlike those used in training?",
        "",
        "## Dataset",
        "",
        f"- Source: {dataset_summary.get('source')}",
        f"- Access date: {dataset_summary.get('access_date')}",
        f"- Modeling compounds (unique parents): {dataset_summary.get('n_compounds')}",
        f"- pIC50 range: {dataset_summary.get('pic50_min'):.2f} – {dataset_summary.get('pic50_max'):.2f}",
        f"- Endpoint definition: pIC50 = -log10(IC50[M]) from uncensored ChEMBL IC50 rows",
        "",
        "## Models compared",
        "",
        "| Model | Features | Role |",
        "|---|---|---|",
        "| mean_baseline | none | Trivial reference |",
        "| ridge_descriptors | MW, LogP, HBD, HBA, TPSA, rotatable bonds | Simple conventional model |",
        "| rf_morgan | Morgan FP (radius 2, 1024 bits) | Conventional nonlinear fingerprint model |",
        "",
        "Name reserved: **QSAR with descriptors and fingerprints**. This is not 3D-QSAR.",
        "",
        "## Split diagnostics",
        "",
    ]
    for split_name, rep in split_reports.items():
        lines += [
            f"### {split_name}",
            "",
            _md_table(pd.DataFrame([rep])),
            "",
        ]

    lines += [
        "## Metrics",
        "",
        "Hyperparameters were not tuned on the held-out test set. The test set is used once per split for reporting.",
        "",
        _md_table(metrics.round(4)),
        "",
        "## Applicability domain (RF / scaffold split)",
        "",
        "Max Tanimoto similarity to the nearest training fingerprint is a simple AD proxy — not a complete domain theory.",
        "",
    ]
    for name, tab in ad_tables.items():
        lines += [f"### {name}", "", _md_table(tab.round(4)), ""]

    lines += [
        "## Interpretation limits",
        "",
        "- Modest performance that is honestly reported is a valid delivery.",
        "- Random splits can overestimate generalization when scaffolds leak across folds (MoleculeNet).",
        "- Assay heterogeneity in ChEMBL is not fully harmonized here.",
        "- Scores are model estimates of pIC50, not clinical efficacy or safety.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
