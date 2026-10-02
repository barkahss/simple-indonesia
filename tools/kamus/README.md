# Daftar kata baku, dibuat di mesin Anda

Direktori ini berisi ekstraktor dan lint pilihan kata. Berisi **tidak ada
konten KBBI**. KBBI adalah hak Badan Bahasa. Repo hanya ship tool; daftar
dibuat dari berkas milik repo ini atau daftar yang Anda tulis sendiri dari
kata yang Anda cek di KBBI Daring.

## Buat daftar

1. Jalankan ekstraktor atas `references/kata-baku.md` (tulisan repo ini):
   `python tools/kamus/ekstrak.py`. Ini menulis `kata-baku.tsv`
   (format: `hindari<TAB>baku`).
2. Tambahkan kata Anda sendiri ke `kata-saya.tsv` (tidak ikut commit, lihat
   `.gitignore`) dengan format yang sama, dari kata yang Anda cek di
   https://kbbi.kemdikbud.go.id.

Keluaran deterministik. `kata-baku.tsv` dan `kata-saya.tsv` generated/lokal:
jangan commit.

## Lint pilihan kata

`evals/id_lint.py` mengukur aturan mekanis. Ia tidak melihat pilihan kata.
Linter ini membaca TSV dan melaporkan tiap kata yang sebaiknya diganti
dengan saran bakunya:

```
python tools/kamus/ekstrak.py
python tools/kamus/kamus_lint.py tools/kamus/kata-baku.tsv file.md
python tools/kamus/ekstrak.py --self-test
python tools/kamus/kamus_lint.py --self-test
```

Batasan: cocok whole-word case-insensitive plus akhiran melekat umum
(-nya, -ku, -mu, -lah, -kah). Tanpa penguraian imbuhan dan tanpa bedakan
kelas kata. Angka hanya untuk bandingkan dua teks dengan versi yang sama.
Bukan vonis kebakuan.
