"""Four-parameter logistic concentration–response fitting."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def four_param_logistic(
    log10_conc_M: np.ndarray,
    top: float,
    bottom: float,
    log_ic50: float,
    hill: float,
) -> np.ndarray:
    """y = bottom + (top - bottom) / (1 + 10**((x - log_ic50) * hill)).

    ``log_ic50`` and ``log10_conc_M`` are log10 of molar concentration.
    With hill > 0 this falls from ``top`` (low concentration) to ``bottom``
    (high concentration). IC50 is the concentration at the mid-response of
    this model (inflection on the log-concentration axis).
    """
    return bottom + (top - bottom) / (1.0 + 10 ** ((log10_conc_M - log_ic50) * hill))

@dataclass
class FitResult:
    compound_id: str
    n_points: int
    top: float
    bottom: float
    hill: float
    ic50_M: float
    ic50_nM: float
    ic50_nM_ci_low: float
    ic50_nM_ci_high: float
    rmse: float
    flag_outside_range: bool
    conc_min_nM: float
    conc_max_nM: float
    status: str
    message: str


def _fit_one(
    conc_nM: np.ndarray,
    response: np.ndarray,
    compound_id: str,
    min_points: int = 5,
) -> FitResult:
    mask = np.isfinite(conc_nM) & np.isfinite(response) & (conc_nM > 0)
    conc_nM = conc_nM[mask]
    response = response[mask]
    conc_min = float(conc_nM.min()) if len(conc_nM) else np.nan
    conc_max = float(conc_nM.max()) if len(conc_nM) else np.nan

    empty = FitResult(
        compound_id=compound_id,
        n_points=int(len(conc_nM)),
        top=np.nan,
        bottom=np.nan,
        hill=np.nan,
        ic50_M=np.nan,
        ic50_nM=np.nan,
        ic50_nM_ci_low=np.nan,
        ic50_nM_ci_high=np.nan,
        rmse=np.nan,
        flag_outside_range=False,
        conc_min_nM=conc_min,
        conc_max_nM=conc_max,
        status="SKIPPED",
        message="insufficient_points",
    )
    if len(conc_nM) < min_points:
        return empty

    x = np.log10(conc_nM * 1e-9)
    y = response
    p0 = [float(np.nanmax(y)), float(np.nanmin(y)), float(np.median(x)), 1.0]
    bounds = ([0.0, -50.0, x.min() - 2, 0.1], [150.0, 150.0, x.max() + 2, 5.0])

    try:
        popt, pcov = curve_fit(
            four_param_logistic,
            x,
            y,
            p0=p0,
            bounds=bounds,
            maxfev=20000,
        )
    except (RuntimeError, ValueError) as exc:
        empty.status = "FAILED"
        empty.message = f"fit_error:{exc}"
        return empty

    top, bottom, log_ic50, hill = map(float, popt)
    ic50_M = 10 ** log_ic50
    ic50_nM = ic50_M * 1e9
    yhat = four_param_logistic(x, *popt)
    rmse = float(np.sqrt(np.mean((y - yhat) ** 2)))

    # Approximate Wald CI on log10(IC50), then transform.
    try:
        se_log = float(np.sqrt(pcov[2, 2]))
        if np.isfinite(se_log):
            lo = 10 ** (log_ic50 - 1.96 * se_log) * 1e9
            hi = 10 ** (log_ic50 + 1.96 * se_log) * 1e9
        else:
            lo = hi = np.nan
    except Exception:
        lo = hi = np.nan

    outside = bool(ic50_nM < conc_min or ic50_nM > conc_max)
    msg = "ok"
    if outside:
        msg = "ic50_outside_tested_concentration_range"

    return FitResult(
        compound_id=compound_id,
        n_points=int(len(conc_nM)),
        top=top,
        bottom=bottom,
        hill=hill,
        ic50_M=ic50_M,
        ic50_nM=ic50_nM,
        ic50_nM_ci_low=lo,
        ic50_nM_ci_high=hi,
        rmse=rmse,
        flag_outside_range=outside,
        conc_min_nM=conc_min,
        conc_max_nM=conc_max,
        status="OK",
        message=msg,
    )


def fit_compounds(
    normalized: pd.DataFrame,
    *,
    min_points: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit per compound using SAMPLE wells that passed QC.

    Technical replicates (same plate or across plates) are retained as
    individual observations; independence is NOT assumed for inference beyond
    the approximate parameter CI from the nonlinear least-squares covariance.
    """
    samples = normalized[
        (normalized["role"] == "SAMPLE")
        & (~normalized["exclude"])
        & normalized["percent_response"].notna()
        & normalized["concentration_nM"].notna()
    ].copy()

    fit_rows: list[dict] = []
    residual_rows: list[dict] = []

    for compound_id, g in samples.groupby("compound_id"):
        result = _fit_one(
            g["concentration_nM"].to_numpy(dtype=float),
            g["percent_response"].to_numpy(dtype=float),
            compound_id=str(compound_id),
            min_points=min_points,
        )
        fit_rows.append(result.__dict__)

        if result.status == "OK":
            x = np.log10(g["concentration_nM"].to_numpy(dtype=float) * 1e-9)
            y = g["percent_response"].to_numpy(dtype=float)
            yhat = four_param_logistic(x, result.top, result.bottom, np.log10(result.ic50_M), result.hill)
            for i, (_, row) in enumerate(g.iterrows()):
                residual_rows.append(
                    {
                        "compound_id": compound_id,
                        "plate_id": row["plate_id"],
                        "well": row["well"],
                        "sample_id": row["sample_id"],
                        "concentration_nM": row["concentration_nM"],
                        "percent_response": y[i],
                        "fitted": yhat[i],
                        "residual": y[i] - yhat[i],
                    }
                )

    return pd.DataFrame(fit_rows), pd.DataFrame(residual_rows)
