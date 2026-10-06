"""Run Project 05 docking validation demo."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from . import __version__
from .prepare import (
    box_from_ligand,
    pdb_or_smi_to_pdbqt_ligand,
    pdb_to_pdbqt_receptor,
    split_receptor_ligand,
)
from .report import write_docking_report
from .rmsd import hungarian_rmsd, typed_coords_from_pdb_het
from .screening import enrichment_factor
from .vina_io import find_vina, parse_poses, pose_heavy_coords, run_vina, write_config
from .visualize import redock_summary_fig, score_distribution

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def vina_version() -> str:
    out = subprocess.run([find_vina(), "--version"], capture_output=True, text=True, check=True)
    return out.stdout.strip().splitlines()[0]


def run(config_path: Path | None = None) -> Path:
    config_path = config_path or (ROOT / "configs" / "demo.yaml")
    cfg = load_config(config_path)
    out_dir = ROOT / cfg["paths"]["output_dir"]
    work = out_dir / "workdir"
    out_dir.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)

    pdb_path = ROOT / cfg["paths"]["complex_pdb"]
    rec_pdb, lig_pdb, lig_coords = split_receptor_ligand(
        pdb_path,
        ligand_resname=cfg["ligand_resname"],
        chain=cfg.get("chain", "A"),
        out_dir=work,
    )
    rec_pdbqt = pdb_to_pdbqt_receptor(rec_pdb, work / "receptor.pdbqt")
    lig_pdbqt = pdb_or_smi_to_pdbqt_ligand(lig_pdb, work / "ligand_stu.pdbqt", ph=float(cfg["ph"]))
    box = box_from_ligand(lig_coords, padding=float(cfg["box_padding"]))

    conf = write_config(
        work / "vina_redock.conf",
        receptor=rec_pdbqt,
        ligand=lig_pdbqt,
        box=box,
        exhaustiveness=int(cfg["exhaustiveness"]),
        num_modes=int(cfg["num_modes"]),
        seed=int(cfg["seed"]),
    )
    run_vina(conf, work / "redocked.pdbqt", work / "redock.log")
    poses = parse_poses(work / "redocked.pdbqt")
    if not poses:
        raise RuntimeError("No poses parsed from Vina output")
    best = poses[0]
    ref_atoms = typed_coords_from_pdb_het(lig_pdb, resname=cfg["ligand_resname"])
    mob_atoms = pose_heavy_coords(best)
    rmsd = hungarian_rmsd(ref_atoms, mob_atoms)
    redock = {
        "affinity": best.affinity,
        "rmsd_A": rmsd,
        "success": bool(rmsd <= float(cfg["rmsd_success_threshold"])),
        "n_modes": len(poses),
    }
    pd.DataFrame(
        [
            {
                "mode": p.mode,
                "affinity": p.affinity,
                "rmsd_lb": p.rmsd_lb,
                "rmsd_ub": p.rmsd_ub,
            }
            for p in poses
        ]
    ).to_csv(out_dir / "redock_modes.csv", index=False)
    (out_dir / "redock_summary.json").write_text(json.dumps(redock, indent=2), encoding="utf-8")
    redock_summary_fig(rmsd, best.affinity, out_dir / "redock_summary.png")

    # Tiny screen
    lib = pd.read_csv(ROOT / cfg["paths"]["screen_library"])
    rows = []
    for _, row in lib.iterrows():
        name = row["name"]
        if row["smiles"] == "FROM_CRYSTAL":
            ligand_qt = lig_pdbqt
        else:
            smi_path = work / f"{name}.smi"
            smi_path.write_text(f"{row['smiles']} {name}\n", encoding="utf-8")
            ligand_qt = work / f"{name}.pdbqt"
            pdb_or_smi_to_pdbqt_ligand(smi_path, ligand_qt, ph=float(cfg["ph"]))
        conf_i = write_config(
            work / f"vina_{name}.conf",
            receptor=rec_pdbqt,
            ligand=ligand_qt,
            box=box,
            exhaustiveness=int(cfg["exhaustiveness"]),
            num_modes=1,
            seed=int(cfg["seed"]),
        )
        out_i = work / f"docked_{name}.pdbqt"
        run_vina(conf_i, out_i, work / f"docked_{name}.log")
        pose_i = parse_poses(out_i)[0]
        rows.append(
            {
                "name": name,
                "label": row["label"],
                "score": pose_i.affinity,
                "note": row.get("note", ""),
            }
        )
    ranks = pd.DataFrame(rows).sort_values("score").reset_index(drop=True)
    ranks.to_csv(out_dir / "screen_ranks.csv", index=False)
    enrichment = enrichment_factor(ranks, early_fraction=float(cfg["enrichment_fraction"]))
    (out_dir / "enrichment.json").write_text(json.dumps(enrichment, indent=2), encoding="utf-8")
    score_distribution(ranks, out_dir / "score_distribution.png")

    protocol = {
        "receptor_source": str(cfg["paths"]["complex_pdb"]),
        "ligand_resname": cfg["ligand_resname"],
        "ph": cfg["ph"],
        "vina_version": vina_version(),
        "center": f"{box['center_x']:.2f}, {box['center_y']:.2f}, {box['center_z']:.2f}",
        "size": f"{box['size_x']:.2f}, {box['size_y']:.2f}, {box['size_z']:.2f}",
        "exhaustiveness": cfg["exhaustiveness"],
        "seed": cfg["seed"],
    }
    write_docking_report(
        out_dir / "docking_report.md",
        protocol=protocol,
        redock=redock,
        ranks=ranks,
        enrichment=enrichment,
    )

    manifest = {
        "project": "05_validated_docking",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "vina": vina_version(),
        "redock": redock,
        "enrichment": enrichment,
        "outputs": sorted(p.name for p in out_dir.iterdir() if p.is_file()),
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Demo complete → {out_dir}")
    print(f"  redock RMSD={rmsd:.3f} Å success={redock['success']} score={best.affinity}")
    print(f"  enrichment EF={enrichment.get('EF')}")
    return out_dir


if __name__ == "__main__":
    run()
