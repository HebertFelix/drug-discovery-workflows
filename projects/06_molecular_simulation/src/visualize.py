"""Figures for trajectory analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def series_plot(series: pd.DataFrame, output_path: Path, eq_ps: float) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5", "font.size": 9})
    metrics = [("rmsd_ca_nm", "RMSD CA (nm)"), ("rg_nm", "Rg (nm)"), ("n_hbonds_wernet", "H-bonds (count)")]
    fig, axes = plt.subplots(len(metrics), 1, figsize=(7.5, 7.0), sharex=True)
    for ax, (col, label) in zip(axes, metrics):
        for rid, g in series.groupby("replica_id"):
            ax.plot(g["time_ps"], g[col], lw=1.2, label=rid)
        ax.axvline(eq_ps, color="#c45c26", ls="--", lw=1, label=f"eq discard {eq_ps} ps")
        ax.set_ylabel(label)
        ax.grid(True, ls=":", alpha=0.45)
        ax.legend(fontsize=8, loc="best")
    axes[-1].set_xlabel("Time (ps)")
    fig.suptitle("Trajectory series (production includes post-eq frames only in tables)", y=1.01)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def rmsf_plot(rmsf: pd.DataFrame, output_path: Path) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5"})
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    for rid, g in rmsf.groupby("replica_id"):
        ax.plot(g["resSeq"], g["rmsf_ca_nm"], marker="o", ms=3, lw=1.2, label=rid)
    ax.set_xlabel("Residue number")
    ax.set_ylabel("RMSF CA (nm)")
    ax.set_title("Per-residue CA RMSF (aligned on production ref frame)")
    ax.grid(True, ls=":", alpha=0.45)
    ax.legend(fontsize=8)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
