"""Tests protecting scientific transforms for Project 01."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.curve_fit import fit_compounds, four_param_logistic
from src.generate_demo_data import generate
from src.normalize import normalize_plates, percent_response
from src.qc import run_qc, zprime

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def demo_data(tmp_path_factory):
    out = tmp_path_factory.mktemp("data")
    paths = generate(out, seed=20261006)
    readings = pd.read_csv(paths["readings"])
    plate_map = pd.read_csv(paths["plate_map"])
    return readings, plate_map


def test_units_are_single(demo_data):
    readings, _ = demo_data
    assert set(readings["readout_unit"]) == {"RFU"}


def test_identifiers_unique_per_plate_well(demo_data):
    _, plate_map = demo_data
    dup = plate_map.duplicated(subset=["plate_id", "well"]).sum()
    assert dup == 0


def test_zprime_perfect_controls():
    neg = np.array([1.0, 1.0, 1.0, 1.0])
    pos = np.array([0.0, 0.0, 0.0, 0.0])
    assert zprime(neg, pos) == pytest.approx(1.0)


def test_planted_edge_effect_is_detected(demo_data):
    readings, plate_map = demo_data
    qc = run_qc(readings, plate_map)
    assert not qc.exclusions.empty
    assert (qc.exclusions["reason"] == "edge_control_outlier").any()
    p02 = qc.plate_summary.loc[qc.plate_summary["plate_id"] == "P02"].iloc[0]
    # After excluding edge outliers, P02 should improve / pass.
    assert p02["edge_controls_excluded"] >= 1


def test_missing_readout_recorded(demo_data):
    readings, plate_map = demo_data
    qc = run_qc(readings, plate_map)
    assert (qc.exclusions["reason"] == "missing_readout").any()


def test_normalization_maps_controls():
    # Vehicle (neg) → ~100; inhibited (pos) → ~0
    assert percent_response(np.array([1.2]), 1.2, 0.3)[0] == pytest.approx(100.0)
    assert percent_response(np.array([0.3]), 1.2, 0.3)[0] == pytest.approx(0.0)


def test_normalization_rejects_collapsed_controls():
    with pytest.raises(ValueError):
        percent_response(np.array([1.0]), 1.0, 1.0)


def test_four_param_logistic_midpoint():
    # At x = log_ic50, response equals mid of top/bottom.
    y = four_param_logistic(np.array([-7.0]), top=100, bottom=0, log_ic50=-7.0, hill=1.0)
    assert y[0] == pytest.approx(50.0)


def test_fit_recovers_approximate_ic50(demo_data):
    readings, plate_map = demo_data
    qc = run_qc(readings, plate_map)
    normalized = normalize_plates(qc.merged, qc.plate_summary)
    fits, residuals = fit_compounds(normalized)
    assert not residuals.empty
    a = fits.loc[fits["compound_id"] == "CMP-A"].iloc[0]
    assert a["status"] == "OK"
    # True IC50 was 80 nM; allow broad tolerance for noise + two plates.
    assert 20 < a["ic50_nM"] < 300


def test_weak_compound_flagged_or_high_ic50(demo_data):
    readings, plate_map = demo_data
    qc = run_qc(readings, plate_map)
    normalized = normalize_plates(qc.merged, qc.plate_summary)
    fits, _ = fit_compounds(normalized)
    c = fits.loc[fits["compound_id"] == "CMP-C"].iloc[0]
    assert c["status"] == "OK"
    # True IC50 8000 nM near top of range — outside-range flag may or may not
    # trigger; require the estimate to be high.
    assert c["ic50_nM"] > 1000
