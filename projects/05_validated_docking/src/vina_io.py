"""AutoDock Vina runner and PDBQT pose parsing."""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VinaPose:
    mode: int
    affinity: float
    rmsd_lb: float
    rmsd_ub: float
    lines: list[str]


def find_vina() -> str:
    path = shutil.which("vina")
    if not path:
        raise RuntimeError("AutoDock Vina executable `vina` not found on PATH")
    return path


def write_config(
    path: Path,
    *,
    receptor: Path,
    ligand: Path,
    box: dict[str, float],
    exhaustiveness: int,
    num_modes: int,
    seed: int,
) -> Path:
    text = f"""receptor = {receptor}
ligand = {ligand}
center_x = {box['center_x']:.3f}
center_y = {box['center_y']:.3f}
center_z = {box['center_z']:.3f}
size_x = {box['size_x']:.3f}
size_y = {box['size_y']:.3f}
size_z = {box['size_z']:.3f}
exhaustiveness = {exhaustiveness}
num_modes = {num_modes}
energy_range = 4
seed = {seed}
"""
    path = Path(path)
    path.write_text(text, encoding="utf-8")
    return path


def run_vina(config: Path, out_pdbqt: Path, log_path: Path) -> str:
    vina = find_vina()
    cmd = [vina, "--config", str(config), "--out", str(out_pdbqt)]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    log_path.write_text(proc.stdout + "\n" + proc.stderr, encoding="utf-8")
    return proc.stdout


def parse_poses(pdbqt_path: Path) -> list[VinaPose]:
    text = Path(pdbqt_path).read_text(encoding="utf-8", errors="replace").splitlines()
    poses: list[VinaPose] = []
    mode = None
    affinity = rmsd_lb = rmsd_ub = None
    lines: list[str] = []
    header_re = re.compile(
        r"REMARK VINA RESULT:\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)"
    )
    for line in text:
        if line.startswith("MODEL"):
            mode = int(line.split()[1])
            lines = []
            affinity = rmsd_lb = rmsd_ub = None
        elif line.startswith("REMARK VINA RESULT:"):
            m = header_re.search(line)
            if m:
                affinity, rmsd_lb, rmsd_ub = map(float, m.groups())
        elif line.startswith("ENDMDL"):
            if mode is not None and affinity is not None:
                poses.append(
                    VinaPose(mode, affinity, float(rmsd_lb), float(rmsd_ub), lines[:])
                )
        else:
            lines.append(line)
    return poses


def pose_heavy_coords(pose: VinaPose) -> list[tuple[str, list[float]]]:
    atoms: list[tuple[str, list[float]]] = []
    for line in pose.lines:
        if not line.startswith(("ATOM", "HETATM")):
            continue
        atype = line.split()[-1]
        el = "".join(c for c in atype if c.isalpha()).upper()
        el = {"A": "C", "OA": "O", "NA": "N", "SA": "S"}.get(el, el[:1])
        if el == "H" or el == "HD":
            continue
        xyz = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
        atoms.append((el, xyz))
    return atoms
