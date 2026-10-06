"""QSAR model wrappers with separate feature matrices per model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class FitBundle:
    name: str
    feature_set: str
    model: object
    y_train_pred: np.ndarray
    y_test_pred: np.ndarray


class MeanBaseline:
    def __init__(self) -> None:
        self.mean_: float = 0.0

    def fit(self, X, y):
        self.mean_ = float(np.mean(y))
        return self

    def predict(self, X):
        return np.full(shape=(len(X),), fill_value=self.mean_, dtype=float)


def fit_models(
    *,
    y_train: np.ndarray,
    y_test: np.ndarray,
    X_desc_train: np.ndarray,
    X_desc_test: np.ndarray,
    X_fp_train: np.ndarray,
    X_fp_test: np.ndarray,
    seed: int = 20261006,
) -> list[FitBundle]:
    bundles: list[FitBundle] = []

    mean = MeanBaseline().fit(X_desc_train, y_train)
    bundles.append(
        FitBundle(
            "mean_baseline",
            "none",
            mean,
            mean.predict(X_desc_train),
            mean.predict(X_desc_test),
        )
    )

    ridge = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=10.0)),
        ]
    )
    ridge.fit(X_desc_train, y_train)
    bundles.append(
        FitBundle(
            "ridge_descriptors",
            "descriptors",
            ridge,
            ridge.predict(X_desc_train),
            ridge.predict(X_desc_test),
        )
    )

    rf = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=2,
        random_state=seed,
        n_jobs=-1,
    )
    rf.fit(X_fp_train, y_train)
    bundles.append(
        FitBundle(
            "rf_morgan",
            "morgan_fp",
            rf,
            rf.predict(X_fp_train),
            rf.predict(X_fp_test),
        )
    )
    return bundles
