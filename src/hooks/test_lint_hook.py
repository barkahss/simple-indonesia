"""Uji hook simple-indonesia. Jalankan: python src/hooks/test_lint_hook.py"""

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
HOOK = HERE / "lint_hook.py"


def run(event):
    p = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
    )
    return p.returncode, p.stdout, p.stderr


def main():
    # 1. Stop: balasan bersih lolos
    code, out, _ = run(
        {
            "hook_event_name": "Stop",
            "last_assistant_message": "Scraper selesai. 13 portal berhasil dalam 123 detik. Hasil tersimpan di data/terbaru.json.",
        }
    )
    assert code == 0 and "systemMessage" not in out, out
    # 2. Stop: bold + header + opener terdeteksi
    code, out, _ = run(
        {
            "hook_event_name": "Stop",
            "last_assistant_message": "Selesai.\n\n**Ya** — ini buruk.\n\n## Mengapa\n- Lag.",
        }
    )
    assert code == 0 and "systemMessage" in out, out
    # 3. PostToolUse: bukan .md dilewati
    code, _, _ = run(
        {
            "hook_event_name": "PostToolUse",
            "tool_input": {"file_path": "a.py"},
            "cwd": ".",
        }
    )
    assert code == 0
    print("hook test OK")


if __name__ == "__main__":
    main()
