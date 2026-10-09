#!/usr/bin/env python3
"""Skor keterbacaan deterministik untuk Bahasa Indonesia. Gratis, tanpa API.

Menghitung dari teks polos: rata-rata kata per kalimat, persen kalimat
panjang (>20 kata prosedural, >25 deskriptif), persen kalimat pasif (awalan
di-/ter- tanpa pelaku jelas), dan kerapatan kata slop per 100 kata.

Pemakaian:
  python evals/readability.py berkas.md
  python evals/readability.py --type procedural berkas.md
  cat teks.md | python evals/readability.py --type descriptive -
  python evals/readability.py --self-test
"""

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import id_lint  # noqa: E402

PASSIVE = re.compile(
    r"\b(di|ter)[a-z]+(?:kan|i)?\b", re.I
)
ACTOR = re.compile(
    r"\b(anda|sistem|teknisi|layanan|server|aplikasi|kami|pengguna)\b", re.I
)


def readability(text, text_type="descriptive"):
    body = id_lint.strip_code(text)
    sents = id_lint.sentences(body)
    limit = 20 if text_type == "procedural" else 25
    words = [len(s.split()) for s in sents]
    n = max(1, len(sents))
    long_n = sum(1 for w in words if w > limit)
    passive_n = 0
    for s in sents:
        if PASSIVE.search(s) and not ACTOR.search(s):
            passive_n += 1
    lint = id_lint.lint(text, text_type)
    slop = lint["violations"].get("slop_word", 0)
    total_words = max(1, lint["words"])
    return {
        "type": text_type,
        "sentences": len(sents),
        "words": total_words,
        "mean_sentence_words": round(sum(words) / n, 1),
        "long_sentence_pct": round(100.0 * long_n / n, 1),
        "passive_pct": round(100.0 * passive_n / n, 1),
        "slop_per_100w": round(100.0 * slop / total_words, 2),
        "violations_total": lint["violations_total"],
    }


def self_test():
    buruk = (
        "Dengan memanfaatkan arsitektur yang tangguh, pengguna dapat dengan mudah "
        "menyelaraskan data antar sistem yang terdistribusi secara komprehensif. "
        "Pastikan semuanya sudah dikonfigurasi dengan benar sebelum layanan dimulai."
    )
    baik = (
        "Sistem menyalin data antar server. Anda menjalankan satu perintah. "
        "Jika gagal, baca log."
    )
    rb = readability(buruk)
    rg = readability(baik)
    assert rb["slop_per_100w"] > rg["slop_per_100w"], (rb, rg)
    assert rb["passive_pct"] >= rg["passive_pct"], (rb, rg)
    assert rg["violations_total"] == 0, rg
    print("readability self-test OK")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        sys.exit(0)
    text_type = "descriptive"
    if "--type" in args:
        i = args.index("--type")
        text_type = args[i + 1]
        del args[i : i + 2]
    src = args[0] if args else "-"
    if src == "-":
        text = sys.stdin.read()
    else:
        with open(src, encoding="utf-8") as fh:
            text = fh.read()
    print(json.dumps(readability(text, text_type), indent=2, ensure_ascii=False))
