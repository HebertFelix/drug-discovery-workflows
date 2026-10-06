"""Audit experimental structure coordinates vs sequence."""

from __future__ import annotations

from pathlib import Path


def parse_pdb_chain_residues(path: Path, chain: str = "A") -> dict:
    """Return observed residue numbers, missing relative to SEQRES if present."""
    seqres: list[str] = []
    observed: set[int] = set()
    atoms = 0
    het_resnames: set[str] = set()
    with Path(path).open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("SEQRES") and len(line) > 11 and line[11] == chain:
                seqres.extend(line[19:].split())
            elif line.startswith("ATOM") and len(line) > 21 and line[21] == chain:
                atoms += 1
                try:
                    observed.add(int(line[22:26]))
                except ValueError:
                    pass
            elif line.startswith("HETATM") and len(line) > 21 and line[21] == chain:
                resname = line[17:20].strip()
                if resname not in {"HOH", "DOD", "WAT"}:
                    het_resnames.add(resname)

    observed_sorted = sorted(observed)
    missing: list[int] = []
    if observed_sorted:
        full = set(range(observed_sorted[0], observed_sorted[-1] + 1))
        missing = sorted(full - observed)
    return {
        "chain": chain,
        "n_atom_records": atoms,
        "n_observed_residues": len(observed),
        "residue_min": observed_sorted[0] if observed_sorted else None,
        "residue_max": observed_sorted[-1] if observed_sorted else None,
        "missing_residues_in_span": missing,
        "n_seqres_residues": len(seqres) if seqres else None,
        "het_resnames": sorted(het_resnames),
    }
