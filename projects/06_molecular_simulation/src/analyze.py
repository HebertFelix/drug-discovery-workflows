"""Trajectory observables with equilibration discard and uncertainty."""

from __future__ import annotations

from dataclasses import dataclass

import mdtraj as md
import numpy as np
import pandas as pd


@dataclass
class TrajBundle:
    replica_id: str
    traj: md.Trajectory
    time_ps: np.ndarray


def load_traj(topology: str, trajectory: str, replica_id: str, dt_ps: float) -> TrajBundle:
    traj = md.load(trajectory, top=topology)
    time = np.arange(traj.n_frames, dtype=float) * dt_ps
    return TrajBundle(replica_id=replica_id, traj=traj, time_ps=time)


def discard_equilibration(bundle: TrajBundle, eq_ps: float) -> TrajBundle:
    keep = bundle.time_ps >= eq_ps
    if keep.sum() < 5:
        raise ValueError(
            f"Too few frames after discarding {eq_ps} ps equilibration "
            f"(replica {bundle.replica_id})"
        )
    return TrajBundle(
        replica_id=bundle.replica_id,
        traj=bundle.traj[keep],
        time_ps=bundle.time_ps[keep],
    )


def rmsd_ca(bundle: TrajBundle, reference: md.Trajectory) -> np.ndarray:
    ca = bundle.traj.topology.select("name CA")
    return md.rmsd(bundle.traj, reference, atom_indices=ca)


def rmsf_ca(bundle: TrajBundle) -> tuple[np.ndarray, np.ndarray]:
    ca = bundle.traj.topology.select("name CA")
    # align to first production frame
    bundle.traj.superpose(bundle.traj, 0, atom_indices=ca)
    rmsf = md.rmsf(bundle.traj, bundle.traj, 0, atom_indices=ca)
    resSeq = np.array([bundle.traj.topology.atom(i).residue.resSeq for i in ca])
    return resSeq, rmsf


def radius_of_gyration(bundle: TrajBundle) -> np.ndarray:
    return md.compute_rg(bundle.traj)


def backbone_hbonds_fraction(bundle: TrajBundle) -> np.ndarray:
    """Per-frame count of backbone H-bonds (Baker-Hubbard), not a free-energy."""
    hbonds = md.baker_hubbard(bundle.traj, periodic=False)
    # baker_hubbard returns bonds present in the ensemble; compute occupancy via compute_contacts-like
    # Use wernet_nilsson for per-frame instead
    per_frame = md.wernet_nilsson(bundle.traj, periodic=False)
    return np.array([len(frame) for frame in per_frame], dtype=float)


def autocorrelation(x: np.ndarray, max_lag: int | None = None) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    n = len(x)
    if n < 3:
        return np.array([1.0])
    max_lag = max_lag or min(n // 2, 200)
    var = np.dot(x, x) / n
    if var <= 0:
        return np.ones(max_lag + 1)
    ac = np.empty(max_lag + 1, dtype=float)
    ac[0] = 1.0
    for lag in range(1, max_lag + 1):
        ac[lag] = np.dot(x[:-lag], x[lag:]) / (n - lag) / var
    return ac


def integrated_autocorr_time(ac: np.ndarray) -> float:
    """Rough τ_int ≈ 1 + 2 Σ ρ(k) until first non-positive ρ (teaching estimator)."""
    s = 0.0
    for rho in ac[1:]:
        if rho <= 0:
            break
        s += rho
    return float(1.0 + 2.0 * s)


def block_standard_error(x: np.ndarray, n_blocks: int = 5) -> dict:
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < n_blocks:
        n_blocks = max(1, n // 2)
    block = n // n_blocks
    if block < 1:
        return {"mean": float(x.mean()), "se": float("nan"), "n_blocks": 0, "block_size": 0}
    means = np.array([x[i * block : (i + 1) * block].mean() for i in range(n_blocks)])
    se = float(means.std(ddof=1) / np.sqrt(len(means))) if len(means) > 1 else float("nan")
    return {
        "mean": float(x.mean()),
        "se": se,
        "n_blocks": int(len(means)),
        "block_size": int(block),
    }


def analyze_replica(
    bundle: TrajBundle,
    reference: md.Trajectory,
    *,
    eq_ps: float,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    prod = discard_equilibration(bundle, eq_ps)
    rmsd = rmsd_ca(prod, reference)
    rg = radius_of_gyration(prod)
    hb = backbone_hbonds_fraction(prod)
    resSeq, rmsf = rmsf_ca(prod)

    series = pd.DataFrame(
        {
            "replica_id": prod.replica_id,
            "frame": np.arange(len(prod.time_ps)),
            "time_ps": prod.time_ps,
            "rmsd_ca_nm": rmsd,
            "rg_nm": rg,
            "n_hbonds_wernet": hb,
        }
    )
    rmsf_df = pd.DataFrame(
        {
            "replica_id": prod.replica_id,
            "resSeq": resSeq,
            "rmsf_ca_nm": rmsf,
        }
    )

    ac = autocorrelation(rmsd)
    tau = integrated_autocorr_time(ac)
    summary = {
        "replica_id": prod.replica_id,
        "n_frames_production": int(len(prod.time_ps)),
        "eq_discard_ps": float(eq_ps),
        "rmsd": block_standard_error(rmsd),
        "rg": block_standard_error(rg),
        "hbonds": block_standard_error(hb),
        "rmsd_autocorr_time_frames": tau,
        "note": (
            "Block SE respects temporal grouping better than treating every frame "
            "as independent; successive frames are correlated."
        ),
    }
    return series, rmsf_df, summary
