from __future__ import annotations

import argparse

from anomaly_ai.common.paths import backend_root, resolve_under_root
from anomaly_ai.services.artifact_loader import load_waf_artifact
from anomaly_ai.waf_payload.service import WafPayloadService


def main() -> None:
    parser = argparse.ArgumentParser(description="WAF payload CLI predict")
    parser.add_argument("--payload", required=True)
    parser.add_argument(
        "--model",
        default="models/waf_payload_model.joblib",
        help="Path to joblib artifact (relative to backend cwd unless absolute)",
    )
    args = parser.parse_args()

    base = backend_root()
    model_path = resolve_under_root(args.model, base)
    artifact = load_waf_artifact(model_path)
    service = WafPayloadService(artifact)
    result = service.predict(args.payload)
    print(result.model_dump())


if __name__ == "__main__":
    main()
