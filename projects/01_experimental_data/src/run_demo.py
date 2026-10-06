"""Run the Project 01 demonstration end-to-end."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from . import __version__
from .curve_fit import fit_compounds
from .generate_demo_data import generate
from .normalize import normalize_plates
from .qc import run_qc
from .report import write_qc_report
from .visualize import dose_response_curves, plate_heatmap, residual_plot

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run(config_path: Path | None = None) -> Path:
    config_path = config_path or (ROOT / "configs" / "demo.yaml")
    cfg = load_config(config_path)

    data_dir = ROOT / "data" / "example"
    # Always regenerate so the planted failure stays consistent with the seed.
    generate(data_dir, seed=int(cfg["seed"]))

    readings = pd.read_csv(ROOT / cfg["paths"]["readings"])
    plate_map = pd.read_csv(ROOT / cfg["paths"]["plate_map"])
    out_dir = ROOT / cfg["paths"]["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    qc = run_qc(
        readings,
        plate_map,
        max_missing_fraction=float(cfg["qc"]["max_missing_fraction"]),
        min_zprime=float(cfg["qc"]["min_zprime"]),
        edge_columns=list(cfg["qc"]["edge_columns"]),
        edge_control_cv_threshold=float(cfg["qc"]["edge_control_cv_threshold"]),
    )

    normalized = normalize_plates(qc.merged, qc.plate_summary)
    fits, residuals = fit_compounds(
        normalized,
        min_points=int(cfg["fitting"]["min_points"]),
    )

    # Persist tables
    normalized.to_csv(out_dir / "normalized_readings.csv", index=False)
    qc.exclusions.to_csv(out_dir / "exclusions.csv", index=False)
    qc.plate_summary.to_csv(out_dir / "plate_summary.csv", index=False)
    fits.to_csv(out_dir / "fit_parameters.csv", index=False)
    residuals.to_csv(out_dir / "fit_residuals.csv", index=False)

    plate_heatmap(qc.merged, out_dir / "plate_heatmap.png")
    if not residuals.empty:
        dose_response_curves(residuals, fits, out_dir / "dose_response_curves.png")
        residual_plot(residuals, out_dir / "fit_residuals.png")

    write_qc_report(
        out_dir / "qc_report.md",
        plate_summary=qc.plate_summary,
        exclusions=qc.exclusions,
        fits=fits,
        messages=qc.messages,
        ic50_definition=cfg["fitting"]["ic50_definition"],
    )

    manifest = {
        "project": "01_experimental_data",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seed": cfg["seed"],
        "config": str(config_path.relative_to(ROOT)),
        "python": sys.version,
        "platform": platform.platform(),
        "packages": {
            "pandas": pd.__version__,
        },
        "outputs": sorted(p.name for p in out_dir.iterdir() if p.is_file()),
        "qc_messages": qc.messages,
    }
    (out_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print(f"Demo complete → {out_dir}")
    for line in qc.messages:
        print(f"  QC: {line}")
    return out_dir


if __name__ == "__main__":
    run()
