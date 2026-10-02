#!/usr/bin/env python3
"""Hook nasihat untuk agen. Tidak pernah memblokir.

PostToolUse (Write|Edit pada berkas .md): lint berkas dengan evals/id_lint.py
dan bila ada pelanggaran, cetak teks pelanggar dan nomor baris tiap temuan
(maks MAX_HOOK_HITS) ke stderr dan keluar 2 agar model melihatnya.
Keluar 2 pada PostToolUse bersifat nasihat: alat sudah jalan.

Stop: baca `last_assistant_message`, periksa register balasan (tanpa header,
bullet, bold, atau em-dash, tanpa pembuka/penutup), dan kembalikan
systemMessage hanya bila balasan melanggar. Selalu keluar 0 agar sesi tidak loop.
"""

import fnmatch
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "evals"))

MAX_HOOK_HITS = 12
CLAUDE_DIR = ".claude"
OPENERS = re.compile(r"^\s*(tentu|baik|selesai\.|pertanyaan bagus|hebat|siap\b)", re.I)
CLOSERS = re.compile(
    r"(semoga membantu|beri tahu saya|beritahu saya|jangan ragu|ada pertanyaan lain)",
    re.I,
)


def load_linter():
    try:
        import id_lint  # noqa

        return id_lint
    except Exception:
        return None


def absolute(path, cwd=None):
    return pathlib.Path(cwd or ".", pathlib.Path(path).expanduser()).absolute()


def excluded(target):
    config_dirs = {absolute(os.environ.get("CLAUDE_CONFIG_DIR") or f"~/{CLAUDE_DIR}")}
    raw = os.environ.get("SIMPLE_INDONESIA_LINT_EXCLUDE", "").split(os.pathsep)
    patterns = [os.path.expanduser(p) for p in raw if p]
    form = pathlib.Path(os.path.normpath(target))
    if CLAUDE_DIR in form.parts:
        return True
    if any(fnmatch.fnmatch(str(form), p) for p in patterns):
        return True
    return False


def post_tool_use(event):
    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".md"):
        return 0
    target = absolute(path, event.get("cwd"))
    if excluded(target):
        return 0
    lint = load_linter()
    if lint is None:
        return 0
    try:
        text = target.read_text(encoding="utf-8")
    except OSError:
        return 0
    report = lint.lint(text, "descriptive")
    if not report["violations_total"]:
        return 0
    detail = lint.lint_detail(text, "descriptive")
    lines = [
        f"simple-indonesia: {target.name} ada {report['violations_total']} pelanggaran."
    ]
    for h in detail[:MAX_HOOK_HITS]:
        lines.append(f"  baris {h['line']}, {h['category']}: {h['text']}")
    if len(detail) > MAX_HOOK_HITS:
        lines.append(f"  dan {len(detail) - MAX_HOOK_HITS} temuan lain.")
    lines.append("Perbaiki temuan di berkas yang baru ditulis, lalu lanjut.")
    sys.stderr.write("\n".join(lines) + "\n")
    return 2


def stop(event):
    reply = event.get("last_assistant_message") or ""
    problems = []
    lint = load_linter()
    if lint is not None:
        c = lint.reader_check(reply)["counts"]
        for key, label in (
            ("em_dash", "em-dash"),
            ("bold_spans", "bold"),
            ("headers", "header"),
            ("bullets", "item daftar"),
        ):
            if c[key]:
                problems.append(f"{c[key]} {label}")
        if c.get("opener"):
            problems.append("pembuka pengisi")
        if c.get("closer"):
            problems.append("penutup pengisi")
    if OPENERS.search(reply.split("\n")[0] if reply.strip() else ""):
        if "pembuka pengisi" not in problems:
            problems.append("pembuka pengisi")
    if CLOSERS.search(reply):
        if "penutup pengisi" not in problems:
            problems.append("penutup pengisi")
    if problems:
        print(
            json.dumps(
                {
                    "systemMessage": "simple-indonesia reply check: "
                    + "; ".join(problems)
                    + ". Jawab dalam prosa."
                }
            )
        )
    return 0


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    try:
        name = event.get("hook_event_name", "")
        if name == "PostToolUse":
            return post_tool_use(event)
        if name == "Stop":
            return stop(event)
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
