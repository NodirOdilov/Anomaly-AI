"""Калибровка вероятностей через CalibratedClassifierCV.

Применяется поверх обученного классификатора для получения честных
``predict_proba`` (особенно полезно для RandomForest, у которого raw-вероятности
систематически завышены к крайностям).
"""

from __future__ import annotations

from typing import Any, Literal

from sklearn.calibration import CalibratedClassifierCV

CalibrationMethod = Literal["sigmoid", "isotonic"]


def calibrate_classifier(
    base_estimator: Any,
    X_calib: Any,
    y_calib: Any,
    *,
    method: CalibrationMethod = "isotonic",
    cv: int = 5,
) -> CalibratedClassifierCV:
    """Обернуть классификатор калибратором и обучить на отдельной выборке."""
    cal = CalibratedClassifierCV(base_estimator, method=method, cv=cv)
    cal.fit(X_calib, y_calib)
    return cal


__all__ = ["CalibrationMethod", "calibrate_classifier"]
