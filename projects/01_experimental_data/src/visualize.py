"""Figures for Project 01."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .curve_fit import four_param_logistic


def _setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "#f7f7f5",
            "axes.edgecolor": "#333333",
            "axes.labelcolor": "#222222",
            "text.color": "#222222",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
        }
    )


def plate_heatmap(merged: pd.DataFrame, output_path: Path) -> Path:
    _setup_style()
    plates = sorted(merged["plate_id"].unique())
    fig, axes = plt.subplots(1, len(plates), figsize=(5.5 * len(plates), 4.2), squeeze=False)
    row_order = list("ABCDEFGH")

    for ax, plate_id in zip(axes[0], plates):
        g = merged.loc[merged["plate_id"] == plate_id]
        grid = np.full((8, 12), np.nan)
        for _, row in g.iterrows():
            r = row_order.index(row["row"])
            c = int(row["column"]) - 1
            grid[r, c] = row["readout_RFU"]
        im = ax.imshow(grid, aspect="equal", cmap="viridis")
        ax.set_title(f"Plate {plate_id} — raw RFU")
        ax.set_xticks(range(12))
        ax.set_xticklabels([str(i) for i in range(1, 13)])
        ax.set_yticks(range(8))
        ax.set_yticklabels(row_order)
        ax.set_xlabel("Column")
        ax.set_ylabel("Row")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="RFU")

    fig.suptitle("Simulated assay plate heatmaps (raw readout)", y=1.02)
    fig.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def dose_response_curves(
    residuals: pd.DataFrame,
    fits: pd.DataFrame,
    output_path: Path,
) -> Path:
    _setup_style()
    compounds = sorted(fits["compound_id"].unique())
    n = len(compounds)
    fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 3.8), sharey=True, squeeze=False)

    for ax, cid in zip(axes[0], compounds):
        fr = fits.loc[fits["compound_id"] == cid].iloc[0]
        pts = residuals.loc[residuals["compound_id"] == cid]
        ax.scatter(
            pts["concentration_nM"],
            pts["percent_response"],
            s=28,
            alpha=0.75,
            c="#1f4e5f",
            label="observations",
            zorder=3,
        )
        if fr["status"] == "OK":
            grid = np.logspace(
                np.log10(fr["conc_min_nM"]),
                np.log10(fr["conc_max_nM"]),
                200,
            )
            x = np.log10(grid * 1e-9)
            y = four_param_logistic(
                x,
                fr["top"],
                fr["bottom"],
                np.log10(fr["ic50_M"]),
                fr["hill"],
            )
            ax.plot(grid, y, color="#c45c26", lw=2, label="4PL fit")
            ax.axvline(fr["ic50_nM"], color="#c45c26", ls="--", lw=1, alpha=0.8)
            title_extra = f"IC50={fr['ic50_nM']:.1f} nM"
            if fr["flag_outside_range"]:
                title_extra += " [OUTSIDE RANGE]"
        else:
            title_extra = fr["status"]
        ax.set_xscale("log")
        ax.set_title(f"{cid}\n{title_extra}")
        ax.set_xlabel("Concentration (nM)")
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend(fontsize=8, loc="best")

    axes[0, 0].set_ylabel("Percent response")
    fig.suptitle("Concentration–response (individual observations)", y=1.05)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def residual_plot(residuals: pd.DataFrame, output_path: Path) -> Path:
    _setup_style()
    compounds = sorted(residuals["compound_id"].unique())
    fig, axes = plt.subplots(1, len(compounds), figsize=(4.0 * len(compounds), 3.4), squeeze=False)
    for ax, cid in zip(axes[0], compounds):
        pts = residuals.loc[residuals["compound_id"] == cid]
        ax.axhline(0.0, color="#666666", lw=1)
        ax.scatter(pts["fitted"], pts["residual"], s=24, alpha=0.75, c="#1f4e5f")
        ax.set_title(cid)
        ax.set_xlabel("Fitted percent response")
        ax.set_ylabel("Residual")
        ax.grid(True, ls=":", alpha=0.5)
    fig.suptitle("Fit residuals", y=1.03)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
