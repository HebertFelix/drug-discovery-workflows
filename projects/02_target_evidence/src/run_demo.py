"""Run the Project 02 target-evidence demonstration."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from . import __version__
from .conservation import conservation_vs_reference
from .fasta_io import parse_uniprot_header, read_fasta
from .pdb_audit import parse_pdb_chain_residues
from .report import write_target_brief
from .structure_select import choose_structure, score_structures
from .visualize import conservation_plot, write_ngl_html

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def run(config_path: Path | None = None) -> Path:
    config_path = config_path or (ROOT / "configs" / "demo.yaml")
    cfg = load_config(config_path)
    out_dir = ROOT / cfg["paths"]["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    card = json.loads((ROOT / cfg["paths"]["target_card"]).read_text(encoding="utf-8"))
    catalog = pd.read_csv(ROOT / cfg["paths"]["structures_catalog"], sep="\t")
    ref_records = read_fasta(ROOT / cfg["paths"]["target_sequence"])
    if len(ref_records) != 1:
        raise ValueError("Expected exactly one reference sequence")
    ref_header, ref_seq = ref_records[0]
    orthologs = read_fasta(ROOT / cfg["paths"]["orthologs"])

    # Exclude identical accession from conservation partners
    ref_acc = parse_uniprot_header(ref_header)["accession"]
    partner_seqs = []
    partner_meta = []
    for header, seq in orthologs:
        meta = parse_uniprot_header(header)
        if meta["accession"] == ref_acc:
            continue
        partner_seqs.append(seq)
        partner_meta.append(meta)

    cons = conservation_vs_reference(ref_seq, partner_seqs)
    cons_df = pd.DataFrame(
        {
            "position": range(1, len(ref_seq) + 1),
            "residue": list(ref_seq),
            "conservation": cons,
        }
    )
    cons_df.to_csv(out_dir / "conservation_by_position.csv", index=False)

    # Active-site neighborhood mean if annotated
    active_mean = None
    for f in card.get("features_selected") or []:
        if f.get("type") == "Active site" and f.get("start"):
            start = max(1, int(f["start"]) - 5)
            end = min(len(cons), int(f.get("end") or f["start"]) + 5)
            active_mean = float(cons[start - 1 : end].mean())
            break

    conservation_plot(
        cons,
        features=card.get("features_selected") or [],
        output_path=out_dir / "conservation_map.png",
        title=f"{card.get('uniprot_id')} conservation across {len(partner_seqs)} orthologs",
    )

    scored = score_structures(
        catalog,
        target_uniprot=cfg["target_uniprot"],
        intent=cfg["study_intent"],
    )
    scored.to_csv(out_dir / "structures_ranked.csv", index=False)
    choice = choose_structure(scored)
    (out_dir / "structure_choice.json").write_text(
        json.dumps(choice, indent=2), encoding="utf-8"
    )

    pdb_path = ROOT / cfg["paths"]["demo_pdb"]
    audit = parse_pdb_chain_residues(pdb_path, chain=cfg.get("demo_pdb_chain", "A"))
    (out_dir / "pdb_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    annotations = {
        **choice,
        "viewer_pdb_bundled": pdb_path.name,
        "viewer_note": (
            "Interactive coordinates are the bundled chain-A demo slice "
            f"({pdb_path.name}). The ranked selection may be a different PDB id; "
            "download official files from RCSB for production analyses."
        ),
        "n_observed_residues": audit["n_observed_residues"],
        "residue_min": audit["residue_min"],
        "residue_max": audit["residue_max"],
        "n_missing": len(audit.get("missing_residues_in_span") or []),
        "het_resnames": audit.get("het_resnames") or [],
    }
    write_ngl_html(
        pdb_path,
        out_dir / "structure_view.html",
        title=f"{choice['selected_pdb_id']} — {card.get('uniprot_id')}",
        annotations=annotations,
    )

    write_target_brief(
        out_dir / "target_brief.md",
        card=card,
        choice=choice,
        scored=scored,
        audit=audit,
        conservation_summary={
            "n_orthologs": len(partner_seqs),
            "mean_conservation": float(cons.mean()),
            "active_site_mean": f"{active_mean:.3f}" if active_mean is not None else "n/a",
        },
    )

    # Also dump partner list for provenance
    pd.DataFrame(partner_meta).to_csv(out_dir / "orthologs_used.csv", index=False)

    manifest = {
        "project": "02_target_evidence",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": str(config_path.relative_to(ROOT)),
        "python": sys.version,
        "platform": platform.platform(),
        "reference_header": ref_header,
        "study_intent": cfg["study_intent"],
        "choice": choice,
        "outputs": sorted(p.name for p in out_dir.iterdir() if p.is_file()),
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Demo complete → {out_dir}")
    print(f"  Selected {choice['selected_pdb_id']} for intent={choice['study_intent']}")
    return out_dir


if __name__ == "__main__":
    run()
