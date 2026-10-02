#!/usr/bin/env python3
"""Bangun daftar kata baku dari berkas milik sendiri.

Sumber: references/kata-baku.md (tulisan repo ini sendiri, bukan isi KBBI).
Keluaran: tools/kamus/kata-baku.tsv  (format: hindari<TAB>baku).
Berkas keluaran bersifat generated dan TIDAK ikut commit (lihat .gitignore),
sama seperti tools/ste-dictionary milik SimpleEnglish yang tidak ship isi kamus.

Pemakaian:
  python tools/kamus/ekstrak.py                 # tulis kata-baku.tsv
  python tools/kamus/ekstrak.py --self-test     # uji parser di fixture kecil
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "references" / "kata-baku.md"
OUT = pathlib.Path(__file__).resolve().parent / "kata-baku.tsv"


def bersih(s):
    return re.sub(r"\s+", " ", s.strip().strip("-").strip())


def pecah_varian(s):
    """Pecah 'a, b / c' menjadi varian, buang keterangan dalam kurung."""
    s = re.sub(r"\([^)]*\)", "", s)
    out = []
    for bagian in re.split(r"[/,]", s):
        w = bersih(bagian).lower()
        if w:
            out.append(w)
    return out


def ekstrak(teks):
    """Kembalikan daftar (hindari, baku). Dukung dua pola kata-baku.md:
    '- baku -> hindari' dan '- baku (bukan a, b)'. Sisi hindari boleh frasa
    ('nara sumber'); sisi baku boleh frasa ('bertanggung jawab').
    """
    rows = []
    for baris in teks.splitlines():
        baris = baris.strip()
        if not baris.startswith("-"):
            continue
        isi = baris[1:].strip()
        if "->" in isi:
            kiri, kanan = isi.split("->", 1)
            baku = bersih(re.sub(r"\([^)]*\)", "", kiri)).lower()
            if not baku:
                continue
            for v in pecah_varian(kanan):
                if v and v != baku:
                    rows.append((v, baku))
        else:
            m = re.match(r"^(\S+)\s+\(bukan\s+([^)]+)\)", isi)
            if m:
                baku = m.group(1).lower()
                for v in pecah_varian(m.group(2)):
                    if v and v != baku:
                        rows.append((v, baku))
    # Deterministik: unik + urut.
    return sorted(set(rows))


def self_test():
    teks = """
- apotek -> apotik
- jadwal -> jadual
- praktik (kata benda) / praktis (kata sifat) -> praktek
- konfigurasi (bukan konfig, config)
- antre -> antri
- narasumber -> nara sumber
- kalimat tanpa panah dilewati
"""
    rows = ekstrak(teks)
    assert ("apotik", "apotek") in rows, rows
    assert ("jadual", "jadwal") in rows, rows
    assert ("praktek", "praktik") not in rows  # arah salah tidak boleh masuk
    assert ("konfig", "konfigurasi") in rows, rows
    assert ("config", "konfigurasi") in rows, rows
    assert ("antri", "antre") in rows, rows
    assert ("nara sumber", "narasumber") in rows, rows  # frasa hindari didukung
    assert rows == sorted(set(rows)), "tidak deterministik"
    print(f"ekstrak self-test OK: {len(rows)} baris fixture")


def main():
    if "--self-test" in sys.argv[1:]:
        self_test()
        return 0
    rows = ekstrak(SRC.read_text(encoding="utf-8"))
    OUT.write_text("".join(f"{h}\t{b}\n" for h, b in rows), encoding="utf-8")
    print(f"ditulis {OUT} ({len(rows)} baris)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
