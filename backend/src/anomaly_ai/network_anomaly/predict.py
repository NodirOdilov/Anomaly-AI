from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from anomaly_ai.common.paths import backend_root, resolve_under_root
from anomaly_ai.network_anomaly.service import NetworkAnomalyService
from anomaly_ai.services.artifact_loader import load_network_artifact


def main() -> None:
    parser = argparse.ArgumentParser(description="Network anomaly CLI predict (CSV batch)")
    parser.add_argument("--model", required=True)
    parser.add_argument("--input", required=True, dest="input_path", help="CSV with feature columns")
    args = parser.parse_args()

    base = backend_root()
    model_path = Path(args.model)
    if not model_path.is_absolute():
        model_path = resolve_under_root(str(model_path), base)
    in_path = Path(args.input_path)
    if not in_path.is_absolute():
        in_path = resolve_under_root(str(in_path), base)

    artifact = load_network_artifact(model_path)
    service = NetworkAnomalyService(artifact)
    df = pd.read_csv(in_path)
    res = service.predict_csv(df)
    print(res.model_dump())


if __name__ == "__main__":
    main()
