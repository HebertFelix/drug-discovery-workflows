"""Train/test splitting strategies."""

from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd


def random_split(
    df: pd.DataFrame,
    *,
    test_size: float = 0.25,
    seed: int = 20261006,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    idx = np.arange(len(df))
    rng.shuffle(idx)
    n_test = max(1, int(round(len(df) * test_size)))
    test_idx = np.sort(idx[:n_test])
    train_idx = np.sort(idx[n_test:])
    return train_idx, test_idx


def scaffold_split(
    df: pd.DataFrame,
    *,
    test_size: float = 0.25,
    seed: int = 20261006,
) -> tuple[np.ndarray, np.ndarray]:
    """Bemis–Murcko scaffold split (greedy fill of test scaffolds).

    Inspired by MoleculeNet: compounds sharing a scaffold stay together.
    """
    rng = np.random.default_rng(seed)
    scaffolds: dict[str, list[int]] = defaultdict(list)
    for i, scaff in enumerate(df["scaffold_smiles"].fillna("").astype(str)):
        key = scaff if scaff else f"NOSCAFFOLD_{i}"
        scaffolds[key].append(i)

    # Shuffle scaffold groups by size then random tie-break
    groups = list(scaffolds.items())
    rng.shuffle(groups)
    groups.sort(key=lambda kv: len(kv[1]), reverse=True)

    train, test = [], []
    n = len(df)
    n_test_target = max(1, int(round(n * test_size)))
    for _, idxs in groups:
        if len(test) < n_test_target:
            test.extend(idxs)
        else:
            train.extend(idxs)
    # If test overshot badly and train empty, rebalance
    if not train:
        train = test[n_test_target:]
        test = test[:n_test_target]
    return np.array(sorted(train), dtype=int), np.array(sorted(test), dtype=int)


def split_overlap_report(
    df: pd.DataFrame,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
) -> dict:
    train_s = set(df.iloc[train_idx]["scaffold_smiles"].fillna(""))
    test_s = set(df.iloc[test_idx]["scaffold_smiles"].fillna(""))
    inter = train_s & test_s
    return {
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "n_train_scaffolds": len(train_s),
        "n_test_scaffolds": len(test_s),
        "n_shared_scaffolds": len(inter),
        "shared_scaffold_fraction_of_test": float(len(inter) / len(test_s)) if test_s else 0.0,
    }
