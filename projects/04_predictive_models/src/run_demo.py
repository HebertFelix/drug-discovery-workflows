"""Run Project 04 QSAR demonstration."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from . import __version__
from .curate_qsar import prepare_modeling_table
from .features import descriptor_matrix, morgan_matrix, tanimoto_max_to_train
from .metrics import metrics_table, subgroup_by_similarity
from .models import fit_models
from .report import write_qsar_report
from .splits import random_split, scaffold_split, split_overlap_report
from .visualize import metrics_barplot, pred_vs_obs_grid, residual_plot

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _evaluate_split(
    df: pd.DataFrame,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
    *,
    split_name: str,
    cfg: dict,
    out_dir: Path,
) -> tuple[pd.DataFrame, dict, object, np.ndarray]:
    train = df.iloc[train_idx].reset_index(drop=True)
    test = df.iloc[test_idx].reset_index(drop=True)
    y_train = train["pIC50"].to_numpy(dtype=float)
    y_test = test["pIC50"].to_numpy(dtype=float)

    Xd_tr = descriptor_matrix(train)
    Xd_te = descriptor_matrix(test)
    Xf_tr = morgan_matrix(
        train["smiles_canonical"].tolist(),
        radius=int(cfg["fingerprint"]["radius"]),
        n_bits=int(cfg["fingerprint"]["n_bits"]),
    )
    Xf_te = morgan_matrix(
        test["smiles_canonical"].tolist(),
        radius=int(cfg["fingerprint"]["radius"]),
        n_bits=int(cfg["fingerprint"]["n_bits"]),
    )

    bundles = fit_models(
        y_train=y_train,
        y_test=y_test,
        X_desc_train=Xd_tr,
        X_desc_test=Xd_te,
        X_fp_train=Xf_tr,
        X_fp_test=Xf_te,
        seed=int(cfg["seed"]),
    )
    metrics = metrics_table(bundles, y_train, y_test)
    metrics.insert(0, "split_strategy", split_name)

    overlap = split_overlap_report(df, train_idx, test_idx)
    max_sim = tanimoto_max_to_train(Xf_te, Xf_tr)

    # Pred vs obs for all models on test
    panels = [(b.name, y_test, b.y_test_pred) for b in bundles]
    pred_vs_obs_grid(
        panels,
        out_dir / f"pred_vs_obs_{split_name}.png",
        title=f"Test pred vs obs — {split_name} split",
    )
    metrics_barplot(metrics, out_dir / f"test_rmse_{split_name}.png", split_name)

    rf = next(b for b in bundles if b.name == "rf_morgan")
    residual_plot(
        y_test,
        rf.y_test_pred,
        max_sim,
        out_dir / f"residuals_rf_{split_name}.png",
        title=f"RF residuals colored by train similarity — {split_name}",
    )

    pred_detail = test[["inchikey", "smiles_canonical", "scaffold_smiles", "pIC50", "molecule_chembl_id"]].copy()
    pred_detail["split_strategy"] = split_name
    pred_detail["max_tanimoto_to_train"] = max_sim
    for b in bundles:
        pred_detail[f"pred_{b.name}"] = b.y_test_pred
        pred_detail[f"resid_{b.name}"] = b.y_test_pred - y_test
    pred_detail.to_csv(out_dir / f"predictions_{split_name}.csv", index=False)

    return metrics, overlap, rf, max_sim


def run(config_path: Path | None = None) -> Path:
    config_path = config_path or (ROOT / "configs" / "demo.yaml")
    cfg = load_config(config_path)
    out_dir = ROOT / cfg["paths"]["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(ROOT / cfg["paths"]["raw"])
    modeling, exclusions = prepare_modeling_table(raw)
    modeling.to_csv(out_dir / "modeling_table.csv", index=False)
    exclusions.to_csv(out_dir / "exclusions.csv", index=False)

    if len(modeling) < 30:
        raise RuntimeError(f"Modeling table too small for demo: n={len(modeling)}")

    all_metrics = []
    split_reports = {}
    ad_tables = {}

    # Random split
    tr, te = random_split(modeling, test_size=float(cfg["split"]["test_size"]), seed=int(cfg["seed"]))
    m_rand, ov_rand, rf_rand, sim_rand = _evaluate_split(
        modeling, tr, te, split_name="random", cfg=cfg, out_dir=out_dir
    )
    all_metrics.append(m_rand)
    split_reports["random"] = ov_rand
    ad_tables["random / rf_morgan"] = subgroup_by_similarity(
        modeling.iloc[te]["pIC50"].to_numpy(),
        rf_rand.y_test_pred,
        sim_rand,
        threshold=float(cfg["applicability"]["tanimoto_threshold"]),
    )

    # Scaffold split
    tr_s, te_s = scaffold_split(modeling, test_size=float(cfg["split"]["test_size"]), seed=int(cfg["seed"]))
    m_scaf, ov_scaf, rf_scaf, sim_scaf = _evaluate_split(
        modeling, tr_s, te_s, split_name="scaffold", cfg=cfg, out_dir=out_dir
    )
    all_metrics.append(m_scaf)
    split_reports["scaffold"] = ov_scaf
    ad_tables["scaffold / rf_morgan"] = subgroup_by_similarity(
        modeling.iloc[te_s]["pIC50"].to_numpy(),
        rf_scaf.y_test_pred,
        sim_scaf,
        threshold=float(cfg["applicability"]["tanimoto_threshold"]),
    )

    metrics = pd.concat(all_metrics, ignore_index=True)
    metrics.to_csv(out_dir / "metrics.csv", index=False)
    for name, tab in ad_tables.items():
        safe = name.replace(" ", "_").replace("/", "_")
        tab.to_csv(out_dir / f"ad_subgroups_{safe}.csv", index=False)

    write_qsar_report(
        out_dir / "qsar_report.md",
        dataset_summary={
            "source": "ChEMBL target CHEMBL301 (CDK2) IC50 snapshot",
            "access_date": "2026-10-06",
            "n_compounds": int(len(modeling)),
            "pic50_min": float(modeling["pIC50"].min()),
            "pic50_max": float(modeling["pIC50"].max()),
        },
        split_reports=split_reports,
        metrics=metrics,
        ad_tables=ad_tables,
    )

    manifest = {
        "project": "04_predictive_models",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": str(config_path.relative_to(ROOT)),
        "python": sys.version,
        "platform": platform.platform(),
        "n_raw": int(len(raw)),
        "n_modeling": int(len(modeling)),
        "n_excluded_rows": int(len(exclusions)),
        "split_reports": split_reports,
        "outputs": sorted(p.name for p in out_dir.iterdir() if p.is_file()),
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Demo complete → {out_dir}")
    print(f"  modeling compounds: {len(modeling)}")
    # Print test RMSE comparison
    for split_name in ("random", "scaffold"):
        sub = metrics[(metrics["split_strategy"] == split_name) & (metrics["split_eval"] == "test")]
        print(f"  [{split_name}] test RMSE:")
        for _, row in sub.iterrows():
            print(f"    {row['model']}: {row['RMSE']:.3f} (R2={row['R2']:.3f})")
    return out_dir


if __name__ == "__main__":
    run()
