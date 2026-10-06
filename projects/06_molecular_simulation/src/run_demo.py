"""Run Project 06 production + analysis demo."""

from __future__ import annotations

import json
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import mdtraj as md
import pandas as pd
import yaml

from . import __version__
from .analyze import analyze_replica, load_traj
from .produce import prepare_topology, run_replica, write_run_table
from .report import write_md_report
from .visualize import rmsf_plot, series_plot

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run(config_path: Path | None = None) -> Path:
    config_path = config_path or (ROOT / "configs" / "demo.yaml")
    cfg = load_config(config_path)
    out_dir = ROOT / cfg["paths"]["output_dir"]
    work = out_dir / "workdir"
    out_dir.mkdir(parents=True, exist_ok=True)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    pdb_in = ROOT / cfg["paths"]["pdb"]
    top0 = work / "system_top.pdb"
    topology, positions = prepare_topology(pdb_in, top0)

    n_steps = int(cfg["production"]["n_steps"])
    dt = float(cfg["production"]["timestep_ps"])
    report_interval = int(cfg["production"]["report_interval"])
    dt_frame = dt * report_interval
    eq_ps = float(cfg["analysis"]["equilibration_ps"])
    prod_ps = n_steps * dt

    records = []
    for i, seed in enumerate(cfg["production"]["seeds"], start=1):
        rid = f"rep{i}"
        rec = run_replica(
            topology=topology,
            positions=positions,
            out_dir=work,
            replica_id=rid,
            n_steps=n_steps,
            report_interval=report_interval,
            temperature_K=float(cfg["production"]["temperature_K"]),
            friction_per_ps=float(cfg["production"]["friction_per_ps"]),
            timestep_ps=dt,
            seed=int(seed),
            minimize_iterations=int(cfg["production"]["minimize_iterations"]),
        )
        records.append(rec)
    write_run_table(records, out_dir / "production_runs.csv")

    # Reference = first replica topology after minimization
    reference = md.load_pdb(str(work / "rep1_top.pdb"))

    series_all = []
    rmsf_all = []
    summaries = []
    # Also keep full series including eq for plotting with eq line
    full_series = []
    for rec in records:
        bundle = load_traj(rec["topology"], rec["trajectory"], rec["replica_id"], dt_frame)
        # full series for plot (before discard)
        from .analyze import backbone_hbonds_fraction, radius_of_gyration, rmsd_ca

        full_series.append(
            pd.DataFrame(
                {
                    "replica_id": bundle.replica_id,
                    "time_ps": bundle.time_ps,
                    "rmsd_ca_nm": rmsd_ca(bundle, reference),
                    "rg_nm": radius_of_gyration(bundle),
                    "n_hbonds_wernet": backbone_hbonds_fraction(bundle),
                }
            )
        )
        series, rmsf, summary = analyze_replica(bundle, reference, eq_ps=eq_ps)
        series_all.append(series)
        rmsf_all.append(rmsf)
        summaries.append(summary)

    series_df = pd.concat(series_all, ignore_index=True)
    rmsf_df = pd.concat(rmsf_all, ignore_index=True)
    full_df = pd.concat(full_series, ignore_index=True)
    series_df.to_csv(out_dir / "series_production.csv", index=False)
    full_df.to_csv(out_dir / "series_full.csv", index=False)
    rmsf_df.to_csv(out_dir / "rmsf_ca.csv", index=False)

    summary_rows = []
    for s in summaries:
        summary_rows.append(
            {
                "replica_id": s["replica_id"],
                "n_frames_production": s["n_frames_production"],
                "rmsd_mean_nm": s["rmsd"]["mean"],
                "rmsd_block_se_nm": s["rmsd"]["se"],
                "rg_mean_nm": s["rg"]["mean"],
                "rg_block_se_nm": s["rg"]["se"],
                "hbonds_mean": s["hbonds"]["mean"],
                "hbonds_block_se": s["hbonds"]["se"],
                "rmsd_tau_int_frames": s["rmsd_autocorr_time_frames"],
            }
        )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(out_dir / "replica_summary.csv", index=False)
    (out_dir / "analysis_summaries.json").write_text(json.dumps(summaries, indent=2), encoding="utf-8")

    series_plot(full_df, out_dir / "series_plot.png", eq_ps=eq_ps)
    rmsf_plot(rmsf_df, out_dir / "rmsf_plot.png")

    protocol = {
        "system": "Trp-cage / PDB 1L2Y (waters removed), implicit solvent demo",
        "forcefield": "amber14-all.xml + implicit/obc2.xml",
        "temperature_K": cfg["production"]["temperature_K"],
        "timestep_ps": dt,
        "n_steps": n_steps,
        "prod_ps": prod_ps,
        "eq_ps": eq_ps,
        "seeds": cfg["production"]["seeds"],
    }
    write_md_report(
        out_dir / "md_report.md",
        protocol=protocol,
        summary_rows=summary_df,
        caveats=[
            "Implicit solvent omits explicit water structure and viscosity effects.",
            "Demo length is pedagogical (tens of ps), not converged conformational sampling.",
            "H-bond counts depend on geometric criteria (Wernet–Nilsson) and are not populations from enhanced sampling.",
            "This entry point emphasizes analysis discipline; full protein–ligand production MD is an advanced track.",
        ],
    )

    manifest = {
        "project": "06_molecular_simulation",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "protocol": protocol,
        "outputs": sorted(p.name for p in out_dir.iterdir() if p.is_file()),
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Demo complete → {out_dir}")
    print(summary_df.to_string(index=False))
    return out_dir


if __name__ == "__main__":
    run()
