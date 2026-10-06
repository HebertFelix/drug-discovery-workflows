"""Figures for QSAR evaluation."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def pred_vs_obs_grid(
    panels: list[tuple[str, np.ndarray, np.ndarray]],
    output_path: Path,
    title: str,
) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5", "font.size": 9})
    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(4.0 * n, 3.6), squeeze=False)
    for ax, (name, y_true, y_pred) in zip(axes[0], panels):
        ax.scatter(y_true, y_pred, s=22, alpha=0.7, c="#1f4e5f", edgecolors="white", linewidths=0.3)
        lo = float(min(y_true.min(), y_pred.min()))
        hi = float(max(y_true.max(), y_pred.max()))
        ax.plot([lo, hi], [lo, hi], ls="--", color="#c45c26", lw=1)
        ax.set_xlabel("Observed pIC50")
        ax.set_ylabel("Predicted pIC50")
        ax.set_title(name)
        ax.grid(True, ls=":", alpha=0.45)
    fig.suptitle(title, y=1.03)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def residual_plot(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    max_sim: np.ndarray,
    output_path: Path,
    title: str,
) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5"})
    resid = y_pred - y_true
    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    sc = ax.scatter(y_pred, resid, c=max_sim, cmap="viridis", s=28, alpha=0.85)
    ax.axhline(0.0, color="#666666", lw=1)
    ax.set_xlabel("Predicted pIC50")
    ax.set_ylabel("Residual (pred − obs)")
    ax.set_title(title)
    cb = fig.colorbar(sc, ax=ax)
    cb.set_label("Max Tanimoto to train")
    ax.grid(True, ls=":", alpha=0.45)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def metrics_barplot(metrics: pd.DataFrame, output_path: Path, split_name: str) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5"})
    sub = metrics.loc[metrics["split_eval"] == "test"].copy()
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    x = np.arange(len(sub))
    ax.bar(x, sub["RMSE"], color="#1f4e5f", alpha=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(sub["model"], rotation=20, ha="right")
    ax.set_ylabel("Test RMSE (pIC50)")
    ax.set_title(f"Test RMSE by model — {split_name} split")
    ax.grid(True, axis="y", ls=":", alpha=0.45)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
