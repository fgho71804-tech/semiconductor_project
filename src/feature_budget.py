"""Feature-budget experiments for performance, runtime, and token footprint."""

from __future__ import annotations

import json
from collections.abc import Sequence
from time import perf_counter

import numpy as np
import pandas as pd
import tiktoken
from sklearn.base import BaseEstimator, clone
from sklearn.metrics import average_precision_score
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate


def compact_json_token_counts(
    X: pd.DataFrame,
    encoding_name: str = "cl100k_base",
    decimal_places: int = 6,
) -> np.ndarray:
    """Count tokens for one compact feature-value JSON object per sample."""
    encoding = tiktoken.get_encoding(encoding_name)
    counts = []
    for record in X.to_dict(orient="records"):
        normalized = {
            key: None if pd.isna(value) else round(float(value), decimal_places)
            for key, value in record.items()
        }
        payload = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))
        counts.append(len(encoding.encode(payload)))
    return np.asarray(counts, dtype=int)


def cumulative_feature_budget_experiment(
    model: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    timestamps: pd.Series,
    ranked_features: Sequence[str],
    n_splits: int = 5,
    n_repeats: int = 3,
    random_state: int = 42,
    inference_repeats: int = 30,
    min_feature_count: int = 1,
) -> pd.DataFrame:
    """Evaluate cumulative top-k features with repeated CV and temporal holdout."""
    order = timestamps.sort_values(kind="stable").index
    temporal_split = int(len(order) * 0.8)
    temporal_train_index = order[:temporal_split]
    temporal_test_index = order[temporal_split:]
    cv = RepeatedStratifiedKFold(
        n_splits=n_splits, n_repeats=n_repeats, random_state=random_state
    )
    fold_count = n_splits * n_repeats
    rows = []

    if not 1 <= min_feature_count <= len(ranked_features):
        raise ValueError("min_feature_count must be between 1 and ranked feature count")

    for feature_count in range(min_feature_count, len(ranked_features) + 1):
        features = list(ranked_features[:feature_count])
        X_subset = X[features]
        scores = cross_validate(
            clone(model),
            X_subset,
            y,
            scoring={
                "pr_auc": "average_precision",
                "roc_auc": "roc_auc",
                "balanced_accuracy": "balanced_accuracy",
            },
            cv=cv,
            n_jobs=1,
            error_score="raise",
        )

        fitted = clone(model).fit(
            X_subset.loc[temporal_train_index], y.loc[temporal_train_index]
        )
        temporal_probability = fitted.predict_proba(
            X_subset.loc[temporal_test_index]
        )[:, 1]
        temporal_pr_auc = average_precision_score(
            y.loc[temporal_test_index], temporal_probability
        )

        inference_start = perf_counter()
        for _ in range(inference_repeats):
            fitted.predict_proba(X_subset.loc[temporal_test_index])
        inference_seconds = (perf_counter() - inference_start) / inference_repeats

        token_counts = compact_json_token_counts(X_subset)
        pr_auc_values = scores["test_pr_auc"]
        rows.append(
            {
                "feature_count": feature_count,
                "features": ",".join(features),
                "added_feature": features[-1],
                "cv_pr_auc_mean": float(pr_auc_values.mean()),
                "cv_pr_auc_std": float(pr_auc_values.std(ddof=1)),
                "cv_pr_auc_sem": float(
                    pr_auc_values.std(ddof=1) / np.sqrt(fold_count)
                ),
                "cv_roc_auc_mean": float(scores["test_roc_auc"].mean()),
                "cv_balanced_accuracy_mean": float(
                    scores["test_balanced_accuracy"].mean()
                ),
                "temporal_test_pr_auc": float(temporal_pr_auc),
                "fit_time_mean_seconds": float(scores["fit_time"].mean()),
                "fit_time_std_seconds": float(scores["fit_time"].std(ddof=1)),
                "score_time_mean_seconds": float(scores["score_time"].mean()),
                "inference_time_ms_per_sample": float(
                    inference_seconds * 1000 / len(temporal_test_index)
                ),
                "tokens_mean_per_sample": float(token_counts.mean()),
                "tokens_std_per_sample": float(token_counts.std(ddof=1)),
                "tokens_total_dataset": int(token_counts.sum()),
                "json_encoding": "cl100k_base",
                "token_scope": "feature-value JSON only; prompt overhead excluded",
            }
        )
    return pd.DataFrame(rows)


def feature_budget_conclusions(
    results: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Quantify linearity and identify best and one-standard-error points."""
    results = results.copy()
    x = results["feature_count"].to_numpy(dtype=float)
    linear_rows = []
    for metric in [
        "cv_pr_auc_mean",
        "temporal_test_pr_auc",
        "fit_time_mean_seconds",
        "inference_time_ms_per_sample",
        "tokens_mean_per_sample",
    ]:
        y = results[metric].to_numpy(dtype=float)
        coefficient = np.polyfit(x, y, 1)
        prediction = np.polyval(coefficient, x)
        residual_sum = float(np.square(y - prediction).sum())
        total_sum = float(np.square(y - y.mean()).sum())
        r_squared = 1 - residual_sum / total_sum if total_sum > 0 else 1.0
        linear_rows.append(
            {
                "metric": metric,
                "slope_per_added_feature": float(coefficient[0]),
                "intercept": float(coefficient[1]),
                "linear_r_squared": r_squared,
                "approximately_linear_r2_ge_0_90": r_squared >= 0.90,
            }
        )

    best = results.loc[results["cv_pr_auc_mean"].idxmax()]
    one_se_floor = best["cv_pr_auc_mean"] - best["cv_pr_auc_sem"]
    one_se = results[results["cv_pr_auc_mean"] >= one_se_floor].iloc[0]
    results["token_multiplier_vs_top1"] = (
        results["tokens_mean_per_sample"] / results.iloc[0]["tokens_mean_per_sample"]
    )
    results["pr_auc_gain_vs_top1"] = (
        results["cv_pr_auc_mean"] - results.iloc[0]["cv_pr_auc_mean"]
    )
    results["marginal_pr_auc_gain"] = results["cv_pr_auc_mean"].diff()
    results["marginal_tokens"] = results["tokens_mean_per_sample"].diff()
    results["marginal_pr_auc_per_100_tokens"] = (
        results["marginal_pr_auc_gain"] / results["marginal_tokens"] * 100
    )

    optimum = pd.DataFrame(
        [
            {
                "criterion": "maximum_mean_cv_pr_auc",
                "feature_count": int(best["feature_count"]),
                "features": best["features"],
                "cv_pr_auc_mean": float(best["cv_pr_auc_mean"]),
                "cv_pr_auc_sem": float(best["cv_pr_auc_sem"]),
                "tokens_mean_per_sample": float(best["tokens_mean_per_sample"]),
                "fit_time_mean_seconds": float(best["fit_time_mean_seconds"]),
            },
            {
                "criterion": "one_standard_error_simplest",
                "feature_count": int(one_se["feature_count"]),
                "features": one_se["features"],
                "cv_pr_auc_mean": float(one_se["cv_pr_auc_mean"]),
                "cv_pr_auc_sem": float(one_se["cv_pr_auc_sem"]),
                "tokens_mean_per_sample": float(one_se["tokens_mean_per_sample"]),
                "fit_time_mean_seconds": float(one_se["fit_time_mean_seconds"]),
            },
        ]
    )
    return results, pd.DataFrame(linear_rows), optimum
