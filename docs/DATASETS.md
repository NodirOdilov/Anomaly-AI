# Datasets

## Expectations

### WAF payload data

- **Format**: JSON array of `{ "payload": "...", "label": "..." }` or CSV with `payload,label`.
- **Labels** (demo): `benign`, `sql_injection`, `xss`, `path_traversal`, `command_injection`, `generic_injection`.
- **Location (sample)**: `backend/data/samples/sample_payloads.json` and `sample_payloads.csv`.

These samples are **tiny** and only validate the training/inference plumbing.

### Network flow data

- **Format**: CSV with numeric feature columns and a `Label` column for training.
- **Sample labels**: `BENIGN`, `HTTP_ATTACK`, `UDP_ATTACK`.
- **Location (sample)**: `backend/data/samples/sample_network_flows.csv`.

## Preparing real data

1. Place authorized raw exports under `backend/data/raw/` (not shipped).
2. Normalize column names and remove identifiers you do not want in training.
3. Generate splits under `backend/data/processed/` with clear provenance.
4. Retrain using `configs/*.yaml` and record metrics honestly in artifacts and `reports/`.

## Limitations

Demo samples are not representative of production traffic or attacker diversity. For coursework/portfolio, disclose dataset size and limitations explicitly.
