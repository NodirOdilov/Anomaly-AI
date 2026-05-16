"""Лёгкая объяснимость предсказаний (без зависимости от SHAP).

- :func:`explain_linear_text` — топ-N n-грамм для текстовых моделей (TF-IDF + LogReg/SVM).
- :func:`explain_tree_tabular` — топ-N важных признаков для деревьев/леса.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class FeatureContribution:
    """Один признак и его вклад в предсказание."""

    name: str
    weight: float


def explain_linear_text(
    pipeline: Any,
    text: str,
    *,
    top_n: int = 10,
    class_label: str | None = None,
) -> list[FeatureContribution]:
    """Объяснение для pipeline ``vectorizer -> linear_classifier``.

    Берёт коэффициенты классификатора для выбранного класса и умножает на
    активные TF-IDF признаки текста. Сортирует по абсолютному весу.
    """
    try:
        vectorizer = pipeline.named_steps.get("vectorizer") or pipeline.named_steps.get("tfidf")
        classifier = (
            pipeline.named_steps.get("classifier")
            or pipeline.named_steps.get("clf")
            or pipeline.named_steps.get("lr")
        )
        if vectorizer is None or classifier is None:
            return []
    except AttributeError:
        return []

    feature_names = np.asarray(vectorizer.get_feature_names_out())
    vec = vectorizer.transform([text])
    if vec.nnz == 0:
        return []

    coefs = getattr(classifier, "coef_", None)
    classes = getattr(classifier, "classes_", None)
    if coefs is None or classes is None:
        return []

    # Выбор строки коэффициентов для нужного класса.
    class_idx = (
        list(classes).index(class_label)
        if class_label is not None and class_label in classes
        else 0
    )
    row = coefs[class_idx] if coefs.ndim > 1 else coefs

    # Активные индексы в текущем документе.
    indices = vec.indices
    values = vec.data
    contributions = values * row[indices]
    pairs = list(zip(feature_names[indices], contributions, strict=True))
    pairs.sort(key=lambda kv: abs(kv[1]), reverse=True)
    return [FeatureContribution(name=str(n), weight=float(w)) for n, w in pairs[:top_n]]


def explain_tree_tabular(
    pipeline: Any,
    feature_names: list[str],
    *,
    top_n: int = 10,
) -> list[FeatureContribution]:
    """Глобальная важность признаков для tree-based моделей."""
    try:
        classifier = (
            pipeline.named_steps.get("classifier")
            or pipeline.named_steps.get("clf")
            or pipeline.named_steps.get("rf")
        )
    except AttributeError:
        return []
    if classifier is None:
        return []
    importances = getattr(classifier, "feature_importances_", None)
    if importances is None:
        return []
    pairs = list(zip(feature_names, importances, strict=True))
    pairs.sort(key=lambda kv: kv[1], reverse=True)
    return [FeatureContribution(name=str(n), weight=float(w)) for n, w in pairs[:top_n]]


__all__ = ["FeatureContribution", "explain_linear_text", "explain_tree_tabular"]
