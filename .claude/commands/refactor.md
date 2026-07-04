---
description: Split, merge, rename, or hub-extract pages; reorganize a domain
argument-hint: <target page or domain, and the desired operation>
---

Run the **refactor** mode for: $ARGUMENTS

Identify the operation — **hub-extract**, **split**, **merge**, or **move/rename** —
then follow `wiki/_operations.md` § 7:

### Hub-extract (pocketing)
A concept past ~2,000 words with separable concerns, or a cluster needing routing.

1. Each separable concern becomes a child page with its own thesis + `load_when`,
   **owning** its claims.
2. Move depth into the children (anchor citations intact).
3. Reduce the parent to a hub: compact opening, Key Points, **Decision Map**
   (task → child → guardrail), Boundaries, Related naming what each child owns.
4. Re-point inbound links that were about a child's content; update the index (the hub
   becomes the domain's routing entry).

### Split
One page conflating two theses → find the seam, create both pages, original becomes a
hub or is deleted, re-point inbound links, update index.

### Merge
Two pages on one concept → choose the canonical title, merge bodies keeping the
strongest citations, loser's title into winner's `aliases:`, fix inbound links anyway,
delete the loser, update index.

### Move / Rename
Rename the file (filenames are titles), old title into `aliases:`, update inbound links
and index; retire the alias at a later review.

### After every refactor

- Run `python tools/lint.py` — links resolve, registration intact, no orphans created.
- Append a `wiki/log.md` entry with the old → new mapping
  (`[[Old]] → hub + [[Child A]] + [[Child B]]`).

If the refactor would touch >5 pages and the user is unavailable, log the intent and
surface it next interactive session — large refactors deserve a confirmation step.
