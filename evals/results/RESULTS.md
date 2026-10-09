# Hasil eval — simple-indonesia

Dihitung ulang oleh `evals/run_eval.py` dari berkas mentah memakai `evals/id_lint.py`.
Bukan vonis kepatuhan ASD-STE100. Tidak ada alat yang menjamin kepatuhan.

| Pasangan | Asli (pelanggaran) | Bersih (pelanggaran) | Turun | per-100kata asli -> bersih | Kategori teratas asli |
|---|---|---|---|---|---|
| screenshot1-reply.txt -> screenshot1-bersih.txt | 14 + opener=1 | 0 | 100% | 5.38 -> 0.0 | english_bare=9, comma_overload=2, perfect_tense=1 |
| screenshot2-reply.txt -> screenshot2-bersih.txt | 4 | 0 | 100% | 3.81 -> 0.0 | sentence_over_limit=1, perfect_tense=1, english_bare=1 |
| contoh sebelum-sesudah.md (agregat) | 13 | 0 | 100% | - | - |

