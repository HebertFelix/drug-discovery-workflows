"""Symmetry-tolerant heavy-atom RMSD via Hungarian matching by element."""

from __future__ import annotations

from collections import defaultdict

import numpy as np
from scipy.optimize import linear_sum_assignment


def hungarian_rmsd(
    ref: list[tuple[str, list[float]]] | np.ndarray,
    mob: list[tuple[str, list[float]]],
) -> float:
    """Return RMSD after optimal assignment within each element type."""
    if isinstance(ref, np.ndarray):
        # assume carbons-only fallback not used; require typed list
        raise TypeError("ref must be list of (element, xyz)")

    ga: dict[str, list[np.ndarray]] = defaultdict(list)
    gb: dict[str, list[np.ndarray]] = defaultdict(list)
    for el, xyz in ref:
        ga[el].append(np.asarray(xyz, dtype=float))
    for el, xyz in mob:
        gb[el].append(np.asarray(xyz, dtype=float))
    if set(ga) != set(gb):
        raise ValueError(f"Element mismatch: {sorted(ga)} vs {sorted(gb)}")
    for el in ga:
        if len(ga[el]) != len(gb[el]):
            raise ValueError(f"Count mismatch for {el}: {len(ga[el])} vs {len(gb[el])}")

    sse = 0.0
    n = 0
    for el in ga:
        A = np.vstack(ga[el])
        B = np.vstack(gb[el])
        cost = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
        r, c = linear_sum_assignment(cost)
        sse += float((cost[r, c] ** 2).sum())
        n += len(r)
    return float(np.sqrt(sse / n)) if n else float("nan")


def typed_coords_from_pdb_het(path, resname: str | None = None) -> list[tuple[str, list[float]]]:
    atoms: list[tuple[str, list[float]]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("HETATM"):
            continue
        if resname and line[17:20].strip() != resname:
            continue
        name = line[12:16].strip()
        el = "".join(c for c in name if c.isalpha())
        el = el[0].upper() if el else "C"
        if el == "H":
            continue
        xyz = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
        atoms.append((el, xyz))
    return atoms
