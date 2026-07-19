"""Reusable SECOM data-quality and EDA helpers."""

from pathlib import Path

import numpy as np
import pandas as pd


def load_secom(raw_dir: str | Path = "data/raw") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load SECOM features and labels and return X plus label metadata."""
    raw_dir = Path(raw_dir)
    feature_path = raw_dir / "secom.data"
    label_path = raw_dir / "secom_labels.data"
    missing = [str(path) for path in (feature_path, label_path) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "SECOM 원본 파일이 없습니다: " + ", ".join(missing)
            + ". 두 파일을 data/raw/에 배치하세요."
        )

    X = pd.read_csv(feature_path, sep=r"\s+", header=None)
    X.columns = [f"feature_{index}" for index in range(X.shape[1])]
    labels = pd.read_csv(
        label_path,
        sep=r"\s+",
        header=None,
        names=["label", "timestamp"],
    )
    labels["timestamp"] = pd.to_datetime(
        labels["timestamp"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
    )
    labels["is_fail"] = (labels["label"] == 1).astype(int)

    if len(X) != len(labels):
        raise ValueError(f"feature 행({len(X)})과 label 행({len(labels)}) 수가 다릅니다.")
    return X, labels


def data_quality_reports(
    X: pd.DataFrame,
    is_fail: pd.Series,
    missing_threshold: float = 0.5,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str]]:
    """Build summary and removal-candidate reports without imputing data."""
    missing_rate = X.isna().mean()
    missing_summary = (
        pd.DataFrame({"feature": X.columns, "missing_rate": missing_rate.values})
        .sort_values("missing_rate", ascending=False)
        .reset_index(drop=True)
    )
    high_missing = set(missing_rate[missing_rate >= missing_threshold].index)
    constant = set(X.columns[X.nunique(dropna=True) <= 1])
    drop_candidates = sorted(high_missing | constant)
    kept_features = [column for column in X.columns if column not in drop_candidates]

    constant_features = pd.DataFrame({"feature": sorted(constant)})
    drop_candidate_features = pd.DataFrame(
        {
            "feature": drop_candidates,
            "high_missing": [feature in high_missing for feature in drop_candidates],
            "constant": [feature in constant for feature in drop_candidates],
        }
    )
    fail_count = int(is_fail.sum())
    summary = pd.DataFrame(
        {
            "metric": [
                "total_samples", "total_features", "pass_count", "fail_count",
                "fail_rate", "features_with_missing", "features_missing_ge_50pct",
                "constant_features", "features_after_drop_candidates",
            ],
            "value": [
                len(X), X.shape[1], len(X) - fail_count, fail_count,
                float(is_fail.mean()), int((missing_rate > 0).sum()), len(high_missing),
                len(constant), len(kept_features),
            ],
        }
    )
    return summary, missing_summary, constant_features, drop_candidate_features, kept_features


def compare_pass_fail(
    X: pd.DataFrame,
    is_fail: pd.Series,
    features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Rank candidates by standardized mean difference and Mann-Whitney U test."""
    try:
        from scipy.stats import mannwhitneyu
    except ImportError as exc:
        raise ImportError(
            "통계 EDA에는 scipy가 필요합니다. `pip install -r requirements.txt`를 실행하세요."
        ) from exc

    rows = []
    for feature in features:
        passed = X.loc[is_fail.eq(0), feature].dropna()
        failed = X.loc[is_fail.eq(1), feature].dropna()
        if passed.empty or failed.empty:
            continue

        pooled_sd = np.sqrt((passed.var(ddof=1) + failed.var(ddof=1)) / 2)
        standardized_diff = (
            (failed.mean() - passed.mean()) / pooled_sd if pooled_sd > 0 else np.nan
        )
        statistic, p_value = mannwhitneyu(failed, passed, alternative="two-sided")
        rows.append(
            {
                "feature": feature,
                "pass_n": len(passed),
                "fail_n": len(failed),
                "pass_mean": passed.mean(),
                "fail_mean": failed.mean(),
                "mean_diff": failed.mean() - passed.mean(),
                "standardized_mean_diff": standardized_diff,
                "mannwhitney_u": statistic,
                "p_value": p_value,
            }
        )

    result = pd.DataFrame(rows)
    if result.empty:
        return result, result
    by_difference = result.assign(
        abs_standardized_mean_diff=result["standardized_mean_diff"].abs()
    ).sort_values("abs_standardized_mean_diff", ascending=False)
    by_test = result.assign(
        fdr_bh=_benjamini_hochberg(result["p_value"].to_numpy())
    ).sort_values(["fdr_bh", "p_value"])
    return by_difference, by_test


def _benjamini_hochberg(p_values: np.ndarray) -> np.ndarray:
    """Return Benjamini-Hochberg adjusted p-values."""
    order = np.argsort(p_values)
    ranked = p_values[order]
    adjusted = ranked * len(ranked) / np.arange(1, len(ranked) + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1].clip(0, 1)
    output = np.empty_like(adjusted)
    output[order] = adjusted
    return output
