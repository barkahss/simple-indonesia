# Katalog aturan — adaptasi 53 aturan Issue 9 untuk Bahasa Indonesia

Berkas ini untuk mode PERIKSA. Jangan kutip nomor aturan dari ingatan. Salin nomor, kutip teks pelanggar, lalu beri tulis ulang yang patuh.

Catatan hak: Ini parafrasa untuk pengajaran. Tidak mereproduksi teks spec atau isi kamus. Teks resmi adalah ASD-STE100 Issue 9, unduhan gratis di asd-ste100.org. ASD tidak mensertifikasi alat apa pun.

Aturan dikelompokkan seperti Issue 9: kata, frasa, kata kerja, kalimat, prosedur vs deskripsi, peringatan dan penekanan. Nomor memakai format Seksi-Nomor agar mudah dirujuk tanpa mengklaim nomor resmi.

## Bagian 1 — Pilihan kata (1.1 – 1.13)

1.1 Gunakan kata yang disetujui hanya dengan makna yang disetujui. Satu kata, satu makna, satu kelas kata untuk seluruh dokumen.

1.2 Bila kata tidak ada di daftar baku Anda, pilih padanan baku KBBI dan pakai konsisten. Jangan campur sinonim.

1.3 Kata teknis (nama alat, perintah, protokol) adalah pengecualian. Tetapkan sekali, lalu pakai persis sama.

1.4 Jangan buat kata baru dengan menggabung dua kata baku bila KBBI sudah punya bentuknya.

1.5 Jangan pakai kata yang sama sebagai kata benda di satu kalimat dan kata kerja di kalimat lain bila maknanya berubah.

1.6 Pilih kata kerja spesifik "mulai", bukan "awali, mulai, inisiasi, commence". Pilih satu, buang sisanya.

1.7 Gunakan "pastikan" untuk semua pemeriksaan. Jangan putar periksa, verifikasi, validasi, konfirmasi, cek.

1.8 Gunakan "konfigurasi" untuk semua pengaturan. Jangan putar `config`, setelan, opsi.

1.9 Hapus kata yang tidak menambah fakta: secara sederhana, mulus, kuat, canggih, komprehensif, manfaatkan, cukup, relatif, umumnya, biasanya bila menyamarkan fakta.

1.10 Jangan pakai idiom atau kiasan: di balik layar, masuk angin, membuka jalan. Tulis makna harfiah.

1.11 Gunakan ejaan baku EYD V. Lihat `kata-baku.md` untuk daftar jebakan umum.

1.12 Frasa benda teknis yang tidak ada di kamus boleh dipakai bila perlu untuk menjelaskan sistem, tetapi batasi dan definisikan.

1.13 Jangan pakai singkatan informal (yg, dgn, spt) atau ragam lisan (nggak, gimana) dalam dokumen.

## Bagian 2 — Frasa benda (2.1 – 2.5)

2.1 Jangan tulis frasa benda lebih dari tiga kata tanpa preposisi. Pecah dengan dari, untuk, pada.

Contoh langgar: "nilai batas waktu kolam koneksi"
Patuh: "nilai batas waktu untuk kolam koneksi"

2.2 Jangan tumpuk pewatas di depan benda. Pindahkan keterangan ke belakang dengan yang.

2.3 Gunakan "yang", "bahwa", "tersebut" untuk menjaga hubungan antar klausa jelas bagi pembaca dan mesin terjemah.

2.4 Jangan hilangkan subjek, predikat, atau artikel demi memendekkan teks. Tulis kalimat penuh.

2.5 Beri penentu yang cukup: host mana, flag mana, berkas mana. "Mulai ulang layanan" menjadi "Mulai ulang layanan `sync`".

## Bagian 3 — Kata kerja (3.1 – 3.9)

3.1 Gunakan hanya bentuk sederhana: perintah, kini sederhana, lampau sederhana, akan datang sederhana.

3.2 Jangan gunakan konstruksi kompleks dengan kata bantu bertumpuk. Satu predikat inti per klausa.

3.3 Gunakan kalimat aktif. Sebutkan pelaku. Pasif di- hanya bila pelaku tidak diketahui dalam teks deskriptif.

Contoh langgar: "Panel dilepas oleh teknisi."
Patuh: "Teknisi melepas panel."

3.4 Jangan gunakan bentuk "-kan/-i" yang menggantung setelah koma (", memudahkan pengguna"). Buat kalimat baru.

3.5 Jangan nominalisasi: ubah benda hasil verba menjadi verba. "Sebelum penerimaan unit" menjadi "Sebelum Anda menerima unit".

3.6 Jangan gunakan bentuk "-ing" Inggris yang diterjemahkan kaku. Tulis verba Indonesia yang aktif.

3.7 Modal yang diizinkan: dapat, bisa, akan, harus, wajib. Modal yang dilarang: sebaiknya, semestinya, seharusnya, harusnya, mungkin, barangkali, kiranya, sekiranya, seandainya.

3.8 "Harus" untuk kewajiban. "Akan" untuk masa depan. "Dapat/bisa" untuk kemampuan. Jangan campur.

3.9 Satu instruksi per kalimat kerja. Jangan gabung dua perintah dengan "dan lalu".

## Bagian 4 — Kalimat prosedural (4.1 – 4.7)

4.1 Maksimal 20 kata per kalimat instruksi. Hitung. Lebih, pecah.

4.2 Satu instruksi per kalimat. Satu kalimat, satu tindakan yang dapat diverifikasi.

Contoh langgar: "Lepas panel, yang dipegang empat sekrup, dan periksa kabel dari kerusakan."
Patuh: "Lepas panel. Empat sekrup menahan panel. Periksa kabel. Pastikan kabel tidak rusak."

4.3 Tulis perintah dalam imperatif: "Baca log." bukan "Log harus dibaca."

4.4 Syarat sebelum perintah, dengan koma: "Jika build gagal, baca log."

4.5 Beri fakta sebelum langkah yang membutuhkannya. Jangan minta pembaca menebak host atau flag.

4.6 Akhiri tiap item daftar dengan titik bila berupa kalimat. Awali huruf kapital.

4.7 Daftar vertikal untuk tiga item sejajar atau lebih. Pengantar diakhiri titik dua.

## Bagian 5 — Kalimat deskriptif (5.1 – 5.7)

5.1 Maksimal 25 kata per kalimat deskripsi.

5.2 Satu topik per paragraf. Maksimal enam kalimat per paragraf.

5.3 Gunakan kala lampau sederhana untuk kejadian: "Deploy menghapus langkah." bukan "Deploy telah menghapus".

5.4 Jangan gunakan kini sempurna ("telah mengidentifikasi") untuk menyamarkan waktu. Sebutkan waktu bila tahu.

5.5 Definisikan istilah konsep saat pertama dipakai, di bawah sepuluh kata. Satu per kalimat.

5.6 Nyatakan yang diketahui. Tulis "tidak diketahui" untuk sisanya. Jangan pagar dengan mungkin.

5.7 Jangan nilai pentingnya fakta. Hapus "sangat penting", "perlu dicatat", "tidak hanya X melainkan Y".

## Bagian 6 — Peringatan dan keselamatan (6.1 – 6.5)

6.1 Awali instruksi keselamatan dengan perintah atau syarat yang jelas.

6.2 Perintah atau syarat dulu, risiko kemudian: "Jangan jalankan ini di produksi. Perintah ini menghapus baris."

6.3 Jangan sembunyikan risiko di anak kalimat. Buat kalimat sendiri.

6.4 Jangan persingkat peringatan keamanan atau konfirmasi sebelum tindakan destruktif.

6.5 Gunakan kata peringatan konsisten: Peringatan, Perhatian, Bahaya — satu makna masing-masing.

## Bagian 7 — Gaya dan tanda baca (7.1 – 7.7)

7.1 Tanpa titik koma untuk menggabung dua pikiran. Tulis dua kalimat.

7.2 Tanpa em-dash. Sebutkan hubungan dengan karena, tetapi, contohnya, atau pecah kalimat.

7.3 Tanpa bold sebagai penekanan dan tanpa bold lead-in. Gunakan struktur heading dan daftar, bukan dekorasi.

7.4 Tanpa emoji dalam dokumen teknis.

7.5 Tanpa heading yang hanya menaungi satu atau dua kalimat. Gabung atau hapus heading.

7.6 Gunakan ejaan Amerika untuk Inggris yang tersisa, EYD V untuk Indonesia. Jangan campur "center/centre" bila ada istilah Inggris.

7.7 Jaga konsistensi tanda baca kode: backtick untuk identifier, blok kode untuk yang harus disalin.

## Bagian 8 — Konsistensi dokumen (8.1 – 8.4)

8.1 Satu istilah untuk satu konsep di seluruh dokumen, dari judul hingga contoh terakhir.

8.2 Jangan ganti sudut pandang: pilih "Anda" untuk instruksi pengguna, "sistem" untuk perilaku otomatis, lalu konsisten.

8.3 Angka, unit, dan format waktu konsisten. Sebutkan zona waktu: "14:02 UTC".

8.4 Contoh kode dan output tidak diedit gayanya, tetapi prosa di sekitarnya ikut aturan ini.

## Bagian 9 — Pemeriksaan (9.1 – 9.3)

9.1 Saat memeriksa, laporkan: nomor aturan, teks pelanggar, tulis ulang patuh. Satu pelanggaran per baris.

9.2 Jangan menilai suara merek atau persuasi dengan aturan ini. Nyatakan tidak cocok, tawarkan untuk dokumennya.

9.3 Akhiri pemeriksaan kepatuhan dengan: tidak ada alat yang menjamin kepatuhan ASD-STE100.

---

Contoh laporan PERIKSA:

Aturan 4.1 — "Lepas panel yang dipegang oleh empat sekrup dengan hati-hati dan kemudian dengan segera periksa kabel yang mungkin rusak untuk memastikan semuanya baik-baik saja."
Masalah: 24 kata, dua instruksi, pagar "mungkin".
Patuh: "Lepas panel. Empat sekrup menahan panel. Periksa kabel. Pastikan kabel tidak rusak."
