"""Rank candidate experimental structures for a stated study intent."""

from __future__ import annotations

import pandas as pd


def score_structures(
    catalog: pd.DataFrame,
    *,
    target_uniprot: str = "P24941",
    intent: str = "ligand_pose_reference",
) -> pd.DataFrame:
    """Score structures for a declared use-case.

    Intents:
      - ligand_pose_reference: prefer high-res inhibitor co-crystals of the target
      - nucleotide_reference: prefer ATP-bound forms
      - activated_complex: prefer cyclin-partner complexes
      - apo_reference: prefer ligand-free high resolution
    """
    df = catalog.copy()
    df["has_target"] = df["uniprot_ids"].fillna("").astype(str).str.contains(target_uniprot)
    df["resolution_A"] = pd.to_numeric(df["resolution_A"], errors="coerce")
    df["n_ligands"] = pd.to_numeric(df["n_ligands"], errors="coerce").fillna(0).astype(int)
    df["ligand_ids"] = df["ligand_ids"].fillna("").astype(str).replace({"nan": ""})
    ligands = df["ligand_ids"]

    df["has_atp"] = ligands.str.contains(r"\bATP\b", regex=True)
    solvent_like = {"", "MG", "EDO", "GOL", "DMSO", "SO4", "PO4", "CL", "NA", "K", "ZN"}

    def _nontrivial(ligand_ids: str) -> bool:
        parts = [p.strip() for p in str(ligand_ids).split(",") if p.strip()]
        return any(p not in solvent_like for p in parts)

    df["has_nontrivial_ligand"] = ligands.apply(_nontrivial)
    df["has_cyclin_partner"] = df["uniprot_ids"].fillna("").astype(str).apply(
        lambda s: any(u != target_uniprot for u in s.split(",") if u)
    )

    scores = []
    reasons = []
    for _, row in df.iterrows():
        score = 0.0
        reason: list[str] = []
        if not row["has_target"]:
            scores.append(-100.0)
            reasons.append("missing_target_uniprot")
            continue
        score += 10.0
        reason.append("maps_to_target")
        if pd.notna(row["resolution_A"]):
            # higher score for better resolution
            score += max(0.0, 8.0 - float(row["resolution_A"]))
            reason.append(f"resolution={row['resolution_A']}")

        if intent == "ligand_pose_reference":
            if row["has_nontrivial_ligand"] and not row["has_atp"]:
                score += 8.0
                reason.append("inhibitor_like_ligand")
            elif row["has_atp"]:
                score += 2.0
                reason.append("nucleotide_only")
            if not row["has_cyclin_partner"]:
                score += 1.0
                reason.append("monomeric_simpler_system")
        elif intent == "nucleotide_reference":
            if row["has_atp"]:
                score += 8.0
                reason.append("has_ATP")
        elif intent == "activated_complex":
            if row["has_cyclin_partner"]:
                score += 8.0
                reason.append("cyclin_partner_present")
            if row["has_nontrivial_ligand"]:
                score += 3.0
                reason.append("ligand_present")
        elif intent == "apo_reference":
            if int(row["n_ligands"]) == 0:
                score += 8.0
                reason.append("apo")
            elif not row["has_nontrivial_ligand"]:
                score += 3.0
                reason.append("no_druglike_ligand")
        else:
            reason.append(f"unknown_intent:{intent}")

        scores.append(score)
        reasons.append("; ".join(reason))

    df["selection_score"] = scores
    df["selection_reason"] = reasons
    df["study_intent"] = intent
    return df.sort_values(["selection_score", "resolution_A"], ascending=[False, True]).reset_index(drop=True)


def choose_structure(scored: pd.DataFrame) -> dict:
    if scored.empty:
        raise ValueError("No structures to choose from")
    top = scored.iloc[0]
    return {
        "selected_pdb_id": top["pdb_id"],
        "selection_score": float(top["selection_score"]),
        "selection_reason": top["selection_reason"],
        "study_intent": top["study_intent"],
        "caveat": (
            "A detected cavity or co-crystallized ligand does not by itself prove "
            "an allosteric mechanism. Choice is relative to the declared intent and "
            "the curated catalog, not an exhaustive PDB survey."
        ),
    }
