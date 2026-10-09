# Simple Indonesia

Skill Agent Skills agar LLM menulis Bahasa Indonesia yang bersih tanpa bau AI. Skill ini memakai disiplin ASD-STE100 yang diadaptasi ke EYD V dan KBBI. Skill ini dioptimasi khusus Bahasa Indonesia: kalimat efektif, 238 kata baku terverifikasi silang, dan leksikon slop AI Indonesia. Ini bukan terjemahan mentah versi Inggris.

Repo ini adalah skill-nya langsung. `SKILL.md` ada di root.

## Kenapa begini (metode Karpathy)

Karpathy menyarankan: minta LLM menjelaskan dalam ASD-STE100. ASD-STE100 adalah bahasa terkendali aerospace untuk manual perawatan. LLM sangat paham bahasa ini. Batasannya yang berat menghasilkan gaya tulisan yang jauh lebih mudah dibaca. Spec aslinya sangat ketat. Baku skill ini adalah 80 persen jalan ke ASD-STE100: tegas tetapi tetap natural.

## Fitur

- Dua register. Dokumen memakai prosedural 20 kata per kalimat dan deskriptif 25 kata. Balasan memakai prosa saja dan jawab dulu.
- Dua mode. Plain adalah baku. Strict tambah disiplin KBBI dan EYD V. Strict aktif bila Anda sebut STE, ASD-STE100, EYD, KBBI, atau kepatuhan.
- Lint deterministik, bench terukur, hook sesi, plugin Claude dan Codex, tool kamus kata baku.
- Lapis gratis tiap commit: skor keterbacaan dan golden set 6 tugas.

## Isi

```text
simple-indonesia/
  SKILL.md                    # instruksi utama
  references/
    kata-ganti.md             # peta kata berlebih AI ke pengganti polos
    kasus-pakai.md            # pola galat, runbook, insiden, rilis, UI, terjemahan
    katalog-aturan.md         # adaptasi 53 aturan untuk mode PERIKSA
    kata-baku.md              # 238 kata baku vs tidak baku plus disiplin KBBI dan EYD V
  examples/
    sebelum-sesudah.md        # contoh rewrite Indonesia (Sesudah 0 pelanggaran)
  evals/
    id_lint.py                # lint deterministik plus self-test
    readability.py            # skor keterbacaan plus self-test
    golden.json               # 6 tugas baku
    scenarios.json            # 8 skenario uji Bahasa Indonesia
    pressure_scenarios.json   # 5 skenario tekanan plus hasil tercatat
    reply_scenarios.json      # 8 pertanyaan chat untuk bench balasan
    slop_id.tsv               # leksikon bau AI Indonesia
    check_examples.py         # pastikan Sesudah lebih bersih dari Sebelum
    run_eval.py               # hitung ulang angka ke results/RESULTS.md
    run_bench.py              # bench dokumen (opsi resume dan dry-run)
    run_reply_bench.py        # bench balasan (opsi resume dan dry-run)
    fixtures/                 # bukti uji (asli vs bersih)
    results/                  # angka terukur plus output mentah bench
  prompts/
    system-prompt.md          # versi ringkas plus 60 token untuk harness tanpa SKILL.md
  output-styles/
    simple-indonesia.md       # gaya output untuk Claude Code
  src/hooks/
    lint_hook.py              # hook nasihat PostToolUse dan Stop
    simple-indonesia-activate.js  # hook SessionStart, muat blok aturan
  .claude-plugin/             # marketplace plus plugin Claude Code
  .codex-plugin/              # plugin Codex
  tools/kamus/                # ekstraktor plus lint pilihan kata (tanpa isi KBBI)
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

Gaya output saja: pilih `simple-indonesia:simple-indonesia` di `/config` Output style. Nama pendek tidak resolve.

Opencode, Cursor, Copilot, Gemini CLI: salin folder repo ini ke folder skills agen. Tanpa dukungan skill? Tempel blok dari `prompts/system-prompt.md` ke system prompt, `AGENTS.md`, atau `.cursorrules`.

Lalu minta: "tulis ulang ini dengan simple-indonesia" atau "jelaskan dengan bahasa sederhana".

## Bukti angka (Okt 2026)

Bench lama qwen3.8-max lokal:

| Bench | Baseline | Skill | Turun |
|---|---|---|---|
| Dokumen (8 skenario) | 25 | 1 | 96% |
| Balasan (8 pertanyaan) | 349 | 70 | 80% |
| Contoh (sebelum ke sesudah) | 13 | 0 | 100% |
| Pressure (5 jebakan) | 15 | 10 | 33% plus 1 lulus, 4 parsial kriteria perilaku |

Uji live qwen3.8-max 9 Okt 2026:

| Kasus | Baseline | Skill |
|---|---|---|
| Runbook (prosedural) | 4 pelanggaran | 0 pelanggaran |
| Balasan chat | 19 bold, 4 header, 7 bullet | 0 bold, 0 header, 0 bullet |
| Tekanan pemasaran | tidak diuji | lulus penuh (tolak salinan persuasif, tawarkan dokumen) |

Detail mentah ada di `evals/results/`. Ini bukan vonis kepatuhan. Tidak ada alat yang menjamin kepatuhan ASD-STE100.

## Uji

```sh
python evals/id_lint.py --self-test
python evals/readability.py --self-test
python src/hooks/test_lint_hook.py
node --test src/hooks/simple-indonesia-activate.test.js
python evals/check_examples.py
python evals/run_eval.py --check
python evals/run_bench.py --dry-run
python evals/run_reply_bench.py --dry-run
python tools/kamus/ekstrak.py --self-test
python tools/kamus/kamus_lint.py --self-test
```

Bench asli butuh `$env:LLM_API_KEY`.

## Sumber

- Saran Karpathy soal ASD-STE100 untuk output LLM: [postingan @karpathy](https://x.com/karpathy/status/2105819303471976479)
- Acuan struktur (Inggris): [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish)
- Standar ASD-STE100 Issue 9 (53 aturan), unduhan resmi gratis: [asd-ste100.org](https://www.asd-ste100.org)
- Spesifikasi Agent Skills (Anthropic, standar terbuka): [agentskills.io](https://agentskills.io/specification)
- KBBI Daring, wasit akhir kata baku: [kbbi.kemdikbud.go.id](https://kbbi.kemdikbud.go.id)
- EYD V, Badan Bahasa: [badanbahasa.kemdikbud.go.id](https://badanbahasa.kemdikbud.go.id)
- Daftar kata baku pembanding: [Ruangguru](https://www.ruangguru.com/blog/contoh-kata-baku-dan-tidak-baku) dan [Deepublish](https://penerbitdeepublish.com/panduan-menulis/kata-baku-dan-tidak-baku/)
- Repo ini: [barkahss/simple-indonesia](https://github.com/barkahss/simple-indonesia)

## Lisensi

MIT. Lihat `LICENSE`. Parafrasa untuk pengajaran. Tidak mereproduksi teks spec ASD-STE100 maupun isi KBBI. Proyek tidak berafiliasi dengan ASD, STEMG, atau Badan Bahasa.
