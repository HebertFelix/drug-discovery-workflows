"""Tests for Project 05 docking helpers (RMSD + enrichment)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.rmsd import hungarian_rmsd
from src.screening import enrichment_factor

ROOT = Path(__file__).resolve().parents[1]


def test_hungarian_rmsd_identity():
    atoms = [("C", [0.0, 0.0, 0.0]), ("N", [1.0, 0.0, 0.0]), ("C", [0.0, 1.0, 0.0])]
    assert hungarian_rmsd(atoms, atoms) == pytest.approx(0.0)


def test_hungarian_rmsd_permutation():
    ref = [("C", [0.0, 0.0, 0.0]), ("C", [1.0, 0.0, 0.0])]
    mob = [("C", [1.0, 0.0, 0.0]), ("C", [0.0, 0.0, 0.0])]
    assert hungarian_rmsd(ref, mob) == pytest.approx(0.0)


def test_enrichment_perfect():
    ranks = pd.DataFrame(
        {
            "name": list("ABCDEF"),
            "label": ["active", "active", "decoy", "decoy", "decoy", "decoy"],
            "score": [-10, -9, -1, 0, 1, 2],
        }
    )
    ef = enrichment_factor(ranks, early_fraction=1 / 3)
    assert ef["actives_in_top_k"] == 2
    assert ef["EF"] == pytest.approx(3.0)


def test_complex_file_present():
    assert (ROOT / "data/example/1AQ1_chainA.pdb").exists()
    assert (ROOT / "data/example/screen_library.csv").exists()


@pytest.mark.integration
def test_redock_rmsd_under_threshold():
    """Optional integration test when vina/obabel are installed."""
    import shutil

    if shutil.which("vina") is None or shutil.which("obabel") is None:
        pytest.skip("vina/obabel not available")
    from src.run_demo import run

    out = run()
    summary = json_load(out / "redock_summary.json")
    assert summary["rmsd_A"] <= 2.0
    assert summary["success"] is True


def json_load(path: Path):
    import json

    return json.loads(path.read_text(encoding="utf-8"))
