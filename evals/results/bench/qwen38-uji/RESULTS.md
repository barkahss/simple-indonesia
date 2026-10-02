# Bench — simple-indonesia (qwen3.8-max)

8 skenario x 2 kondisi (baseline vs skill). Dinilai dengan `evals/id_lint.py`.

| Kondisi | Pelanggaran total | per-100kata |
|---|---|---|
| baseline | 25 | 3.28 |
| skill | 1 | 0.13 |

Penurunan: 96%.

| Skenario | Tipe | baseline | skill |
|---|---|---|---|
| readme-intro | descriptive | 4 | 0 |
| getting-started | procedural | 3 | 0 |
| troubleshooting | procedural | 5 | 0 |
| error-message | procedural | 4 | 0 |
| incident-report | descriptive | 2 | 1 |
| release-notes | descriptive | 2 | 0 |
| runbook-terse | procedural | 0 | 0 |
| architecture | descriptive | 5 | 0 |
