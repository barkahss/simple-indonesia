# Kasus pakai di luar dokumentasi

STE dibuat untuk manual perawatan pesawat. Sifat yang sama berlaku untuk teks apa pun di mana salah baca berbiaya: satu makna per kata, kalimat pendek, perintah yang diawali syarat. Setiap kasus di bawah menyebut mode dan adaptasinya ke Bahasa Indonesia.

## Pesan galat dan keluaran CLI

Mode: prosedural. Pesan galat adalah instruksi untuk pembaca yang sedang gagal. Pola: nyatakan apa yang terjadi (lampau sederhana), nyatakan sebab bila tahu, beri perintah atau syarat yang memperbaiki.

> Sebelum: Ups! Terjadi kesalahan saat mencoba membuat koneksi. Pastikan kredensial telah dikonfigurasi dengan benar dan coba lagi.
> Sesudah: Koneksi ke basis data gagal. Kata sandi untuk pengguna `app` tidak benar. Atur `DB_PASSWORD` dan sambung lagi.

## Runbook dan prosedur operasi standar

Mode: prosedural. Runbook on-call adalah manual perawatan, yaitu jenis teks asal STE.

- Setiap langkah imperatif, satu instruksi per langkah, syarat dulu.
- Peringatan sebelum langkahnya: perintah dulu, risiko kemudian.
- Tidak ada kalimat lebih dari 20 kata.

## Laporan insiden dan postmortem

Mode: deskriptif, hanya lampau sederhana. Linimasa dalam bentuk "kami telah mengidentifikasi" menyembunyikan kapan hal terjadi.

> Sebelum: Kami telah mengidentifikasi isu yang mungkin berdampak pada kemampuan pengguna mengakses layanan.
> Sesudah: Antara 14:02 dan 14:31 UTC, 12% permintaan gagal. Deploy pada 14:00 menghapus langkah pemanasan cache.

STE melarang pagar seperti "mungkin berdampak". Laporan menyatakan yang diketahui dan menulis "tidak diketahui" untuk sisanya.

## Pesan commit dan deskripsi PR

Mode: subjek imperatif, badan deskriptif. Konvensi sudah cocok dengan STE. Terapkan daftar kata ganti dan batas 25 kata ke badan. Hapus "PR ini bertujuan untuk".

## Changelog API dan catatan rilis

Mode: deskriptif. Satu entri, satu perubahan, satu kalimat bila mungkin. Entri "Breaking:" ikut pola peringatan, perintah dulu: "Perbarui panggilan ke `v2/users`. Field `name` pecah menjadi `first_name` dan `last_name`."

## Instruksi untuk agen AI (prompt, AGENTS.md, skills)

Mode: prosedural. Prompt sistem adalah prosedur untuk pembaca yang tidak dapat bertanya.

- Satu instruksi per kalimat membuat tiap aturan mudah dikutip dan sulit diikuti setengah.
- Satu kata, satu makna menghentikan model yang menganggap "periksa", "verifikasi", dan "validasi" sebagai tiga operasi.
- Syarat di awal ("Jika build gagal, henti") mengalahkan syarat di akhir, yang sering diabaikan model.
- Tanpa "sebaiknya". Model membaca "sebaiknya" sebagai opsional. Tulis "harus" atau hapus aturan.

## Makro dukungan dan update status-page

Mode: deskriptif, batas 25 kata. Banyak pembaca pesan ini bukan penutur asli.

> Sebelum: Kami mohon maaf atas ketidaknyamanan yang mungkin terjadi.
> Sesudah: API berhenti selama 18 menit. Unggahan selama waktu itu tersimpan dan sistem memprosesnya hari ini.

## Persiapan terjemahan dan lokalisasi

Mode: strict. STE ditulis agar kru perawatan non-native dapat membaca manual Inggris. Aturan yang sama menyiapkan teks untuk terjemahan mesin. Satu makna per kata dan tata bahasa lengkap (yang, bahwa) menghapus banyak ambiguitas yang harus ditebak penerjemah.

Untuk Bahasa Indonesia ke Inggris atau sebaliknya: jaga satu istilah konsisten, hindari idiom ("di balik layar", "masuk angin"), tulis kalimat penuh agar mesin menerjemahkan subjek dengan benar.

## Salinan UI dan empty state

Mode: prosedural, batas panjang ketat. Tombol dan label adalah nama teknis dan dikecualikan dari aturan gaya, tetapi prosa badan tetap ikut aturan. Salinan badan ikut aturan: "Belum ada proyek. Buat proyek untuk mulai." Subjek commit memakai imperatif singkat di bawah 50 karakter bila mungkin.

## Di mana STE tidak cocok

Jangan gunakan STE untuk halaman pemasaran, posting peluncuran, posting blog, atau tulisan merek. STE menghapus persuasi. Bila pengguna meminta salinan pemasaran, nyatakan skill tidak cocok, jangan tulis salinan persuasif bergaya STE, dan tawarkan untuk dokumennya. Tulis teks itu dengan suara Anda, dan gunakan STE untuk dokumen yang ditautkannya.
