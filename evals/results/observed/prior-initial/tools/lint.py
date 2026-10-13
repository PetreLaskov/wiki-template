#!/usr/bin/env python3
"""Knowledge Compiler mechanical checks (Python standard library only).

Usage: python tools/lint.py [--json] [--stats] [--legacy] [root]
Errors exit 1; warnings alone exit 0. Passing is not proof of evidence quality.

Frontmatter subset: unique top-level keys; single-line plain or quoted scalars;
inline lists or consistently indented dash lists. Double quotes use JSON escapes;
single quotes escape with ''. Comments start with # after whitespace, outside
quotes. Nested collections, tags, anchors, aliases, and multiline scalars are
unsupported: quote strings containing YAML punctuation. Integer fields accept
integers or quoted integer strings. List fields require lists of strings.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys

TYPES = {"source", "entity", "concept", "thesis", "synthesis", "analysis", "question"}
STATUSES = {"seed", "live"}
LEGACY_STATUSES = {"working", "mature", "evergreen", "draft", "in-progress", "completed"}
CONFIDENCES = {"established", "probable", "speculative", "contested"}
REQUIRED = {"type", "thesis", "load_when", "status", "domain", "importance",
            "confidence", "aliases", "sources", "updated"}
LIST_FIELDS = {"domain", "aliases", "sources", "tags"}
STRING_FIELDS = {"type", "thesis", "load_when", "status", "confidence", "updated", "src_sha256"}
FIELDS = REQUIRED | {"src_bytes", "src_sha256", "tags"}
LINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")
CLAIM_RE = re.compile(r"^ {0,3}(?:[-*] +)?\*\*S(\d+)\*\*(?=\s|[:.\u2014\u2013-]|$)", re.M)
RANGE_RE = re.compile(r"S(\d+)(?:\s*[-\u2013\u2014]\s*S?(\d+))?(?!\w)")
MOJIBAKE_RE = re.compile("[\u00c2\u00c3\u00e2][\u00a0-\u00bf\u20ac\u201a\u0192\u201e\u2026\u2018\u2019\u201c\u201d\u2013\u2014]|\u00f0\u0178|\ufffd")


class FrontmatterError(ValueError):
    pass


def uncomment(value: str) -> str:
    quote, i = None, 0
    while i < len(value):
        ch = value[i]
        if (quote == '"' and ch == "\\") or (quote == "'" and value[i:i + 2] == "''"):
            i += 2
            continue
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'" and (i == 0 or value[i - 1] in " [,:"):
            quote = ch
        elif ch == "#" and (i == 0 or value[i - 1].isspace()):
            return value[:i].rstrip()
        i += 1
    return value.rstrip()


def scalar(value: str):
    value = value.strip()
    if not value:
        raise FrontmatterError("empty scalar; use an explicit quoted string or []")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError) as exc:
            raise FrontmatterError("invalid double-quoted scalar") from exc
        if not isinstance(parsed, str):
            raise FrontmatterError("expected a quoted string")
        return parsed
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise FrontmatterError("invalid single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value[0] in "[]{}!&*|>@`%" or re.search(r":\s|[\[\]{}]", value):
        raise FrontmatterError("unsupported YAML syntax; quote this scalar")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "~"}:
        return None
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][-+]?\d+)?", value):
        return float(value)
    return value


def inline_list(value: str) -> list:
    if not value.endswith("]"):
        raise FrontmatterError("unterminated inline list")
    inner = value[1:-1].strip()
    if not inner:
        return []
    result, start, i, quote = [], 0, 0, None
    while i < len(inner):
        ch = inner[i]
        if (quote == '"' and ch == "\\") or (quote == "'" and inner[i:i + 2] == "''"):
            i += 2
            continue
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'" and not inner[start:i].strip():
            quote = ch
        elif ch == ",":
            result.append(scalar(inner[start:i]))
            start = i + 1
        i += 1
    if quote:
        raise FrontmatterError("unterminated quote in inline list")
    result.append(scalar(inner[start:]))
    return result


def parse_frontmatter(text: str) -> tuple[dict, str]:
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0] != "---":
        raise FrontmatterError("missing opening --- frontmatter delimiter")
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if end is None:
        raise FrontmatterError("missing closing --- frontmatter delimiter")
    result, pending, indent = {}, None, None
    for number, line in enumerate(lines[1:end], 2):
        line = uncomment(line)
        if not line.strip():
            continue
        try:
            if line[0].isspace():
                match = re.fullmatch(r"( +)- +(.*)", line)
                if not match or pending is None:
                    raise FrontmatterError("only dash-list indentation is supported")
                width = len(match[1])
                if indent is not None and width != indent:
                    raise FrontmatterError("inconsistent block-list indentation")
                indent = width
                result[pending].append(scalar(match[2]))
                continue
            if pending is not None and not result[pending]:
                raise FrontmatterError(f"{pending}: missing block-list items (use [] for empty)")
            match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(?: +(.*))?", line)
            if not match:
                raise FrontmatterError("expected top-level key: value")
            key, value = match[1], (match[2] or "").strip()
            if key in result:
                raise FrontmatterError(f"duplicate key '{key}'")
            pending, indent = None, None
            if not value:
                result[key], pending = [], key
            else:
                result[key] = inline_list(value) if value.startswith("[") else scalar(value)
        except FrontmatterError as exc:
            raise FrontmatterError(f"line {number}: {exc}") from exc
    if pending is not None and not result[pending]:
        raise FrontmatterError(f"{pending}: missing block-list items (use [] for empty)")
    return result, "\n".join(lines[end + 1:])


def visible_markdown(text: str) -> str:
    """Ignore comments, fenced/indented samples and inline code for checks."""
    text = re.sub(r"<!--[\s\S]*?(?:-->|\Z)", lambda m: "\n" * m[0].count("\n"), text)
    output, fence, width = [], None, 0
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence and len(marker[1]) >= width and not marker[2].strip():
                fence = None
            output.append("")
        elif marker:
            fence, width = marker[1][0], len(marker[1])
            output.append("")
        elif line.startswith(("    ", "\t")):
            output.append("")
        else:
            output.append(line)
    text = "\n".join(output)
    return re.sub(r"(?<!`)(`+)(?!`)([\s\S]*?)(?<!`)\1(?!`)",
                  lambda m: " " + "\n" * m[0].count("\n"), text)


def section(text: str, title: str) -> str | None:
    match = re.search(r"^## " + re.escape(title) + r"\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match[1].strip() if match else None


def integer(value) -> int | None:
    if type(value) is int:
        return value
    if isinstance(value, str) and re.fullmatch(r"\d+", value):
        return int(value)
    return None


@dataclass
class Page:
    name: str
    path: str
    fm: dict = field(default_factory=dict)
    body: str = ""
    parsed: bool = False

    def strings(self, key: str) -> list[str]:
        value = self.fm.get(key)
        return [x for x in value if isinstance(x, str) and x.strip()] if isinstance(value, list) else []

    @property
    def type(self):
        value = self.fm.get("type")
        return value if isinstance(value, str) else ""


def check(root: str | Path = ".", *, legacy: bool = False, today: date | None = None) -> dict:
    """Return JSON-serializable errors, warnings and stats without printing."""
    root = Path(root).resolve()
    today = today or date.today()
    errors, warnings = [], []

    def report(code, path, message, *, warning=False):
        (warnings if warning else errors).append({"code": code, "path": path, "message": message})

    def read(path: Path) -> str | None:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            report("read", rel, f"cannot read UTF-8 text: {exc}")
            return None
        if MOJIBAKE_RE.search(text):
            report("encoding-suspect", rel, "possible mojibake; inspect original text", warning=True)
        if "\ufeff" in text[1:]:
            report("encoding-bom", rel, "stray BOM inside file")
        return text

    wiki, raw = root / "wiki", root / "raw"
    pages, system = [], {}
    if not wiki.is_dir():
        report("wiki-missing", "wiki", "wiki directory is required")
    if not raw.is_dir():
        report("raw-missing", "raw", "raw directory is required")
    for path in sorted(wiki.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if path.parent != wiki:
            report("layout", rel, "wiki must be flat")
            continue
        text = read(path)
        if text is None:
            continue
        if path.name.startswith("_") or path.name in {"index.md", "log.md"}:
            system[path.name] = text
            continue
        page = Page(path.stem, rel, body=text)
        try:
            page.fm, page.body = parse_frontmatter(text)
            page.parsed = True
        except FrontmatterError as exc:
            report("frontmatter", rel, str(exc))
        pages.append(page)
    for filename in ("index.md", "log.md"):
        if not (wiki / filename).is_file():
            report("system-missing", "wiki/" + filename, "required system file is missing")
    index = visible_markdown(system.get("index.md", ""))
    charter = section(index, "Charter")
    if pages and (not charter or re.search(r"not yet written|awaiting charter|TODO|\[placeholder\]", charter, re.I)):
        report("charter", "wiki/index.md", "a populated wiki requires a written Charter")
    if pages:
        for heading in ("State of the Model", "Load Next By Task"):
            if section(index, heading) is None:
                report("router-section", "wiki/index.md", f"missing {heading} section", warning=True)

    for page in pages:
        if not page.parsed:
            continue
        fm = page.fm
        for key in sorted(REQUIRED - fm.keys()):
            report("field-missing", page.path, f"required field '{key}' missing", warning=legacy and key in {"load_when", "status"})
        for key in sorted(fm.keys() - FIELDS):
            report("field-unknown", page.path, f"unsupported field '{key}'")
        for key in sorted(STRING_FIELDS & fm.keys()):
            if not isinstance(fm[key], str) or not fm[key].strip():
                report("field-type", page.path, f"{key} must be a nonempty string")
        for key in sorted(LIST_FIELDS & fm.keys()):
            value = fm[key]
            if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                report("field-type", page.path, f"{key} must be a list of nonempty strings")
            elif len(set(value)) != len(value):
                report("field-duplicate", page.path, f"{key} has duplicate entries")
        for key, choices in (("type", TYPES), ("confidence", CONFIDENCES), ("status", STATUSES)):
            value = fm.get(key)
            if key in fm and (not isinstance(value, str) or value not in choices):
                report("field-value", page.path, f"{key} must be one of {', '.join(sorted(choices))}",
                       warning=legacy and key == "status" and isinstance(value, str) and value in LEGACY_STATUSES)
        for key in ("thesis", "load_when"):
            value = fm.get(key)
            if isinstance(value, str) and value.startswith("["):
                report("placeholder", page.path, f"{key} is a placeholder")
        imp = integer(fm.get("importance"))
        if "importance" in fm and (imp is None or not 1 <= imp <= 10):
            report("importance", page.path, "importance must be an integer 1-10")
        if "domain" in fm and not page.strings("domain"):
            report("domain", page.path, "domain needs at least one value")
        updated = fm.get("updated")
        if "updated" in fm:
            try:
                if not isinstance(updated, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated):
                    raise ValueError
                parsed_date = date.fromisoformat(updated)
                if parsed_date > today:
                    report("date-future", page.path, f"updated {updated} is in the future")
                elif today - parsed_date > timedelta(days=180):
                    report("stale", page.path, f"updated {updated}; inspect whether the page needs review", warning=True)
            except ValueError:
                report("date", page.path, "updated must be a real date in YYYY-MM-DD format")
        if page.type not in {"source", "question"} and fm.get("sources") == [] and "pure synthesis" not in visible_markdown(page.body).lower():
            report("provenance", page.path, "empty sources requires an explicit pure synthesis note")
        if "src_bytes" in fm and (integer(fm["src_bytes"]) is None or integer(fm["src_bytes"]) < 0):
            report("src-bytes", page.path, "src_bytes must be a nonnegative integer")
        if "src_sha256" in fm and (not isinstance(fm["src_sha256"], str) or not re.fullmatch(r"[0-9a-fA-F]{64}", fm["src_sha256"])):
            report("src-hash", page.path, "src_sha256 must be a 64-character hexadecimal string")
        if page.type != "source" and any(key in fm for key in ("src_bytes", "src_sha256")):
            report("source-metadata", page.path, "src_bytes and src_sha256 belong only on source pages")

    names, spellings = {}, {}
    for name, page in [(p.name, p) for p in pages] + [(a, p) for p in pages for a in p.strings("aliases")]:
        key = name.casefold()
        if key in names:
            report("alias-collision", page.path, f"name '{name}' collides with '{spellings[key]}' on {names[key].path}")
        else:
            names[key], spellings[key] = page, name
    bodies = {p.name: visible_markdown(p.body) for p in pages}
    anchors = {}
    for page in pages:
        if page.type != "source":
            continue
        definitions = [int(n) for n in CLAIM_RE.findall(bodies[page.name])]
        anchors[page.name] = set(definitions)
        for number, count in Counter(definitions).items():
            if number < 1 or count > 1:
                report("claim-definition", page.path, f"S{number} must be positive and defined only once")
        if not definitions and not re.search(r"\bno material claims\b", bodies[page.name], re.I):
            report("claim-missing", page.path, "source page requires an S1-style claim definition or explicit 'No material claims' note")

    inbound, registered = Counter(), set()
    texts = [(p.path, bodies[p.name], p) for p in pages]
    texts += [("wiki/" + n, visible_markdown(system[n]), None) for n in ("index.md", "_catalog.md") if n in system]
    for location, body, origin in texts:
        for match in LINK_RE.finditer(body):
            target = match[1].split("|", 1)[0].strip()
            title, _, fragment = target.partition("#")
            title = title.strip()
            owner = names.get(title.casefold())
            if owner is None:
                target_file = title if title.endswith(".md") else title + ".md"
                is_system = "/" not in title and (title.startswith("_") or title in {"index", "log", "index.md", "log.md"})
                if (is_system or target_file in {"../AGENTS.md", "../CLAUDE.md", "../README.md"}) and (wiki / target_file).is_file():
                    if fragment.startswith("S") or re.match(r"\s+S\d", body[match.end():]):
                        report("claim-target", location, f"claim citation [[{target}]] must target a source page")
                    continue
                report("link", location, f"unresolved link [[{target}]]")
                continue
            if title != spellings[title.casefold()]:
                report("link-case", location, f"[[{title}]] differs in case from '{spellings[title.casefold()]}'", warning=True)
            if origin is None:
                registered.add(owner.name)
            elif origin.name != owner.name:
                inbound[owner.name] += 1
            ranges = []
            if fragment.startswith("S"):
                parsed = RANGE_RE.fullmatch(fragment)
                if parsed:
                    ranges.append(parsed)
                else:
                    report("claim-citation", location, f"malformed claim fragment [[{target}]]")
            suffix = re.match(r"\s+(S\d+(?:\s*[-\u2013\u2014]\s*S?\d+)?)(?!\w)", body[match.end():])
            if suffix:
                ranges.append(RANGE_RE.fullmatch(suffix[1]))
            for claim in ranges:
                if owner.type != "source":
                    report("claim-target", location, f"[[{title}]] S{claim[1]} targets a non-source page")
                    continue
                lo, hi = int(claim[1]), int(claim[2] or claim[1])
                have = anchors.get(owner.name, set())
                if lo > hi:
                    report("claim-range", location, f"[[{title}]] has reversed range S{lo}-S{hi}")
                elif hi - lo + 1 > len(have) or any(n not in have for n in range(lo, hi + 1)):
                    report("claim-anchor", location, f"[[{title}]] S{lo}" + (f"-S{hi}" if hi != lo else "") + " includes an undefined anchor")

    raw_owners, raw_resolved = defaultdict(list), raw.resolve()
    for page in pages:
        refs = page.strings("sources")
        if page.type == "source" and len(refs) != 1:
            report("source-cardinality", page.path, "source pages must reference exactly one raw file")
        for ref in refs:
            posix, win = PurePosixPath(ref.replace("\\", "/")), PureWindowsPath(ref)
            valid = bool(posix.parts) and posix.parts[0] == "raw" and len(posix.parts) > 1 and ".." not in posix.parts and not posix.is_absolute() and not win.drive and not win.root
            target = root.joinpath(*posix.parts)
            try:
                contained = target.resolve().is_relative_to(raw_resolved)
            except (OSError, RuntimeError):
                contained = False
            if not valid or not contained:
                report("raw-path", page.path, f"raw reference must remain inside raw/: {ref}")
                continue
            if not target.is_file():
                report("raw-missing", page.path, f"referenced raw file does not exist: {ref}")
                continue
            if page.type == "source":
                raw_owners[target.resolve()].append(page.name)
                try:
                    data = target.read_bytes()
                    expected = page.fm.get("src_sha256")
                    if expected is None:
                        report("hash-missing", page.path, "src_sha256 absent; record the hash at next verified ingest", warning=True)
                    elif isinstance(expected, str) and re.fullmatch(r"[0-9a-fA-F]{64}", expected) and hashlib.sha256(data).hexdigest() != expected.lower():
                        report("hash-drift", page.path, "raw content SHA-256 changed; re-ingest candidate", warning=True)
                    size = integer(page.fm.get("src_bytes"))
                    if size is not None and size != len(data):
                        report("size-drift", page.path, f"src_bytes {size} differs from actual {len(data)}; re-ingest candidate", warning=True)
                except OSError as exc:
                    report("raw-read", page.path, f"cannot fingerprint {ref}: {exc}")
        if page.name not in registered:
            report("registration", page.path, "page is not registered in index.md or _catalog.md")
    for path, owners in raw_owners.items():
        if len(owners) > 1:
            report("source-duplicate", path.relative_to(root).as_posix(), "multiple source ledgers: " + ", ".join(owners))
    raw_files = []
    for path in sorted(raw.rglob("*")):
        rel = path.relative_to(raw)
        if not path.is_file() or any(p.startswith((".", "_")) for p in rel.parts) or rel.parts[0] == "assets":
            continue
        if path.suffix.lower() in {".py", ".pyc", ".cmd", ".sh", ".bat", ".ps1", ".exe"}:
            continue
        raw_files.append(path)
        if path.resolve() not in raw_owners:
            report("raw-backlog", path.relative_to(root).as_posix(), "raw source has no compiled ledger", warning=True)

    for page in pages:
        if not inbound[page.name] and page.type != "synthesis":
            report("orphan", page.path, "no inbound content links; router registration is separate", warning=True)
        imp = integer(page.fm.get("importance")) or 0
        if imp >= 7 and page.fm.get("status") == "seed":
            report("important-seed", page.path, "high-importance seed; develop or demote", warning=True)
        words = len(bodies[page.name].split())
        if words > 2500:
            report("oversized", page.path, f"{words} words; inspect for separable claim ownership", warning=True)
        related = section(bodies[page.name], "Related") or ""
        if len(re.findall(r"^\s*-\s", related, re.M)) > 10:
            report("related-long", page.path, "Related exceeds ~10 entries; keep high-value edges", warning=True)
    state = section(index, "State of the Model") or ""
    if len(state.split()) > 300:
        report("state-long", "wiki/index.md", "State of the Model exceeds 300 words", warning=True)
    log = visible_markdown(system.get("log.md", ""))
    log_dates = re.findall(r"^## \[(\d{4}-\d{2}-\d{2})\]", log, re.M)
    for value in log_dates:
        try:
            if date.fromisoformat(value) > today:
                report("date-future", "wiki/log.md", f"log date {value} is in the future")
        except ValueError:
            report("date", "wiki/log.md", f"invalid log date {value}")
    if len(log_dates) > 200:
        report("log-long", "wiki/log.md", f"{len(log_dates)} entries; rotate older entries at review", warning=True)
    domains = Counter(p.strings("domain")[0] for p in pages if p.strings("domain"))
    for domain, count in sorted(domains.items()):
        if count > 30:
            report("domain-large", "wiki/index.md", f"domain '{domain}' has {count} pages; inspect routing", warning=True)
    stats = {"pages": len(pages), "raw_files": len(raw_files), "log_entries": len(log_dates),
             "errors": len(errors), "warnings": len(warnings),
             "types": dict(Counter(p.type or "?" for p in pages)),
             "statuses": dict(Counter(str(p.fm.get("status", "?")) for p in pages)),
             "confidence": dict(Counter(str(p.fm.get("confidence", "?")) for p in pages)),
             "primary_domains": dict(domains), "words": sum(len(bodies[p.name].split()) for p in pages),
             "most_linked": dict(inbound.most_common(5))}
    return {"errors": errors, "warnings": warnings, "stats": stats}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--json", action="store_true", help="machine-readable errors, warnings and stats")
    parser.add_argument("--legacy", action="store_true", help="downgrade missing routing/status and known legacy statuses only")
    args = parser.parse_args(argv)
    result = check(args.root, legacy=args.legacy)
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        counts = result["stats"]
        print(f"Knowledge Compiler lint: {counts['pages']} pages, {counts['raw_files']} raw files, "
              f"{counts['errors']} errors, {counts['warnings']} warnings")
        for level in ("errors", "warnings"):
            for item in result[level]:
                print(f"{level[:-1]} [{item['code']}] {item['path']}: {item['message']}")
        if args.stats:
            print(json.dumps(counts, ensure_ascii=True, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    sys.exit(main())
