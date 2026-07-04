---
description: Compose a synthesis or thesis page from existing wiki material
argument-hint: <domain, topic, or question>
---

Run the **synthesize** mode for: $ARGUMENTS

Procedure (canonical: `AGENTS.md` § Modes; extended: `wiki/_operations.md` § 3):

1. Pull all wiki pages in scope (filter `wiki/index.md` by the named domain,
   tag, or topic).
2. Distill the through-line — the single argument or pattern that organizes
   them. If you can't name one in a sentence, the synthesis isn't ready;
   surface that and stop.
3. Choose the page type:
   - **synthesis** — if the work maps a territory (lists sub-areas + the
     through-line that holds them together).
   - **thesis** — if the work argues a position from accumulated evidence.
4. Draft the page from the appropriate scaffold in `wiki/_templates.md`.
5. Update each touched page with a Related entry pointing to the new
   synthesis / thesis (links are bidirectional).
6. Index it under its primary domain. If it spans multiple domains, list it
   under the primary and note in the secondary's header.
7. Append a `wiki/log.md` entry.

A good synthesis tells you what the field looks like when seen as a whole. A
bad one just enumerates pages — if you find yourself listing without
distilling, stop and revisit step 2.
