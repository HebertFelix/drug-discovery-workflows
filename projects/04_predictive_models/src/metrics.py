"""Regression metrics and applicability-domain summaries."""

from __future__ import annotations

import numpy as np
import pandas as pd


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    resid = y_pred - y_true
    mae = float(np.mean(np.abs(resid)))
    rmse = float(np.sqrt(np.mean(resid**2)))
    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    return {"MAE": mae, "RMSE": rmse, "R2": r2, "n": int(len(y_true))}


def metrics_table(
    bundles,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> pd.DataFrame:
    rows = []
    for b in bundles:
        for split, yt, yp in (
            ("train", y_train, b.y_train_pred),
            ("test", y_test, b.y_test_pred),
        ):
            m = regression_metrics(yt, yp)
            rows.append(
                {
                    "model": b.name,
                    "feature_set": b.feature_set,
                    "split_eval": split,
                    **m,
                }
            )
    return pd.DataFrame(rows)


def subgroup_by_similarity(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    max_sim: np.ndarray,
    threshold: float = 0.4,
) -> pd.DataFrame:
    """Compare errors inside vs outside a simple AD gate (max train Tanimoto)."""
    rows = []
    for label, mask in (
        ("in_domain_sim>={:.2f}".format(threshold), max_sim >= threshold),
        ("out_of_domain_sim<{:.2f}".format(threshold), max_sim < threshold),
    ):
        if mask.sum() == 0:
            continue
        m = regression_metrics(y_true[mask], y_pred[mask])
        rows.append({"subgroup": label, **m, "mean_max_tanimoto": float(max_sim[mask].mean())})
    return pd.DataFrame(rows)
