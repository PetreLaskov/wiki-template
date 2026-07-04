---
description: Verify wiki invariants; report violations
---

Run the **lint** mode. Verify each invariant from `AGENTS.md` § Lint and
report violations. Do not auto-fix — surface findings for the user to direct
into a `review` or `refactor`.

Invariants to check (system files `_*.md` excluded throughout):

1. **Link resolution.** Every `[[link]]` resolves to an existing page or to a
   page's `aliases:`. List broken links as `target ← page-with-link`.
2. **Source coverage.** Every file in `raw/` (excluding `raw/assets/`) has
   exactly one source page in `wiki/`. List orphan raw files (no source page)
   and duplicate source pages (>1 page citing the same raw file).
3. **Index coverage.** Every page in `wiki/` (excl. `_*.md`) appears in
   `wiki/index.md`. List pages not in the index.
4. **Source attribution.** Every non-source page has ≥1 entry in `sources:`,
   or `sources: []` with an explicit "pure synthesis" note in the body. List
   pages failing this.
5. **Temporal sanity.** No page's `updated:` predates its raw source's mtime.
   List pages older than their sources.
6. **Contradiction marking.** Pages making contradictory claims should both
   carry `confidence: contested` and reference each other in Related. List
   pages with `contested` that lack the cross-reference, and any obvious
   contradictions not yet marked.

Then list **diagnostics** (not invariants — surface only):

- Orphan pages (no inbound links).
- `importance ≥ 7 ∧ status = seed`.
- Tag singletons and over-represented tags.
- `[[…]]` to nonexistent pages.
- Domains exceeding ~30 pages.

Output: a structured report. No log entry for `lint` unless the run reveals
violations that demand follow-up; in that case, log the count and the suggested
next mode (`review` or `refactor`).
