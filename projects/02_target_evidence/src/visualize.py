"""Visualizations for the target evidence atlas."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def conservation_plot(
    conservation: np.ndarray,
    *,
    features: list[dict],
    output_path: Path,
    title: str = "Positional conservation vs orthologs",
) -> Path:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "#f7f7f5",
            "font.size": 10,
        }
    )
    fig, ax = plt.subplots(figsize=(10, 3.2))
    x = np.arange(1, len(conservation) + 1)
    ax.fill_between(x, conservation, color="#1f4e5f", alpha=0.35, linewidth=0)
    ax.plot(x, conservation, color="#1f4e5f", lw=1.0)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Reference residue position")
    ax.set_ylabel("Match fraction")
    ax.set_title(title)
    ax.grid(True, ls=":", alpha=0.5)

    # Annotate domain / active site spans lightly
    for f in features:
        if f.get("type") in {"Domain", "Active site"} and f.get("start") and f.get("end"):
            ax.axvspan(float(f["start"]), float(f["end"]), color="#c45c26", alpha=0.12)
            ax.text(
                (float(f["start"]) + float(f["end"])) / 2.0,
                1.02,
                f.get("type", ""),
                ha="center",
                va="bottom",
                fontsize=8,
                color="#c45c26",
            )

    fig.tight_layout()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def write_ngl_html(
    pdb_path: Path,
    output_path: Path,
    *,
    title: str,
    annotations: dict,
) -> Path:
    """Self-contained HTML that embeds PDB text and loads NGL from CDN."""
    pdb_text = Path(pdb_path).read_text(encoding="utf-8", errors="replace")
    # Escape for JS template literal
    pdb_js = json.dumps(pdb_text)
    ann_js = json.dumps(annotations, indent=2)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <style>
    body {{ margin: 0; font-family: Georgia, 'Times New Roman', serif; background: #f4f1ea; color: #1b1b1b; }}
    header {{ padding: 1rem 1.25rem; background: #1f4e5f; color: #f7f7f5; }}
    header h1 {{ margin: 0; font-size: 1.25rem; font-weight: 600; }}
    header p {{ margin: 0.35rem 0 0; opacity: 0.9; font-size: 0.95rem; }}
    #viewport {{ width: 100%; height: 70vh; background: #0f2a33; }}
    .notes {{ padding: 1rem 1.25rem 2rem; max-width: 900px; line-height: 1.45; }}
    code {{ background: #e8e4da; padding: 0.1rem 0.35rem; }}
    .warn {{ border-left: 3px solid #c45c26; padding-left: 0.75rem; margin-top: 1rem; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/ngl@2.1.0/dist/ngl.js"></script>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p>Annotated 3D view (NGL). Coordinates are a chain-A demo slice — see provenance in the target brief.</p>
  </header>
  <div id="viewport"></div>
  <div class="notes">
    <div id="annotations"></div>
    <div class="warn">
      Experimental coordinates support structural hypotheses. They do not alone
      establish allosteric function. AlphaFold models (not shown here) require
      local confidence interpretation and are not general mutation-effect validators.
    </div>
  </div>
  <script>
    const pdbText = {pdb_js};
    const annotations = {ann_js};
    document.getElementById('annotations').innerHTML =
      '<p><strong>Selected structure:</strong> ' + annotations.selected_pdb_id +
      ' &nbsp;|&nbsp; <strong>Intent:</strong> ' + annotations.study_intent + '</p>' +
      '<p><strong>Reason:</strong> ' + annotations.selection_reason + '</p>' +
      '<p><strong>Viewer coordinates:</strong> ' + annotations.viewer_pdb_bundled +
      ' — ' + annotations.viewer_note + '</p>' +
      '<p><strong>Observed residues:</strong> ' + annotations.n_observed_residues +
      ' (span ' + annotations.residue_min + '–' + annotations.residue_max + '); missing in span: ' +
      annotations.n_missing + '</p>' +
      '<p><strong>HET groups:</strong> ' + (annotations.het_resnames.join(', ') || 'none') + '</p>';

    const stage = new NGL.Stage('viewport', {{ backgroundColor: '#0f2a33' }});
    window.addEventListener('resize', () => stage.handleResize());
    const blob = new Blob([pdbText], {{ type: 'text/plain' }});
    stage.loadFile(blob, {{ ext: 'pdb' }}).then(comp => {{
      comp.addRepresentation('cartoon', {{ colorScheme: 'residueindex' }});
      comp.addRepresentation('ball+stick', {{
        sele: 'hetero and not water',
        colorScheme: 'element'
      }});
      comp.autoView();
    }});
  </script>
</body>
</html>
"""
    output_path = Path(output_path)
    output_path.write_text(html, encoding="utf-8")
    return output_path
