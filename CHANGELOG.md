# Changelog — simple-indonesia

## v1.1.0

- Port `ste_lint.py` SimpleEnglish menjadi `evals/id_lint.py` untuk Bahasa Indonesia + EYD V: modal terlarang, `telah/sudah`, singkatan informal, klausa menggantung, `english_bare`, `comma_overload`, `paragraph_overload`, opener/closer balasan.
- Tambah `evals/scenarios.json` (8 skenario Indonesia), `evals/slop_id.tsv`, `evals/check_examples.py`.
- Tambah `prompts/system-prompt.md` (versi ringkas + ~60 token) dan `output-styles/simple-indonesia.md`.
- Tambah `src/hooks/lint_hook.py` (nasihat PostToolUse dan Stop) + `test_lint_hook.py`.
- Bukti uji di `evals/fixtures/`: balasan asli 14 dan 4 pelanggaran menjadi 0 setelah tulis ulang bersih.
- `SKILL.md` naik ke versi 1.1.0 dengan bagian alat dan evaluasi.

## v1.0.0

- Skill awal: `SKILL.md` dua register (Dokumen dan Balasan), mode Plain 80% STE dan Strict EYD/KBBI.
- Referensi: `kata-ganti.md`, `kasus-pakai.md`, `katalog-aturan.md`, `kata-baku.md`.
- Contoh: `examples/sebelum-sesudah.md`.
