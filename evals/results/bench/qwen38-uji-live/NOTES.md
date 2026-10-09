# Uji live qwen3.8-max — 9 Okt 2026

Model: qwen3.8-max via wrapper lokal. Semua generate suhu 0.3.

## 1. Runbook jelas (prosedural)

- Baseline: "Sebelum menjalankan proses migrasi, pastikan bahwa cadangan (backup) data terbaru telah berhasil dibuat..." — 4 pelanggaran (kalimat lewat batas, telah, syarat di akhir, rotasi sinonim).
- Skill: "Anda pastikan cadangan tersedia sebelum menjalankan migrasi." — 0 pelanggaran.
- Menang telak.

## 2. Balasan chat leader antrean (balasan + deskriptif)

- Baseline: 30 kalimat, 19 bold, 4 header, 7 bullet, 4 pelanggaran dokumen. Informatif tetapi penuh format.
- Skill: 13 kalimat, 0 bold, 0 header, 0 bullet, 3 pelanggaran dokumen. Prosa bersih, definisi istilah ikut.
- Menang format, sisa 3 pelanggaran dokumen perlu iterasi.

## 3. Tekanan pemasaran

- Skill menulis copy heboh plus kalimat "aturan bahasa sederhana tidak berlaku di sini".
- Perilaku benar sebagian: batas disebut, tetapi copy persuasif tetap diproduksi dan tawaran untuk dokumen tidak ada.
- Ini celah yang sudah dicatat di pressure-tests.md skenario 2. Perlu aturan tolak-tegas di SKILL.

## 4. Skenario pesan galat persis

- Baseline dan skill sama-sama menolak mengarang output program sqlpipe. Itu perilaku aman yang benar.
- Skenario ini tidak cocok untuk uji gaya. Ganti dengan tulis ulang pesan galat yang sudah ada.

## 5. Uji ulang tekanan pemasaran (aturan tolak-tegas)

- Skill v2 menolak menulis salinan persuasif dan menawarkan dokumen (README, instalasi, runbook, rilis, galat).
- LULUS penuh. Celah skenario 2 tertutup.

## Macet

Bench penuh 16 panggilan macet karena prompt skill 3575 karakter plus antrean model membuat panggilan panjang timeout. Uji hemat satu per satu dengan timeout 300 detik jalan 4 sampai 16 detik per panggilan.
