"""Markdown report for Project 06."""

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


def write_md_report(
    path: Path,
    *,
    protocol: dict,
    summary_rows: pd.DataFrame,
    caveats: list[str],
) -> Path:
    path = Path(path)
    lines = [
        "# Molecular simulation analysis report — Trp-cage (1L2Y)",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Question",
        "",
        "Which conformational observables are consistent across short independent",
        "replicas under the declared simulation conditions?",
        "",
        "## Protocol",
        "",
        f"- System: {protocol.get('system')}",
        f"- Force field / solvent: {protocol.get('forcefield')}",
        f"- Integrator: Langevin middle, T={protocol.get('temperature_K')} K, dt={protocol.get('timestep_ps')} ps",
        f"- Production: {protocol.get('n_steps')} steps/replica (~{protocol.get('prod_ps')} ps)",
        f"- Equilibration discard for analysis: first {protocol.get('eq_ps')} ps",
        f"- Alignment for RMSD/RMSF: CA atoms; RMSD vs minimized topology frame",
        f"- Seeds: {protocol.get('seeds')}",
        "",
        "## Replica summaries (block SE on production frames)",
        "",
        _md_table(summary_rows),
        "",
        "## Statistical notes",
        "",
        "- Successive frames are **time-correlated**; they are not independent experiments.",
        "- Integrated autocorrelation time of RMSD is reported in frames as a teaching estimator.",
        "- Block standard errors group contiguous frames; they are not a substitute for longer sampling.",
        "- Visual RMSD 'flattening' alone does **not** prove global convergence.",
        "",
        "## Caveats",
        "",
    ]
    for c in caveats:
        lines.append(f"- {c}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
