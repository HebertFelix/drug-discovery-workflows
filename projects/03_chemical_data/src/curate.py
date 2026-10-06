"""Structure standardization and bioactivity curation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski
from rdkit.Chem.SaltRemover import SaltRemover

REMOVER = SaltRemover()


def mol_from_smiles(smiles: str) -> Chem.Mol | None:
    if not isinstance(smiles, str) or not smiles.strip():
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        return None
    return mol


def parent_mol(mol: Chem.Mol) -> Chem.Mol:
    """Remove salts; keep largest fragment; do not invent stereo."""
    stripped = REMOVER.StripMol(mol, dontRemoveEverything=True)
    frags = Chem.GetMolFrags(stripped, asMols=True, sanitizeFrags=True)
    if not frags:
        return stripped
    return max(frags, key=lambda m: m.GetNumHeavyAtoms())


def canonical_smiles(mol: Chem.Mol) -> str:
    return Chem.MolToSmiles(mol, canonical=True)


def to_nM(value: float, unit: str) -> float | None:
    unit = (unit or "").strip().lower().replace("μ", "u")
    factors = {
        "nm": 1.0,
        "un": None,
        "um": 1e3,
        "µm": 1e3,
        "mm": 1e6,
        "m": 1e9,
        "pm": 1e-3,
    }
    # normalize keys
    if unit in {"nm", "nanomolar"}:
        return float(value) * 1.0
    if unit in {"um", "µm", "micromolar", "microm"}:
        return float(value) * 1e3
    if unit in {"mm", "millimolar"}:
        return float(value) * 1e6
    if unit in {"m", "molar"}:
        return float(value) * 1e9
    if unit in {"pm", "picomolar"}:
        return float(value) * 1e-3
    return None


def pic50_from_nM(ic50_nM: float) -> float:
    """pIC50 = -log10(IC50[M]); 100 nM → 7."""
    m = ic50_nM * 1e-9
    if m <= 0:
        raise ValueError("IC50 must be positive for pIC50")
    return -np.log10(m)


@dataclass
class CurateResult:
    curated: pd.DataFrame
    exclusions: pd.DataFrame
    dictionary: pd.DataFrame


def curate_bioactivity(raw: pd.DataFrame) -> CurateResult:
    exclusions: list[dict] = []
    rows: list[dict] = []

    for idx, r in raw.iterrows():
        source_id = r.get("source_id")
        mol = mol_from_smiles(r["smiles"])
        if mol is None:
            exclusions.append(
                {
                    "source_id": source_id,
                    "reason": "invalid_smiles",
                    "detail": r["smiles"],
                }
            )
            continue

        parent = parent_mol(mol)
        can = canonical_smiles(parent)
        value_nM = to_nM(float(r["value"]), str(r["unit"]))
        if value_nM is None:
            exclusions.append(
                {
                    "source_id": source_id,
                    "reason": "unrecognized_unit",
                    "detail": r["unit"],
                }
            )
            continue

        assay = str(r["assay_type"]).strip()
        relation = str(r.get("relation", "=")).strip()
        pic50 = np.nan
        if assay.upper() == "IC50" and relation == "=":
            pic50 = pic50_from_nM(value_nM)

        rows.append(
            {
                "source_id": source_id,
                "name": r.get("name"),
                "smiles_original": r["smiles"],
                "smiles_canonical": can,
                "inchikey": Chem.MolToInchiKey(parent),
                "assay_type": assay,
                "relation": relation,
                "value_original": float(r["value"]),
                "unit_original": r["unit"],
                "value_nM": value_nM,
                "pActivity": pic50,
                "pActivity_def": "pIC50=-log10(IC50[M]) only for uncensored IC50"
                if assay.upper() == "IC50" and relation == "="
                else "not_defined_for_this_endpoint_or_censoring",
                "organism": r.get("organism"),
                "target_name": r.get("target_name"),
                "target_uniprot": r.get("target_uniprot"),
                "mw": Descriptors.MolWt(parent),
                "logp": Descriptors.MolLogP(parent),
                "hbd": Lipinski.NumHDonors(parent),
                "hba": Lipinski.NumHAcceptors(parent),
                "tpsa": Descriptors.TPSA(parent),
                "rotatable_bonds": Lipinski.NumRotatableBonds(parent),
                "qed": Descriptors.qed(parent),
                "lipinski_violations": int(
                    (Descriptors.MolWt(parent) > 500)
                    + (Descriptors.MolLogP(parent) > 5)
                    + (Lipinski.NumHDonors(parent) > 5)
                    + (Lipinski.NumHAcceptors(parent) > 10)
                ),
                "data_origin": r.get("data_origin"),
                "note": r.get("note"),
            }
        )

    curated = pd.DataFrame(rows)
    # Duplicate policy: same inchikey + assay_type + organism + target_uniprot + relation
    # Keep first by source_id sort; log others. Do NOT merge different assay_types.
    if not curated.empty:
        curated = curated.sort_values("source_id").reset_index(drop=True)
        key_cols = [
            "inchikey",
            "assay_type",
            "organism",
            "target_uniprot",
            "relation",
        ]
        dup = curated.duplicated(subset=key_cols, keep="first")
        for _, r in curated.loc[dup].iterrows():
            exclusions.append(
                {
                    "source_id": r["source_id"],
                    "reason": "duplicate_inchikey_same_endpoint_context",
                    "detail": r["inchikey"],
                }
            )
        curated = curated.loc[~dup].reset_index(drop=True)

    dictionary = pd.DataFrame(
        [
            {"column": "smiles_canonical", "definition": "RDKit canonical SMILES after salt stripping / largest fragment"},
            {"column": "inchikey", "definition": "InChIKey of parent mol; duplicate key with same endpoint context → exclusion"},
            {"column": "assay_type", "definition": "IC50 / Ki / Kd / EC50 kept separate; never silently fused"},
            {"column": "relation", "definition": "Qualifiers =, <, >; censored rows keep relation and skip pIC50"},
            {"column": "value_nM", "definition": "Activity converted to nM; original unit preserved"},
            {"column": "pActivity", "definition": "pIC50 only for uncensored IC50; else NA"},
            {"column": "lipinski_violations", "definition": "Contextual count; not an automatic exclusion rule"},
        ]
    )
    return CurateResult(curated=curated, exclusions=pd.DataFrame(exclusions), dictionary=dictionary)


def morgan_fingerprint_matrix(smiles_list: list[str], n_bits: int = 1024, radius: int = 2):
    from rdkit.Chem import DataStructs
    from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

    gen = GetMorganGenerator(radius=radius, fpSize=n_bits)
    fps = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        fp = gen.GetFingerprint(mol)
        arr = np.zeros((n_bits,), dtype=int)
        DataStructs.ConvertToNumpyArray(fp, arr)
        fps.append(arr)
    return np.vstack(fps)
