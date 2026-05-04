# Model card (summary)

## Purpose

Provide **baseline** classifiers for:

- Malicious web payload categories (defensive labeling).
- Network flow labels for demo feature sets.

## Intended use

- Education, portfolio demos, local experimentation, and interviews.
- Triage assistance on data you are authorized to process.

## Not intended use

- Unsupervised authorization to attack external systems.
- Sole decision-maker for blocking production traffic without human review.
- Claiming calibrated production metrics without proper validation data.

## Metrics

Metrics are stored inside each joblib artifact under `metrics` after training/evaluation. If you have not trained locally, API summaries may show zeros — this is intentional honesty for fresh checkouts.

## Limitations

- Small demo datasets can yield unstable or non-generalizable performance.
- Attackers adapt; static ML models drift without monitoring and retraining.
- Rule hints are conservative pattern matchers — they reduce ambiguity but are not a complete WAF.

## Ethical / security posture

Defensive-only. Payload strings are treated as data for classification, not executed.

## Operational notes

For real deployments you would add authentication, audit logging, rate limits, SIEM export, and model monitoring — see `ROADMAP.md`.
