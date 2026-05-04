from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Anomaly AI backend CLI")
    parser.add_argument(
        "command",
        choices=["waf-predict", "network-predict"],
        help="High-level command (prefer module-specific `python -m ...` entrypoints).",
    )
    parser.parse_args()
    print("Use: python -m anomaly_ai.waf_payload.predict / python -m anomaly_ai.network_anomaly.predict")


if __name__ == "__main__":
    main()
