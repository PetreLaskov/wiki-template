#!/usr/bin/env python3
"""Create a blank compiler instance from this template; never merge into existing work."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

FILES = (
    "AGENTS.md", "CLAUDE.md", ".gitignore", "wiki/index.md", "wiki/log.md",
    "docs/WORKFLOWS.md", "docs/SCHEMA.md", "docs/TEMPLATES.md",
    "tools/kc.py", "tools/kc.ps1", "tools/lint.py",
)

# Factory defaults are separate from the editable live index and history. A user
# may personalize those files before adding a corpus; they must not leak to a clone.
BOOTSTRAP_INDEX = """# Working understanding

## Charter

**State: bootstrap.** No corpus or personal priorities have been supplied to this
instance. Draft a short charter from the user's purpose and representative sources
when first compiling: purpose, recurring questions, evidence posture, boundaries,
and page economics. Do not mistake these prompts for a completed charter.

## Current understanding

No compiled conclusions yet.

## Where to look

| Question or task | Page | Why it helps / important limit |
| --- | --- | --- |

## Open questions and revision triggers

None recorded yet.

## Page register

No content pages yet. Register every content page here with a wikilink.

## Recent changes

No corpus changes yet. See `log.md` for operations after first use.
"""

BOOTSTRAP_LOG = """# Operation history

Newest first. Record material operations, concise no-op ingests, actual verification,
and pending work. Do not log every lookup or store a conversation transcript here.
Archive old entries when this file becomes inconvenient; preserve their history.
"""

INSTANCE_README = """# Your Knowledge Compiler

Open this folder in your agent. Ask it to read `AGENTS.md`, then describe your
purpose, recurring questions, and a real task. Add source snapshots to `raw/`.
The agent maintains `wiki/`; you can read it in any Markdown editor.

Start with [the index](wiki/index.md). [Workflows](docs/WORKFLOWS.md),
[schema](docs/SCHEMA.md), and [templates](docs/TEMPLATES.md) are available on demand.

Python 3.10+; standard library only:

```text
python tools/kc.py status
python tools/kc.py search "your question"
python tools/kc.py check
```

Windows convenience: `./tools/kc.ps1 check` locates an existing Python runtime;
set `KC_PYTHON` to an explicit interpreter path if needed.

For research, migration, software tests, and behavioral evaluation, return to the
template repository used to create this instance. Those development materials and
their grading keys are deliberately not copied into your working knowledge base.
"""


def create_instance(template: Path, destination: Path) -> Path:
    template = template.resolve()
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Destination already exists; refusing to merge: {destination}")
    raw = template / "raw"
    if raw.exists() and any(p.is_file() and p.name != ".gitkeep" for p in raw.rglob("*")):
        raise ValueError("Source template has raw material. Use a blank template, not a populated instance.")
    wiki = template / "wiki"
    if any(p.stem not in {"index", "log"} and not p.stem.startswith("_") for p in wiki.glob("*.md")):
        raise ValueError("Source template has content pages. Use the blank template.")
    index = template / "wiki/index.md"
    if not index.is_file() or "State: bootstrap" not in index.read_text(encoding="utf-8-sig"):
        raise ValueError("The source index is not a blank bootstrap template.")
    for relative in FILES:
        path = template / relative
        if not path.is_file() or not path.resolve().is_relative_to(template):
            raise ValueError(f"Required template file is missing or unsafe: {relative}")
    # Exclusive directory creation protects prior work. A failed copy is left visibly
    # incomplete for inspection; no recursive deletion or rollback of user files.
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    for relative in FILES:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative == "wiki/index.md":
            target.write_text(BOOTSTRAP_INDEX, encoding="utf-8")
        elif relative == "wiki/log.md":
            target.write_text(BOOTSTRAP_LOG, encoding="utf-8")
        else:
            shutil.copyfile(template / relative, target)
    (destination / "raw").mkdir()
    (destination / "raw/.gitkeep").write_text("", encoding="utf-8")
    (destination / "README.md").write_text(INSTANCE_README, encoding="utf-8")
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--template", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        path = create_instance(args.template, args.destination)
    except (OSError, ValueError) as exc:
        print(f"new_instance: {exc}", file=sys.stderr)
        return 1
    print(f"Created blank instance: {path}")
    print("Fresh charter/history; no raw sources, compiled pages, grading keys, or research reports copied. Operating instructions were reused.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
