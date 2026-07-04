---
description: Split, merge, rename, or move pages; reorganize a domain
argument-hint: <target page or domain, and the desired operation>
---

Run the **refactor** mode for: $ARGUMENTS

Procedure (canonical: `wiki/_operations.md` § 5):

Identify the operation — **split**, **merge**, or **move/rename** — then:

### Split
A page conflating two distinct concepts, or grown past ~600 words with internal
seams.

1. Identify the seam. Each side should have its own thesis.
2. Create the new page(s).
3. Move content over; tighten each side.
4. Original either becomes a synthesis (if both halves are still related) or is
   deleted.
5. Update every inbound link to point to the right side.
6. Update `wiki/index.md`.

### Merge
Two pages on the same concept (commonly stub + richer page, or parallel pages
from different ingests).

1. Choose the canonical title — reads naturally as `[[X]]`, covers the broader
   scope.
2. Merge bodies. Deduplicate. Resolve framing conflicts.
3. Add the loser's title to the winner's `aliases:`.
4. Update inbound links to the new canonical name (don't rely solely on the
   alias — fix the graph).
5. Delete the loser. Update `wiki/index.md`.

### Move / Rename
Domain reorganization, or a page's name no longer fits its content.

1. Rename the file. Filenames are titles in this system.
2. Add the old title to `aliases:` for transition.
3. Update every inbound link to the new name.
4. Update `wiki/index.md` (placement may change).

### After every refactor

- Run `lint` mentally: links resolve, every page in index, no orphans created.
- Append a `wiki/log.md` entry with the old → new mapping, e.g.
  `[[Old Page]] → split into [[New A]] + [[New B]]`.

If the refactor would touch >5 pages and the user is unavailable, log the
intent and surface for the next interactive session — large refactors deserve
a confirmation step.
