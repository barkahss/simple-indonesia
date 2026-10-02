# Changelog — simple-indonesia

## v1.6.0

- Contoh Sesudah kini 0 pelanggaran (baris meta ditulis ulang tanpa sebut kata slop).
- Pressure test: `evals/pressure_scenarios.json` (5 jebakan) + `evals/pressure-tests.md` berisi hasil tercatat qwen3.8-max (lint 15 vs 10; 1 lulus, 4 parsial). Temuan skenario-3 melahirkan aturan anti-penomoran di SKILL.md.
- Bench balasan: `evals/reply_scenarios.json` (8 pertanyaan) + `evals/run_reply_bench.py` (skor format+isi, resume, dry-run). Hasil qwen3.8-max: 349 vs 70 (turun 80%), menang 8/8.

## v1.5.0

- Riset ulang kamus: `references/kata-baku.md` dari 24 menjadi 238 entri terverifikasi silang (Ruangguru 655 x Deepublish 302, Okt 2026). Baris meragukan dibuang: beda makna, varian cakapan, ejaan Inggris, arah tak pasti. KBBI Daring wasit akhir (blokir bot, cek manual).
- `ekstrak.py` dukung frasa hindari (`nara sumber`, `olah raga`); `kamus_lint.py` cocok frasa + buang frontmatter YAML. Nol false-positive di seluruh korpus bersih repo.
- Betulkan `telanjur->terlanjur`, `cedera->cidera`, `praktik->praktek`; hapus baris noise; selaraskan `luring/offline` menjadi panduan audiens (tidak di-lint).

## v1.4.0

- Tool kamus `tools/kamus/`: `ekstrak.py` membangun `kata-baku.tsv` dari `references/kata-baku.md` (tulisan sendiri, bukan isi KBBI), `kamus_lint.py` melint pilihan kata plus akhiran melekat (-nya/-ku/-mu/-lah/-kah), keduanya dengan `--self-test`. Berkas TSV generated/lokal tidak ikut commit, mirror `tools/ste-dictionary` SimpleEnglish.

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
