"""Signal normalization for concentration–response analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def percent_response(
    values: np.ndarray,
    neg_median: float,
    pos_median: float,
) -> np.ndarray:
    """Map raw signal to percent response.

    Definition used here (signal decreases with activity):
        100% = negative/vehicle control median (no inhibition)
          0% = positive control median (full inhibition reference)

        percent = 100 * (value - pos) / (neg - pos)

    So vehicle wells sit near 100 and inhibited wells near 0.
    """
    denom = neg_median - pos_median
    if not np.isfinite(denom) or abs(denom) < 1e-12:
        raise ValueError("Cannot normalize: neg and pos control medians are not separable")
    return 100.0 * (np.asarray(values, dtype=float) - pos_median) / denom


def normalize_plates(merged: pd.DataFrame, plate_summary: pd.DataFrame) -> pd.DataFrame:
    """Add percent_response column using per-plate control medians after QC."""
    out = merged.copy()
    out["percent_response"] = np.nan
    summary = plate_summary.set_index("plate_id")

    for plate_id, g in out.groupby("plate_id"):
        if plate_id not in summary.index:
            raise KeyError(f"No QC summary for plate {plate_id}")
        neg_m = float(summary.loc[plate_id, "neg_median"])
        pos_m = float(summary.loc[plate_id, "pos_median"])
        mask = ~out.loc[g.index, "exclude"] & out.loc[g.index, "readout_RFU"].notna()
        idxs = g.index[mask]
        out.loc[idxs, "percent_response"] = percent_response(
            out.loc[idxs, "readout_RFU"].to_numpy(),
            neg_m,
            pos_m,
        )
    return out
