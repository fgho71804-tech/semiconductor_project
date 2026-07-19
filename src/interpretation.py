"""Model interpretation and monitoring-candidate helpers for SECOM."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import average_precision_score


def random_forest_impurity_importance(
    fitted_pipeline: BaseEstimator,
    feature_names: Sequence[str],
) -> pd.DataFrame:
    """Extract fitted Random Forest impurity importance with explicit caveats."""
    model = fitted_pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        raise TypeError("선택 모델에 feature_importances_ 속성이 없습니다.")
    result = pd.DataFrame(
        {
            "feature": list(feature_names),
            "impurity_importance": model.feature_importances_,
        }
    ).sort_values("impurity_importance", ascending=False)
    result["impurity_rank"] = np.arange(1, len(result) + 1)
    return result.reset_index(drop=True)


def candidate_permutation_importance(
    fitted_model: BaseEstimator,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    candidate_features: Sequence[str],
    n_repeats: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Measure Test PR-AUC decrease after shuffling selected Train-ranked features."""
    rng = np.random.default_rng(random_state)
    baseline_probabilities = fitted_model.predict_proba(X_test)[:, 1]
    baseline_pr_auc = average_precision_score(y_test, baseline_probabilities)
    rows = []
    for feature in candidate_features:
        repeat_scores = []
        original = X_test[feature].to_numpy(copy=True)
        for _ in range(n_repeats):
            shuffled = X_test.copy()
            shuffled[feature] = rng.permutation(original)
            probability = fitted_model.predict_proba(shuffled)[:, 1]
            repeat_scores.append(average_precision_score(y_test, probability))
        scores = np.asarray(repeat_scores)
        rows.append(
            {
                "feature": feature,
                "baseline_pr_auc": baseline_pr_auc,
                "permuted_pr_auc_mean": float(scores.mean()),
                "permutation_importance_mean": float(baseline_pr_auc - scores.mean()),
                "permutation_importance_std": float(scores.std(ddof=1 if len(scores) > 1 else 0)),
            }
        )
    result = pd.DataFrame(rows).sort_values("permutation_importance_mean", ascending=False)
    result["permutation_rank"] = np.arange(1, len(result) + 1)
    return result.reset_index(drop=True)


def combine_feature_evidence(
    impurity: pd.DataFrame,
    permutation: pd.DataFrame,
    mean_difference: pd.DataFrame,
    statistical_test: pd.DataFrame,
    top_n: int = 20,
) -> pd.DataFrame:
    """Combine model and univariate evidence without treating any method as causal."""
    mean_columns = [
        "feature",
        "pass_mean",
        "fail_mean",
        "standardized_mean_diff",
        "abs_standardized_mean_diff",
    ]
    test_columns = ["feature", "p_value", "fdr_bh"]
    combined = (
        impurity.merge(permutation, on="feature", how="left")
        .merge(mean_difference[mean_columns], on="feature", how="left")
        .merge(statistical_test[test_columns], on="feature", how="left")
    )
    combined["effect_rank"] = (
        combined["abs_standardized_mean_diff"].rank(method="min", ascending=False).astype("Int64")
    )
    combined["fdr_rank"] = combined["fdr_bh"].rank(method="min", ascending=True).astype("Int64")
    combined["top_impurity"] = combined["impurity_rank"] <= top_n
    combined["top_permutation"] = combined["permutation_rank"].le(top_n).fillna(False)
    combined["top_effect"] = combined["effect_rank"] <= top_n
    combined["top_fdr"] = combined["fdr_rank"] <= top_n
    evidence_columns = ["top_impurity", "top_permutation", "top_effect", "top_fdr"]
    combined["evidence_count"] = combined[evidence_columns].sum(axis=1)
    combined["fdr_significant_05"] = combined["fdr_bh"] < 0.05
    return combined.sort_values(
        ["evidence_count", "permutation_importance_mean", "impurity_importance"],
        ascending=[False, False, False],
        na_position="last",
    ).reset_index(drop=True)


def robust_monitoring_candidates(
    evidence: pd.DataFrame,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    minimum_evidence: int = 2,
    max_features: int = 10,
    max_missing_rate: float = 0.2,
) -> pd.DataFrame:
    """Create robust Pass-reference screening limits for engineering review."""
    candidates = evidence[evidence["evidence_count"] >= minimum_evidence].copy()
    candidates["train_missing_rate"] = candidates["feature"].map(X_train.isna().mean())
    candidates = candidates[candidates["train_missing_rate"] <= max_missing_rate].head(max_features)
    pass_mask = y_train.eq(0)
    rows = []
    for _, candidate in candidates.iterrows():
        feature = candidate["feature"]
        pass_values = X_train.loc[pass_mask, feature].dropna()
        median = float(pass_values.median())
        mad = float((pass_values - median).abs().median())
        robust_sigma = 1.4826 * mad
        if robust_sigma > 0:
            lower = median - 3 * robust_sigma
            upper = median + 3 * robust_sigma
            limit_method = "Pass median ± 3×robust sigma (MAD)"
        else:
            lower = float(pass_values.quantile(0.01))
            upper = float(pass_values.quantile(0.99))
            limit_method = "Pass 1st–99th percentile fallback"
        mean_diff = float(candidate["fail_mean"] - candidate["pass_mean"])
        rows.append(
            {
                "feature": feature,
                "evidence_count": int(candidate["evidence_count"]),
                "fail_shift_direction": "higher" if mean_diff > 0 else "lower",
                "train_pass_n": int(pass_values.size),
                "train_missing_rate": float(candidate["train_missing_rate"]),
                "pass_median": median,
                "pass_mad": mad,
                "candidate_lower_limit": lower,
                "candidate_upper_limit": upper,
                "limit_method": limit_method,
                "validation_status": "engineering and temporal validation required",
            }
        )
    return pd.DataFrame(rows)
