#!/usr/bin/env python3
"""Bench beneran simple-indonesia: generate teks via API model lalu nilai dengan lint.

AMAN: kunci API hanya dibaca dari environment, tidak pernah dicetak atau
ditulis ke berkas. Jangan tempel kunci di chat atau commit.

  $env:LLM_API_KEY="..."            # PowerShell (wajib untuk bench asli)
  $env:LLM_MODEL="gpt-4o-mini"      # opsional
  $env:LLM_BASE_URL="https://api.openai.com/v1"  # opsional, OpenAI-compatible

Pemakaian:
  python evals/run_bench.py --dry-run   # tanpa API: nilai fixture yang ada
  python evals/run_bench.py             # bench asli: baseline vs skill per skenario
  python evals/run_bench.py --only baseline --max-scenarios 2
  python evals/run_bench.py --outdir evals/results/bench/coba1   # folder tetap,
      # bisa diulang untuk lanjutkan bila terputus (berkas raw yang ada dipakai lagi)

Keluaran: evals/results/bench/<UTC-timestamp>/raw/*.txt + RESULTS.md + usage.json
(usage.json hanya berisi hitungan token, tanpa kunci).

Konfigurasi (urutan menang: CLI > env > berkas lokal > baku):
  --base-url / $env:LLM_BASE_URL / evals/.bench.local.json
  --model    / $env:LLM_MODEL    / evals/.bench.local.json
  (kunci)    / $env:LLM_API_KEY   / evals/.bench.local.json {"api_key": ...}

Berkas evals/.bench.local.json TIDAK masuk git (lihat .gitignore).
Contoh isinya: {"base_url": "http://localhost:1234/v1", "model": "nama-model", "api_key": "..."}
Untuk model lokal, api_key boleh string bebas bila server tidak cek kunci.
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

LOCAL_CFG = ROOT / "evals" / ".bench.local.json"


def local_cfg():
    """Baca evals/.bench.local.json bila ada (gitignored, tidak ikut commit)."""
    try:
        return json.loads(LOCAL_CFG.read_text(encoding="utf-8"))
    except OSError:
        return {}
    except ValueError:
        sys.exit(f"{LOCAL_CFG} bukan JSON valid.")


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
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--max-tokens", type=int, default=400)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--offset", type=int, default=0, help="lewati N skenario pertama")
    ap.add_argument(
        "--scenarios", default="evals/scenarios.json", help="berkas skenario JSON"
    )
    ap.add_argument(
        "--outdir",
        default=None,
        help="pakai folder hasil tetap (untuk lanjutkan bench yang terputus)",
    )
    args = ap.parse_args()

    scenarios = json.loads((ROOT / args.scenarios).read_text(encoding="utf-8"))
    if args.offset:
        scenarios = scenarios[args.offset :]
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
    cfg = local_cfg()
    if not api_key:
        api_key = str(cfg.get("api_key", ""))
    if not api_key:
        sys.exit(
            'LLM_API_KEY kosong dan tidak ada evals/.bench.local.json. Set di PowerShell: $env:LLM_API_KEY="..." lalu ulangi. Coba --dry-run untuk tanpa API.'
        )
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
    system_skill = skill_system_prompt()
    system_base = "Anda asisten yang membantu. Jawab dalam Bahasa Indonesia."

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.outdir:
        outdir = ROOT / args.outdir
    else:
        outdir = (
            ROOT / "evals" / "results" / "bench" / f"{model.replace('/', '_')}-{stamp}"
        )
    rawdir = outdir / "raw"
    rawdir.mkdir(parents=True, exist_ok=True)
    rows = {"texts": [], "scores": [], "table": []}
    usage = {"prompt_tokens": 0, "completion_tokens": 0}
    total_calls = len(scenarios) * len(conds)
    done = 0
    import time as _time

    for sc in scenarios:
        line = {}
        for cond in conds:
            done += 1
            target = rawdir / f"{cond}__{sc['id']}.txt"
            if target.exists():
                # Lanjutkan bench yang terputus: pakai hasil yang sudah ada.
                text = target.read_text(encoding="utf-8")
                v, _, w = score(text, sc["type"])
                use = {"prompt_tokens": 0, "completion_tokens": 0}
                print(
                    f"[{done}/{total_calls}] {sc['id']}/{cond}: sudah ada, {v} pelanggaran",
                    flush=True,
                )
            else:
                sys_ = system_skill if cond == "skill" else system_base
                print(
                    f"[{done}/{total_calls}] {sc['id']}/{cond}: generate...", flush=True
                )
                t0 = _time.time()
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
                dt = _time.time() - t0
                target.write_text(
                    text, encoding="utf-8"
                )  # simpan langsung tiap panggil
                v, _, w = score(text, sc["type"])
                print(
                    f"[{done}/{total_calls}] {sc['id']}/{cond}: {v} pelanggaran ({dt:.0f} dtk)",
                    flush=True,
                )
            usage["prompt_tokens"] += use["prompt_tokens"]
            usage["completion_tokens"] += use["completion_tokens"]
            rows["texts"].append((cond, sc["id"], text))
            rows["scores"].append((cond, sc["id"], sc["type"], v, 0, w))
            line[cond] = v
        if set(line) == {"baseline", "skill"}:
            rows["table"].append(
                (sc["id"], sc["type"], line["baseline"], line["skill"])
            )
    write_results(outdir, rows, usage, model)
    return 0


if __name__ == "__main__":
    sys.exit(main())
