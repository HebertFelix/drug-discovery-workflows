"""Run Project 03 chemical curation demo."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from . import __version__
from .curate import curate_bioactivity, morgan_fingerprint_matrix
from .generate_demo_data import generate
from .report import write_curation_report
from .visualize import pca_fingerprint_plot, property_distributions

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run(config_path: Path | None = None) -> Path:
    config_path = config_path or (ROOT / "configs" / "demo.yaml")
    cfg = load_config(config_path)
    data_dir = ROOT / "data" / "example"
    generate(data_dir)

    raw = pd.read_csv(ROOT / cfg["paths"]["raw"])
    out_dir = ROOT / cfg["paths"]["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    result = curate_bioactivity(raw)
    result.curated.to_csv(out_dir / "curated_bioactivity.csv", index=False)
    result.exclusions.to_csv(out_dir / "exclusions.csv", index=False)
    result.dictionary.to_csv(out_dir / "data_dictionary.csv", index=False)

    property_distributions(result.curated, out_dir / "property_distributions.png")
    fp = morgan_fingerprint_matrix(
        result.curated["smiles_canonical"].tolist(),
        n_bits=int(cfg["fingerprint"]["n_bits"]),
        radius=int(cfg["fingerprint"]["radius"]),
    )
    _, proj = pca_fingerprint_plot(result.curated, fp, out_dir / "chemical_space_pca.png")
    if not proj.empty:
        proj.to_csv(out_dir / "pca_projection.csv", index=False)

    write_curation_report(
        out_dir / "curation_report.md",
        curated=result.curated,
        exclusions=result.exclusions,
        dictionary=result.dictionary,
    )

    manifest = {
        "project": "03_chemical_data",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": str(config_path.relative_to(ROOT)),
        "python": sys.version,
        "platform": platform.platform(),
        "n_raw": int(len(raw)),
        "n_curated": int(len(result.curated)),
        "n_excluded": int(len(result.exclusions)),
        "outputs": sorted(p.name for p in out_dir.iterdir() if p.is_file()),
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Demo complete → {out_dir}")
    print(f"  curated={manifest['n_curated']} excluded={manifest['n_excluded']}")
    return out_dir


if __name__ == "__main__":
    run()
