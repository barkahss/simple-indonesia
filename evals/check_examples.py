#!/usr/bin/env python3
"""Pemeriksaan angka dan kebersihan contoh. Port check_numbers.py yang disederhanakan.

- Menjalankan id_lint --self-test
- Menjalankan uji hook
- Memastikan examples/sebelum-sesudah.md bagian Sesudah lebih bersih dari Sebelum
"""

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))
import id_lint  # noqa: E402


def main():
    r1 = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "id_lint.py"), "--self-test"]
    )
    assert r1.returncode == 0, "id_lint self-test gagal"
    r2 = subprocess.run(
        [sys.executable, str(ROOT / "src" / "hooks" / "test_lint_hook.py")]
    )
    assert r2.returncode == 0, "hook test gagal"

    ex = (ROOT / "examples" / "sebelum-sesudah.md").read_text(encoding="utf-8")
    # Pisahkan blok Sebelum dan Sesudah secara kasar: hitung pelanggaran per bagian.
    befores = re.findall(r"Sebelum:(.*?)(?:Sesudah:|$)", ex, flags=re.S)
    afters = re.findall(r"Sesudah:(.*?)(?:## |$)", ex, flags=re.S)
    b_total = sum(id_lint.lint(b, "descriptive")["violations_total"] for b in befores)
    a_total = sum(id_lint.lint(a, "descriptive")["violations_total"] for a in afters)
    print(f"sebelum={b_total} sesudah={a_total}")
    assert a_total < b_total, (
        f"bagian Sesudah ({a_total}) harus lebih bersih dari Sebelum ({b_total})"
    )
    print("check OK")


if __name__ == "__main__":
    main()
