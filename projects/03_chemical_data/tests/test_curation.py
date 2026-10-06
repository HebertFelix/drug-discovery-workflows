"""Tests for Project 03 curation policies."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.curate import curate_bioactivity, pic50_from_nM, to_nM
from src.generate_demo_data import generate

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def curated_bundle(tmp_path_factory):
    out = tmp_path_factory.mktemp("chem")
    path = generate(out)
    raw = pd.read_csv(path)
    return curate_bioactivity(raw)


def test_unit_conversion():
    assert to_nM(0.04, "uM") == pytest.approx(40.0)
    assert to_nM(100, "nM") == pytest.approx(100.0)


def test_pic50_100nM_is_7():
    assert pic50_from_nM(100.0) == pytest.approx(7.0)


def test_invalid_smiles_excluded(curated_bundle):
    assert (curated_bundle.exclusions["reason"] == "invalid_smiles").any()


def test_salt_duplicate_excluded(curated_bundle):
    assert (curated_bundle.exclusions["reason"] == "duplicate_inchikey_same_endpoint_context").any()


def test_endpoints_not_fused(curated_bundle):
    assays = set(curated_bundle.curated["assay_type"])
    assert "IC50" in assays
    assert "Ki" in assays
    assert "Kd" in assays


def test_censored_has_no_pic50(curated_bundle):
    cens = curated_bundle.curated.loc[curated_bundle.curated["relation"] != "="]
    assert cens["pActivity"].isna().all()


def test_um_converted(curated_bundle):
    flav = curated_bundle.curated.loc[curated_bundle.curated["name"] == "flavopiridol"].iloc[0]
    assert flav["value_nM"] == pytest.approx(40.0)
