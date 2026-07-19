"""Chronological validation and simple feature-drift diagnostics."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd


def chronological_holdout(
    X: pd.DataFrame,
    y: pd.Series,
    timestamps: pd.Series,
    test_size: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]:
    """Split earlier observations for training and later observations for testing."""
    if not 0 < test_size < 1:
        raise ValueError("test_size는 0과 1 사이여야 합니다.")
    order = timestamps.sort_values(kind="stable").index
    split = int(len(order) * (1 - test_size))
    train_index = order[:split]
    test_index = order[split:]
    return (
        X.loc[train_index],
        X.loc[test_index],
        y.loc[train_index],
        y.loc[test_index],
        timestamps.loc[train_index],
        timestamps.loc[test_index],
    )


def temporal_feature_drift(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    features: Sequence[str],
) -> pd.DataFrame:
    """Compare robust location and missingness between earlier and later periods."""
    rows = []
    for feature in features:
        train_values = X_train[feature].dropna()
        test_values = X_test[feature].dropna()
        train_median = float(train_values.median())
        test_median = float(test_values.median())
        train_mad = float((train_values - train_median).abs().median())
        robust_sigma = 1.4826 * train_mad
        standardized_shift = (
            (test_median - train_median) / robust_sigma if robust_sigma > 0 else np.nan
        )
        rows.append(
            {
                "feature": feature,
                "train_median": train_median,
                "test_median": test_median,
                "train_mad": train_mad,
                "median_shift_robust_sigma": standardized_shift,
                "train_missing_rate": float(X_train[feature].isna().mean()),
                "test_missing_rate": float(X_test[feature].isna().mean()),
                "missing_rate_change": float(
                    X_test[feature].isna().mean() - X_train[feature].isna().mean()
                ),
            }
        )
    result = pd.DataFrame(rows)
    result["abs_median_shift_robust_sigma"] = result["median_shift_robust_sigma"].abs()
    return result.sort_values("abs_median_shift_robust_sigma", ascending=False).reset_index(drop=True)

