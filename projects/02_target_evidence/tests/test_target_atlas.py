"""Tests for Project 02 scientific transforms."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.conservation import conservation_vs_reference, needleman_wunsch
from src.fasta_io import parse_uniprot_header, read_fasta
from src.pdb_audit import parse_pdb_chain_residues
from src.structure_select import choose_structure, score_structures

ROOT = Path(__file__).resolve().parents[1]


def test_fasta_roundtrip_reference():
    recs = read_fasta(ROOT / "data/example/target_sequence.fasta")
    assert len(recs) == 1
    header, seq = recs[0]
    meta = parse_uniprot_header(header)
    assert meta["accession"] == "P24941"
    assert len(seq) == 298
    assert seq.startswith("MENFQK")


def test_needleman_identity():
    a, b = needleman_wunsch("ACDE", "ACDE")
    assert a == "ACDE"
    assert b == "ACDE"


def test_conservation_self_is_one():
    ref = "ACDEFGHIKL"
    cons = conservation_vs_reference(ref, [ref, ref])
    assert cons.mean() == pytest.approx(1.0)


def test_structure_ranking_prefers_inhibitor_for_pose_intent():
    catalog = pd.read_csv(ROOT / "data/example/structures_catalog.tsv", sep="\t")
    scored = score_structures(catalog, intent="ligand_pose_reference")
    top = choose_structure(scored)
    # Apo should not win this intent
    assert top["selected_pdb_id"] != "4EK3"
    # Winner should carry a nontrivial ligand
    row = scored.iloc[0]
    assert row["has_nontrivial_ligand"]


def test_apo_intent_selects_empty_ligand():
    catalog = pd.read_csv(ROOT / "data/example/structures_catalog.tsv", sep="\t")
    scored = score_structures(catalog, intent="apo_reference")
    top = choose_structure(scored)
    assert top["selected_pdb_id"] == "4EK3"


def test_pdb_audit_finds_het_and_residues():
    audit = parse_pdb_chain_residues(ROOT / "data/example/1AQ1_chainA.pdb", chain="A")
    assert audit["n_observed_residues"] > 200
    assert "STU" in audit["het_resnames"]
