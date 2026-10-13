#!/usr/bin/env python3
"""A local, standard-library knowledge compiler workbench.

Frontmatter accepts one `key: value` per line: plain strings, JSON quoted
strings, or JSON arrays of strings. No nested YAML, implicit types, or folding.
Page identity is its filename stem. Sealing attests bytes and source identity,
not truth, entailment, completeness, or independence of evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from datetime import date
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit


TYPES = {"source", "note", "question", "decision", "practice"}
STATUSES = {"draft", "current", "contested", "superseded"}
FIELDS = {"type", "summary", "read_when", "status", "updated", "aliases",
          "raw", "sha256", "origin", "coverage", "coverage_note", "disposition", "source_date", "accessed"}
CLAIM_ID = re.compile(r"S[1-9][0-9]*\Z")
WIKILINK = re.compile(r"\[\[([^\]\n]+)\]\]")
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def mask(text: str) -> str:
    return re.sub(r"[^\n\r]", " ", text)


def visible_markdown(text: str) -> str:
    """Mask examples/comments while preserving offsets and line numbers."""
    text = re.sub(r"<!--[\s\S]*?(?:-->|\Z)", lambda m: mask(m[0]), text)
    result = []
    fence = None
    for line in text.splitlines(keepends=True):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            result.append(mask(line))
            if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*$", line):
                fence = None
        elif opening:
            fence = (opening[1][0], len(opening[1]))
            result.append(mask(line))
        elif line.startswith("    ") or line.startswith("\t"):
            result.append(mask(line))
        else:
            # Matching backtick runs, including code that contains shorter runs.
            result.append(re.sub(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)", lambda m: mask(m[0]), line))
    return "".join(result)


@dataclass
class Issue:
    severity: str
    code: str
    path: str
    message: str
    line: int | None = None

    def as_dict(self):
        return {k: v for k, v in vars(self).items() if v is not None}


@dataclass
class Link:
    page: str
    anchor: str | None
    line: int


@dataclass
class Page:
    path: Path
    relative: str
    title: str
    operational: bool
    metadata: dict = field(default_factory=dict)
    body: str = ""
    visible: str = ""
    body_line: int = 1
    headings: list[str] = field(default_factory=list)
    claims: dict[str, str] = field(default_factory=dict)
    links: list[Link] = field(default_factory=list)


class Workspace:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.issues: list[Issue] = []
        self.pages: dict[str, Page] = {}
        self.names: dict[str, str] = {}
        self.raw: dict[str, str] = {}
        self.raw_bytes: dict[str, bytes] = {}
        self.baseline: dict | None = None
        self._load()

    def issue(self, severity, code, path, message, line=None):
        self.issues.append(Issue(severity, code, str(path), message, line))

    def error(self, code, path, message, line=None):
        self.issue("error", code, path, message, line)

    def warning(self, code, path, message, line=None):
        self.issue("warning", code, path, message, line)

    def confined(self, path: Path, scope: Path | None = None) -> bool:
        try:
            resolved = path.resolve()
            resolved.relative_to(self.root)
            if scope is not None:
                resolved.relative_to(scope.resolve())
            return True
        except (ValueError, OSError, RuntimeError):
            return False

    def files(self, name: str):
        base = self.root / name
        if not self.confined(base):
            self.error("path.escape", name, "Directory resolves outside the workspace.")
            return []
        if not base.exists():
            return []
        if not base.is_dir():
            self.error("path.directory", name, "Expected a directory.")
            return []
        found = []
        for directory, dirs, files in os.walk(base, followlinks=False):
            for entry in sorted(dirs + files):
                path = Path(directory) / entry
                relative = path.relative_to(self.root).as_posix()
                if not self.confined(path, base):
                    self.error("path.escape", relative, "Path resolves outside its workspace directory.")
                elif path.is_symlink() and path.is_dir():
                    self.error("path.symlink", relative, "Directory symlinks are unsupported; use real directories.")
                elif entry in files:
                    if path.is_file():
                        found.append(path)
                    else:
                        self.error("path.file", relative, "Expected a readable regular file.")
        return sorted(found, key=lambda p: p.as_posix().casefold())

    def _load(self):
        if not self.root.is_dir():
            self.error("root.missing", str(self.root), "Workspace root does not exist or is not a directory.")
            return
        for path in self.files("raw"):
            relative = path.relative_to(self.root).as_posix()
            if path.name == ".gitkeep":
                continue
            try:
                data = path.read_bytes()
                self.raw[relative] = digest(data)
                self.raw_bytes[relative] = data
            except OSError as exc:
                self.error("raw.read", relative, str(exc))
        for path in self.files("wiki"):
            if path.suffix.lower() != ".md":
                continue
            relative = path.relative_to(self.root).as_posix()
            if path.parent != self.root / "wiki":
                self.error("wiki.flat", relative, "Content and operational Markdown pages must be directly in wiki/.")
                continue
            title = path.stem
            operational = title.startswith("_") or title.casefold() in {"index", "log"}
            page = Page(path, relative, title, operational)
            if title in self.pages:
                self.error("page.duplicate", relative, "Duplicate page title.")
                continue
            self.pages[title] = page
            try:
                text = normalize_newlines(path.read_bytes().decode("utf-8-sig"))
            except (UnicodeError, OSError) as exc:
                self.error("page.read", relative, f"Markdown must be readable UTF-8: {exc}")
                continue
            self.parse_page(page, text)
        for page in self.pages.values():
            aliases = page.metadata.get("aliases", [])
            for name in [page.title] + (aliases if isinstance(aliases, list) else []):
                key = name.casefold()
                if key in self.names:
                    self.error("alias.duplicate", page.relative, f"Ambiguous title/alias: {name!r}.")
                elif any(c in name for c in "#|[]/\\") or not name.strip():
                    self.error("alias.invalid", page.relative, f"Invalid title/alias: {name!r}.")
                else:
                    self.names[key] = page.title
        for page in self.pages.values():
            self.validate_source(page)
            self.validate_links(page)
        self.validate_index()
        self.load_integrity()
        self.validate_integrity()

    def parse_page(self, page: Page, text: str):
        lines = text.splitlines(keepends=True)
        if lines and lines[0].strip() == "---":
            end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
            if end is None:
                self.error("metadata.unclosed", page.relative, "Frontmatter has no closing ---.", 1)
                page.body = text
            else:
                for i, line in enumerate(lines[1:end], 2):
                    if not line.strip() or line.startswith("#"):
                        continue
                    match = re.fullmatch(r"([a-z][a-z0-9_]*):[ \t]*(.*?)[\r\n]*", line)
                    if not match:
                        self.error("metadata.syntax", page.relative, "Use key: scalar or a JSON inline string array; nested YAML is unsupported.", i)
                        continue
                    key, value = match.groups()
                    if key in page.metadata:
                        self.error("metadata.duplicate", page.relative, f"Duplicate field: {key}.", i)
                        continue
                    try:
                        if value.startswith(('"', "[", "{")):
                            value = json.loads(value)
                            if not isinstance(value, str) and not (isinstance(value, list) and all(isinstance(v, str) for v in value)):
                                raise ValueError("only strings and arrays of strings are supported")
                        elif value.startswith(("'", "|", ">", "&", "*", "!")):
                            raise ValueError("use a plain or JSON double-quoted string")
                    except (ValueError, json.JSONDecodeError) as exc:
                        self.error("metadata.syntax", page.relative, f"Invalid {key}: {exc}.", i)
                        continue
                    page.metadata[key] = value
                    if key not in FIELDS:
                        self.warning("metadata.unknown", page.relative, f"Unrecognized optional field: {key}.", i)
                page.body = "".join(lines[end + 1:])
                page.body_line = end + 2
        else:
            page.body = text
            if not page.operational:
                self.error("metadata.missing", page.relative, "Content pages require frontmatter at the start of the file.", 1)
        if not page.operational:
            for key in ("type", "summary", "read_when", "status", "updated"):
                if not isinstance(page.metadata.get(key), str) or not page.metadata[key].strip():
                    self.error("metadata.required", page.relative, f"Required nonempty string field: {key}.")
            if not isinstance(page.metadata.get("type"), str) or page.metadata["type"] not in TYPES:
                self.error("metadata.type", page.relative, "type must be source, note, question, decision, or practice.")
            if not isinstance(page.metadata.get("status"), str) or page.metadata["status"] not in STATUSES:
                self.error("metadata.status", page.relative, "status must be draft, current, contested, or superseded.")
            updated = page.metadata.get("updated")
            try:
                if not isinstance(updated, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated):
                    raise ValueError()
                date.fromisoformat(updated)
            except ValueError:
                self.error("metadata.date", page.relative, "updated must be a valid YYYY-MM-DD date.")
        if "aliases" in page.metadata and (not isinstance(page.metadata["aliases"], list) or any(not v.strip() for v in page.metadata["aliases"])):
            self.error("metadata.aliases", page.relative, "aliases must be a JSON inline array of nonempty strings.")
        page.visible = visible_markdown(page.body)
        visible_lines = page.visible.splitlines(keepends=True)
        body_lines = page.body.splitlines(keepends=True)
        headings = []
        for i, line in enumerate(visible_lines):
            match = HEADING.fullmatch(line.rstrip("\r\n"))
            if match:
                level, title = len(match[1]), match[2].strip()
                headings.append((i, level, title))
                page.headings.append(title)
        for title, count in Counter(page.headings).items():
            if count > 1:
                self.error("heading.duplicate", page.relative, f"Heading occurs {count} times: {title!r}.")
        if page.metadata.get("type") == "source":
            for position, (start, level, title) in enumerate(headings):
                if CLAIM_ID.fullmatch(title):
                    if level != 3:
                        self.error("claim.heading", page.relative, f"{title} must use an exact level-three heading: ### {title}.", page.body_line + start)
                        continue
                    stop = next((idx for idx, other_level, _ in headings[position + 1:] if other_level <= 3), len(body_lines))
                    if title not in page.claims:
                        page.claims[title] = "".join(body_lines[start:stop])
                elif re.match(r"S\d", title) and level == 3:
                    self.error("claim.heading", page.relative, "Claim headings must be exactly ### S1, ### S2, and so on.", page.body_line + start)

    def validate_source(self, page: Page):
        if page.metadata.get("type") != "source":
            return
        meta = page.metadata
        for key in ("raw", "sha256", "origin", "coverage"):
            if not isinstance(meta.get(key), str) or not meta[key].strip():
                self.error("source.required", page.relative, f"Source requires a nonempty string field: {key}.")
        raw = meta.get("raw", "")
        raw_valid = isinstance(raw, str) and self.valid_raw_path(raw)
        if not raw_valid:
            self.error("source.raw_path", page.relative, "raw must name one confined relative raw/... file using forward slashes and no .. segments.")
        elif raw not in self.raw:
            self.error("source.raw_missing", page.relative, f"Raw file not found or unsafe: {raw}.")
        expected = meta.get("sha256", "")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            self.error("source.hash_format", page.relative, "sha256 must be a lowercase 64-character hexadecimal digest.")
        elif raw_valid and raw in self.raw and self.raw[raw] != expected:
            self.error("source.hash_mismatch", page.relative, f"Raw bytes changed: {raw}. Preserve the old source and register a new revision.")
        if not isinstance(meta.get("coverage"), str) or meta["coverage"] not in {"full", "partial"}:
            self.error("source.coverage", page.relative, "coverage must be full or partial.")
        if meta.get("coverage") == "partial" and (not isinstance(meta.get("coverage_note"), str) or not meta["coverage_note"].strip()):
            self.error("source.coverage_note", page.relative, "Partial coverage requires a nonempty coverage_note naming reviewed and missing portions.")
        if not page.claims:
            if "No relevant claims." not in page.visible or not isinstance(meta.get("disposition"), str) or not meta["disposition"].strip():
                self.error("source.no_claims", page.relative, "Source needs ### S<number> claims, or 'No relevant claims.' plus a disposition field.")
        for claim_id, block in page.claims.items():
            active = visible_markdown(block)
            locators = re.findall(r"^Locator:[ \t]*(.+?)\s*$", active, re.MULTILINE)
            if len(locators) != 1:
                self.error("claim.locator", page.relative, f"{claim_id} needs exactly one explicit Locator: line.")
                continue
            locator = locators[0]
            match = re.fullmatch(r"lines ([0-9]+)-([0-9]+)", locator)
            if match:
                start, end = map(int, match.groups())
                if start < 1 or end < start:
                    self.error("claim.range", page.relative, f"{claim_id} has an invalid line range: {locator}.")
                elif raw_valid and raw in self.raw_bytes:
                    try:
                        count = len(self.raw_bytes[raw].decode("utf-8-sig").splitlines())
                        if end > count:
                            self.error("claim.range", page.relative, f"{claim_id} ends at line {end}; {raw} has {count} decoded text lines.")
                    except UnicodeError:
                        self.error("claim.binary_lines", page.relative, f"{claim_id}: line locators require UTF-8 raw text; use a page/timestamp/section locator for other formats.")
            elif re.match(r"(?:pages?|timestamps?|sections?)(?:\s|:)\S|(?:pages?|timestamps?|sections?)\s+\S", locator):
                self.warning("claim.manual_locator", page.relative, f"{claim_id}: manually verify locator {locator!r}; it is not machine-checked.")
            else:
                self.error("claim.locator", page.relative, f"{claim_id}: use 'Locator: lines N-M' or a page/timestamp/section locator.")

    def valid_raw_path(self, raw: str) -> bool:
        parts = PurePosixPath(raw).parts
        return (len(parts) >= 2 and parts[0] == "raw" and ".." not in parts
                and "\\" not in raw and ":" not in raw
                and self.confined(self.root / raw, self.root / "raw"))

    def resolve_name(self, name: str) -> str | None:
        return self.names.get(name.casefold())

    def add_reference(self, page: Page, name: str, anchor: str | None, line: int):
        title = self.resolve_name(name or page.title)
        if title is None:
            self.error("link.page", page.relative, f"Unknown wiki page or alias: {name!r}.", line)
            return
        target = self.pages[title]
        if anchor is not None and anchor not in target.headings:
            self.error("link.anchor", page.relative, f"Unknown exact heading: {title}#{anchor}.", line)
            return
        page.links.append(Link(title, anchor, line))

    def validate_links(self, page: Page):
        for match in WIKILINK.finditer(page.visible):
            target = match[1].split("|", 1)[0].strip()
            name, separator, anchor = target.partition("#")
            line = page.body_line + page.visible.count("\n", 0, match.start())
            self.add_reference(page, name.strip(), anchor.strip() if separator else None, line)
        # Local Markdown links and images, with optional titles; reference-style
        # links are resolved through their definitions below.
        definitions = {}
        for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:\s*(<[^>]+>|\S+)", page.visible, re.MULTILINE):
            definitions[match[1].casefold()] = match[2].strip("<>")
        destinations = []
        pattern = r"(?<!!)\[(?!\[)([^\]\n]*)\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)"
        image_pattern = r"!\[([^\]\n]*)\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)"
        for regex in (pattern, image_pattern):
            for match in re.finditer(regex, page.visible):
                destinations.append((match[2].strip("<>"), match.start()))
        for match in re.finditer(r"(?<!!)\[(?!\[)([^\]\n]+)\]\[([^\]\n]*)\]", page.visible):
            key = (match[2] or match[1]).casefold()
            if key in definitions:
                destinations.append((definitions[key], match.start()))
            else:
                line = page.body_line + page.visible.count("\n", 0, match.start())
                self.error("link.definition", page.relative, f"Missing Markdown link definition: {key}.", line)
        for destination, position in destinations:
            line = page.body_line + page.visible.count("\n", 0, position)
            self.validate_markdown_link(page, destination, line)

    def validate_markdown_link(self, page: Page, destination: str, line: int):
        try:
            parsed = urlsplit(destination)
        except ValueError:
            self.error("link.syntax", page.relative, f"Malformed link: {destination!r}.", line)
            return
        if parsed.scheme or parsed.netloc:
            # Remote links are never fetched. Local file URIs cannot bypass confinement.
            if parsed.scheme.lower() == "file" or (len(parsed.scheme) == 1 and ":" in destination):
                self.error("link.escape", page.relative, "Use a confined relative path instead of an absolute local path.", line)
            return
        decoded = unquote(parsed.path)
        if "\\" in decoded or decoded.startswith("/"):
            self.error("link.escape", page.relative, f"Local link must be relative: {destination!r}.", line)
            return
        target = page.path.parent / decoded if decoded else page.path
        if not self.confined(target):
            self.error("link.escape", page.relative, f"Local link escapes the workspace: {destination!r}.", line)
            return
        if not target.exists():
            self.error("link.file", page.relative, f"Missing local link target: {destination!r}.", line)
            return
        anchor = unquote(parsed.fragment) if parsed.fragment else None
        canonical = next((p for p in self.pages.values() if p.path.resolve() == target.resolve()), None)
        if canonical:
            if anchor:
                choices = [heading for heading in canonical.headings if heading == anchor or slug(heading) == anchor]
                if len(choices) != 1:
                    self.error("link.anchor", page.relative, f"Missing or ambiguous heading: {destination!r}.", line)
                    return
                anchor = choices[0]
            page.links.append(Link(canonical.title, anchor, line))
        elif anchor and target.is_file() and target.suffix.lower() == ".md":
            try:
                headings = [m[2].strip() for line_text in visible_markdown(target.read_text(encoding="utf-8-sig")).splitlines()
                            if (m := HEADING.fullmatch(line_text))]
                if not any(h == anchor or slug(h) == anchor for h in headings):
                    self.error("link.anchor", page.relative, f"Missing local Markdown heading: {destination!r}.", line)
            except (OSError, UnicodeError) as exc:
                self.error("link.read", page.relative, str(exc), line)
        elif anchor:
            self.warning("link.manual_anchor", page.relative, f"Manually verify non-Markdown fragment: {destination!r}.", line)

    def validate_index(self):
        content = {p.title for p in self.pages.values() if not p.operational}
        index = self.pages.get("index")
        for title in ("index", "log"):
            if title not in self.pages:
                self.error(f"{title}.missing", f"wiki/{title}.md", f"Expected wiki/{title}.md; check that --root points to a compiler instance.")
        if index is None or not content:
            return
        if re.search(r"\bstate:\s*bootstrap\b|No corpus or personal priorities have been supplied", index.visible, re.IGNORECASE):
            self.error("charter.bootstrap", index.relative, "Compiled content exists but the index still declares bootstrap state; replace the placeholder with a scoped charter.")
        registered = {link.page for link in index.links}
        for title in sorted(content - registered, key=str.casefold):
            self.error("index.unregistered", self.pages[title].relative, "Content page is not linked from wiki/index.md.")

    def current_claims(self):
        return {f"{page.title}#{claim_id}": {
                    "sha256": digest(normalize_newlines(block).encode("utf-8")),
                    "raw": page.metadata.get("raw"),
                    "source_sha256": page.metadata.get("sha256")}
                for page in self.pages.values() for claim_id, block in page.claims.items()}

    def load_integrity(self):
        path = self.root / ".kc" / "integrity.json"
        if not self.confined(path):
            self.error("path.escape", ".kc/integrity.json", "Integrity path resolves outside the workspace.")
            return
        if not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or set(data) != {"version", "raw", "claims"} or data["version"] != 1:
                raise ValueError("expected version 1 with exactly version, raw, and claims fields")
            if not isinstance(data["raw"], dict) or not isinstance(data["claims"], dict):
                raise ValueError("raw and claims must be objects")
            for key, value in data["raw"].items():
                if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                    raise ValueError(f"invalid raw digest: {key}")
            for key, value in data["claims"].items():
                if (not isinstance(value, dict) or set(value) != {"sha256", "raw", "source_sha256"}
                        or not all(isinstance(v, str) for v in value.values())
                        or not re.fullmatch(r"[0-9a-f]{64}", value["sha256"])
                        or not re.fullmatch(r"[0-9a-f]{64}", value["source_sha256"])):
                    raise ValueError(f"invalid claim record: {key}")
            self.baseline = data
        except (ValueError, OSError, UnicodeError) as exc:
            self.error("integrity.invalid", ".kc/integrity.json", f"Cannot trust integrity baseline: {exc}.")

    def validate_integrity(self):
        claims = self.current_claims()
        if self.baseline is None:
            if self.raw or claims:
                self.warning("integrity.unsealed", ".kc/integrity.json", "Raw files and source claims have no accepted integrity baseline; review, then seal.")
            return
        for category, current in (("raw", self.raw), ("claims", claims)):
            previous = self.baseline[category]
            for key, accepted in sorted(previous.items()):
                if key not in current:
                    self.error("integrity.missing", key, f"Previously sealed {category} record is missing; accepted records cannot be deleted or renamed.")
                elif current[key] != accepted:
                    self.error("integrity.changed", key, f"Sealed {category} bytes or source binding changed; preserve the accepted record and add a correction/new revision.")
            for key in sorted(current.keys() - previous.keys()):
                self.warning("integrity.unsealed", key, f"New {category} record has not been sealed.")

    @property
    def errors(self):
        return [issue for issue in self.issues if issue.severity == "error"]

    def report(self):
        return {"root": str(self.root), "pages": len([p for p in self.pages.values() if not p.operational]),
                "raw_files": len(self.raw), "claims": len(self.current_claims()),
                "errors": len(self.errors), "warnings": sum(i.severity == "warning" for i in self.issues),
                "issues": [i.as_dict() for i in self.issues]}


def slug(heading):
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def print_check(workspace, as_json=False):
    report = workspace.report()
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for issue in workspace.issues:
            location = issue.path + (f":{issue.line}" if issue.line else "")
            print(f"{issue.severity.upper()} [{issue.code}] {location}: {issue.message}")
        print(f"{report['errors']} errors, {report['warnings']} warnings; {report['pages']} pages, {report['raw_files']} raw files, {report['claims']} source claims.")
    return 1 if workspace.errors else 0


def status(workspace):
    sources = {p.metadata.get("raw") for p in workspace.pages.values() if p.metadata.get("type") == "source" and isinstance(p.metadata.get("raw"), str)}
    categories = {
        "Unregistered raw files": sorted(set(workspace.raw) - sources),
        "Pending pages": sorted(p.title for p in workspace.pages.values() if not p.operational and p.metadata.get("status") == "draft"),
        "Limited coverage": sorted(p.title + ": " + str(p.metadata.get("coverage_note", "(missing scope)")) for p in workspace.pages.values() if p.metadata.get("coverage") == "partial"),
        "Contested pages": sorted(p.title for p in workspace.pages.values() if p.metadata.get("status") == "contested"),
    }
    for label, entries in categories.items():
        print(label + ":")
        print("\n".join("  " + item for item in entries) if entries else "  (none)")
    state = next((p for p in workspace.pages.values() if p.title == "_state"), None)
    if state:
        print("\nRecovery state (human-authored; inspect before continuing):")
        content = state.body.strip()
        print(content[:8000] if content else "  (empty)")
        if len(content) > 8000:
            print("  [truncated; read wiki/_state.md]")
    print(f"\nCheck: {len(workspace.errors)} errors, {sum(i.severity == 'warning' for i in workspace.issues)} warnings. Run check for details.")
    return 1 if workspace.errors else 0


def search(workspace, query, limit, include_raw):
    terms = list(dict.fromkeys(re.findall(r"\w+", query.casefold())))
    if not terms:
        print("Search needs at least one word.", file=sys.stderr)
        return 2
    results = []
    for page in workspace.pages.values():
        if page.operational:
            continue
        fields = [(page.title, 8), (" ".join(page.headings), 5), (str(page.metadata.get("summary", "")), 4),
                  (str(page.metadata.get("read_when", "")), 3), (page.visible, 1)]
        counts = [(Counter(re.findall(r"\w+", text.casefold())), weight) for text, weight in fields]
        score = sum(min(counter[term], 8) * weight for term in terms for counter, weight in counts)
        if score:
            snippet = str(page.metadata.get("summary", ""))
            label = f"{page.metadata.get('type', '?')}; {page.metadata.get('status', '?')}"
            if page.metadata.get("type") == "source":
                label += f"; coverage={page.metadata.get('coverage', '?')}"
            results.append((score, page.relative, snippet, label[:120]))
    if include_raw:
        for path, data in workspace.raw_bytes.items():
            try:
                raw_text = data.decode("utf-8-sig")
            except UnicodeError:
                continue
            words = Counter(re.findall(r"\w+", raw_text.casefold()))
            score = sum(min(words[term], 8) for term in terms)
            if score:
                snippet = next((line.strip() for line in raw_text.splitlines() if any(term in line.casefold() for term in terms)), "")
                results.append((score, path, snippet, "raw snapshot; not compiled"))
    results.sort(key=lambda item: (-item[0], item[1].casefold(), item[1]))
    for score, path, snippet, label in results[:limit]:
        print(f"{score:>3}  {path} [{label}]\n     {' '.join(snippet.split())[:220]}")
    print(f"{min(len(results), limit)} of {len(results)} matching records shown.")
    if any(i.code == "integrity.unsealed" for i in workspace.issues):
        print("WARNING: source material is unsealed; run check before relying on its recorded integrity.", file=sys.stderr)
    if workspace.errors:
        print("WARNING: workspace has validation errors, possibly source/integrity drift; search results may be stale or incomplete. Run check.", file=sys.stderr)
        return 1
    return 0


def impact(workspace, target):
    name, separator, anchor = target.partition("#")
    title = workspace.resolve_name(name.strip())
    if title is None:
        print(f"Unknown page or alias: {name}", file=sys.stderr)
        return 2
    if separator and anchor not in workspace.pages[title].headings:
        print(f"Unknown exact heading: {title}#{anchor}", file=sys.stderr)
        return 2
    candidates = {}
    content = [p for p in workspace.pages.values() if not p.operational and p.title != title]
    queue = deque()
    for page in content:
        if any(link.page == title and (not separator or link.anchor is None or link.anchor == anchor) for link in page.links):
            candidates[page.title] = ("direct", target)
            queue.append(page.title)
    while queue:
        affected = queue.popleft()
        for page in content:
            if page.title not in candidates and any(link.page == affected for link in page.links):
                candidates[page.title] = ("transitive", affected)
                queue.append(page.title)
    print(f"Review candidates for {title + ('#' + anchor if separator else '')}; links indicate possible dependence, not automatic semantic invalidity:")
    print("Review index summaries and uncited copies separately; operational pages are excluded from this graph.")
    for name in sorted(candidates, key=lambda value: (candidates[value][0] != "direct", value.casefold())):
        kind, via = candidates[name]
        print(f"  {kind}: {name} (via {via})")
    if not candidates:
        print("  (none)")
    if workspace.errors:
        print("WARNING: workspace has validation errors; this graph may be incomplete. Run check.", file=sys.stderr)
        return 1
    return 0


def seal(workspace):
    if workspace.errors:
        print_check(workspace)
        print("Seal refused: fix validation errors without replacing accepted hashes.", file=sys.stderr)
        return 1
    directory = workspace.root / ".kc"
    if not workspace.confined(directory):
        print("Seal refused: unsafe .kc directory.", file=sys.stderr)
        return 1
    directory.mkdir(exist_ok=True)
    lock = directory / "seal.lock"
    lock_fd = None
    temporary = None
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        # Reload while holding the writer lock: concurrent additions must not be lost.
        fresh = Workspace(workspace.root)
        if fresh.errors:
            print_check(fresh)
            print("Seal refused: workspace changed or failed validation.", file=sys.stderr)
            return 1
        data = fresh.baseline or {"version": 1, "raw": {}, "claims": {}}
        raw_added = len(fresh.raw.keys() - data["raw"].keys())
        claims = fresh.current_claims()
        claims_added = len(claims.keys() - data["claims"].keys())
        if fresh.baseline is not None and not raw_added and not claims_added:
            print("Already sealed; no records or bytes changed.")
            return 0
        data["raw"].update({key: value for key, value in fresh.raw.items() if key not in data["raw"]})
        data["claims"].update({key: value for key, value in claims.items() if key not in data["claims"]})
        fd, temporary = tempfile.mkstemp(prefix="integrity-", suffix=".tmp", dir=directory)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as output:
            output.write(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, directory / "integrity.json")
        temporary = None
        print(f"Sealed {raw_added} new raw files and {claims_added} new claims. Existing records unchanged.")
        print("This attests bytes and source identity only; semantic review remains necessary.")
        return 0
    except FileExistsError:
        print("Seal refused: .kc/seal.lock exists. Check for an active writer; remove a stale lock only after inspection.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Seal failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
        if lock_fd is not None:
            os.close(lock_fd)
            lock.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Workspace root (default: parent of tools/)")
    commands = parser.add_subparsers(dest="command", required=True)
    check_parser = commands.add_parser("check", help="Validate structure, references, provenance, and accepted integrity")
    check_parser.add_argument("--json", action="store_true")
    commands.add_parser("status", help="List pending work and display the human-authored recovery state")
    search_parser = commands.add_parser("search", help="Rank local content using bounded lexical scores")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--raw", action="store_true", help="Also search UTF-8 raw files")
    impact_parser = commands.add_parser("impact", help="Find direct and transitive review candidates")
    impact_parser.add_argument("target", help="Page title/alias, optionally #Exact Heading")
    commands.add_parser("seal", help="Add new raw/claim integrity records; never replace accepted records")
    args = parser.parse_args(argv)
    if args.command == "search" and not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    try:
        workspace = Workspace(args.root)
        if args.command == "check":
            return print_check(workspace, args.json)
        if args.command == "status":
            return status(workspace)
        if args.command == "search":
            return search(workspace, args.query, args.limit, args.raw)
        if args.command == "impact":
            return impact(workspace, args.target)
        return seal(workspace)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"kc: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
