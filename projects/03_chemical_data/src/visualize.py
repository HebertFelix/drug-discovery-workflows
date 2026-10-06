"""Chemical-space figures for Project 03."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


def property_distributions(curated: pd.DataFrame, output_path: Path) -> Path:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5", "font.size": 10})
    cols = ["mw", "logp", "tpsa", "qed"]
    fig, axes = plt.subplots(1, len(cols), figsize=(11, 3.0))
    for ax, col in zip(axes, cols):
        vals = curated[col].dropna()
        ax.hist(vals, bins=min(8, max(3, len(vals))), color="#1f4e5f", alpha=0.85, edgecolor="white")
        ax.set_title(col)
        ax.set_xlabel(col)
        ax.grid(True, ls=":", alpha=0.4)
    axes[0].set_ylabel("count")
    fig.suptitle("Descriptor distributions (curated parents)", y=1.05)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def pca_fingerprint_plot(
    curated: pd.DataFrame,
    fp_matrix: np.ndarray,
    output_path: Path,
) -> tuple[Path, pd.DataFrame]:
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "#f7f7f5"})
    n = len(curated)
    if n < 3:
        # Still write an empty-ish figure explaining insufficiency
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.text(0.5, 0.5, "PCA skipped: need ≥3 compounds", ha="center", va="center")
        ax.set_axis_off()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return Path(output_path), pd.DataFrame()

    pca = PCA(n_components=2, random_state=20261006)
    xy = pca.fit_transform(fp_matrix)
    proj = curated[["source_id", "name", "assay_type"]].copy()
    proj["PC1"] = xy[:, 0]
    proj["PC2"] = xy[:, 1]
    proj["pca_var_PC1"] = pca.explained_variance_ratio_[0]
    proj["pca_var_PC2"] = pca.explained_variance_ratio_[1]

    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    assays = proj["assay_type"].unique()
    colors = {"IC50": "#1f4e5f", "Ki": "#c45c26", "Kd": "#5c7a3a", "EC50": "#6b4c7a"}
    for assay in assays:
        sub = proj.loc[proj["assay_type"] == assay]
        ax.scatter(
            sub["PC1"],
            sub["PC2"],
            s=55,
            alpha=0.85,
            c=colors.get(assay, "#333333"),
            label=assay,
            edgecolors="white",
            linewidths=0.4,
        )
        for _, row in sub.iterrows():
            ax.annotate(row["name"], (row["PC1"], row["PC2"]), fontsize=7, alpha=0.9)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)")
    ax.set_title("Morgan FP PCA (exploratory — not class proof)")
    ax.grid(True, ls=":", alpha=0.45)
    ax.legend(title="assay_type", fontsize=8)
    fig.tight_layout()
    output_path = Path(output_path)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path, proj
