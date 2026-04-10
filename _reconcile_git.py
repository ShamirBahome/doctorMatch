#!/usr/bin/env python3
"""One-shot: stage flat layout, stop tracking .env, commit."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout, end="")
    if r.stderr:
        print(r.stderr, end="", file=sys.stderr)
    if r.returncode != 0:
        sys.exit(r.returncode)


def main() -> None:
    # Untrack secrets if present in index
    run(["git", "rm", "--cached", "--ignore-unmatch", ".env"])
    run(["git", "add", "-A"])
    r = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if not r.stdout.strip():
        print("Nothing to commit.")
        return
    run(
        [
            "git",
            "commit",
            "-m",
            "Restructure: single guelph_doctor_finder folder at repo root\n\n"
            "Remove legacy doctorMatch nested layout, backend, and root duplicate app.\n"
            "Stop tracking .env (use .env.example or local .env only).",
        ]
    )


if __name__ == "__main__":
    main()
