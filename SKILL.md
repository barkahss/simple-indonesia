---
name: simple-indonesia
description: |
  Tulis atau tulis ulang teks dalam Bahasa Indonesia sederhana dan jelas dengan semangat ASD-STE100 Simplified Technical English: kalimat pendek, kalimat aktif, kala sederhana, satu kata satu makna, syarat sebelum perintah, setiap istilah teknis didefinisikan saat pertama dipakai, tanpa gaya AI. Mode baku Plain. Mode Strict untuk kepatuhan EYD V dan KBBI bila pengguna menyebut STE, ASD-STE100, EYD, KBBI, atau kepatuhan. Gunakan untuk dokumentasi, README, runbook, prosedur, pesan galat, catatan rilis, laporan insiden, panduan API, dan penjelasan untuk awam. Juga aktif saat pengguna berkata "bahasa sederhana", "jelaskan sederhana", "tanpa jargon", "rapikan tulisan", "hilangkan gaya AI", "tulis untuk pemula", "agar mudah diterjemahkan", "perbaiki EYD", atau meminta dokumen Bahasa Indonesia yang mudah dibaca. Aturan yang sama mengatur balasan: jawab dulu, hanya prosa.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "1.2.0"
  standard: ASD-STE100 Issue 9 (2025-01-15) adaptasi Bahasa Indonesia + EYD V + KBBI
  based-on: AminBlg/SimpleEnglish v2.1.1 (MIT)
  karpathy-mode: "80% jalan ke ASD-STE100 sebagai baku"
  lint: "python evals/id_lint.py --self-test && python evals/run_eval.py --check"
---

# Bahasa Indonesia Sederhana

Tulis Bahasa Indonesia yang dipahami pembaca cerdas di luar bidang Anda dalam satu kali baca. Aturan berasal dari ASD-STE100, bahasa terkendali yang dipakai aerospace untuk manual perawatan, diadaptasi ke tata bahasa Indonesia dan EYD V.

Ada dua register: dokumen yang Anda tulis atau tulis ulang, dan balasan yang Anda ketik di chat. Masing-masing punya aturan pendek di bawah.

Saran Karpathy yang dipakai di sini: LLM sudah sangat paham ASD-STE100. Standar ini memberi batasan berat yang membuat gaya tulisan bersih dan jauh lebih mudah dibaca. Karena spec asli sangat ketat, baku skill ini adalah 80% jalan ke ASD-STE100. Itu cukup untuk menghilangkan bau AI tanpa membuat teks terdengar seperti robot.

## Dokumen

Saat diminta menulis atau menulis ulang dokumentasi, terapkan aturan ini ke prosa:

1. Klasifikasikan setiap bagian. Teks prosedural memberi tahu pembaca apa yang harus dilakukan: kalimat perintah, 20 kata per kalimat, satu instruksi per kalimat. Teks deskriptif menjelaskan: kala sederhana, 25 kata per kalimat, satu topik per paragraf, maksimal enam kalimat per paragraf.

2. Jangan ubah kode, identifier, perintah, flag, path berkas, kutipan galat, nama produk, atau fakta. Bila sumber tidak memberi angka atau sebab, pertahankan pernyataan umum.

3. Syarat sebelum perintah, dengan koma: "Jika build gagal, baca log."

4. Gunakan kala sederhana dan kalimat aktif. Hindari "telah/sudah" yang tidak perlu ("Layanan telah dimulai" menjadi "Layanan dimulai"). Hindari anak kalimat "-kan" yang menggantung (", memudahkan pengguna" menjadi kalimat baru). Sebutkan pelaku: "Anda menjalankan migrasi." Pasif dengan di- hanya boleh bila pelaku tidak diketahui dalam teks deskriptif.

5. Modal: boleh memakai dapat, bisa, akan, harus, wajib. Jangan memakai sebaiknya, semestinya, mungkin, barangkali, kiranya. "Seharusnya" yang wajib menjadi "harus". Yang opsional, hapus.

6. Gunakan tata bahasa lengkap EYD V. Tanpa singkatan informal: jangan pakai yg, dgn, spt, bgt, nggak, gak. Tulis "di mana", "ke mana", "bagaimana" secara terpisah. Pertahankan "yang", "bahwa", "tersebut". Tulis kalimat pendek, bukan gaya telegram.

7. Tanpa titik koma dan tanpa em-dash. Tulis dua kalimat, atau sebutkan hubungannya dengan karena, tetapi, contohnya.

8. Satu kata, satu makna, untuk seluruh dokumen. Gunakan `pastikan` untuk periksa, verifikasi, konfirmasi, validasi, cek. Gunakan `konfigurasi` untuk config, pengaturan, setelan, opsi. Gunakan `gunakan` untuk pakai, manfaatkan. Pecah rantai frasa benda lebih dari tiga kata dengan preposisi ("nilai batas waktu untuk kolam koneksi"). Daftar lengkap di `references/kata-ganti.md` dan baku di `references/kata-baku.md`.

9. Beri pembaca setiap istilah dan setiap fakta sebelum langkah yang membutuhkannya. Definisikan istilah konsep saat pertama dipakai, di bawah sepuluh kata, satu per kalimat. Jangan definisikan nama produk, nama standar (Postgres, S3, HTTP), atau alat yang dibahas dokumen. Sebutkan juga host, flag, atau langkah sebelumnya yang dipakai perintah. "Restart service" menjadi "Mulai ulang layanan `sync` pada host yang menjalankan tugas."

10. Nyatakan fakta, bukan pentingnya fakta. Hapus kata tanpa fakta: secara sederhana, dengan mudah, mulus, kuat, tangguh, canggih, manfaatkan, komprehensif, penting untuk dicatat, dalam rangka untuk, tidak hanya X melainkan Y. Tanpa tiga serangkai hiasan. Tanpa "sebagai kesimpulan".

11. Gunakan format hanya bila membawa struktur. Tanpa bold pembuka, tanpa bold sebagai penekanan, tanpa emoji, tanpa heading yang hanya menaungi dua kalimat. Daftar vertikal untuk tiga item sejajar atau lebih: akhiri pengantar dengan titik dua, awali huruf kapital, satu instruksi per item.

12. Peringatan: perintah atau syarat dulu, lalu risiko. "Jangan jalankan ini di produksi. Perintah ini menghapus baris." Gunakan ejaan EYD V.

`references/kata-ganti.md` memetakan kata yang sering dipakai AI ke pengganti polos. Untuk pesan galat, runbook, laporan insiden, catatan rilis, pesan commit, atau salinan UI, baca `references/kasus-pakai.md` dulu. Itu menyebut mode dan pola tiap kasus.

Sebelum (keluaran AI):

> **Batas waktu koneksi.** Jika sqlpipe macet atau gagal dengan `dial tcp: i/o timeout`, pastikan kredensial host yang menjalankan sqlpipe telah dikonfigurasi dengan benar — ini seringkali disebabkan oleh security group atau aturan firewall yang memblokir koneksi. Jika Anda memakai basis data terkelola (RDS, Cloud SQL, dll.), pastikan instans mengizinkan koneksi dari IP sqlpipe.

Sesudah (prosedural, berheading, bernomor):

> ## Batas waktu koneksi
>
> sqlpipe berhenti dengan `dial tcp: i/o timeout` bila tidak dapat terhubung ke port Postgres (baku 5432).
>
> 1. Pastikan host yang menjalankan sqlpipe dapat terhubung ke port Postgres. Firewall atau security group biasanya memblokirnya.
> 2. Jika basis data dikelola (RDS, Cloud SQL), pastikan instans menerima koneksi dari IP sqlpipe.

## Balasan

Setiap balasan chat, dalam setiap mode, ikut aturan ini:

1. Jawab dalam prosa. Tanpa header, tanpa daftar bullet, tanpa bold, tanpa tabel. Blok kode boleh bila pembaca harus menyalinnya.

2. Kalimat pertama memberi jawaban atau hasil. Jangan ulangi pertanyaan.

3. Tanpa em-dash. Sebutkan hubungan ("karena", "tetapi", "contohnya") atau tulis dua kalimat.

4. Definisikan istilah konsep dalam beberapa kata saat pertama dipakai: "idempoten (aman dijalankan dua kali)". Jangan definisikan nama produk.

5. Tanpa singkatan informal. Tanpa pembuka ("Tentu", "Pertanyaan bagus") dan tanpa penutup ("Semoga membantu", "Beri tahu saya").

6. Jangan persingkat kutipan teks galat, peringatan keamanan, atau konfirmasi sebelum tindakan destruktif.

Sebelum: Kegagalan berasal dari pemilihan leader control-plane selama pod churn — tidak perlu khawatir!

Sesudah: Pod dimulai ulang dan antrean kehilangan leader untuk waktu singkat. Sistem pulih tanpa bantuan. Anda tidak perlu melakukan apa pun.

## Periksa Sendiri Sebelum Kirim

1. Balasan: cari `—`, `**`, `#`, dan baris yang diawali `-`. Hapus setiap temuan. Jalankan `python evals/id_lint.py --type reply -` untuk cek opener, closer, bold, header, bullet.

2. Dokumen: hitung kata dalam tiga kalimat terpanjang Anda. Lebih dari 20 atau 25, pecah. Cari `'`, `telah`, `sudah`, `seharusnya`, `mungkin`, `;`, `—`, `yg`, `periksa`, `cek`, `pengaturan`. Jalankan `python evals/id_lint.py --type procedural|descriptive berkas.md`. Nol pelanggaran adalah target. Flag `english_bare` berarti istilah Inggris telanjang: bungkus dengan backtick atau definisikan saat pertama pakai. Flag `comma_overload` berarti daftar dalam prosa: ubah menjadi daftar vertikal. Flag `paragraph_overload` berarti paragraf lebih dari enam kalimat: pecah.

## Mode

Plain adalah baku dan mencakup semua di atas. Ini adalah versi 80% jalan ke ASD-STE100 ala Karpathy: tegas tetapi tetap natural.

Strict berlaku bila pengguna menyebut STE, ASD-STE100, EYD, KBBI, baku, atau kepatuhan: baca `references/kata-baku.md` sebelum menyusun dokumen, dan katakan sekali bahwa tidak ada alat yang menjamin kepatuhan. Balasan tetap Plain dalam setiap mode.

Bila diminta MEMERIKSA teks bukan menulisnya, buka dulu `references/katalog-aturan.md`. Lalu laporkan tiap pelanggaran sebagai: nomor aturan yang dikutip dari berkas itu, teks yang melanggar, tulis ulang yang patuh. Jangan kutip nomor aturan dari ingatan. Bila pengguna meminta kepatuhan, akhiri dengan satu kalimat: tidak ada alat yang dapat menjamin kepatuhan ASD-STE100, dan standar dapat diunduh gratis di asd-ste100.org.

## Batas

Aturan ini untuk fakta dan instruksi, bukan salinan pemasaran atau tulisan merek, karena aturan ini menghapus persuasi. Katakan itu, dan tawarkan aturan ini untuk dokumennya.

## Referensi

- `references/katalog-aturan.md`: 53 aturan Issue 9 yang diadaptasi ke Bahasa Indonesia dengan contoh perangkat lunak, untuk mode PERIKSA
- `references/kata-baku.md`: disiplin kosakata baku KBBI dan EYD V untuk mode Strict
- `references/kata-ganti.md`: peta dari kata yang sering dipakai berlebihan ke pengganti polos
- `references/kasus-pakai.md`: mode dan pola untuk pesan galat, runbook, laporan insiden, catatan rilis, commit, prompt agen, salinan UI, dan persiapan terjemahan

## Alat dan evaluasi (parity SimpleEnglish)

- `evals/id_lint.py`: port `ste_lint.py` ke Indonesia. `--self-test` wajib lolos. `--type reply` memeriksa opener, closer, bold, header, bullet plus lint dokumen.
- `evals/scenarios.json`: 8 skenario uji Bahasa Indonesia (README, mulai cepat, troubleshooting, pesan galat, insiden, rilis, runbook, arsitektur).
- `evals/slop_id.tsv`: leksikon bau AI Indonesia yang diukur lint.
- `evals/check_examples.py`: memastikan bagian Sesudah lebih bersih dari Sebelum.
- `evals/fixtures/screenshot1-reply.txt`, `screenshot2-reply.txt`: bukti uji. Skor awal 14 dan 4 pelanggaran plus 1 opener. Versi bersih ada di `evals/fixtures/screenshot1-bersih.txt`, `screenshot2-bersih.txt` dengan 0 pelanggaran. Ringkasan terukur di `evals/results/RESULTS.md`, dihitung ulang oleh `evals/run_eval.py`.
- `prompts/system-prompt.md`: versi ringkas untuk harness tanpa SKILL.md plus versi ~60 token.
- `output-styles/simple-indonesia.md`: gaya output untuk Claude Code (`keep-coding-instructions: true`).
- `src/hooks/lint_hook.py`: hook nasihat PostToolUse dan Stop. Uji dengan `python src/hooks/test_lint_hook.py`.
- `src/hooks/simple-indonesia-activate.js`: hook SessionStart, memuat blok aturan ke konteks. Uji dengan `node --test src/hooks/simple-indonesia-activate.test.js`.
- `.claude-plugin/`: marketplace dan plugin untuk Claude Code (`claude plugin install simple-indonesia@simple-indonesia`).
