# Simple Indonesia — Skill Bahasa Indonesia Sederhana ala ASD-STE100

Repo ini **adalah** skill-nya langsung (skill-at-root): `SKILL.md` ada di root, siap dipasang ke agen apa pun yang ikut standar Agent Skills (`agentskills.io/specification`).

Skill agar LLM menulis Bahasa Indonesia yang bersih, tanpa bau AI, dengan disiplin ASD-STE100 yang diadaptasi ke EYD V dan KBBI. Dioptimasi khusus Bahasa Indonesia: kalimat efektif, kata baku KBBI, dan daftar slop AI Indonesia — bukan terjemahan mentah dari versi Inggris.

Terinspirasi oleh:
- Saran Karpathy: minta LLM menjelaskan dalam ASD-STE100. LLM sangat paham bahasa ini. Batasannya berat, hasilnya jauh lebih mudah dibaca. Karena spec asli sangat ketat, baku skill ini adalah 80% jalan ke ASD-STE100.
- Referensi: AminBlg/SimpleEnglish (MIT) untuk Bahasa Inggris — struktur parity: lint, eval, hooks, output style.
- Standar: ASD-STE100 Issue 9 (15 Jan 2025, 53 aturan, ~900 kata) + Agent Skills specification.

## Isi

```
simple-indonesia/
  SKILL.md                    # instruksi utama (progressive disclosure)
  references/
    kata-ganti.md             # peta kata berlebih AI -> pengganti polos
    kasus-pakai.md            # pola untuk galat, runbook, insiden, rilis, UI, terjemahan
    katalog-aturan.md         # adaptasi 53 aturan untuk mode PERIKSA (parafrasa)
    kata-baku.md              # disiplin KBBI + EYD V untuk mode Strict
  examples/
    sebelum-sesudah.md        # contoh rewrite Indonesia
  evals/
    id_lint.py                # lint deterministik + --self-test
    scenarios.json            # 8 skenario uji Bahasa Indonesia
    slop_id.tsv               # leksikon bau AI Indonesia
    check_examples.py         # pastikan Sesudah lebih bersih dari Sebelum
    run_eval.py               # hitung ulang angka ke results/RESULTS.md
    fixtures/                 # bukti uji (asli vs bersih)
    results/RESULTS.md        # ringkasan angka terukur
  prompts/
    system-prompt.md          # versi ringkas + ~60 token untuk harness tanpa SKILL.md
  output-styles/
    simple-indonesia.md       # gaya output untuk Claude Code
  src/hooks/
    lint_hook.py              # hook nasihat PostToolUse dan Stop
    simple-indonesia-activate.js  # hook SessionStart, muat blok aturan
  .claude-plugin/             # marketplace + plugin Claude Code
  .codex-plugin/              # plugin Codex
```

## Pasang

Agen apa pun dengan skills CLI, dari root repo ini:

```sh
npx skills add ./
```

Atau dari GitHub:

```sh
npx skills add barkahss/simple-indonesia
```

Claude Code (plugin):

```sh
claude plugin marketplace add barkahss/simple-indonesia && claude plugin install simple-indonesia@simple-indonesia
```

Gaya output saja: pilih `simple-indonesia:simple-indonesia` di `/config` Output style (nama pendek tidak resolve).

Codex (plugin, hook SessionStart butuh Node):

```sh
codex plugin marketplace add barkahss/simple-indonesia
codex plugin add simple-indonesia@simple-indonesia
```

Codex meminta trust hook sebelum jalan pertama. Hook butuh Node.js.

Opencode / Cursor / VS Code Copilot / Codex / Gemini CLI:
salin folder repo ini ke folder skills agen Anda. Skill ikut standar `agentskills.io/specification`: folder + `SKILL.md` dengan frontmatter `name` dan `description` (`name` cocok dengan nama folder).

Tanpa dukungan skill? Tempel blok aturan dari `prompts/system-prompt.md` ke system prompt, `AGENTS.md`, atau `.cursorrules`.

Lalu minta: "tulis ulang ini dengan simple-indonesia" atau "jelaskan dengan bahasa sederhana".

## Uji

```sh
python evals/id_lint.py --self-test
python src/hooks/test_lint_hook.py
node --test src/hooks/simple-indonesia-activate.test.js
python evals/check_examples.py
python evals/run_eval.py --check   # tulis ulang evals/results/RESULTS.md + gate
python evals/run_bench.py --dry-run   # bench tanpa API; bench asli butuh $env:LLM_API_KEY
```

## Dua mode

- Plain (baku, 80% STE ala Karpathy): kalimat pendek, aktif, syarat dulu, satu kata satu makna, definisikan istilah, tanpa slop AI. Balasan selalu Plain: prosa saja, jawab dulu.
- Strict (bila Anda sebut STE, ASD-STE100, EYD, KBBI, baku, kepatuhan): tambah disiplin kosakata `kata-baku.md`. Tidak ada alat yang menjamin kepatuhan.

## Bukan sertifikasi

Tidak ada alat yang tersertifikasi ASD. Ini parafrasa untuk pengajaran, tidak mereproduksi teks spec atau kamus. Unduhan resmi gratis di asd-ste100.org. Proyek tidak berafiliasi dengan ASD atau STEMG.
