#!/usr/bin/env python3
"""Bench register balasan: jawab pertanyaan chat baseline vs skill, lalu nilai.

Yang dinilai per balasan: format terlihat (header/bold/bullet/em-dash),
pembuka/penutup pengisi (reader_check), plus pelanggaran dokumen (id_lint).

Kunci API hanya dari env atau evals/.bench.local.json (lihat run_bench.py).
Tidak pernah dicetak atau ditulis ke berkas.

Pemakaian:
  python evals/run_reply_bench.py --dry-run   # tanpa API: nilai fixture screenshot
  python evals/run_reply_bench.py --outdir evals/results/bench/qwen38-balasan
"""

import argparse
import datetime
import json
import os
import pathlib
import sys
import time as _time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))
import id_lint  # noqa: E402
from run_bench import chat, local_cfg  # noqa: E402

SYSTEM_BALASAN = """Jawab dalam Bahasa Indonesia polos, hanya prosa: tanpa header, tanpa daftar bullet, tanpa bold, tanpa tabel. Blok kode boleh bila pembaca harus menyalinnya. Kalimat pertama memberi jawaban atau hasil. Jangan ulangi pertanyaan. Tanpa em-dash. Definisikan istilah konsep dalam beberapa kata saat pertama kali. Tanpa singkatan informal. Tanpa pembuka (Tentu, Pertanyaan bagus) dan tanpa penutup (Semoga membantu, Beri tahu saya)."""
SYSTEM_BEBAS = "Anda asisten yang membantu. Jawab dalam Bahasa Indonesia."


def nilai(balasan):
    rc = id_lint.reader_check(balasan)
    doc = id_lint.lint(balasan, "descriptive")
    return (
        rc["visible_total"]
        + rc["counts"]["opener"]
        + rc["counts"]["closer"]
        + doc["violations_total"]
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", choices=["baseline", "skill"], default=None)
    ap.add_argument("--max-scenarios", type=int, default=None)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--scenarios", default="evals/reply_scenarios.json")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--max-tokens", type=int, default=150)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--model", default=None)
    args = ap.parse_args()

    if args.dry_run:
        fix = ROOT / "evals" / "fixtures"
        for o, c in [
            ("screenshot1-reply.txt", "screenshot1-bersih.txt"),
            ("screenshot2-reply.txt", "screenshot2-bersih.txt"),
        ]:
            ro = nilai((fix / o).read_text(encoding="utf-8"))
            rc = nilai((fix / c).read_text(encoding="utf-8"))
            assert rc < ro, (o, ro, rc)
            print(f"dry-run {o}: {ro} -> {rc} OK")
        print("dry-run balasan OK (tanpa API)")
        return 0

    api_key = os.environ.get("LLM_API_KEY", "")
    cfg = local_cfg()
    if not api_key:
        api_key = str(cfg.get("api_key", ""))
    if not api_key:
        sys.exit("LLM_API_KEY kosong dan tidak ada evals/.bench.local.json.")
    base_url = (
        args.base_url
        or os.environ.get("LLM_BASE_URL", "")
        or str(cfg.get("base_url", ""))
        or "http://127.0.0.1:7936/v1"
    )
    model = (
        args.model
        or os.environ.get("LLM_MODEL", "")
        or str(cfg.get("model", ""))
        or "qwen3.8-max"
    )

    scenarios = json.loads((ROOT / args.scenarios).read_text(encoding="utf-8"))
    if args.offset:
        scenarios = scenarios[args.offset :]
    if args.max_scenarios:
        scenarios = scenarios[: args.max_scenarios]
    conds = [args.only] if args.only else ["baseline", "skill"]
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = (
        ROOT / args.outdir
        if args.outdir
        else ROOT
        / "evals"
        / "results"
        / "bench"
        / f"{model.replace('/', '_')}-balasan-{stamp}"
    )
    rawdir = outdir / "raw"
    rawdir.mkdir(parents=True, exist_ok=True)

    total = len(scenarios) * len(conds)
    done, agg, tabel, usage = 0, {}, [], {"prompt_tokens": 0, "completion_tokens": 0}
    for sc in scenarios:
        baris = {}
        for cond in conds:
            done += 1
            target = rawdir / f"{cond}__{sc['id']}.txt"
            if target.exists():
                teks = target.read_text(encoding="utf-8")
                v = nilai(teks)
                print(
                    f"[{done}/{total}] {sc['id']}/{cond}: sudah ada, skor {v}",
                    flush=True,
                )
            else:
                sys_ = SYSTEM_BALASAN if cond == "skill" else SYSTEM_BEBAS
                print(f"[{done}/{total}] {sc['id']}/{cond}: generate...", flush=True)
                t0 = _time.time()
                try:
                    teks, use = chat(
                        base_url,
                        api_key,
                        model,
                        sys_,
                        sc["prompt"],
                        args.timeout,
                        args.max_tokens,
                    )
                except Exception as err:  # noqa: BLE001 — jangan bocorkan kunci
                    sys.exit(
                        f"gagal memanggil API untuk {sc['id']}/{cond}: {type(err).__name__}"
                    )
                dt = _time.time() - t0
                target.write_text(teks, encoding="utf-8")
                v = nilai(teks)
                usage["prompt_tokens"] += use.get("prompt_tokens", 0)
                usage["completion_tokens"] += use.get("completion_tokens", 0)
                print(
                    f"[{done}/{total}] {sc['id']}/{cond}: skor {v} ({dt:.0f} dtk)",
                    flush=True,
                )
            agg.setdefault(cond, []).append(v)
            baris[cond] = v
        if set(baris) == {"baseline", "skill"}:
            tabel.append((sc["id"], baris["baseline"], baris["skill"]))

    def total_cond(c):
        return sum(agg.get(c, []))

    red = "n/a"
    if total_cond("baseline"):
        red = f"{100.0 * (total_cond('baseline') - total_cond('skill')) / total_cond('baseline'):.0f}%"
    md = [
        f"# Bench balasan — simple-indonesia ({model})",
        "",
        f"{len(tabel)} pertanyaan chat x 2 kondisi. Skor = format terlihat + pembuka/penutup + pelanggaran dokumen.",
        "",
        "| Kondisi | Skor total |",
        "|---|---|",
        f"| baseline | {total_cond('baseline')} |",
        f"| skill | {total_cond('skill')} |",
        "",
        f"Penurunan: {red}.",
        "",
        "| Pertanyaan | baseline | skill |",
        "|---|---|---|",
    ]
    md += [f"| {sid} | {b} | {s} |" for sid, b, s in tabel] + [""]
    (outdir / "RESULTS.md").write_text("\n".join(md), encoding="utf-8")
    (outdir / "usage.json").write_text(
        json.dumps({"model": model, **usage}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(
        f"baseline {total_cond('baseline')} vs skill {total_cond('skill')}, turun {red}. Hasil di {outdir}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
