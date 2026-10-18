# Pattern Shield evaluation report

Data: Built-in synthetic template-generated requests

Training seconds: 29.5

Validation-selected threshold: 0.930

## Results

test: transformer macro-F1=0.9478; baseline macro-F1=1.0000; alert FPR=0.0067; attack recall=1.0000

challenge: transformer macro-F1=0.7593; baseline macro-F1=0.8869; alert FPR=0.5200; attack recall=1.0000

## Interpretation

Dataset-specific measurements; not production accuracy or proof of zero-day detection.

## Triage

Flagged requests are investigation leads, not confirmed vulnerabilities. Validate application behavior in an authorized test environment.

## Remediation

SQLi: parameterized queries and least-privilege database accounts. XSS: context-aware output encoding, safe DOM APIs and suitable sanitization; CSP as defense in depth.

CWE-89 and CWE-79 describe the weakness classes. ATT&CK T1190 is conditional on exploitation context, not an automatic payload label.

## Reproduce

Use this notebook, saved dataset and manifest. Only load trusted model/joblib files.