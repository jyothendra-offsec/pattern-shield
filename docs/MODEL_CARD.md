# Model card

## Identity
**Pattern Shield**, a 64,579-parameter byte-level transformer classifier trained from scratch. Labels in index order: benign, sqli, xss.

## Intended use
Learning, reproducible offline experiments, and supervised review of request-like text in an application-security research context.

## Not established
Production WAF effectiveness; general vulnerability detection; zero-day detection; real-time throughput; adversarial robustness; calibrated attack probability; successful exploitation; discovery scanning; cloud deployment.

## Data
The recorded run uses internally generated synthetic request templates. No production/customer traffic or external benchmark dataset was used. See the data card for exact counts, partitioning and limitations.

## Metrics
| Split | Accuracy | Macro-F1 | Baseline macro-F1 | Alert FPR | Attack recall |
|---|---:|---:|---:|---:|---:|
| Test | 0.9489 | 0.9478 | 1.0000 | 0.0067 | 1.0000 |
| Challenge | 0.7900 | 0.7593 | 0.8869 | 0.5200 | 1.0000 |

The baseline is better on both macro-F1 comparisons. The challenge false-positive rate indicates poor transfer of the selected alert policy to difficult benign examples. These findings must remain visible when presenting the project.

## Evaluation limitations
One seeded run, synthetic partitions from one generator, balanced evaluation classes, no production prevalence, no confidence intervals, no source-independent external validation and no robustness benchmark. Template-disjoint does not mean distribution-independent.

## Known failure modes
- Benign technical documentation can resemble payloads.
- Decoding can make escaped benign syntax look executable.
- Attacks outside the first 256 normalized bytes can be missed.
- Multipart, JSON, cookies, headers and application-specific encodings are not parsed semantically.
- A closed-set model must assign known-class scores even to unfamiliar inputs.
- Wrapper artifacts or generator regularities may influence learning.
- High confidence does not imply correctness.

## Operational safeguards before any deployment
Use representative authorized traffic; audit labels; evaluate real prevalence and cost; calibrate on separate data; benchmark throughput; define oversized-input behavior; use human-reviewed shadow mode; monitor drift. No automatic blocking is justified by this experiment.

## Reproduction
Run the notebook from top to bottom or execute the script from the repository root. The archived results include the dataset, digest, configuration and tested version snapshot. Runtime differences may change exact measurements.

## Provenance
Developed with AI assistance. Validation was executed locally on CPU, not within the user's Google Colab session. This project should be represented as a prototype, not as previously deployed professional work.

