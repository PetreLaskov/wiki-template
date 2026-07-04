#!/usr/bin/env python3
"""Knowledge Compiler lint — mechanical invariants and diagnostics.

Usage:
    python tools/lint.py [--stats] [--legacy] [root]

Checks the invariants of AGENTS.md § Lint that a script can check, so agent
context is spent on judgment, not counting. Errors are violations of the
contract (never acceptable standing state); warnings are diagnostics for the
next review. --legacy downgrades v2-only requirements (load_when, seed|live
status vocabulary) to warnings, for wikis created under earlier contracts.

Stdlib only. Exit code 1 if errors, else 0.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

TYPES = {"source", "entity", "concept", "thesis", "synthesis", "analysis", "question"}
STATUS_V2 = {"seed", "live"}
STATUS_LEGACY = {"working", "mature", "evergreen", "draft", "in-progress", "completed"}
CONFIDENCE = {"established", "probable", "speculative", "contested"}

OVERSIZE_WORDS = 2500
STALE_DAYS = 180
DOMAIN_SWELL = 30
LOG_ROTATE_ENTRIES = 200
MODEL_WORD_CAP = 300
RELATED_CAP = 15

# CP1252-mojibake signatures: A-circumflex / A-tilde / a-circumflex followed by
# a Latin-1 high byte or CP1252 punctuation char, broken emoji, or U+FFFD.
MOJIBAKE_RE = re.compile(
    "[\u00c2\u00c3\u00e2][\u00a0-\u00bf\u20ac\u201a\u0192\u201e\u2026\u2020"
    "\u2021\u02c6\u2030\u0160\u2039\u0152\u017d\u2018\u2019\u201c\u201d\u2022"
    "\u2013\u2014\u02dc\u2122\u0161\u203a\u0153\u017e\u0178]"
    "|\u00f0\u0178|\ufffd")

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
ANCHOR_CITE_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]\s+S(\d+)(?:\s*[-–]\s*S?(\d+))?")
ANCHOR_DEF_RE = re.compile(r"\*\*S(\d+)\*\*")
FENCE_RE = re.compile(r"^(```|~~~)", re.MULTILINE)


@dataclass
class Page:
    path: Path
    name: str  # filename stem == canonical title
    fm: dict = field(default_factory=dict)
    body: str = ""  # text after frontmatter
    fm_ok: bool = False

    @property
    def type(self) -> str:
        return self.fm.get("type", "")

    @property
    def domains(self) -> list[str]:
        d = self.fm.get("domain", [])
        return d if isinstance(d, list) else [d] if d else []

    @property
    def aliases(self) -> list[str]:
        a = self.fm.get("aliases", [])
        return a if isinstance(a, list) else [a] if a else []

    @property
    def sources(self) -> list[str]:
        s = self.fm.get("sources", [])
        return s if isinstance(s, list) else [s] if s else []

    @property
    def words(self) -> int:
        return len(self.body.split())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_list(inner: str) -> list[str]:
    """Split a YAML inline list body, respecting simple quoting."""
    out, buf, quote = [], [], None
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf.append(ch)
        elif ch in "\"'":
            quote = ch
        elif ch == ",":
            item = "".join(buf).strip()
            if item:
                out.append(item)
            buf = []
        else:
            buf.append(ch)
    item = "".join(buf).strip()
    if item:
        out.append(item)
    return out


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """Tolerant line-based YAML subset: scalars, inline lists, dash lists."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    fm: dict = {}
    key = None
    for raw_line in lines[1:end]:
        line = raw_line.rstrip()
        if not line.strip():
            continue
        dash = re.match(r"^\s+-\s+(.*)$", line)
        if dash and key:
            existing = fm.get(key)
            if not isinstance(existing, list):
                existing = [] if existing in (None, "") else [existing]
            existing.append(dash.group(1).strip().strip("\"'"))
            fm[key] = existing
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            fm[key] = split_list(value[1:-1])
        elif value == "":
            fm[key] = ""
        else:
            fm[key] = value.strip().strip("\"'")
    body = "\n".join(lines[end + 1:])
    return fm, body


def strip_fences(text: str) -> str:
    """Remove fenced code blocks so their [[links]] don't count."""
    out, fenced = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return "\n".join(out)


def norm_raw(p: str) -> str:
    return p.replace("\\", "/").lstrip("./").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", nargs="?", default=".", help="repo root (default: cwd)")
    ap.add_argument("--stats", action="store_true", help="print distribution stats")
    ap.add_argument("--legacy", action="store_true",
                    help="downgrade v2-only requirements to warnings")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    wiki, raw = root / "wiki", root / "raw"
    if not wiki.is_dir():
        print(f"error: {wiki} is not a directory (run from the repo root)")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    # ---- collect pages -------------------------------------------------
    pages: list[Page] = []
    system_texts: dict[str, str] = {}
    for path in sorted(wiki.rglob("*.md")):
        rel = path.relative_to(wiki)
        if len(rel.parts) > 1:
            errors.append(f"non-flat wiki file: wiki/{rel} (wiki/ is flat by design)")
            continue
        text = read_text(path)
        if MOJIBAKE_RE.search(text):
            snippet = MOJIBAKE_RE.search(text).group(0)
            errors.append(f"encoding corruption (mojibake '{snippet}') in wiki/{rel}")
        if "\ufeff" in text[1:]:
            errors.append(f"stray BOM inside wiki/{rel}")
        if path.name.startswith("_") or path.name in ("index.md", "log.md"):
            system_texts[path.name] = text
            continue
        fm, body = parse_frontmatter(text)
        page = Page(path=path, name=path.stem)
        if fm is None:
            errors.append(f"missing/unparseable frontmatter: wiki/{rel}")
            page.body = text
        else:
            page.fm, page.body, page.fm_ok = fm, body, True
        pages.append(page)

    index_text = system_texts.get("index.md", "")
    catalog_text = system_texts.get("_catalog.md", "")
    log_text = system_texts.get("log.md", "")

    # ---- frontmatter schema --------------------------------------------
    today = date.today()
    legacy_status: list[str] = []
    no_load_when: list[str] = []
    for p in pages:
        if not p.fm_ok:
            continue
        loc = f"[[{p.name}]]"
        if p.type not in TYPES:
            errors.append(f"{loc}: type '{p.type}' not in {sorted(TYPES)}")
        thesis = p.fm.get("thesis", "")
        if not thesis or "[" in thesis[:1]:
            errors.append(f"{loc}: thesis missing or placeholder")
        status = p.fm.get("status", "")
        if status in STATUS_LEGACY:
            legacy_status.append(p.name)
        elif status not in STATUS_V2:
            errors.append(f"{loc}: status '{status}' not in seed | live")
        conf = p.fm.get("confidence", "")
        if conf not in CONFIDENCE:
            errors.append(f"{loc}: confidence '{conf}' not in {sorted(CONFIDENCE)}")
        imp = p.fm.get("importance", "")
        try:
            if not 1 <= int(str(imp)) <= 10:
                raise ValueError
        except (ValueError, TypeError):
            errors.append(f"{loc}: importance '{imp}' not an integer 1-10")
        upd = p.fm.get("updated", "")
        try:
            datetime.strptime(str(upd), "%Y-%m-%d")
        except (ValueError, TypeError):
            errors.append(f"{loc}: updated '{upd}' not YYYY-MM-DD")
        if not p.domains:
            errors.append(f"{loc}: domain missing")
        lw = p.fm.get("load_when", "")
        if not lw or lw.startswith("["):
            if args.legacy:
                no_load_when.append(p.name)
            else:
                errors.append(f"{loc}: load_when missing (v2 routing field)")
        if p.type not in ("source", "question") and not p.sources:
            body_l = p.body.lower()
            if "pure synthesis" not in body_l:
                errors.append(f"{loc}: non-source page with empty sources and no "
                              f"'pure synthesis' note")

    # ---- link + alias resolution ----------------------------------------
    title_map: dict[str, Page] = {}
    lower_map: dict[str, str] = {}
    for p in pages:
        title_map[p.name] = p
        lower_map.setdefault(p.name.lower(), p.name)
        for a in p.aliases:
            if a:
                title_map.setdefault(a, p)
                lower_map.setdefault(a.lower(), a)

    inbound: Counter[str] = Counter()
    for p in pages:
        text = strip_fences(p.body)
        for target in LINK_RE.findall(text):
            t = target.strip()
            if not t or t.startswith("../"):
                continue
            if t in title_map:
                owner = title_map[t]
                if owner.name != p.name:
                    inbound[owner.name] += 1
            elif t.lower() in lower_map:
                warnings.append(f"[[{p.name}]] links [[{t}]] — case mismatch with "
                                f"'{lower_map[t.lower()]}'")
            else:
                errors.append(f"broken link [[{t}]] ← [[{p.name}]]")

    # ---- claim-anchor citations ------------------------------------------
    anchors: dict[str, set[int]] = {}
    for p in pages:
        if p.type == "source":
            anchors[p.name] = {int(n) for n in ANCHOR_DEF_RE.findall(p.body)}
    for p in pages:
        for target, a, b in ANCHOR_CITE_RE.findall(strip_fences(p.body)):
            t = target.strip()
            owner = title_map.get(t)
            if owner is None or owner.type != "source":
                continue
            have = anchors.get(owner.name, set())
            lo, hi = int(a), int(b) if b else int(a)
            for n in range(lo, hi + 1):
                if n not in have:
                    errors.append(f"[[{p.name}]] cites [[{t}]] S{n} — anchor not "
                                  f"defined on that source page")

    # ---- raw coverage ----------------------------------------------------
    AUX_EXT = {".py", ".pyc", ".cmd", ".sh", ".bat", ".ps1", ".exe"}
    raw_files: list[str] = []
    if raw.is_dir():
        for f in sorted(raw.rglob("*")):
            if not f.is_file() or f.name.startswith((".", "_")):
                continue
            if f.suffix.lower() in AUX_EXT:
                continue
            relr = f.relative_to(root)
            if relr.parts[:2] == ("raw", "assets"):
                continue
            raw_files.append(norm_raw(str(relr)))
    cited_by: dict[str, list[str]] = defaultdict(list)
    for p in pages:
        if p.type == "source":
            for s in p.sources:
                cited_by[norm_raw(s)].append(p.name)
    for rf in raw_files:
        owners = cited_by.get(rf, [])
        if not owners:
            warnings.append(f"unprocessed raw file (ingest backlog): {rf}")
        elif len(owners) > 1:
            errors.append(f"raw file has {len(owners)} source pages: {rf} ← "
                          + ", ".join(f"[[{o}]]" for o in owners))
    known_raw = set(raw_files)
    for p in pages:
        if p.type == "source":
            for s in p.sources:
                if norm_raw(s) not in known_raw:
                    errors.append(f"[[{p.name}]] cites missing raw file: {s}")
            sb = p.fm.get("src_bytes", "")
            if sb and p.sources:
                target = root / norm_raw(p.sources[0])
                if target.is_file():
                    actual = target.stat().st_size
                    try:
                        if int(str(sb)) != actual:
                            warnings.append(f"[[{p.name}]]: src_bytes {sb} ≠ actual "
                                            f"{actual} — re-ingest candidate")
                    except ValueError:
                        errors.append(f"[[{p.name}]]: src_bytes '{sb}' not an integer")

    # ---- registration (index/catalog) ------------------------------------
    reg_text = index_text + "\n" + catalog_text
    for p in pages:
        if f"[[{p.name}]]" not in reg_text and f"[[{p.name}|" not in reg_text \
                and f"[[{p.name}#" not in reg_text:
            errors.append(f"[[{p.name}]] not registered in index.md or _catalog.md")

    # ---- diagnostics -------------------------------------------------------
    for p in pages:
        loc = f"[[{p.name}]]"
        if inbound[p.name] == 0 and p.type != "synthesis":
            warnings.append(f"orphan (no inbound links): {loc}")
        try:
            imp = int(str(p.fm.get("importance", 0)))
        except ValueError:
            imp = 0
        if imp >= 7 and p.fm.get("status") == "seed":
            warnings.append(f"high-importance seed: {loc} (importance {imp}) — "
                            f"develop or demote")
        if p.words > OVERSIZE_WORDS:
            warnings.append(f"oversized page: {loc} ({p.words} words) — hub-extract "
                            f"candidate")
        try:
            upd = datetime.strptime(str(p.fm.get("updated", "")), "%Y-%m-%d").date()
            if today - upd > timedelta(days=STALE_DAYS):
                warnings.append(f"stale page (updated {upd}): {loc}")
        except ValueError:
            pass
        rel_m = re.search(r"^## Related\s*$(.*?)(?=^## |\Z)", p.body,
                          re.MULTILINE | re.DOTALL)
        if rel_m:
            n_rel = len(re.findall(r"^\s*-\s", rel_m.group(1), re.MULTILINE))
            if n_rel > RELATED_CAP:
                warnings.append(f"Related section has {n_rel} entries (cap ~{RELATED_CAP}): {loc}")

    domain_pages: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        if p.domains:
            domain_pages[p.domains[0]].append(p)
    for dom, plist in sorted(domain_pages.items()):
        if len(plist) > DOMAIN_SWELL:
            has_syn = any(q.type == "synthesis" for q in plist)
            warnings.append(f"domain '{dom}' has {len(plist)} pages"
                            + ("" if has_syn else " and no synthesis")
                            + " — hub/catalog candidate")

    tag_count: Counter[str] = Counter()
    for p in pages:
        t = p.fm.get("tags", [])
        for tag in (t if isinstance(t, list) else [t]):
            if tag:
                tag_count[tag] += 1
    for tag, n in tag_count.items():
        if n == 1:
            warnings.append(f"tag singleton: '{tag}'")
        if pages and n > 0.4 * len(pages):
            warnings.append(f"tag '{tag}' on >40% of pages — a domain in disguise")

    if legacy_status:
        warnings.append(f"{len(legacy_status)} pages carry legacy status vocabulary "
                        f"(v2: seed | live) — migrate opportunistically")
    if no_load_when:
        warnings.append(f"{len(no_load_when)} pages missing load_when (v2 routing "
                        f"field) — add on touch, and to the top pages by importance")

    n_log = len(re.findall(r"^## \[\d{4}-\d{2}-\d{2}\]", log_text, re.MULTILINE))
    if n_log > LOG_ROTATE_ENTRIES:
        warnings.append(f"log.md has {n_log} entries — rotate to _log-archive-YYYY.md")

    if pages and index_text:
        for section in ("## Charter", "## State of the Model", "## Load Next By Task"):
            if section not in index_text:
                warnings.append(f"index.md missing '{section}' section")
        m = re.search(r"^## State of the Model\s*$(.*?)(?=^## |\Z)", index_text,
                      re.MULTILINE | re.DOTALL)
        if m:
            n_words = len(m.group(1).split())
            if n_words > MODEL_WORD_CAP:
                warnings.append(f"State of the Model is {n_words} words "
                                f"(cap {MODEL_WORD_CAP}) — recompress at review")

    # ---- report -----------------------------------------------------------
    print(f"# Lint report — {root.name}")
    print(f"\npages: {len(pages)} | raw files: {len(raw_files)} | "
          f"errors: {len(errors)} | warnings: {len(warnings)}")
    if errors:
        print("\n## Errors (invariant violations — fix before anything else)\n")
        for e in errors:
            print(f"- {e}")
    if warnings:
        print("\n## Diagnostics (review disposal queue)\n")
        for w in warnings:
            print(f"- {w}")
    if not errors and not warnings:
        print("\nAll invariants hold; no diagnostics.")

    if args.stats:
        print("\n## Stats\n")
        for label, key in (("type", "type"), ("status", "status"),
                           ("confidence", "confidence")):
            c = Counter(str(p.fm.get(key, "?")) for p in pages)
            print(f"- {label}: " + ", ".join(f"{k}={v}" for k, v in c.most_common()))
        c = Counter(p.domains[0] if p.domains else "?" for p in pages)
        print("- primary domain: " + ", ".join(f"{k}={v}" for k, v in c.most_common()))
        total = sum(p.words for p in pages)
        print(f"- words: {total} total, {total // max(1, len(pages))} mean")
        top = inbound.most_common(5)
        if top:
            print("- most linked: " + ", ".join(f"[[{k}]]×{v}" for k, v in top))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
