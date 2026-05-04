# Security Policy

## Defensive use only

Anomaly AI is intended **only** for defensive security purposes: education, research, portfolio demonstration, and **detection** of potentially malicious patterns in data you are authorized to analyze.

## Allowed uses

- Learning how ML can assist SOC and application security workflows
- Classifying payloads and network flow features **you own or have permission to process**
- Local demos, coursework, and interviews with synthetic or authorized datasets

## Prohibited uses

1. Attacking or attempting to compromise real systems without explicit authorization
- Unauthorized scanning, exploitation, or bypass of production defenses
- Using the project as offensive tooling against third parties

2. Misrepresenting model outputs as guaranteed ground truth — models here may be **demo/baseline** quality; always validate in your environment.

## Reporting vulnerabilities

If you discover a security issue in this repository (e.g., unsafe defaults in deployment), please open a private report or issue according to the repository maintainer’s preferred process.

## Payload examples

Sample payloads (e.g., SQLi/XSS strings) exist **solely** as labeled inputs for classification demos. They must not be used to attack live applications.

## Contact

Use the repository’s issue tracker for security-related questions tied to this codebase.
