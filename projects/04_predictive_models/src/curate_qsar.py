"""Prepare a modeling table from ChEMBL-like bioactivity rows."""

from __future__ import annotations

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski
from rdkit.Chem.SaltRemover import SaltRemover
from rdkit.Chem.Scaffolds import MurckoScaffold

REMOVER = SaltRemover()


def _parent_canonical(smiles: str) -> tuple[str | None, str | None, str | None]:
    mol = Chem.MolFromSmiles(str(smiles)) if pd.notna(smiles) else None
    if mol is None:
        return None, None, None
    parent = REMOVER.StripMol(mol, dontRemoveEverything=True)
    frags = Chem.GetMolFrags(parent, asMols=True, sanitizeFrags=True)
    if frags:
        parent = max(frags, key=lambda m: m.GetNumHeavyAtoms())
    can = Chem.MolToSmiles(parent, canonical=True)
    ik = Chem.MolToInchiKey(parent)
    try:
        scaff = MurckoScaffold.MurckoScaffoldSmiles(mol=parent, includeChirality=False)
    except Exception:
        scaff = ""
    return can, ik, scaff


def to_nM(value: float, unit: str) -> float | None:
    u = (unit or "").strip().lower().replace("μ", "u")
    if u in {"nm", "nanomolar"}:
        return float(value)
    if u in {"um", "µm", "micromolar"}:
        return float(value) * 1e3
    if u in {"mm", "millimolar"}:
        return float(value) * 1e6
    return None


def prepare_modeling_table(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (modeling_df, exclusions_df).

    Modeling rows are uncensored IC50 with valid parents, aggregated by InChIKey
    (median pIC50) so each chemical parent appears once.
    """
    exclusions: list[dict] = []
    rows: list[dict] = []

    for _, r in raw.iterrows():
        sid = r.get("source_id")
        if str(r.get("assay_type", "")).upper() != "IC50":
            exclusions.append({"source_id": sid, "reason": "non_ic50"})
            continue
        if str(r.get("relation", "=")).strip() != "=":
            exclusions.append({"source_id": sid, "reason": "censored_relation", "detail": r.get("relation")})
            continue
        if pd.isna(r.get("value")):
            exclusions.append({"source_id": sid, "reason": "missing_value"})
            continue
        value_nM = to_nM(float(r["value"]), str(r.get("unit", "nM")))
        if value_nM is None or value_nM <= 0:
            exclusions.append({"source_id": sid, "reason": "bad_unit_or_value", "detail": r.get("unit")})
            continue
        can, ik, scaff = _parent_canonical(r.get("smiles"))
        if can is None:
            exclusions.append({"source_id": sid, "reason": "invalid_smiles"})
            continue
        if r.get("data_validity_comment") not in (None, "", np.nan) and pd.notna(r.get("data_validity_comment")):
            # Keep but flag — ChEMBL sometimes marks outside typical range
            pass
        pic50 = -np.log10(value_nM * 1e-9)
        mol = Chem.MolFromSmiles(can)
        rows.append(
            {
                "source_id": sid,
                "molecule_chembl_id": r.get("molecule_chembl_id"),
                "smiles_canonical": can,
                "inchikey": ik,
                "scaffold_smiles": scaff,
                "assay_chembl_id": r.get("assay_chembl_id"),
                "value_nM": value_nM,
                "pIC50": pic50,
                "pchembl_value": r.get("pchembl_value"),
                "target_uniprot": r.get("target_uniprot"),
                "organism": r.get("organism"),
                "data_origin": r.get("data_origin"),
                "mw": Descriptors.MolWt(mol),
                "logp": Descriptors.MolLogP(mol),
                "hbd": Lipinski.NumHDonors(mol),
                "hba": Lipinski.NumHAcceptors(mol),
                "tpsa": Descriptors.TPSA(mol),
                "rotatable_bonds": Lipinski.NumRotatableBonds(mol),
            }
        )

    detail = pd.DataFrame(rows)
    if detail.empty:
        return detail, pd.DataFrame(exclusions)

    # Aggregate duplicate parents: median pIC50, keep representative ChemBL id
    agg_rows = []
    for ik, g in detail.groupby("inchikey"):
        g = g.sort_values("source_id")
        rep = g.iloc[0]
        agg_rows.append(
            {
                "inchikey": ik,
                "smiles_canonical": rep["smiles_canonical"],
                "scaffold_smiles": rep["scaffold_smiles"],
                "n_measurements": len(g),
                "pIC50": float(g["pIC50"].median()),
                "pIC50_std": float(g["pIC50"].std(ddof=0)) if len(g) > 1 else 0.0,
                "molecule_chembl_id": rep["molecule_chembl_id"],
                "source_ids": ";".join(map(str, g["source_id"].tolist())),
                "mw": rep["mw"],
                "logp": rep["logp"],
                "hbd": rep["hbd"],
                "hba": rep["hba"],
                "tpsa": rep["tpsa"],
                "rotatable_bonds": rep["rotatable_bonds"],
                "data_origin": rep["data_origin"],
                "target_uniprot": rep["target_uniprot"],
            }
        )
        if len(g) > 1:
            for _, extra in g.iloc[1:].iterrows():
                exclusions.append(
                    {
                        "source_id": extra["source_id"],
                        "reason": "aggregated_into_parent_median",
                        "detail": ik,
                    }
                )

    modeling = pd.DataFrame(agg_rows).sort_values("inchikey").reset_index(drop=True)
    return modeling, pd.DataFrame(exclusions)
