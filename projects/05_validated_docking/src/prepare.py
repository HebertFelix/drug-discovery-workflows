"""Prepare receptor/ligand PDBQT files and extract crystal ligand coords."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np


def split_receptor_ligand(
    pdb_path: Path,
    *,
    ligand_resname: str,
    chain: str = "A",
    out_dir: Path,
) -> tuple[Path, Path, np.ndarray]:
    """Write receptor.pdb and ligand_xtal.pdb; return ligand heavy-atom coords."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec: list[str] = []
    lig: list[str] = []
    coords: list[list[float]] = []
    for line in Path(pdb_path).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("ATOM") and len(line) > 21 and line[21] == chain:
            rec.append(line)
        elif line.startswith("HETATM") and len(line) > 21 and line[21] == chain:
            res = line[17:20].strip()
            if res == ligand_resname:
                lig.append(line)
                name = line[12:16].strip()
                el = "".join(c for c in name if c.isalpha())
                if el.upper().startswith("H"):
                    continue
                coords.append(
                    [float(line[30:38]), float(line[38:46]), float(line[46:54])]
                )
            elif res not in {"HOH", "WAT", "DOD"}:
                # drop other HET for rigid receptor simplicity
                pass
    if not lig:
        raise ValueError(f"Ligand {ligand_resname} not found in {pdb_path}")
    rec_path = out_dir / "receptor.pdb"
    lig_path = out_dir / "ligand_xtal.pdb"
    rec_path.write_text("\n".join(rec) + "\nEND\n", encoding="utf-8")
    lig_path.write_text("\n".join(lig) + "\nEND\n", encoding="utf-8")
    return rec_path, lig_path, np.asarray(coords, dtype=float)


def run_obabel(args: list[str]) -> None:
    subprocess.run(["obabel", *args], check=True, capture_output=True, text=True)


def pdb_to_pdbqt_receptor(pdb: Path, pdbqt: Path) -> Path:
    run_obabel([str(pdb), "-O", str(pdbqt), "-xr"])
    return pdbqt


def pdb_or_smi_to_pdbqt_ligand(src: Path, pdbqt: Path, *, ph: float = 7.4) -> Path:
    if src.suffix.lower() == ".smi" or src.suffix.lower() == ".smiles":
        run_obabel([str(src), "-O", str(pdbqt), "-p", str(ph), "--gen3d"])
    else:
        run_obabel([str(src), "-O", str(pdbqt), "-p", str(ph)])
    return pdbqt


def box_from_ligand(coords: np.ndarray, padding: float = 8.0) -> dict[str, float]:
    mins = coords.min(axis=0) - padding
    maxs = coords.max(axis=0) + padding
    center = coords.mean(axis=0)
    size = np.maximum(maxs - mins, 15.0)
    # Cap size to a reasonable pocket box
    size = np.minimum(size, 24.0)
    return {
        "center_x": float(center[0]),
        "center_y": float(center[1]),
        "center_z": float(center[2]),
        "size_x": float(size[0]),
        "size_y": float(size[1]),
        "size_z": float(size[2]),
    }
