# Five-minute interview demonstration

## Before the call
Run the notebook once. Save the outputs and download its ZIP. Keep the notebook, README and results image open. Do not rely on obtaining a GPU during the interview.

## 0:00–0:40 — State the problem
“Pattern Shield classifies request text as benign, SQLi or XSS. It is an offline research prototype. It does not scan websites or prove a server is vulnerable.”

Show the three classes and the synthetic-data statement.

## 0:40–1:30 — Explain the architecture
Open assets/architecture.png.
- Left branch: bounded normalization, byte tokens, embeddings, transformer, masked pooling.
- Right branch: eight standardized statistics.
- Merge: 56 features into a small classification head.
- Separate three-class prediction from the binary alert rule.

If asked “Why transformer?”, say it is a hypothesis under comparison, not an assumption of superiority.

## 1:30–2:20 — Explain the experiment
Open assets/evaluation_flow.png.
- Template groups are assigned before generation.
- Training fits parameters and scalers.
- Validation selects checkpoint and threshold.
- Test/challenge remain outside that selection.

Explain that this controls some leakage but does not remove generator bias.

## 2:20–3:20 — Show measured results
Open assets/evaluation.png and assets/confusion_matrices.png.
- Test transformer macro-F1 ≈ 0.948.
- Baseline test macro-F1 = 1.000 on this synthetic set.
- Challenge transformer macro-F1 ≈ 0.759.
- Challenge alert FPR = 52%.

Say: “The baseline won. My next priority would be better data and evaluation, not a larger transformer.”

## 3:20–4:15 — Test a few strings
In the notebook, run predict_requests with:
- A benign shopping search.
- The provided SQLi-like example.
- The provided XSS-like example.
- A benign security-documentation query.

Look at the actual outputs. Do not promise a label before execution. Explain the truncation and low-confidence flags. If a benign request is flagged, use it to discuss false positives.

## 4:15–5:00 — Close with scope and next steps
Show the exported report.
“The pipeline is reproducible and the serialization check passes. Before operational use I need representative authorized data, better parsing, calibration, realistic alert costs and shadow-mode validation.”

## If the runtime fails
Use the saved notebook outputs and archived metrics. Explain that they came from the recorded local run. Do not pretend a saved image is a live result.

## If asked what you personally did
Describe exactly what you ran, understood, modified and verified. Acknowledge AI assistance where asked. Do not invent independent implementation history, customer deployment or months of research.

