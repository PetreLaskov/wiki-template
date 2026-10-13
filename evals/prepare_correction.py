#!/usr/bin/env python3
"""Copy a prepared initial run into a fresh correction workspace without answer files."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
TASK = """Work only in this workspace and follow its AGENTS.md. This is the fictional
Lumen study-method inquiry. Our priorities remain accurate understanding first, then
avoiding unnecessary study time. A new raw/04 Timing Correction.md is available.

Ingest the correction and propagate what changes through stored conclusions and
routes if this condition maintains a wiki. What changes in the speed claim and
study recommendation? What stays valid and unknown? Write correction-answer.md
and finish the appropriate verification. Use only this workspace's evidence.
"""


def prepare(source, destination):
    source = source.resolve()
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("Destination exists; refusing to merge runs.")
    if not (source / "TASK.md").is_file() or not (source / "raw/01 Definition Pilot.md").is_file():
        raise ValueError("Source is not a prepared Lumen run.")
    if destination.is_relative_to(source):
        raise ValueError("Destination must be outside the initial run.")
    destination.mkdir(parents=True)
    # An explicit allowlist prevents accidental copying of grading keys, answer
    # histories, a .git directory, or unrelated personal data.
    for name in ("AGENTS.md", "CLAUDE.md", "README.md", "raw", "wiki", "tools", "docs", ".kc"):
        path = source / name
        if path.is_dir():
            shutil.copytree(path, destination / name, ignore=shutil.ignore_patterns("__pycache__", "*.lock"))
        elif path.is_file():
            shutil.copyfile(path, destination / name)
    correction = ROOT / "evals/fixtures/correction/04 Timing Correction.md"
    shutil.copyfile(correction, destination / "raw" / correction.name)
    (destination / "TASK.md").write_text(TASK, encoding="utf-8")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        print(prepare(args.source, args.destination))
    except (ValueError, OSError) as exc:
        print(f"prepare_correction: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
