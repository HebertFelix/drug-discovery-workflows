"""Quality-control checks for plate-based assay readings."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class QCResult:
    merged: pd.DataFrame
    exclusions: pd.DataFrame
    plate_summary: pd.DataFrame
    messages: list[str] = field(default_factory=list)


def merge_inputs(
    readings: pd.DataFrame,
    plate_map: pd.DataFrame,
) -> pd.DataFrame:
    required_read = {"plate_id", "well", "readout_RFU", "readout_unit"}
    required_map = {"plate_id", "well", "role", "sample_id", "batch"}
    missing_r = required_read - set(readings.columns)
    missing_m = required_map - set(plate_map.columns)
    if missing_r:
        raise ValueError(f"Readings missing columns: {sorted(missing_r)}")
    if missing_m:
        raise ValueError(f"Plate map missing columns: {sorted(missing_m)}")

    units = readings["readout_unit"].dropna().unique()
    if len(units) != 1:
        raise ValueError(f"Expected a single readout unit, found: {units}")

    merged = plate_map.merge(readings, on=["plate_id", "well"], how="left", validate="one_to_one")
    return merged


def zprime(neg: np.ndarray, pos: np.ndarray) -> float:
    """Z′ factor using negative (vehicle) and positive (inhibited) controls."""
    neg = np.asarray(neg, dtype=float)
    pos = np.asarray(pos, dtype=float)
    neg = neg[np.isfinite(neg)]
    pos = pos[np.isfinite(pos)]
    if len(neg) < 2 or len(pos) < 2:
        return float("nan")
    return 1.0 - (3.0 * (np.std(neg, ddof=1) + np.std(pos, ddof=1))) / abs(
        np.mean(neg) - np.mean(pos)
    )


def run_qc(
    readings: pd.DataFrame,
    plate_map: pd.DataFrame,
    *,
    max_missing_fraction: float = 0.05,
    min_zprime: float = 0.4,
    edge_columns: list[int] | None = None,
    edge_control_cv_threshold: float = 0.25,
) -> QCResult:
    edge_columns = edge_columns or [1, 12]
    messages: list[str] = []
    merged = merge_inputs(readings, plate_map)
    exclusions: list[dict] = []

    # Missing values
    missing_mask = merged["readout_RFU"].isna()
    n_missing = int(missing_mask.sum())
    frac_missing = n_missing / len(merged)
    messages.append(f"Missing readings: {n_missing} ({frac_missing:.2%})")
    if frac_missing > max_missing_fraction:
        messages.append(
            f"WARNING: missing fraction {frac_missing:.2%} exceeds threshold {max_missing_fraction:.2%}"
        )
    for _, row in merged.loc[missing_mask].iterrows():
        exclusions.append(
            {
                "plate_id": row["plate_id"],
                "well": row["well"],
                "sample_id": row["sample_id"],
                "reason": "missing_readout",
                "keep_for_fit": False,
            }
        )

    merged = merged.copy()
    merged["exclude"] = False
    merged["exclude_reason"] = ""

    plate_rows: list[dict] = []
    for plate_id, g in merged.groupby("plate_id"):
        neg = g.loc[g["role"] == "NEG_CTRL", "readout_RFU"].to_numpy()
        pos = g.loc[g["role"] == "POS_CTRL", "readout_RFU"].to_numpy()
        zp = zprime(neg, pos)

        # Edge-control diagnostics
        edge = g[
            (g["role"].isin(["NEG_CTRL", "POS_CTRL"]))
            & (g["column"].isin(edge_columns))
        ]
        edge_excluded = 0
        for role in ("NEG_CTRL", "POS_CTRL"):
            role_vals = g.loc[g["role"] == role, "readout_RFU"].dropna()
            if role_vals.empty:
                continue
            med = float(role_vals.median())
            mad = float(np.median(np.abs(role_vals - med))) or 1e-6
            # Flag edge wells that deviate strongly from the plate control median.
            for idx, row in edge.loc[edge["role"] == role].iterrows():
                val = row["readout_RFU"]
                if not np.isfinite(val):
                    continue
                rel = abs(val - med) / abs(med) if med != 0 else abs(val - med)
                robust_z = abs(val - med) / (1.4826 * mad)
                if rel > edge_control_cv_threshold or robust_z > 3.5:
                    exclusions.append(
                        {
                            "plate_id": row["plate_id"],
                            "well": row["well"],
                            "sample_id": row["sample_id"],
                            "reason": "edge_control_outlier",
                            "keep_for_fit": False,
                        }
                    )
                    merged.loc[idx, "exclude"] = True
                    merged.loc[idx, "exclude_reason"] = "edge_control_outlier"
                    edge_excluded += 1

        # Recompute Z′ after edge exclusions
        neg_f = g.loc[
            (g["role"] == "NEG_CTRL") & (~merged.loc[g.index, "exclude"]),
            "readout_RFU",
        ].to_numpy()
        pos_f = g.loc[
            (g["role"] == "POS_CTRL") & (~merged.loc[g.index, "exclude"]),
            "readout_RFU",
        ].to_numpy()
        zp_after = zprime(neg_f, pos_f)
        status = "PASS" if (np.isfinite(zp_after) and zp_after >= min_zprime) else "FAIL"
        if status == "FAIL":
            messages.append(
                f"Plate {plate_id}: Z′ after QC = {zp_after:.3f} < {min_zprime} ({status})"
            )
        else:
            messages.append(
                f"Plate {plate_id}: Z′ raw = {zp:.3f}; after edge QC = {zp_after:.3f} ({status})"
            )

        plate_rows.append(
            {
                "plate_id": plate_id,
                "n_wells": len(g),
                "n_missing": int(g["readout_RFU"].isna().sum()),
                "zprime_raw": zp,
                "zprime_after_qc": zp_after,
                "edge_controls_excluded": edge_excluded,
                "neg_median": float(np.nanmedian(neg_f)) if len(neg_f) else np.nan,
                "pos_median": float(np.nanmedian(pos_f)) if len(pos_f) else np.nan,
                "status": status,
            }
        )

    # Mark missing as excluded
    merged.loc[missing_mask, "exclude"] = True
    merged.loc[missing_mask, "exclude_reason"] = "missing_readout"

    excl_df = pd.DataFrame(exclusions)
    plate_summary = pd.DataFrame(plate_rows)
    return QCResult(
        merged=merged,
        exclusions=excl_df,
        plate_summary=plate_summary,
        messages=messages,
    )
