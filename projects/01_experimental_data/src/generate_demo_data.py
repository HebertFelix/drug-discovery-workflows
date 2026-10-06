"""Generate a small simulated 96-well assay dataset with a planted QC failure.

The dataset is explicitly labeled as SIMULATED. Plate P02 includes an edge
effect that inflates negative-control wells in columns 1 and 12.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROWS = list("ABCDEFGH")
COLS = list(range(1, 13))


def _well_id(row: str, col: int) -> str:
    return f"{row}{col:02d}"


def generate(
    output_dir: Path,
    seed: int = 20261006,
) -> dict[str, Path]:
    rng = np.random.default_rng(seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Three compounds with true IC50 in nM; one weak (mostly outside range).
    compounds = {
        "CMP-A": {"true_ic50_nM": 80.0, "hill": 1.1, "max_inhibition": 0.95},
        "CMP-B": {"true_ic50_nM": 350.0, "hill": 1.4, "max_inhibition": 0.90},
        "CMP-C": {"true_ic50_nM": 8000.0, "hill": 0.9, "max_inhibition": 0.70},
    }
    concentrations_nM = np.array([3, 10, 30, 100, 300, 1000, 3000, 10000], dtype=float)

    plate_maps: list[dict] = []
    readings: list[dict] = []
    metadata: list[dict] = []

    # Layout per plate (96-well):
    # Col 1: NEG controls (vehicle)
    # Col 12: POS controls (reference inhibitor at saturating conc.)
    # Cols 2-9: concentration series for compounds (rows A-C / D-F duplicates)
    # Cols 10-11: blanks / unused buffer
    for plate_idx, plate_id in enumerate(["P01", "P02"]):
        batch = f"BATCH-{plate_idx + 1}"
        plate_shift = rng.normal(0.0, 0.03)  # mild plate-to-plate offset

        for r_i, row in enumerate(ROWS):
            for col in COLS:
                well = _well_id(row, col)
                role = "UNUSED"
                sample_id = ""
                compound_id = ""
                conc_nM = np.nan
                replicate = ""

                if col == 1:
                    role = "NEG_CTRL"
                    sample_id = f"{plate_id}-NEG-{row}"
                elif col == 12:
                    role = "POS_CTRL"
                    sample_id = f"{plate_id}-POS-{row}"
                elif 2 <= col <= 9:
                    conc_nM = float(concentrations_nM[col - 2])
                    if row in "ABC":
                        compound_id = "CMP-A"
                        replicate = "tech1" if row in "AB" else "tech2"
                    elif row in "DEF":
                        compound_id = "CMP-B"
                        replicate = "tech1" if row in "DE" else "tech2"
                    else:  # G, H
                        compound_id = "CMP-C"
                        replicate = "tech1" if row == "G" else "tech2"
                    role = "SAMPLE"
                    sample_id = f"{compound_id}-{conc_nM:g}nM-{replicate}-{plate_id}"
                elif col in (10, 11):
                    role = "BUFFER"
                    sample_id = f"{plate_id}-BUF-{row}{col}"

                plate_maps.append(
                    {
                        "plate_id": plate_id,
                        "well": well,
                        "row": row,
                        "column": col,
                        "role": role,
                        "sample_id": sample_id,
                        "compound_id": compound_id,
                        "concentration_nM": conc_nM,
                        "replicate": replicate,
                        "batch": batch,
                    }
                )

                # Simulate raw RFU: high = inactive / vehicle; low = inhibited.
                baseline = 1.20 + plate_shift
                inhibited = 0.25 + plate_shift
                noise = rng.normal(0.0, 0.025)

                if role == "NEG_CTRL":
                    value = baseline + noise
                    # Planted edge effect on P02 columns 1 and 12 for NEG/POS.
                    if plate_id == "P02" and col == 1 and row in "AH":
                        value += 0.35  # inflated edge wells
                elif role == "POS_CTRL":
                    value = inhibited + noise
                    if plate_id == "P02" and col == 12 and row in "AH":
                        value += 0.30
                elif role == "SAMPLE":
                    info = compounds[compound_id]
                    # Four-parameter logistic in log10(M)
                    x = np.log10(conc_nM * 1e-9)
                    log_ic50 = np.log10(info["true_ic50_nM"] * 1e-9)
                    frac = 1.0 / (1.0 + 10 ** ((log_ic50 - x) * info["hill"]))
                    inhib = info["max_inhibition"] * frac
                    value = baseline - inhib * (baseline - inhibited) + noise
                else:
                    value = 0.05 + abs(noise) * 0.2  # buffer / unused

                # One intentional missing reading on P01 for QC demo.
                if plate_id == "P01" and well == "H11":
                    value = np.nan

                readings.append(
                    {
                        "plate_id": plate_id,
                        "well": well,
                        "readout_RFU": value,
                        "readout_unit": "RFU",
                        "data_origin": "SIMULATED",
                        "simulation_seed": seed,
                    }
                )

        for cid, info in compounds.items():
            metadata.append(
                {
                    "compound_id": cid,
                    "true_ic50_nM": info["true_ic50_nM"],
                    "true_hill": info["hill"],
                    "max_inhibition": info["max_inhibition"],
                    "data_origin": "SIMULATED",
                    "note": "Ground-truth parameters used only for simulation; analysis must not read this file for fitting.",
                }
            )

    # Deduplicate metadata rows (same for both plates).
    meta_df = pd.DataFrame(metadata).drop_duplicates(subset=["compound_id"])

    paths = {
        "plate_map": output_dir / "plate_map.csv",
        "readings": output_dir / "plate_readings.csv",
        "metadata": output_dir / "sample_metadata.csv",
    }
    pd.DataFrame(plate_maps).to_csv(paths["plate_map"], index=False)
    pd.DataFrame(readings).to_csv(paths["readings"], index=False)
    meta_df.to_csv(paths["metadata"], index=False)
    return paths


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "data" / "example"
    generate(out)
    print(f"Wrote simulated demo data to {out}")
