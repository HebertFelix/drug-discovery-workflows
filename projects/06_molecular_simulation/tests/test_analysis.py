"""Tests for Project 06 analysis helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from src.analyze import (
    autocorrelation,
    block_standard_error,
    discard_equilibration,
    integrated_autocorr_time,
)
from src.analyze import TrajBundle
import mdtraj as md

ROOT = Path(__file__).resolve().parents[1]


def test_autocorr_white_noise_decays_fast():
    rng = np.random.default_rng(0)
    x = rng.normal(size=500)
    ac = autocorrelation(x, max_lag=20)
    assert ac[0] == pytest.approx(1.0)
    assert abs(ac[1]) < 0.2


def test_integrated_tau_positive_for_persistent_signal():
    t = np.linspace(0, 20, 400)
    x = np.sin(0.3 * t) + 0.05 * np.random.default_rng(1).normal(size=len(t))
    tau = integrated_autocorr_time(autocorrelation(x))
    assert tau >= 1.0


def test_block_se_known():
    x = np.ones(100)
    out = block_standard_error(x, n_blocks=5)
    assert out["mean"] == pytest.approx(1.0)
    assert out["se"] == pytest.approx(0.0)


def test_discard_equilibration_requires_frames():
    top = md.Topology()
    # minimal fake traj via 1L2Y if available
    pdb = ROOT / "data/example/1L2Y.pdb"
    traj = md.load_pdb(str(pdb))
    # single frame repeated
    traj = traj.join([traj] * 10) if hasattr(traj, 'join') else md.join([traj] * 10)
    bundle = TrajBundle("r", traj, np.linspace(0, 1, traj.n_frames))
    with pytest.raises(ValueError):
        discard_equilibration(bundle, eq_ps=5.0)


def test_pdb_present():
    assert (ROOT / "data/example/1L2Y.pdb").exists()


@pytest.mark.integration
def test_full_demo_runs():
    from src.run_demo import run

    out = run()
    assert (out / "md_report.md").exists()
    assert (out / "replica_summary.csv").exists()
    import pandas as pd

    summary = pd.read_csv(out / "replica_summary.csv")
    assert len(summary) == 2
    assert (summary["n_frames_production"] > 0).all()
