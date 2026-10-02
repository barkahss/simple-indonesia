#!/usr/bin/env python3
"""Eval deterministik simple-indonesia: hitung ulang angka dari berkas mentah.

Tidak butuh API model. Menilai pasangan (asli vs bersih) dan contoh
sebelum-sesudah dengan evals/id_lint.py, lalu menulis evals/results/RESULTS.md.
Gagal bila versi bersih tidak lebih bersih dari versi asli.

Pemakaian:
  python evals/run_eval.py            # tulis RESULTS.md
  python evals/run_eval.py --check    # tulis + gate (gagal bila tidak membaik)
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))
import id_lint  # noqa: E402

FIX = ROOT / "evals" / "fixtures"
RESULTS = ROOT / "evals" / "results"
PAIRS = [
    ("screenshot1-reply.txt", "screenshot1-bersih.txt", "descriptive"),
    ("screenshot2-reply.txt", "screenshot2-bersih.txt", "descriptive"),
]


def top_cats(violations, n=3):
    items = sorted(((k, v) for k, v in violations.items() if v), key=lambda kv: -kv[1])
    return ", ".join(f"{k}={v}" for k, v in items[:n]) or "-"


def pct(before, after):
    if before == 0:
        return "n/a"
    return f"{100.0 * (before - after) / before:.0f}%"


def main():
    RESULTS.mkdir(exist_ok=True)
    rows = []
    for orig_name, clean_name, text_type in PAIRS:
        orig = (FIX / orig_name).read_text(encoding="utf-8")
        clean = (FIX / clean_name).read_text(encoding="utf-8")
        ro = id_lint.lint(orig, text_type)
        rc = id_lint.lint(clean, text_type)
        opener = id_lint.reader_check(orig)["counts"]["opener"]
        rows.append((orig_name, clean_name, ro, rc, opener))

    ex = (ROOT / "examples" / "sebelum-sesudah.md").read_text(encoding="utf-8")
    befores = re.findall(r"Sebelum:(.*?)(?:Sesudah:|$)", ex, flags=re.S)
    afters = re.findall(r"Sesudah:(.*?)(?:## |$)", ex, flags=re.S)
    b_total = sum(id_lint.lint(b, "descriptive")["violations_total"] for b in befores)
    a_total = sum(id_lint.lint(a, "descriptive")["violations_total"] for a in afters)

    lines = [
        "# Hasil eval — simple-indonesia",
        "",
        "Dihitung ulang oleh `evals/run_eval.py` dari berkas mentah memakai `evals/id_lint.py`.",
        "Bukan vonis kepatuhan ASD-STE100. Tidak ada alat yang menjamin kepatuhan.",
        "",
        "| Pasangan | Asli (pelanggaran) | Bersih (pelanggaran) | Turun | per-100kata asli -> bersih | Kategori teratas asli |",
        "|---|---|---|---|---|---|",
    ]
    for orig_name, clean_name, ro, rc, opener in rows:
        extra = f" + opener={opener}" if opener else ""
        lines.append(
            f"| {orig_name} -> {clean_name} | {ro['violations_total']}{extra} | {rc['violations_total']} "
            f"| {pct(ro['violations_total'], rc['violations_total'])} "
            f"| {ro['violations_per_100w']} -> {rc['violations_per_100w']} | {top_cats(ro['violations'])} |"
        )
    lines += [
        f"| contoh sebelum-sesudah.md (agregat) | {b_total} | {a_total} "
        f"| {pct(b_total, a_total)} | - | - |",
        "",
    ]
    (RESULTS / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for orig_name, clean_name, ro, rc, opener in rows:
        print(
            f"{orig_name} -> {clean_name}: {ro['violations_total']} -> {rc['violations_total']} (turun {pct(ro['violations_total'], rc['violations_total'])})"
        )
    print(f"contoh: {b_total} -> {a_total} (turun {pct(b_total, a_total)})")

    if "--check" in sys.argv:
        bad = [
            (o, c)
            for o, c, ro, rc, _ in rows
            for o, c in [(o, c)]
            if rc["violations_total"] >= ro["violations_total"]
        ]
        if bad or a_total >= b_total:
            sys.exit(f"GATE GAGAL: {bad} contoh_buruk={a_total >= b_total}")
        print("gate OK")


if __name__ == "__main__":
    main()
