#!/usr/bin/env python3
"""Bench beneran simple-indonesia: generate teks via API model lalu nilai dengan lint.

AMAN: kunci API hanya dibaca dari environment, tidak pernah dicetak atau
ditulis ke berkas. Jangan tempel kunci di chat atau commit.

  $env:LLM_API_KEY="..."            # PowerShell (wajib untuk bench asli)
  $env:LLM_MODEL="gpt-4o-mini"      # opsional
  $env:LLM_BASE_URL="https://api.openai.com/v1"  # opsional, OpenAI-compatible

Pemakaian:
  python evals/run_bench.py --dry-run   # tanpa API: nilai fixture yang sudah ada
  python evals/run_bench.py             # bench asli: baseline vs skill per skenario
  python evals/run_bench.py --only baseline --max-scenarios 2

Keluaran: evals/results/bench/<UTC-timestamp>/raw/*.txt + RESULTS.md + usage.json
(usage.json hanya berisi hitungan token, tanpa kunci).
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))
import id_lint  # noqa: E402


def skill_system_prompt():
    """Ambil blok aturan dari prompts/system-prompt.md (di antara dua pagar ---)."""
    text = (ROOT / "prompts" / "system-prompt.md").read_text(encoding="utf-8")
    parts = re.split(r"^---[ \t]*$", text, flags=re.M)
    if len(parts) >= 3:
        return parts[1].strip()
    return text.strip()


def chat(base_url, api_key, model, system, user, timeout, max_tokens):
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    msg = data["choices"][0]["message"]["content"]
    use = data.get("usage", {})
    return msg, {
        "prompt_tokens": use.get("prompt_tokens", 0),
        "completion_tokens": use.get("completion_tokens", 0),
    }


def score(text, text_type):
    r = id_lint.lint(text, text_type)
    return r["violations_total"], r["violations_per_100w"], r["words"]


def write_results(outdir, rows, usage, model):
    outdir.mkdir(parents=True, exist_ok=True)
    raw = outdir / "raw"
    raw.mkdir(exist_ok=True)
    for cond, sid, text in rows["texts"]:
        (raw / f"{cond}__{sid}.txt").write_text(text, encoding="utf-8")
    (outdir / "usage.json").write_text(
        json.dumps({"model": model, **usage}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    agg = {}
    for cond in ("baseline", "skill"):
        rs = [r for r in rows["scores"] if r[0] == cond]
        tot = sum(r[3] for r in rs)
        w = sum(r[5] for r in rs)
        agg[cond] = (tot, round(100.0 * tot / max(1, w), 2))
    red = "n/a"
    if agg["baseline"][0]:
        red = f"{100.0 * (agg['baseline'][0] - agg['skill'][0]) / agg['baseline'][0]:.0f}%"
    md = [
        f"# Bench — simple-indonesia ({model})",
        "",
        f"{len(rows['scores']) // 2} skenario x 2 kondisi (baseline vs skill). Dinilai dengan `evals/id_lint.py`.",
        "",
        "| Kondisi | Pelanggaran total | per-100kata |",
        "|---|---|---|",
        f"| baseline | {agg['baseline'][0]} | {agg['baseline'][1]} |",
        f"| skill | {agg['skill'][0]} | {agg['skill'][1]} |",
        "",
        f"Penurunan: {red}.",
        "",
        "| Skenario | Tipe | baseline | skill |",
        "|---|---|---|---|",
    ]
    for sid, stype, b, s in rows["table"]:
        md.append(f"| {sid} | {stype} | {b} | {s} |")
    md.append("")
    (outdir / "RESULTS.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[5:9]), f"\nPenurunan: {red}.")
    print(f"Hasil mentah di {outdir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--dry-run", action="store_true", help="tanpa API: nilai fixture yang ada"
    )
    ap.add_argument("--only", choices=["baseline", "skill"], default=None)
    ap.add_argument("--max-scenarios", type=int, default=None)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--max-tokens", type=int, default=400)
    args = ap.parse_args()

    scenarios = json.loads(
        (ROOT / "evals" / "scenarios.json").read_text(encoding="utf-8")
    )
    if args.max_scenarios:
        scenarios = scenarios[: args.max_scenarios]
    conds = [args.only] if args.only else ["baseline", "skill"]

    if args.dry_run:
        fix = ROOT / "evals" / "fixtures"
        pairs = [
            ("screenshot1-reply.txt", "screenshot1-bersih.txt"),
            ("screenshot2-reply.txt", "screenshot2-bersih.txt"),
        ]
        for o, c in pairs:
            ro = id_lint.lint((fix / o).read_text(encoding="utf-8"), "descriptive")
            rc = id_lint.lint((fix / c).read_text(encoding="utf-8"), "descriptive")
            assert rc["violations_total"] < ro["violations_total"], (o, ro, rc)
            print(
                f"dry-run {o}: {ro['violations_total']} -> {rc['violations_total']} OK"
            )
        print("dry-run OK (tanpa API)")
        return 0

    api_key = os.environ.get("LLM_API_KEY", "")
    if not api_key:
        sys.exit(
            'LLM_API_KEY kosong. Set di PowerShell: $env:LLM_API_KEY="..." lalu ulangi. Coba --dry-run untuk tanpa API.'
        )
    base_url = os.environ.get("LLM_BASE_URL", "http://127.0.0.1:7936/v1")
    model = os.environ.get("LLM_MODEL", "qwen3.8-max")
    system_skill = skill_system_prompt()
    system_base = "Anda asisten yang membantu. Jawab dalam Bahasa Indonesia."

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = ROOT / "evals" / "results" / "bench" / f"{model.replace('/', '_')}-{stamp}"
    rows = {"texts": [], "scores": [], "table": []}
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    for sc in scenarios:
        line = {}
        for cond in conds:
            sys_ = system_skill if cond == "skill" else system_base
            try:
                text, use = chat(
                    base_url,
                    api_key,
                    model,
                    sys_,
                    sc["prompt"],
                    args.timeout,
                    args.max_tokens,
                )
            except Exception as err:  # noqa: BLE001 — bench tidak boleh bocorkan kunci
                sys.exit(
                    f"gagal memanggil API untuk {sc['id']}/{cond}: {type(err).__name__}"
                )
            usage["prompt_tokens"] += use["prompt_tokens"]
            usage["completion_tokens"] += use["completion_tokens"]
            v, _, w = score(text, sc["type"])
            rows["texts"].append((cond, sc["id"], text))
            rows["scores"].append((cond, sc["id"], sc["type"], v, 0, w))
            line[cond] = v
            print(f"{sc['id']}/{cond}: {v} pelanggaran")
        if set(line) == {"baseline", "skill"}:
            rows["table"].append(
                (sc["id"], sc["type"], line["baseline"], line["skill"])
            )
    write_results(outdir, rows, usage, model)
    return 0


if __name__ == "__main__":
    sys.exit(main())
