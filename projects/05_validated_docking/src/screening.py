"""Simple recovery metrics for a tiny active/decoy docking screen."""

from __future__ import annotations

import numpy as np
import pandas as pd


def enrichment_factor(ranks: pd.DataFrame, *, early_fraction: float = 0.2) -> dict:
    """ranks must include columns: name, label (active/decoy), score (lower better)."""
    df = ranks.sort_values("score").reset_index(drop=True)
    n = len(df)
    n_act = int((df["label"] == "active").sum())
    if n == 0 or n_act == 0:
        return {"EF": float("nan"), "n": n, "n_actives": n_act}
    k = max(1, int(np.ceil(n * early_fraction)))
    top = df.iloc[:k]
    hit = int((top["label"] == "active").sum())
    expected = n_act * (k / n)
    ef = hit / expected if expected > 0 else float("nan")
    return {
        "EF_at_fraction": early_fraction,
        "top_k": k,
        "actives_in_top_k": hit,
        "n_actives": n_act,
        "n": n,
        "EF": float(ef),
    }
