"""Feature matrices for QSAR demos."""

from __future__ import annotations

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import DataStructs
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

DESC_COLS = ["mw", "logp", "hbd", "hba", "tpsa", "rotatable_bonds"]


def descriptor_matrix(df: pd.DataFrame) -> np.ndarray:
    return df[DESC_COLS].to_numpy(dtype=float)


def morgan_matrix(smiles: list[str], *, radius: int = 2, n_bits: int = 1024) -> np.ndarray:
    gen = GetMorganGenerator(radius=radius, fpSize=n_bits)
    rows = []
    for smi in smiles:
        mol = Chem.MolFromSmiles(smi)
        fp = gen.GetFingerprint(mol)
        arr = np.zeros((n_bits,), dtype=float)
        DataStructs.ConvertToNumpyArray(fp, arr)
        rows.append(arr)
    return np.vstack(rows)


def tanimoto_max_to_train(test_fps: np.ndarray, train_fps: np.ndarray) -> np.ndarray:
    """Max Tanimoto similarity of each test FP to any training FP (dense bits)."""
    # Tanimoto for binary vectors
    out = np.zeros(len(test_fps), dtype=float)
    train = train_fps.astype(bool)
    for i, fp in enumerate(test_fps.astype(bool)):
        inter = np.logical_and(train, fp).sum(axis=1)
        union = np.logical_or(train, fp).sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            sims = np.where(union > 0, inter / union, 0.0)
        out[i] = float(sims.max()) if len(sims) else 0.0
    return out
