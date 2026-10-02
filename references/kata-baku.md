# Kosakata baku — disiplin Strict untuk Bahasa Indonesia

Dipakai hanya dalam mode Strict, yaitu bila pengguna menyebut STE, ASD-STE100, EYD, KBBI, baku, atau kepatuhan. Balasan tetap Plain.

Prinsip dipinjam dari kamus STE: satu kata, satu makna, satu kelas kata. Untuk Bahasa Indonesia, acuannya adalah KBBI (makna) dan EYD V (ejaan). Berkas ini parafrasa untuk pengajaran, bukan salinan KBBI.

## Cara memakai

1. Baca berkas ini sebelum menyusun dokumen Strict.
2. Pilih satu bentuk baku, pakai untuk seluruh dokumen.
3. Bila ragu, pilih bentuk KBBI daring terbaru. Catat pilihan Anda di awal dokumen bila perlu.
4. Katakan sekali bahwa tidak ada alat yang menjamin kepatuhan.

## Daftar baku vs tidak baku (pilihan umum)

Baku -> hindari:

- apotek -> apotik
- teknik -> tehnik
- sistem -> sistim
- jadwal -> jadual
- risiko -> resiko
- survei -> survey
- analisis -> analisa (sebagai kata benda)
- frekuensi -> frekwensi
- konsekuensi -> konsekwensi
- kualitas -> kwalitas
- objek -> obyek
- praktik (kata benda) / praktis (kata sifat) -> praktek
- aktivitas -> aktifitas
- izin -> ijin
- paham -> faham
- napas -> nafas
- standar (baku) -> standard
- metode -> metoda
- nasihat -> nasehat
- cederai? -> gunakan bentuk KBBI: cedera (bukan cidera)
- sekadar -> sekedar
- telanjur? -> terlanjur (pilih baku KBBI: terlanjur)
- antre -> antri
- limfa? abaikan — contoh: pilih satu dan konsisten.

Untuk istilah teknologi serapan, pilih satu dan konsisten:

- konfigurasi (bukan konfig, config)
- basis data (bukan database bila dokumen Indonesia penuh; bila produk memakai "database", tetapkan sebagai nama teknis dan konsisten)
- kata sandi (bukan password bila dokumen Indonesia; bila UI menulis "password", perlakukan sebagai nama teknis)
- surel (untuk email formal) / email (bila produk memakai itu — tetapkan sekali)
- daring (bukan online bila dokumen formal) / dalam jaringan — pilih satu
- luring (bukan offline) — pilih satu
- tetikus (formal) vs mouse (teknis) — pilih satu sesuai audiens
- papan tik vs keyboard — pilih satu
- peramban vs browser — pilih satu
- gawai vs gadget — pilih satu

Aturan: bila audiens adalah insinyur yang UI-nya berbahasa Inggris, pertahankan istilah Inggris sebagai nama teknis dan jangan terjemahkan setengah. Bila audiens umum Indonesia, gunakan padanan baku.

## Aturan EYD V yang paling sering dilanggar AI

1. Kata depan di, ke, dari dipisah bila penunjuk tempat: "di host", "ke server", "dari log". Imbuhan di- digabung: "dibaca", "ditulis", "dihapus".

2. Kata tanya terpisah: "di mana", "ke mana", "bagaimana", "mengapa". Jangan tulis "dimana", "kemana", "gimana".

3. Huruf kapital untuk nama diri, nama produk, awal kalimat. "Bahasa Indonesia", "Postgres", bukan "bahasa indonesia".

4. Tanda koma untuk syarat di awal: "Jika build gagal, baca log." Tanpa koma bila syarat di akhir, tetapi skill ini meminta syarat selalu di awal.

5. Tanda titik dua untuk pengantar daftar: "Langkah:" lalu daftar bernomor.

6. Tanda hubung untuk pengulangan bermakna? Ikuti KBBI, jangan tambah strip pada istilah serapan yang sudah baku.

7. Penulisan angka dan unit dengan spasi: "18 menit", "12%", "14:02 UTC". Konsisten.

8. Singkatan baku memakai titik: "dll.", "dsb.", "dst." — tetapi skill ini meminta Anda menghindari dll./dsb. dan menyebut itemnya. Dalam mode Strict, bila harus memakai, tulis dengan titik dan konsisten.

## Satu kata satu makna — pasangan yang harus dipilih

- pastikan (untuk semua pemeriksaan) — jangan tukar dengan periksa, cek, verifikasi dalam dokumen yang sama.
- gunakan (untuk semua pemakaian) — jangan tukar dengan pakai, manfaatkan.
- mulai (untuk memulai) — jangan tukar dengan awali, inisiasi.
- hentikan (untuk stop) — jangan tukar dengan setop, berhenti (pilih satu sebagai verba operasional).
- hapus (untuk delete/remove) — pilih satu.
- buat (untuk create) — jangan tukar dengan bikin.
- jalankan (untuk run/execute) — pilih satu.
- simpan (untuk save) — pilih satu.
- kirim (untuk send) — pilih satu.
- terima (untuk receive/accept dalam konteks operasional) — definisikan bila bermakna khusus.

Contoh penetapan di awal dokumen Strict:

> Dokumen ini memakai "pastikan" untuk semua pemeriksaan, "konfigurasi" untuk semua pengaturan, dan "jalankan" untuk semua eksekusi perintah.

## Yang tidak boleh di-Strict-kan

Jangan ubah:

- kode, perintah, flag, path, identifier, nama produk, kutipan galat persis.
- angka, fakta, sebab yang tidak ada di sumber — pertahankan pernyataan umum, jangan karang.
