from __future__ import annotations

from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_waf_pipeline(cfg: dict[str, Any]) -> Pipeline:
    train_cfg = cfg.get("train", {})
    vec_cfg = train_cfg.get("vectorizer", {})
    analyzer = vec_cfg.get("analyzer", "char")
    ngram_range = (int(vec_cfg.get("ngram_min", 2)), int(vec_cfg.get("ngram_max", 5)))
    max_features = int(vec_cfg.get("max_features", 50_000))

    clf_name = train_cfg.get("classifier", "logistic_regression")
    if clf_name != "logistic_regression":
        raise ValueError(f"Unsupported classifier: {clf_name}")

    lr = LogisticRegression(
        C=float(train_cfg.get("lr_c", 1.0)),
        max_iter=int(train_cfg.get("max_iter", 2000)),
        class_weight="balanced",
        solver="saga",
    )

    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer=analyzer,
                    ngram_range=ngram_range,
                    max_features=max_features,
                ),
            ),
            ("clf", lr),
        ]
    )
