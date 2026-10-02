#!/usr/bin/env python3
"""Penghitung pelanggaran deterministik untuk skill simple-indonesia v1.1.

Port dari evals/ste_lint.py milik SimpleEnglish ke Bahasa Indonesia + EYD V.
Menghitung pelanggaran mekanis yang bisa ditangkap regex: panjang kalimat,
modal terlarang, bentuk telah/sudah, singkatan informal, klausa menggantung,
titik koma, em-dash, singkatan Latin/dll, kata berlebih AI, syarat di akhir,
putaran sinonim, koma berlebih, paragraf padat, istilah Inggris telanjang.

Batasan yang diketahui: ini regex, bukan parser tata bahasa. Angka hanya
untuk membandingkan dua teks dengan versi yang sama. Bukan vonis kepatuhan.
Tidak ada alat yang menjamin kepatuhan ASD-STE100.

Pemakaian:
  python evals/id_lint.py --type procedural file.md
  cat text.md | python evals/id_lint.py --type descriptive -
  python evals/id_lint.py --type reply file.md
  python evals/id_lint.py --self-test
"""

import json
import pathlib
import re
import sys
from collections import Counter

BANNED_MODALS = re.compile(
    r"\b(sebaiknya|semestinya|seharusnya|harusnya|mungkin|barangkali|kiranya|sekiranya|seandainya)\b",
    re.I,
)
PERFECT = re.compile(r"\b(telah|sudah)\s+\w+", re.I)
INFORMAL = re.compile(
    r"(?<!\w)(yg|dgn|dg|spt|bgt|nggak|ngga|gak|gimana|dimana|kemana|kpn|blm|sdh|tdk|utk)\b",
    re.I,
)
GANTUNG = re.compile(
    r",\s*(memudah|memungkin|membuat|menjadikan|menyebab|menghasil|mempermudah)\w*",
    re.I,
)
LATIN = re.compile(
    r"\b(e\.g\.|i\.e\.|etc\.?|mis\.|dll\.?|dsb\.?|dst\.?)(?=[\s,)]|$)", re.I
)
SLOP_CORE = re.compile(
    r"\b(manfaatkan|leverage|utilisasi|robust|tangguh|canggih|komprehensif|seamless|mulus|"
    r"penting\s+untuk\s+dicatat|perlu\s+dicatat|dalam\s+rangka\s+untuk|tidak\s+hanya\b|"
    r"melainkan\b|secara\s+sederhana|dengan\s+mudah|"
    r"holistik|sinergi|permadani|revolusioner|transformatif|pengubah\s+permainan|"
    r"memfasilitasi|merampingkan|menyelami|streamlin\w*|facilitat\w*|plethora|myriad|"
    r"delve|crucial|pivotal|blazingly)\b",
    re.I,
)
# Istilah Inggris yang wajib di-backtick atau didefinisikan saat pertama pakai.
# strip_code() sudah mengubah `kode` menjadi CODESPAN, jadi yang tersisa adalah telanjang.
ENGLISH_BARE = re.compile(
    r"\b(retry|fallback|headless|binary|unofficial|pool|render)\b",
    re.I,
)
SLOP_TSV = pathlib.Path(__file__).resolve().parent / "slop_id.tsv"


def slop_pattern():
    terms = []
    if SLOP_TSV.exists():
        for line in SLOP_TSV.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            term = line.split("\t")[0].strip().lower()
            if term:
                terms.append(re.escape(term).replace(r"\ ", r"\s+") + r"\w*")
    if not terms:
        return SLOP_CORE
    return re.compile(
        SLOP_CORE.pattern[: -len(r")\b")] + "|" + "|".join(terms) + r")\b", re.I
    )


SLOP = slop_pattern()
TRAILING_COND = re.compile(r"\s(jika|bila|apabila|ketika|kalau)\s", re.I)
DASH = re.compile(r"—|(?<!\d)–(?!\d)|(?<= )--(?= )|(?<=[^\s\d]{2}) - (?=[^\s\d]{2})")
ROTATION_SETS = [
    (
        "pastikan-group",
        re.compile(
            r"\b(pastikan|periksa|verifikasi|validasi|konfirmasi|cek)\w*\b", re.I
        ),
    ),
    (
        "konfigurasi-group",
        re.compile(r"\b(konfigurasi|config|pengaturan|setelan|opsi|options?)\b", re.I),
    ),
    ("gunakan-group", re.compile(r"\b(gunakan|pakai|manfaatkan|utilisasi)\b", re.I)),
]
LIMITS = {"procedural": 20, "descriptive": 25}
OPENERS = re.compile(
    r"^\s*(tentu|baik|selesai\.|pertanyaan bagus|pertanyaan yang bagus|hebat|siap\b)",
    re.I,
)
CLOSERS = re.compile(
    r"(semoga membantu|beri tahu saya|beritahu saya|jangan ragu|ada pertanyaan lain|let me know|hope this helps)",
    re.I,
)


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " CODESPAN ", text)
    text = re.sub(r"^#+\s.*$", " ", text, flags=re.M)
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"^\s*\|[\s:|-]+\|\s*$", " ", text, flags=re.M)
    text = re.sub(
        r"^\s*\|(.*)\|\s*$",
        lambda m: (
            ". ".join(c.strip() for c in m.group(1).split("|") if c.strip()) + ". "
        ),
        text,
        flags=re.M,
    )
    return text


def sentences(text):
    text = re.sub(
        r"^\s*([-*]|\d+\.)\s+(.*?)([.!?:])?\s*$",
        lambda m: m.group(2) + (m.group(3) or ".") + " ",
        text,
        flags=re.M,
    )
    parts = re.split(r"(?<=[.!?:])\s+", text)
    return [p.strip() for p in parts if len(p.strip().split()) >= 2]


def paragraphs(text):
    body = strip_code(text).strip()
    return [p for p in re.split(r"\n\s*\n", body) if p.strip()]


def lint_detail(text, text_type):
    body = strip_code(text)
    limit = LIMITS[text_type]
    hits = []

    def add(category, m, snippet=None):
        line = body.count("\n", 0, m.start()) + 1
        hits.append(
            {
                "category": category,
                "text": (snippet or m.group(0)).strip(),
                "line": line,
            }
        )

    def locate(sentence, search_from):
        start = body.find(sentence, search_from)
        return start if start != -1 else search_from

    def add_sentence(category, sentence, start):
        line = body.count("\n", 0, start) + 1
        text_out = sentence if len(sentence) <= 80 else sentence[:80] + "…"
        hits.append({"category": category, "text": text_out, "line": line})

    pos = 0
    for s in sentences(body):
        pos = locate(s, pos)
        n = len(s.split())
        if n > limit:
            add_sentence("sentence_over_limit", s, pos)
        if s.count(",") >= 5:
            add_sentence("comma_overload", s, pos)
        m = TRAILING_COND.search(s)
        if m:
            line_start = s.rfind("\n", 0, m.start()) + 1
            if m.start() - line_start >= 4 and not re.match(
                r"^(jika|bila|apabila|ketika|kalau)\b", s, re.I
            ):
                add_sentence("trailing_condition", s, pos)
        pos += max(len(s), 1)

    for m in INFORMAL.finditer(body):
        add("informal_abbrev", m)
    for m in BANNED_MODALS.finditer(body):
        add("banned_modal", m)
    for m in PERFECT.finditer(body):
        add("perfect_tense", m)
    for m in GANTUNG.finditer(body):
        add("gantung_clause", m)
    for m in re.finditer(";", body):
        add("semicolon", m)
    for m in DASH.finditer(body):
        add("em_dash", m)
    for m in LATIN.finditer(body):
        add("latin_abbrev", m)
    for m in SLOP.finditer(body):
        add("slop_word", m)
    for m in ENGLISH_BARE.finditer(body):
        add("english_bare", m)
    for name, rx in ROTATION_SETS:
        seen = {}
        for m in rx.finditer(body):
            stem = m.group(1).lower().rstrip("s")
            seen.setdefault(stem, m)
        for m in list(seen.values())[1:]:
            add("synonym_rotation", m, f"{m.group(0)} ({name})")

    for idx, p in enumerate(paragraphs(text), start=1):
        ns = len(sentences(p))
        if ns > 6:
            hits.append(
                {
                    "category": "paragraph_overload",
                    "text": f"paragraf {idx}: {ns} kalimat",
                    "line": idx,
                }
            )

    return sorted(hits, key=lambda h: h["line"])


def lint(text, text_type):
    body = strip_code(text)
    sents = sentences(body)
    limit = LIMITS[text_type]
    counts = {}
    lengths = [len(s.split()) for s in sents]
    counts["sentence_over_limit"] = sum(1 for n in lengths if n > limit)
    counts["comma_overload"] = sum(1 for s in sents if s.count(",") >= 5)
    counts["informal_abbrev"] = len(INFORMAL.findall(body))
    counts["banned_modal"] = len(BANNED_MODALS.findall(body))
    counts["perfect_tense"] = len([m for m in PERFECT.finditer(body)])
    counts["gantung_clause"] = len(GANTUNG.findall(body))
    counts["semicolon"] = body.count(";")
    counts["em_dash"] = len(DASH.findall(body))
    counts["latin_abbrev"] = len(LATIN.findall(body))
    counts["slop_word"] = len(SLOP.findall(body))
    counts["english_bare"] = len(ENGLISH_BARE.findall(body))

    def trailing_cond(s):
        m = TRAILING_COND.search(s)
        if not m:
            return False
        line_start = s.rfind("\n", 0, m.start()) + 1
        return m.start() - line_start >= 4 and not re.match(
            r"^(jika|bila|apabila|ketika|kalau)\b", s, re.I
        )

    counts["trailing_condition"] = sum(1 for s in sents if trailing_cond(s))
    counts["paragraph_overload"] = sum(
        1 for p in paragraphs(text) if len(sentences(p)) > 6
    )
    rotation = 0
    for _, rx in ROTATION_SETS:
        stems = {m.group(1).lower().rstrip("s") for m in rx.finditer(body)}
        if len(stems) > 1:
            rotation += len(stems) - 1
    counts["synonym_rotation"] = rotation
    words = max(1, len(body.split()))
    total = sum(counts.values())
    return {
        "type": text_type,
        "words": words,
        "sentences": len(sents),
        "mean_sentence_words": round(sum(lengths) / max(1, len(lengths)), 1),
        "longest_sentence_words": max(lengths, default=0),
        "violations": counts,
        "violations_total": total,
        "violations_per_100w": round(100.0 * total / words, 2),
    }


SLOP_FIXTURE = """Dengan memanfaatkan mekanisme retry yang tangguh, unggahan yang gagal secara otomatis
dicoba ulang, memastikan integritas data tetap terjaga selama seluruh proses yang telah
dirancang dari awal untuk menangani bahkan gangguan jaringan yang paling menantang. Anda sebaiknya
verifikasi kredensial Anda; penting untuk dicatat bahwa Anda harus memeriksa pengaturan,
mis. batas waktu konfigurasi. Hubungi dukungan jika masalah berlanjut jika flag diatur."""

CLEAN_FIXTURE = """Sistem mencoba ulang unggahan yang gagal secara otomatis. Proses ini menjaga data tetap benar.

Jika kegagalan berlanjut, pastikan kredensial benar. Jika masalah berlanjut, hubungi dukungan."""

DASH_FIXTURE = """Deploy gagal — disk penuh.
Unggahan gagal -- token kedaluwarsa.
Coba ulang gagal - port tertutup.
Jangan gunakan --force di produksi.
Rentang 5 - 10 menit.
Tulis x - y = z di papan.
Gunakan flag `--config sqlpipe.yaml`.
Hapus panel:
   -   Kendurkan empat baut.
"""

BOLD = re.compile(r"\*\*[^*\n]+\*\*")
HEADER = re.compile(r"^#{1,6}\s", re.M)
BULLET = re.compile(r"^\s*([-*+]|\d+[.)])\s", re.M)


def reader_check(text):
    text = text.replace("\r\n", "\n")
    prose = re.sub(r"```.*?```", " ", text, flags=re.S)
    prose = re.sub(r"`[^`\n]+`", " CODESPAN ", prose)
    prose_no_md = re.sub(r"^\s*(#{1,6}\s|[-*+]\s|\d+[.)]\s|\|)", "", prose, flags=re.M)
    prose_no_md = re.sub(r"^\s*[\s:|-]+$", "", prose_no_md, flags=re.M)
    sents = [
        p
        for p in re.split(r"(?<=[.!?])[\"')\]]*\s+|\n+", prose_no_md)
        if len(p.strip().split()) >= 1
    ]
    sents = [s for s in sents if s.strip()]
    counts = {
        "sentences": len(sents),
        "em_dash": len(DASH.findall(prose)),
        "bold_spans": len(BOLD.findall(prose)),
        "headers": len(HEADER.findall(prose)),
        "bullets": len(BULLET.findall(prose)),
        "informal": len(INFORMAL.findall(prose)),
        "opener": 1
        if OPENERS.search(prose.split("\n")[0] if prose.strip() else "")
        else 0,
        "closer": len(CLOSERS.findall(prose)),
    }
    words = max(1, len(prose_no_md.split()))
    visible = (
        counts["em_dash"] + counts["bold_spans"] + counts["headers"] + counts["bullets"]
    )
    return {"type": "reply", "words": words, "counts": counts, "visible_total": visible}


REPLY_FIXTURE = """**Ya** — ini buruk.

## Mengapa
- Lag bertambah.
- Pengguna menunggu.

Periksa sekarang. Lalu skala."""


def self_test():
    slop = lint(SLOP_FIXTURE, "procedural")
    clean = lint(CLEAN_FIXTURE, "procedural")
    dashes = lint(DASH_FIXTURE, "procedural")
    assert slop["violations"]["banned_modal"] >= 1, slop
    assert slop["violations"]["perfect_tense"] >= 1, slop
    assert slop["violations"]["latin_abbrev"] >= 1, slop
    assert slop["violations"]["slop_word"] >= 2, slop
    assert slop["violations"]["trailing_condition"] >= 1, slop
    assert slop["violations"]["synonym_rotation"] >= 1, slop
    assert slop["violations"]["english_bare"] >= 1, slop
    assert clean["violations_total"] == 0, clean
    assert dashes["violations"]["em_dash"] == 3, dashes
    r = reader_check(REPLY_FIXTURE)["counts"]
    assert (
        r["sentences"],
        r["em_dash"],
        r["bold_spans"],
        r["headers"],
        r["bullets"],
    ) == (6, 1, 1, 1, 2), r
    assert (
        reader_check("Ya. Ini buruk karena lag bertambah. Skala sekarang.")[
            "visible_total"
        ]
        == 0
    )
    assert (
        lint(
            "Pastikan kredensial benar. Periksa pengaturan dan cek log.", "descriptive"
        )["violations"]["synonym_rotation"]
        >= 1
    )
    assert (
        lint("Tulis yg cepat dan dgn benar spt contoh.", "descriptive")["violations"][
            "informal_abbrev"
        ]
        >= 2
    )
    # koma berlebih: daftar portal dalam satu kalimat
    comma_case = "Hasil: detikNews, Antara, Liputan6, JPNN, Suara, Sindonews, Okezone, dan Viva lewat jalur HTML."
    assert lint(comma_case, "descriptive")["violations"]["comma_overload"] == 1
    # paragraf padat: 7 kalimat dalam satu paragraf
    para_case = " ".join(
        [f"Kalimat nomor {i} menjelaskan satu fakta." for i in range(1, 8)]
    )
    assert lint(para_case, "descriptive")["violations"]["paragraph_overload"] == 1
    # istilah Inggris telanjang
    assert (
        lint("Jalankan retry dua kali dengan fallback berjenjang.", "descriptive")[
            "violations"
        ]["english_bare"]
        >= 1
    )
    # pembuka satu kata terdeteksi di reader_check
    assert (
        reader_check("Selesai.\nSemua langkah sudah dijalankan. Hasil tersimpan.")[
            "counts"
        ]["opener"]
        == 1
    )
    detail = lint_detail(SLOP_FIXTURE, "procedural")
    assert len(detail) == slop["violations_total"], (
        len(detail),
        slop["violations_total"],
    )
    print(
        "self-test OK:",
        slop["violations_total"],
        "pelanggaran di slop fixture, 0 di clean",
    )


USAGE = "pemakaian: id_lint.py [--type procedural|descriptive|reply] [--gate] (FILE|-) | --self-test"


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        self_test()
        return 0
    gate = "--gate" in args
    if gate:
        args.remove("--gate")
    text_type = "descriptive"
    if "--type" in args:
        i = args.index("--type")
        if i + 1 >= len(args):
            sys.exit("nilai hilang setelah --type\n" + USAGE)
        text_type = args[i + 1]
        del args[i : i + 2]
    if text_type not in LIMITS and text_type != "reply":
        sys.exit(
            "tipe tak dikenal %r (procedural atau descriptive atau reply)\n%s"
            % (text_type, USAGE)
        )
    if len(args) != 1:
        sys.exit(USAGE)
    src = args[0]
    if src == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(src, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as err:
            sys.exit(str(err))
    if text_type == "reply":
        report = reader_check(text)
        doc = lint(strip_code(text), "descriptive")
        report["doc_lint"] = doc
    else:
        report = lint(text, text_type)
        report["detail"] = lint_detail(text, text_type)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(json.dumps(report, indent=2, ensure_ascii=False))
    total = (
        report["visible_total"] if text_type == "reply" else report["violations_total"]
    )
    if text_type == "reply":
        total += report["doc_lint"]["violations_total"]
    return 1 if gate and total else 0


if __name__ == "__main__":
    sys.exit(main())
