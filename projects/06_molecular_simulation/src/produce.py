"""Produce short OpenMM trajectories for the Project 06 demo (Trp-cage 1L2Y)."""

from __future__ import annotations

import csv
from pathlib import Path

from openmm import LangevinMiddleIntegrator, Platform, unit
from openmm.app import (
    DCDReporter,
    ForceField,
    HBonds,
    Modeller,
    NoCutoff,
    PDBFile,
    Simulation,
    StateDataReporter,
)


def prepare_topology(pdb_path: Path, out_pdb: Path) -> tuple:
    pdb = PDBFile(str(pdb_path))
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.deleteWater()
    PDBFile.writeFile(modeller.topology, modeller.positions, open(out_pdb, "w"))
    return modeller.topology, modeller.positions


def run_replica(
    *,
    topology,
    positions,
    out_dir: Path,
    replica_id: str,
    n_steps: int,
    report_interval: int,
    temperature_K: float,
    friction_per_ps: float,
    timestep_ps: float,
    seed: int,
    minimize_iterations: int,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ff = ForceField("amber14-all.xml", "implicit/obc2.xml")
    system = ff.createSystem(topology, nonbondedMethod=NoCutoff, constraints=HBonds)
    integrator = LangevinMiddleIntegrator(
        temperature_K * unit.kelvin,
        friction_per_ps / unit.picosecond,
        timestep_ps * unit.picoseconds,
    )
    integrator.setRandomNumberSeed(int(seed))
    platform = Platform.getPlatformByName("CPU")
    sim = Simulation(topology, system, integrator, platform)
    sim.context.setPositions(positions)
    sim.minimizeEnergy(maxIterations=int(minimize_iterations))

    top_path = out_dir / f"{replica_id}_top.pdb"
    dcd_path = out_dir / f"{replica_id}_traj.dcd"
    log_path = out_dir / f"{replica_id}_log.csv"
    PDBFile.writeFile(
        sim.topology,
        sim.context.getState(getPositions=True).getPositions(),
        open(top_path, "w"),
    )
    sim.reporters.clear()
    sim.reporters.append(DCDReporter(str(dcd_path), int(report_interval)))
    sim.reporters.append(
        StateDataReporter(
            str(log_path),
            int(report_interval),
            step=True,
            time=True,
            potentialEnergy=True,
            temperature=True,
            speed=True,
        )
    )
    sim.step(int(n_steps))
    return {
        "replica_id": replica_id,
        "topology": str(top_path),
        "trajectory": str(dcd_path),
        "log": str(log_path),
        "n_steps": int(n_steps),
        "timestep_ps": float(timestep_ps),
        "report_interval": int(report_interval),
        "seed": int(seed),
        "temperature_K": float(temperature_K),
        "forcefield": "amber14-all.xml + implicit/obc2.xml",
        "solvent_model": "OBC2 implicit",
        "platform": "CPU",
    }


def write_run_table(records: list[dict], path: Path) -> Path:
    path = Path(path)
    if not records:
        path.write_text("", encoding="utf-8")
        return path
    fields = list(records[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(records)
    return path
