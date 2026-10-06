"""Markdown QC / analysis report writer."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _md_table(df: pd.DataFrame, float_prec: int = 4) -> str:
    """Render a DataFrame as a GitHub-flavored Markdown table (no tabulate)."""
    if df.empty:
        return "_Empty table._"
    cols = list(df.columns)
    header = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows: list[str] = []
    for _, row in df.iterrows():
        cells: list[str] = []
        for c in cols:
            val = row[c]
            if isinstance(val, float):
                cells.append(f"{val:.{float_prec}g}")
            else:
                cells.append(str(val))
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def write_qc_report(
    path: Path,
    *,
    plate_summary: pd.DataFrame,
    exclusions: pd.DataFrame,
    fits: pd.DataFrame,
    messages: list[str],
    ic50_definition: str,
) -> Path:
    path = Path(path)
    lines = [
        "# Assay QC and concentration–response report",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "> Data origin: **SIMULATED**. Ground-truth parameters in",
        "> `sample_metadata.csv` are for simulation audit only and are not used for fitting.",
        "",
        "## Messages",
        "",
    ]
    for m in messages:
        lines.append(f"- {m}")

    lines += [
        "",
        "## Plate summary",
        "",
        _md_table(plate_summary),
        "",
        "## Exclusions",
        "",
    ]
    if exclusions.empty:
        lines.append("_No wells excluded._")
    else:
        lines.append(_md_table(exclusions))

    lines += [
        "",
        "## Fit parameters",
        "",
        f"**IC50 definition:** {ic50_definition}",
        "",
        "Estimates flagged `flag_outside_range=True` lie outside the tested",
        "concentration window and must not be quoted with unwarranted precision.",
        "",
        _md_table(fits),
        "",
        "## Interpretation notes",
        "",
        "- Technical replicates on the same plate are not independent biological experiments.",
        "- Plate-to-plate differences are summarized via control medians and Z′.",
        "- Mean ± SD of raw wells describes dispersion; the IC50 CI below is an",
        "  approximate Wald interval from the nonlinear fit covariance, not a",
        "  biological confidence interval across independent experiments.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
