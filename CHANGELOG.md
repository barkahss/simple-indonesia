# Changelog — simple-indonesia

## v1.3.0

- Plugin Codex: `.codex-plugin/plugin.json` + `hooks.json` (SessionStart, skills di root).
- Bench beneran `evals/run_bench.py`: generate baseline vs skill via API OpenAI-compatible (kunci hanya dari env `LLM_API_KEY`, tidak pernah ditulis ke berkas), nilai dengan `id_lint`, tulis `evals/results/bench/<model-stamp>/`. `--dry-run` untuk tanpa API.

## v1.2.0

- Plugin Claude Code: `.claude-plugin/marketplace.json` + `plugin.json` (SessionStart, PostToolUse, Stop).
- Hook aktivasi `src/hooks/simple-indonesia-activate.js` + uji Node (`node --test`), port dari SimpleEnglish dengan penyesuaian Windows.
- Eval runner `evals/run_eval.py`: hitung ulang angka dari berkas mentah ke `evals/results/RESULTS.md` dengan gate (screenshot 14 dan 4 pelanggaran menjadi 0, contoh 12 menjadi 4).

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
