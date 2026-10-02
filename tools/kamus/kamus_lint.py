#!/usr/bin/env python3
"""Lint pilihan kata Bahasa Indonesia terhadap daftar buatan sendiri.

Membaca TSV `hindari<TAB>baku` (buat dengan tools/kamus/ekstrak.py dari
references/kata-baku.md, atau tulis sendiri dari kata yang Anda cek di KBBI).
Melaporkan tiap kata yang sebaiknya diganti, plus saran bakunya.

Batasan yang diketahui: cocok whole-word case-insensitive plus akhiran
melekat umum (-nya, -ku, -mu, -lah, -kah). Tanpa penguraian imbuhan dan
tanpa bedakan kelas kata. Angka hanya untuk bandingkan dua teks dengan
versi yang sama. Bukan vonis kebakuan.

Pemakaian:
  python tools/kamus/ekstrak.py
  python tools/kamus/kamus_lint.py tools/kamus/kata-baku.tsv file.md
  python tools/kamus/kamus_lint.py --self-test
"""

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "evals"))

AKHIRAN = ("nya", "ku", "mu", "lah", "kah")


def muat_daftar(tsv):
    pairs = []
    for baris in pathlib.Path(tsv).read_text(encoding="utf-8").splitlines():
        if not baris.strip() or baris.startswith("#"):
            continue
        sel = baris.split("\t")
        if len(sel) != 2 or not sel[0].strip() or not sel[1].strip():
            continue
        pairs.append((sel[0].strip().lower(), sel[1].strip()))
    return pairs


def badan(kata):
    k = kata.lower()
    for a in AKHIRAN:
        if k.endswith(a) and len(k) - len(a) >= 3:
            return k[: -len(a)]
    return k


def pola(hindari):
    """Regex whole-word untuk satu kata atau frasa ('nara sumber')."""
    bagian = r"\s+".join(re.escape(p) for p in hindari.split())
    return re.compile(r"(?<!\w)" + bagian + r"(?!\w)", re.I)


def buang_frontmatter(teks):
    return re.sub(r"\A---\r?\n[\s\S]*?\r?\n---\r?\n?", "", teks, count=1)


def lint_teks(teks, pairs):
    teks = buang_frontmatter(teks)
    try:
        import id_lint

        body = id_lint.strip_code(teks)
    except Exception:  # noqa: BLE001 — tetap jalan tanpa id_lint
        body = re.sub(r"```.*?```", " ", teks, flags=re.S)
        body = re.sub(r"`[^`\n]+`", " ", body)
    disusun = []
    for h, b in pairs:
        if " " in h:
            disusun.append((pola(h), h, b, True))
    tunggal = [(h, b) for h, b in pairs if " " not in h]
    peta = {h: b for h, b in tunggal}
    hits = []
    for i, baris in enumerate(body.splitlines(), start=1):
        for rx, h, b, _ in disusun:
            for m in rx.finditer(baris):
                hits.append({"baris": i, "kata": m.group(0), "ganti": b})
        for m in re.finditer(r"[A-Za-z]+(?:'[A-Za-z]+)?", baris):
            w = m.group(0)
            base = badan(w)
            if base in peta:
                hits.append({"baris": i, "kata": w, "ganti": peta[base]})
    return hits


def self_test():
    pairs = [
        ("apotik", "apotek"),
        ("jadual", "jadwal"),
        ("resiko", "risiko"),
        ("nara sumber", "narasumber"),
    ]
    t = "Beli obat di apotik dan cek jadual. Resikonya besar.\n`apotik` dalam kode dilewati.\nHubungi nara sumber untuk konfirmasi.\n"
    hits = lint_teks(t, pairs)
    got = [(h["kata"].lower(), h["ganti"]) for h in hits]
    assert ("apotik", "apotek") in got, got
    assert ("jadual", "jadwal") in got, got
    assert ("resikonya", "risiko") in got, got  # akhiran -nya ikut tertangkap
    assert ("nara sumber", "narasumber") in got, got  # frasa ikut tertangkap
    assert len(hits) == 4, got  # yang dalam backtick tidak dihitung
    assert lint_teks("Sudah sesuai KBBI.", pairs) == []
    print("kamus_lint self-test OK")


def main():
    args = [a for a in sys.argv[1:] if a != "--self-test"]
    if "--self-test" in sys.argv[1:]:
        self_test()
        return 0
    if len(args) != 2:
        sys.exit("pakai: kamus_lint.py DAFTAR.TSV FILE.MD | --self-test")
    pairs = muat_daftar(args[0])
    try:
        teks = pathlib.Path(args[1]).read_text(encoding="utf-8")
    except OSError as err:
        sys.exit(str(err))
    hits = lint_teks(teks, pairs)
    for h in hits:
        print(f"baris {h['baris']}: {h['kata']} -> {h['ganti']}")
    print(f"{len(hits)} temuan dari {len(pairs)} entri daftar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
