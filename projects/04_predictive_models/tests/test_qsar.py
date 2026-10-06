"""Tests for Project 04 QSAR demo."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.curate_qsar import prepare_modeling_table, to_nM
from src.metrics import regression_metrics
from src.splits import random_split, scaffold_split, split_overlap_report

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def modeling():
    raw = pd.read_csv(ROOT / "data/example/raw_chembl_cdk2_ic50.csv")
    df, _ = prepare_modeling_table(raw)
    return df


def test_unit_helper():
    assert to_nM(1.0, "uM") == pytest.approx(1000.0)


def test_modeling_table_has_unique_inchikeys(modeling):
    assert modeling["inchikey"].is_unique
    assert len(modeling) >= 50
    assert modeling["pIC50"].between(0, 12).all()


def test_only_point_ic50_in_modeling(modeling):
    # Aggregation already filtered censored; pIC50 finite
    assert modeling["pIC50"].notna().all()


def test_scaffold_split_reduces_shared_scaffolds(modeling):
    tr_r, te_r = random_split(modeling, test_size=0.25, seed=1)
    tr_s, te_s = scaffold_split(modeling, test_size=0.25, seed=1)
    ov_r = split_overlap_report(modeling, tr_r, te_r)
    ov_s = split_overlap_report(modeling, tr_s, te_s)
    assert ov_s["n_shared_scaffolds"] <= ov_r["n_shared_scaffolds"]
    assert ov_s["n_shared_scaffolds"] == 0 or ov_s["shared_scaffold_fraction_of_test"] < ov_r["shared_scaffold_fraction_of_test"]


def test_regression_metrics_perfect():
    y = np.array([1.0, 2.0, 3.0])
    m = regression_metrics(y, y)
    assert m["MAE"] == pytest.approx(0.0)
    assert m["RMSE"] == pytest.approx(0.0)
    assert m["R2"] == pytest.approx(1.0)


def test_train_test_disjoint_indices(modeling):
    tr, te = scaffold_split(modeling, test_size=0.25, seed=20261006)
    assert len(set(tr) & set(te)) == 0
    assert len(tr) + len(te) == len(modeling)
