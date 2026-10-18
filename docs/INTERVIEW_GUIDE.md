## Interview preparation
**A truthful explanation after you run and understand the notebook:**

“Pattern Shield is a Colab prototype that classifies request text as benign, SQL injection or XSS. It uses byte embeddings and a small transformer encoder, combined with eight statistical features. I compare it against a character TF–IDF logistic-regression baseline. Templates are separated across training, validation and testing; the checkpoint and alert threshold use validation data only. I review false positives and held-out-template failures. The default data are synthetic, so these scores do not establish production accuracy or zero-day detection.”

If asked about development, acknowledge AI assistance and specify what you personally ran, changed and validated. Do not imply previous deployments or months of research that did not happen.

| Likely question | Answer |
|---|---|
| Why a transformer? | Self-attention can learn relations between byte positions. Whether it beats simpler methods must be measured. |
| What is attention? | softmax(QKᵀ / √dₖ)V: queries compare against keys to weight value vectors. Multiple heads learn different relationships. |
| Why bytes? | Fixed vocabulary handles punctuation/encoding without unknown-word tokens; the tradeoff is longer sequences. |
| What encodes position? | A trainable 256-position embedding added to byte embeddings. |
| What is the loss and optimizer? | Class-weighted cross-entropy and AdamW, with gradient clipping and validation checkpoint selection. |
| What features? | Length, percent/quote/angle/digit/space/punctuation ratios and character entropy; scaler fits training only. |
| What prevents leakage? | Disjoint template groups, canonical deduplication, train-only fitting and validation-only selection. Real traffic also needs source/session/time separation and stronger near-duplicate checks. |
| Why macro-F1? | It weights each class equally; accuracy can hide minority-class failures. Also report per-class precision/recall and alert FPR. |
| Precision versus recall? | Precision = TP/(TP+FP), recall = TP/(TP+FN), FPR = FP/(FP+TN). |
| How choose threshold? | Maximize binary validation F1 in this demo. Production needs representative prevalence and a false-positive budget. |
| Does 0.95 mean 95% attack probability? | No: uncalibrated softmax scores. Calibration requires separate representative validation. |
| Unseen attacks? | Held-out templates/subtypes test limited generalization. Zero-day detection is not established. |
| Behavioral analysis? | A separate rules-based aggregation counts requests, alerts and paths per client/minute. It is not a trained behavior model. |
| Is it a vulnerability scanner? | No. Offline request classification; no asset discovery or proof of server-side exploitability. |
| MITRE mapping? | CWE-89 for SQLi and CWE-79 for XSS. ATT&CK T1190 is contextual, only where exploitation of a public-facing application is established. |
| What if baseline wins? | Report it honestly. Simpler models may be better for small datasets and tight latency budgets. |
| Biggest limitations? | Synthetic bias, short context, imperfect decoding, no response context, uncalibrated scores and no production validation. |
| Next steps? | Real authorized data, audited labels, time/source split, HTTP-aware parsing, calibration, drift monitoring and shadow-mode testing. |

### Five-minute demonstration
1. Show data counts and explain synthetic provenance.
2. Explain the model and masks.
3. Show transformer versus baseline results and confusion matrices.
4. Try benign and malicious strings; show a mistake or ambiguous case.
5. Show challenge performance, exported report and limitations.

### What the original resume bullets overstate
- **Previously unseen attacks:** only held-out-template generalization is evaluated.
- **Web traffic datasets:** default data are synthetic, not captured production traffic.
- **Automated discovery scans:** not implemented.
- **Behavioral analysis:** simple log aggregation rules, not learned behavior.
- **PoC reporting:** an evaluation/triage report, not a confirmed exploitation PoC.

A strong interviewer will test these distinctions. Do not defend capabilities you have not implemented and verified.

### Troubleshooting
- No GPU: CPU fallback is automatic. Training may take longer.
- CUDA out of memory: reduce BATCH_SIZE to 16 and rerun all.
- CSV assertion: repair schema/groups/classes; do not delete leakage checks.
- Low challenge score: report the limitation. Do not tune on it while still calling it an untouched test.
- Colab disconnect: runtime files are temporary; download the ZIP and save notebook outputs.

### References
- [PyTorch TransformerEncoder](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder.html)
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)

