"""Leakage-safe baseline modeling utilities for SECOM Fail prediction."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    make_scorer,
)
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_predict,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42


def build_baseline_models(random_state: int = RANDOM_STATE) -> dict[str, BaseEstimator]:
    """Return reproducible baselines with all learned preprocessing in pipelines."""
    return {
        "dummy_prior": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("model", DummyClassifier(strategy="prior", random_state=random_state)),
            ]
        ),
        "logistic_balanced": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=3000,
                        solver="liblinear",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "random_forest_balanced": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        min_samples_leaf=2,
                        class_weight="balanced_subsample",
                        n_jobs=1,
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "hist_gradient_boosting_balanced": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        learning_rate=0.05,
                        max_iter=200,
                        l2_regularization=1.0,
                        class_weight="balanced",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def stratified_holdout(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Create a deterministic holdout while preserving the rare Fail ratio."""
    return train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )


def cross_validated_model_comparison(
    models: Mapping[str, BaseEstimator],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 5,
    n_repeats: int = 3,
    random_state: int = RANDOM_STATE,
) -> pd.DataFrame:
    """Compare models using repeated stratified CV on the training set only."""
    scoring = {
        "pr_auc": "average_precision",
        "fail_recall": make_scorer(recall_score, zero_division=0),
        "precision": make_scorer(precision_score, zero_division=0),
        "f1": make_scorer(f1_score, zero_division=0),
        "balanced_accuracy": "balanced_accuracy",
    }
    cv = RepeatedStratifiedKFold(
        n_splits=n_splits,
        n_repeats=n_repeats,
        random_state=random_state,
    )
    rows: list[dict[str, float | str]] = []
    for name, model in models.items():
        scores = cross_validate(
            model,
            X_train,
            y_train,
            scoring=scoring,
            cv=cv,
            n_jobs=1,
            error_score="raise",
        )
        row: dict[str, float | str] = {"model": name}
        for metric in scoring:
            values = scores[f"test_{metric}"]
            row[f"{metric}_mean"] = float(values.mean())
            row[f"{metric}_std"] = float(values.std(ddof=1))
        rows.append(row)
    return pd.DataFrame(rows).sort_values("pr_auc_mean", ascending=False).reset_index(drop=True)


def default_threshold_test_comparison(
    models: Mapping[str, BaseEstimator],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[pd.DataFrame, dict[str, BaseEstimator]]:
    """Fit each baseline once and evaluate the untouched holdout at threshold 0.5."""
    rows = []
    fitted: dict[str, BaseEstimator] = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        fitted[name] = model
        probabilities = model.predict_proba(X_test)[:, 1]
        rows.append(classification_metrics(y_test, probabilities, threshold=0.5, model=name))
    return (
        pd.DataFrame(rows).sort_values("pr_auc", ascending=False).reset_index(drop=True),
        fitted,
    )


def out_of_fold_probabilities(
    model: BaseEstimator,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 5,
    random_state: int = RANDOM_STATE,
) -> np.ndarray:
    """Generate threshold-tuning probabilities without using the holdout set."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    return cross_val_predict(
        model,
        X_train,
        y_train,
        cv=cv,
        method="predict_proba",
        n_jobs=1,
    )[:, 1]


def threshold_table(
    y_true: pd.Series | np.ndarray,
    probabilities: np.ndarray,
    thresholds: np.ndarray | None = None,
) -> pd.DataFrame:
    """Evaluate operating-point tradeoffs over a fixed threshold grid."""
    if thresholds is None:
        thresholds = np.round(np.linspace(0.01, 0.99, 99), 2)
    rows = [classification_metrics(y_true, probabilities, float(t)) for t in thresholds]
    return pd.DataFrame(rows)


def select_recall_constrained_threshold(
    table: pd.DataFrame,
    minimum_recall: float = 0.8,
) -> float:
    """Maximize precision subject to a minimum Fail Recall requirement."""
    eligible = table[table["fail_recall"] >= minimum_recall]
    if eligible.empty:
        return float(table.sort_values(["fail_recall", "precision"], ascending=False).iloc[0]["threshold"])
    selected = eligible.sort_values(
        ["precision", "fail_recall", "threshold"],
        ascending=[False, False, False],
    ).iloc[0]
    return float(selected["threshold"])


def classification_metrics(
    y_true: pd.Series | np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
    model: str | None = None,
) -> dict[str, float | int | str]:
    """Return quality-oriented binary classification metrics."""
    predictions = (np.asarray(probabilities) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, predictions, labels=[0, 1]).ravel()
    result: dict[str, float | int | str] = {
        "threshold": float(threshold),
        "fail_recall": float(recall_score(y_true, predictions, zero_division=0)),
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
        "pr_auc": float(average_precision_score(y_true, probabilities)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, predictions)),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }
    if model is not None:
        result = {"model": model, **result}
    return result
