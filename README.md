# Simple Indonesia

Skill Agent Skills agar LLM menulis **Bahasa Indonesia yang bersih, tanpa bau AI** — dengan disiplin ASD-STE100 yang diadaptasi ke EYD V dan KBBI. Dioptimasi khusus Bahasa Indonesia (kalimat efektif, 238 kata baku terverifikasi silang, slop AI Indonesia), bukan terjemahan mentah versi Inggris.

Repo ini **adalah** skill-nya langsung (skill-at-root): `SKILL.md` ada di root.

## Kenapa begini (metode Karpathy)

Karpathy menyarankan: minta LLM menjelaskan dalam **ASD-STE100** — bahasa terkendali aerospace untuk manual perawatan. LLM sangat paham bahasa ini; batasannya yang berat menghasilkan gaya tulisan yang jauh lebih mudah dibaca. Karena spec aslinya sangat ketat, baku skill ini adalah **80% jalan ke ASD-STE100**: tegas tetapi tetap natural.

## Fitur

- Dua register: **Dokumen** (prosedural 20 kata/kalimat, deskriptif 25 kata) dan **Balasan** (prosa saja, jawab dulu).
- Dua mode: **Plain** (baku) dan **Strict** (tambah disiplin KBBI + EYD V bila Anda sebut STE/ASD-STE100/EYD/KBBI/kepatuhan).
- Lint deterministik, bench terukur, hook sesi, plugin Claude + Codex, tool kamus kata baku.

## Isi

```
simple-indonesia/
  SKILL.md                    # instruksi utama (progressive disclosure)
  references/
    kata-ganti.md             # peta kata berlebih AI -> pengganti polos
    kasus-pakai.md            # pola untuk galat, runbook, insiden, rilis, UI, terjemahan
    katalog-aturan.md         # adaptasi 53 aturan untuk mode PERIKSA (parafrasa)
    kata-baku.md              # 238 kata baku vs tidak baku + disiplin KBBI/EYD V
  examples/
    sebelum-sesudah.md        # contoh rewrite Indonesia (Sesudah = 0 pelanggaran)
  evals/
    id_lint.py                # lint deterministik + --self-test
    scenarios.json            # 8 skenario uji Bahasa Indonesia
    pressure_scenarios.json   # 5 skenario tekanan + pressure-tests.md berisi hasil
    reply_scenarios.json      # 8 pertanyaan chat untuk bench balasan
    slop_id.tsv               # leksikon bau AI Indonesia
    check_examples.py         # pastikan Sesudah lebih bersih dari Sebelum
    run_eval.py               # hitung ulang angka ke results/RESULTS.md
    run_bench.py              # bench dokumen (--scenarios, resume, dry-run)
    run_reply_bench.py        # bench balasan (resume, dry-run)
    fixtures/                 # bukti uji (asli vs bersih)
    results/                  # angka terukur + output mentah bench
  prompts/
    system-prompt.md          # versi ringkas + ~60 token untuk harness tanpa SKILL.md
  output-styles/
    simple-indonesia.md       # gaya output untuk Claude Code
  src/hooks/
    lint_hook.py              # hook nasihat PostToolUse dan Stop
    simple-indonesia-activate.js  # hook SessionStart, muat blok aturan
  .claude-plugin/             # marketplace + plugin Claude Code
  .codex-plugin/              # plugin Codex
  tools/kamus/                # ekstraktor + lint pilihan kata (tanpa isi KBBI)
```

## Pasang

```sh
# Agen apa pun (skills CLI), dari GitHub:
npx skills add barkahss/simple-indonesia

# Claude Code (plugin):
claude plugin marketplace add barkahss/simple-indonesia && claude plugin install simple-indonesia@simple-indonesia

# Codex (plugin, hook butuh Node.js):
codex plugin marketplace add barkahss/simple-indonesia
codex plugin add simple-indonesia@simple-indonesia
```

Gaya output saja: pilih `simple-indonesia:simple-indonesia` di `/config` Output style (nama pendek tidak resolve).

Opencode / Cursor / Copilot / Gemini CLI: salin folder repo ini ke folder skills agen. Tanpa dukungan skill? Tempel blok dari `prompts/system-prompt.md` ke system prompt, `AGENTS.md`, atau `.cursorrules`.

Lalu minta: "tulis ulang ini dengan simple-indonesia" atau "jelaskan dengan bahasa sederhana".

## Bukti angka (qwen3.8-max lokal, Okt 2026)

| Bench | Baseline | Skill | Turun |
|---|---|---|---|
| Dokumen (8 skenario) | 25 | 1 | 96% |
| Balasan (8 pertanyaan) | 349 | 70 | 80% |
| Contoh (sebelum→sesudah) | 12 | 0 | 100% |
| Pressure (5 jebakan) | 15 | 10 | 33% + 1 lulus, 4 parsial kriteria perilaku |

Detail mentah: `evals/results/`. Bukan vonis kepatuhan — tidak ada alat yang menjamin kepatuhan ASD-STE100.

## Uji

```sh
python evals/id_lint.py --self-test
python src/hooks/test_lint_hook.py
node --test src/hooks/simple-indonesia-activate.test.js
python evals/check_examples.py
python evals/run_eval.py --check
python evals/run_bench.py --dry-run        # bench asli butuh $env:LLM_API_KEY
python evals/run_reply_bench.py --dry-run
python tools/kamus/ekstrak.py --self-test
python tools/kamus/kamus_lint.py --self-test
```

## Sumber

- Saran Karpathy soal ASD-STE100 untuk output LLM — cuitan "We'll be spending a lot more time trying to understand the outputs of language models" (@karpathy, [https://x.com/karpathy](https://x.com/karpathy/status/2105819303471976479)).
- Acuan struktur (Inggris): AminBlg/SimpleEnglish — https://github.com/AminBlg/SimpleEnglish.
- Standar ASD-STE100 Issue 9 (53 aturan, ~900 kata), unduhan resmi gratis — https://www.asd-ste100.org.
- Spesifikasi Agent Skills (Anthropic, standar terbuka) — https://agentskills.io/specification.
- KBBI Daring, wasit akhir kata baku — https://kbbi.kemdikbud.go.id.
- EYD V / Pedoman Umum Ejaan, Badan Bahasa — https://badanbahasa.kemdikbud.go.id.
- Daftar kata baku pembanding (655): Ruangguru — https://www.ruangguru.com/blog/contoh-kata-baku-dan-tidak-baku.
- Daftar kata baku pembanding (302): Deepublish — https://penerbitdeepublish.com/panduan-menulis/kata-baku-dan-tidak-baku/.
- Repo ini: https://github.com/barkahss/simple-indonesia.

## Lisensi

MIT — lihat `LICENSE`. Parafrasa untuk pengajaran; tidak mereproduksi teks spec ASD-STE100 maupun isi KBBI. Proyek tidak berafiliasi dengan ASD, STEMG, atau Badan Bahasa.
