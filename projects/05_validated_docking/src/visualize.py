"""Figures for docking validation."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def score_distribution(ranks: pd.DataFrame, output_path: Path) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5"})
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    for label, color in (("active", "#c45c26"), ("decoy", "#1f4e5f")):
        sub = ranks.loc[ranks["label"] == label, "score"]
        ax.hist(sub, bins=8, alpha=0.65, label=label, color=color, edgecolor="white")
    ax.set_xlabel("Vina score (kcal/mol) — lower is better")
    ax.set_ylabel("count")
    ax.set_title("Docking score distribution (tiny demo screen)")
    ax.legend()
    ax.grid(True, ls=":", alpha=0.45)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def redock_summary_fig(rmsd: float, affinity: float, output_path: Path) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5"})
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    ax.bar(["RMSD (Å)", "Vina score"], [rmsd, abs(affinity)], color=["#1f4e5f", "#c45c26"])
    ax.axhline(2.0, color="#666666", ls="--", lw=1, label="RMSD success threshold (2 Å)")
    ax.set_title(f"Redocking: RMSD={rmsd:.2f} Å, score={affinity:.2f}")
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", ls=":", alpha=0.45)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
