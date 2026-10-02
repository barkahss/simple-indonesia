# Bench balasan — simple-indonesia (qwen3.8-max)

8 pertanyaan chat x 2 kondisi. Skor = format terlihat + pembuka/penutup + pelanggaran dokumen.

| Kondisi | Skor total |
|---|---|
| baseline | 349 |
| skill | 70 |

Penurunan: 80%.

| Pertanyaan | baseline | skill |
|---|---|---|
| balasan-idempoten | 39 | 9 |
| balasan-cache | 51 | 16 |
| balasan-deadlock | 26 | 7 |
| balasan-indeks | 27 | 4 |
| balasan-replikasi | 74 | 9 |
| balasan-rollback | 64 | 10 |
| balasan-webhook | 40 | 6 |
| balasan-retry | 28 | 9 |
