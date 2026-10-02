# Contoh sebelum dan sesudah — Bahasa Indonesia

## 1. README

Sebelum:
> Dengan memanfaatkan arsitektur sqlpipe yang tangguh, pengguna dapat dengan mudah menyinkronkan tabel Postgres ke S3 dengan overhead konfigurasi yang minimal. Sebelum memulai, Anda harus memastikan bahwa kredensial AWS telah dikonfigurasi dengan benar — ini sangat penting untuk menghindari masalah izin yang membuat frustasi.

Sesudah:
> sqlpipe menyalin tabel Postgres ke S3. sqlpipe membutuhkan satu berkas konfigurasi. Sebelum Anda mulai, pastikan kredensial AWS benar. Jika tidak benar, S3 menolak unggahan dengan galat izin.

Mengapa lebih baik: tanpa "memanfaatkan", "tangguh", "dengan mudah", tanpa em-dash, syarat sebelum perintah, satu fakta per kalimat.

## 2. Runbook

Sebelum:
> Jika terjadi kegagalan, disarankan untuk memeriksa log terlebih dahulu sebelum melakukan restart service, karena hal ini penting untuk diagnosis.

Sesudah:
> Jika layanan gagal, baca log. Baca log sebelum Anda memulai ulang layanan `sync` pada host yang menjalankan tugas. Log menunjukkan sebab kegagalan.

## 3. Pesan galat

Sebelum:
> Ups! Terjadi sesuatu yang salah saat mencoba membuat koneksi. Mohon pastikan kredensial Anda telah dikonfigurasi dengan benar dan coba lagi.

Sesudah:
> Koneksi ke basis data gagal. Kata sandi untuk pengguna `app` tidak benar. Atur `DB_PASSWORD` dan sambung lagi.

## 4. Laporan insiden

Sebelum:
> Kami telah mengidentifikasi isu yang mungkin berdampak pada kemampuan sebagian pengguna untuk mengakses layanan.

Sesudah:
> Antara 14:02 dan 14:31 UTC, 12% permintaan gagal. Deploy pada 14:00 menghapus langkah pemanasan cache. Penyebab lain tidak diketahui.

## 5. Catatan rilis

Sebelum:
> Dalam rilis ini, kami dengan bangga mempersembahkan berbagai peningkatan yang komprehensif dan inovatif untuk meningkatkan pengalaman pengguna secara signifikan!

Sesudah:
> Rilis ini mengubah dua hal. Perbarui panggilan ke `v2/users`. Field `name` pecah menjadi `first_name` dan `last_name`.

## 6. Balasan chat

Sebelum:
> Pertanyaan bagus! Kegagalan tersebut berasal dari pemilihan leader control-plane selama pod churn — tidak perlu khawatir! Semoga membantu, beri tahu saya jika ada pertanyaan lain 😊

Sesudah:
> Pod dimulai ulang dan antrean kehilangan leader untuk waktu singkat. Sistem pulih tanpa bantuan. Anda tidak perlu melakukan apa pun.

Mengapa: kalimat pertama menjawab, tanpa pembuka/penutup, tanpa em-dash, tanpa emoji, tanpa bold.
