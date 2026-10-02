# Bench — simple-indonesia (qwen3.8-max)

5 skenario x 2 kondisi (baseline vs skill). Dinilai dengan `evals/id_lint.py`.

| Kondisi | Pelanggaran total | per-100kata |
|---|---|---|
| baseline | 15 | 4.6 |
| skill | 10 | 2.86 |

Penurunan: 33%.

| Skenario | Tipe | baseline | skill |
|---|---|---|---|
| tekanan-terse | procedural | 0 | 0 |
| tekanan-pemasaran | descriptive | 3 | 0 |
| tekanan-nomor-aturan | descriptive | 8 | 9 |
| tekanan-pasif | procedural | 0 | 0 |
| tekanan-panjang | descriptive | 4 | 1 |
