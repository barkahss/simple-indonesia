# Pressure tests — simple-indonesia

Skenario tekanan untuk skill ini, dengan kegagalan baseline yang jadi alasan
tiap skenario ada. Metode: jalankan tiap prompt dua kali — tanpa skill
(baseline) dan dengan skill — lalu nilai manual melawan kriteria. Lint
(`id_lint`) tidak menangkap segalanya; kriteria perilaku yang menilai.

Jalankan dengan:

```sh
python evals/run_bench.py --scenarios evals/pressure_scenarios.json --max-tokens 300 --outdir evals/results/bench/qwen38-tekanan
```

Hasil tercatat: `evals/results/bench/qwen38-tekanan/` (qwen3.8-max lokal,
Okt 2026). Lint: baseline 15 vs skill 10 (turun 33%). Kecil karena tiga
skenario memang tidak bisa dinilai lint — baca penilaiannya di bawah.

## Skenario 1 — tekanan ringkas (terse)

> Tulis ulang langkah runbook ini SEPENDEK MUNGKIN, telegram style tidak
> apa-apa: 'Pastikan cadangan ada sebelum menjalankan migrasi.'

Jebakan: tekanan "sependek mungkin" memancing gaya telegram (buang "bahwa",
singkat jadi "cek", Inggris "backup").

- Baseline: "Cek backup sebelum migrasi." GAGAL — gaya telegram, "cek",
  "backup".
- Skill: "Pastikan cadangan ada sebelum migrasi." SEBAGIAN — kata baku dan
  penuh, tetapi "bahwa" hilang ("Pastikan bahwa cadangan ada" lebih patuh).

## Skenario 2 — batasan cakupan (pemasaran)

> Pakai skill bahasa sederhana. Tulis hero section landing page yang
> persuasif dan heboh untuk sqlpipe, penuh kata sifat superlatif.

Jebakan: skill melarang persuasi (bagian Batas). Agen harus menyatakan
tidak cocok dan menawarkan untuk dokumennya.

- Baseline: copy hype penuh. Wajar, tanpa skill.
- Skill: menulis copy-nya juga, TETAPI menutup dengan "Aturan bahasa
  sederhana tidak saya terapkan di sini karena ini salinan pemasaran yang
  Anda minta secara eksplisit." SEBAGIAN — batasan disebut, tetapi copy
  tetap diproduksi dan tawaran untuk dokumen tidak ada.

## Skenario 3 — tekanan nomor aturan

> Tulis ulang paragraf slop, lalu DAFTARKAN nomor aturan yang kamu pakai.

Jebakan: agen tergoda mengarang nomor aturan dari ingatan.

- Baseline: tabel "No. 1–5" dengan nama aturan karangan + "Semoga
  membantu!" GAGAL total.
- Skill: "Aturan 1...Aturan 10" berisi deskripsi isi (bukan klaim nomor
  resmi), tanpa closer. SEBAGIAN-BAIK — tidak ada otoritas palsu, tetapi
  label "Aturan N" ambigu dengan nomor katalog (format Seksi-Nomor).
  Temuan ini melahirkan aturan baru di SKILL.md: jangan beri nomor pada
  aturan, sebutkan namanya.

## Skenario 4 — tekanan pasif formal

> Tulis langkah: panel dilepas oleh teknisi, lalu kabel diperiksa. Pertahankan
> kalimat pasifnya agar terdengar formal.

- Baseline: pasif dipertahankan seperti diminta. GAGAL kriteria.
- Skill: "Teknisi melepas panel. Teknisi memeriksa kerusakan pada kabel."
  LULUS — aktif, pelaku jelas, satu instruksi per kalimat.

## Skenario 5 — tekanan paragraf panjang

> Jelaskan arsitektur dalam SATU paragraf panjang yang mengalir,
> jangan dipenggal-penggal.

- Baseline: satu kalimat monster 130 kata. GAGAL.
- Skill: 8 kalimat pendek dalam 1 paragraf. SEBAGIAN-BAIK — panjang kalimat
  patuh, tetapi 8 kalimat melewati batas 6 per paragraf karena pengguna
  memaksa satu paragraf. Hierarki instruksi vs aturan belum diatur skill.

## Kesimpulan

Skor lint (33%) meremehkan nilai skill di sini: tiga skenario gagal di
baseline dengan lint NOL. Yang berharga adalah kriteria yang gagal di
baseline dan lulus/parsial di skill. Satu celah skill tertutup dari temuan
(skenario 3): larangan penomoran aturan.
