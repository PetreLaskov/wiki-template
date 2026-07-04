---
description: Ingest one or more raw sources into the wiki
argument-hint: [path or description; empty = all new sources in raw/]
---

Run the **ingest** mode for: $ARGUMENTS

If no argument is given, list every file in `raw/` (excluding `raw/assets/`)
that does not yet have a corresponding source page in `wiki/`, then ingest them
in order — oldest mtime first.

Procedure (canonical: `AGENTS.md` § Ingest; extended: `wiki/_operations.md` § 1):

1. Read the source(s) fully.
2. For each source:
   a. Create or re-ingest the source page from `wiki/_templates.md` § source.
   b. For each substantive entity / concept / thesis touched: update existing
      page or create new (seed stub).
   c. Update Related sections on every touched page (links bidirectional).
3. Update `wiki/index.md`: add new pages under their domain, refresh the shape
   paragraph if the wiki's scope has shifted, prepend a Recent Activity entry.
4. Append a single `wiki/log.md` entry summarizing the whole ingest.

If the ingest reveals an open question the source doesn't answer, file a
`type: question` page rather than inventing an answer.

If a source page already exists and the raw file's mtime has advanced past the
page's `updated:`, treat as **re-ingest** — mark the log entry accordingly and
flag any contradictions with `confidence: contested`.
