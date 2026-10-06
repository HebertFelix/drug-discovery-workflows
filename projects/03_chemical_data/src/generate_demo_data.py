"""Generate a small simulated CDK2-oriented bioactivity table with known pitfalls."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Structures are real public molecules; ACTIVITY VALUES ARE SIMULATED.
COMPOUNDS = [
    {
        "source_id": "SIM-001",
        "name": "staurosporine",
        "smiles": "CN[C@@H]1C[C@H]2O[C@@](C)([C@@H]3C[C@H]4C5=C6C(=CC=C5)NC6=C5C(=O)N(C)C(=O)C5=C4C3=C2C2=C1C=CC=C2)N3C1=C(C=CC=C1)C4=C3C=CC=C4",
        "assay_type": "IC50",
        "relation": "=",
        "value": 7.0,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "canonical row",
    },
    {
        # Duplicate of SIM-001 with salt form and same assay → should collapse
        "source_id": "SIM-001b",
        "name": "staurosporine HCl",
        "smiles": "CN[C@@H]1C[C@H]2O[C@@](C)([C@@H]3C[C@H]4C5=C6C(=CC=C5)NC6=C5C(=O)N(C)C(=O)C5=C4C3=C2C2=C1C=CC=C2)N3C1=C(C=CC=C1)C4=C3C=CC=C4.Cl",
        "assay_type": "IC50",
        "relation": "=",
        "value": 7.5,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "salt duplicate of SIM-001",
    },
    {
        "source_id": "SIM-002",
        "name": "roscovitine",
        "smiles": "CCC(CO)Nc1nc(NCc2ccccc2)c2ncn(C(C)C)c2n1",
        "assay_type": "IC50",
        "relation": "=",
        "value": 700,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "canonical row",
    },
    {
        "source_id": "SIM-003",
        "name": "flavopiridol",
        "smiles": "CN1CCC(c2c(O)cc(O)c3c(=O)cc(-c4ccccc4Cl)oc23)C(O)C1",
        "assay_type": "IC50",
        "relation": "=",
        "value": 0.04,
        "unit": "uM",  # intentional unit variety → convert to nM
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "value in uM",
    },
    {
        "source_id": "SIM-004",
        "name": "olomoucine",
        "smiles": "Cn1cnc2c(NCc3ccccc3)nc(NCCO)nc21",
        "assay_type": "IC50",
        "relation": ">",
        "value": 10000,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "censored IC50",
    },
    {
        "source_id": "SIM-005",
        "name": "ATP",
        "smiles": "Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)[C@@H](O)[C@H]1O",
        "assay_type": "Kd",
        "relation": "=",
        "value": 30,
        "unit": "uM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "Kd — must not merge with IC50",
    },
    {
        "source_id": "SIM-006",
        "name": "dinaciclib",
        "smiles": "CC(C)c1nc(Nc2ccc(C(=O)N3CCN(C)CC3)cc2)nc(-c2cnn(C)c2)c1C#N",
        "assay_type": "Ki",
        "relation": "=",
        "value": 1.0,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "Ki — separate endpoint",
    },
    {
        "source_id": "SIM-007",
        "name": "invalid_smiles",
        "smiles": "this_is_not_smiles",
        "assay_type": "IC50",
        "relation": "=",
        "value": 100,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "should fail structure validation",
    },
    {
        "source_id": "SIM-008",
        "name": "mouse_cdk2_assay",
        "smiles": "CC(C)n1cnc2c(NCc3ccccc3)nc(NCCC)nc21",
        "assay_type": "IC50",
        "relation": "=",
        "value": 500,
        "unit": "nM",
        "organism": "Mus musculus",
        "target_name": "Cdk2",
        "target_uniprot": "P97377",
        "note": "different organism/uniprot — keep separate",
    },
    {
        "source_id": "SIM-009",
        "name": "SNS-032",
        "smiles": "O=C(Nc1nc(Nc2ccccc2)nc2ccccc12)C1CCN(C(=O)C2CC2)CC1",
        "assay_type": "IC50",
        "relation": "=",
        "value": 48,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "canonical row",
    },
    {
        "source_id": "SIM-010",
        "name": "caffeine",
        "smiles": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
        "assay_type": "IC50",
        "relation": "=",
        "value": 500000,
        "unit": "nM",
        "organism": "Homo sapiens",
        "target_name": "CDK2",
        "target_uniprot": "P24941",
        "note": "weak binder / negative-ish control context",
    },
]


def generate(output_dir: Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(COMPOUNDS)
    df.insert(0, "data_origin", "SIMULATED_ACTIVITY_REAL_STRUCTURES")
    path = output_dir / "raw_bioactivity.csv"
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    p = generate(Path(__file__).resolve().parents[1] / "data" / "example")
    print(f"Wrote {p}")
