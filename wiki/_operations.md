# Operations

Extended playbooks for the Knowledge Compiler. Read on demand — `AGENTS.md` is
the contract; this file is the manual. Sections are independent; jump in.

Contents:
1. Ingest (extended)
2. Query (extended)
3. Synthesize
4. Review
5. Refactor — split, merge, move, rename
6. Lifecycles — questions, contradictions, stubs
7. Style — voice, rhythm, anti-patterns
8. Quality heuristics — what makes a page good
9. Index scaling — stages by wiki size
10. Working with the user
11. Conventions — filenames, dates, assets, citations

---

## 1. Ingest (extended)

### Single source

1. Read the raw file fully. Note structure, density, source quality, biases.
2. Identify key claims and the entities / concepts they touch.
3. Decide page allocation:
   - One source page (always — 1:1 with raw file).
   - Plus updates to existing entity / concept pages.
   - Plus new entity / concept pages where warranted (start as seed).
4. Draft the source page from `_templates.md` § source.
5. For each touched entity / concept page:
   - **Existing**: integrate the new claim into the body. If the claim contradicts
     an existing one, both pages get `confidence: contested` and a Related link.
   - **New**: stub with frontmatter, opening, ≥1 key point, sources list.
6. Update Related sections of all touched pages — links go both ways.
7. Update `index.md`: add new pages under their domain, refresh shape paragraph if
   the wiki's scope has shifted, prepend a Recent Activity entry.
8. Append a single `log.md` entry summarizing the ingest.

### Batch ingest

Same procedure per source. Group all touched pages into one log entry per session.
Defer minor cleanup (tag normalization, prose polish) to the next `review`.

### Re-ingest

Triggered when a `raw/` file's mtime advances past its source page's `updated:`.

1. Diff the new source content against the existing source page.
2. Update the source page from the new content.
3. Propagate deltas into entity / concept / thesis pages that draw on it.
4. Where new claims contradict existing pages, mark both `confidence: contested`.
5. Bump `updated:` on every touched page.
6. Log as `ingest` with `(re-ingest)` tag in the subject.

### Asset handling

- Images and PDFs live in `raw/assets/`.
- Reference from a wiki page using `![alt](../raw/assets/file.ext)` for inline
  images, or `[[../raw/assets/file.pdf]]` for documents.
- If an asset is essential to interpreting a source, mention it in the source
  page's Key Claims.

---

## 2. Query (extended)

### Scope detection

The shape of the question dictates the shape of the answer (and where it gets filed):

- **Definitional** ("What is X?") → entity or concept lookup; no new page unless
  the query itself reveals a gap.
- **Comparative** ("X vs Y?") → file as `analysis`.
- **Open survey** ("What do we know about Y?") → file as `synthesis`.
- **Predictive / argued** ("Should we believe Z?") → file as `thesis`.
- **Unanswerable from current sources** → file as `question`.

### Citation discipline

Every load-bearing claim in an answer must trace to a wiki page (and from there to
a `raw/` file), or be marked `(unsupported)`. If you can't trace it, you can't
claim it. Speculation is fine when labelled.

### Filing the answer

If the answer is reusable — likely to be asked again, or sets up future questions —
file it as a wiki page. The conversational answer points to it. Subsequent queries
hit the page first.

---

## 3. Synthesize

When to synthesize:

- A domain has accumulated ≥5 substantive pages without a `synthesis`.
- A query keeps recurring; the answer is now reusable.
- A `thesis` crystallizes from accumulating evidence — the moment the through-line
  becomes visible.
- A `review` surfaces a domain whose pages are well-formed individually but lack a
  map.

Procedure:

1. Pull all relevant pages (filter index by domain or tag).
2. Distill the through-line — the single argument or pattern that organizes them.
3. Write the synthesis page: thesis frontmatter, opening (1 paragraph, the
   landscape), Key Points (sub-areas with their representative pages), Body
   (the through-line argued in full), Open frontiers (questions the synthesis
   surfaces).
4. Update each touched page with a Related entry pointing to the new synthesis.
5. Index it under its primary domain. If it covers two domains, list under primary
   only and note in the secondary domain header.

A good synthesis tells you what the field looks like when seen as a whole. A bad
synthesis just enumerates the pages.

---

## 4. Review

Periodic consolidation. Cadence: every ~25 ingests, or on user request, or
whenever the wiki "feels off" (a perfectly legitimate trigger).

Checklist (work the diagnostics from AGENTS.md § Lint):

1. **Orphans.** List pages with no inbound links. For each: link if relevant,
   archive if obsolete (`status: evergreen` plus a note), merge if redundant, or accept
   isolation if genuinely standalone (rare).
2. **High-importance stubs.** `importance ≥ 7 ∧ status = seed`. Either promote to
   working by adding key points and ≥1 cross-link, or downgrade importance.
3. **Tag hygiene.** Tally tag frequencies. Collapse near-synonyms. Retire
   singletons that don't pull weight. If a tag appears on >40% of pages, it's
   probably a domain in disguise — promote it.
4. **Broken links.** `[[X]]` where X has no page or alias. Either create a stub or
   remove the link (don't leave broken).
5. **Domain swelling.** Any domain with >30 pages: extract a synthesis if missing,
   then evaluate sub-index extraction (see § 9 Index scaling).
6. **Stale pages.** `updated:` >90 days for pages touched by recent ingests
   (contradicted, deprecated, or in need of review).
7. **Contested-claim audit.** Pages with `confidence: contested` — verify the
   disagreement is still live and both sides remain represented.
8. **Question backlog.** `type: question` pages older than 30 days — promote to
   `analysis`/`thesis` if resolvable, retire if no longer interesting, or
   re-frame.
9. **Index sanity.** Every wiki page (excl. `_*.md`) appears under exactly one
   domain header. Recent Activity entries match log.
10. **Shape paragraph drift.** Re-read `index.md`'s shape paragraph. Is it still
    true? If the wiki has grown into a different shape, rewrite the paragraph.

Log a single `review` entry. List counts (e.g. "5 orphans linked, 2 stubs
promoted, 1 tag retired, shape paragraph rewritten").

---

## 5. Refactor

Three operations. Always log with old → new mapping.

### Split

Trigger: a page conflates two distinct concepts, or grows past ~600 words with
internal seams visible.

1. Identify the seam. Each side should have its own thesis.
2. Create the new page (or both new pages, if the original becomes a redirect).
3. Move content over; tighten each side.
4. The original either stays as a synthesis (if both halves are still related) or
   gets deleted.
5. Update all inbound links to point to the right side.
6. Update `index.md`.

### Merge

Trigger: two pages on the same concept (commonly a stub + a richer page, or two
parallel pages from different ingests).

1. Choose the canonical title — the one that reads most naturally as `[[X]]` and
   covers the broader scope.
2. Merge bodies. Deduplicate. Resolve any conflicts in framing.
3. Add the loser's title to the winner's `aliases:`.
4. Update all inbound links (or rely on the alias for backward compatibility, but
   prefer to fix the links so the graph is clean).
5. Delete the loser. Update `index.md`.

### Move / Rename

Trigger: domain reorganization, or a page's name no longer fits its content.

1. Rename the file. Filenames are titles in this system.
2. Add the old title to `aliases:` for transition.
3. Update all inbound links to the new name.
4. Update `index.md` (placement may change with rename).
5. After ~30 days of stable links, the alias can be retired in a future review.

---

## 6. Lifecycles

### Questions

A `type: question` page is born when a query reveals a gap, or when an ingest
raises a question the source doesn't answer.

States:
- **Open** (seed): the question stands.
- **Partial** (working): some pages bear on it, but no resolution.
- **Resolved** (evergreen): a `thesis` or `analysis` has answered it. The question page
  links to its resolution and remains as a permanent record of the inquiry.

Closed-but-not-deleted is the right move — the question's existence is itself
information about the wiki's history.

### Contradictions

When sources disagree, mark both pages `confidence: contested`. Add Related
links between them. Both representations stand. The contestation often itself
becomes a `thesis` (arguing one side) or a `question` (acknowledging the
unresolved disagreement). Don't smooth contradictions away — they are the
honest state of evidence.

### Stubs

seed stubs are commitments to future content, not failures. A stub with thesis +
≥1 key point + ≥1 link is doing useful work. A stub that lingers at seed with
`importance ≥ 7` for >25 ingests is a red flag — promote or demote during the
next review.

### Theses

A `thesis` page is a position. It must be defensible. It must list what would
change your mind (the page template includes this section). When a thesis is
overturned by new evidence, don't delete it — restate it, lower its confidence,
add the counter-evidence to its body, and (often) spawn a new thesis page for
the revised position. The history of arguments is part of the wiki's value.

---

## 7. Style

The wiki should read like one careful mind. Conventions:

- **Voice**: declarative, precise, unhedged when evidence is strong, hedged
  proportionally to confidence. Avoid hype, avoid throat-clearing.
- **Sentence rhythm**: short topic sentences, longer evidence sentences. Vary.
- **No "this article will…"**: pages don't refer to themselves as articles.
- **No "in conclusion"**: the closing should be content, not meta.
- **Use `[[links]]` inline**: don't ghettoize them in a "see also" footer.
  Related is for highest-value cross-domain edges only.
- **Numbers and names** trace to a source — inline citation or `sources:`
  frontmatter.
- **Compression discipline**: every sentence does work. Cut throat-clearing,
  signposting, hedges that don't carry uncertainty information.
- **Active voice when the actor matters**, passive when it doesn't.
- **British or American spelling — pick one and hold to it.**

The Knowledge Compiler's voice is the wiki's voice. Keep it consistent across
sessions — if you find yourself writing in a different register, look at recent
pages and match.

---

## 8. Quality heuristics

A page is **good** when:

- **Thesis predicts content.** A reader could reconstruct the page's shape from
  its thesis frontmatter alone.
- **Compression gradient holds.** Tight at frontmatter, dense in key points,
  full in body. Each layer earns its expansion.
- **≥1 cross-domain link.** The page is connected to the rest of the wiki, not
  isolated in its own silo. (Pure singletons survive only with strong
  justification.)
- **Citations trace.** Every load-bearing claim is sourced.
- **Status reflects reality.** A stub feels like a stub; a mature page feels
  mature; an evergreen feels settled.
- **Confidence is calibrated.** The label matches the actual evidence cited.

A page is **weak** when (anti-patterns):

- Thesis is a topic label ("Things about X"), not a claim.
- Key Points repeat the body in compressed form (redundant — they should *be*
  the page's spine, not a summary of it).
- Body buries the thesis under throat-clearing.
- All links stay within one domain (siloed).
- `confidence:` doesn't match the evidence on the page.
- `mature` status with `sources: []` and no inbound links (claimed maturity, no
  roots).
- Fields are filled in mechanically — `tags: [topic]` where topic just
  duplicates the domain.

If a page review yields more weak markers than good ones, it's a refactor
candidate.

---

## 9. Index scaling

The index.md must remain skim-readable as the wiki grows. Stages by total wiki
page count:

- **<50 pages.** Flat domain list. Recent Activity capped at 5-10. No
  abstracts.
- **50-200 pages.** Domain headers gain a 1-sentence abstract. Recent Activity
  capped at 10. Open Questions surfaced (top 5).
- **200-500 pages.** Each domain has an extracted `synthesis` page that maps it.
  Index header lists the synthesis. The synthesis lists the pages. Index
  becomes a navigation surface, not a content listing.
- **500-1500 pages.** Per-domain index files: `index-{domain}.md`. Main `index.md`
  lists domain syntheses, Recent Activity, Open Questions, and a one-line
  pointer to each `index-{domain}.md`.
- **>1500 pages.** Same as above plus tag-based and time-based pivot views as
  separate `_index-by-tag.md`, `_index-recent.md` files. The main `index.md`
  stays the central routing surface.

Always preserve, at every scale: shape paragraph, Recent Activity, Open
Questions.

---

## 10. Working with the user

**Ambiguity protocol.** If the user's request could mean two reasonable things,
name the mode you'd run and ask one focused question. Don't ask three. Don't
silently pick the wrong interpretation.

**Batch protocol.** If the user is unavailable (autonomous batch), default to
conservative choices:

- Prefer updating existing pages over creating new ones.
- Prefer seed stubs over speculative elaboration.
- Prefer logging open questions over inventing answers.
- Defer refactors that affect >5 pages until a user is available.

**Surfacing state.** If the wiki is in a state that contradicts the user's
request — they asked to ingest a source whose source page already exists, or
they asked about a domain that doesn't exist — surface that *before* proceeding,
in one sentence.

**Scope discipline.** Do exactly what was asked. Don't pile on adjacent work
("I noticed three other things to fix…") — log those for the next review
instead.

---

## 11. Conventions

**Filenames.** Title Case With Spaces, `.md` extension. `Knowledge Compiler.md`
not `knowledge-compiler.md`. The filename is the link target (`[[Knowledge
Compiler]]`). Aliases handle alternate phrasings.

**Dates.** ISO 8601, `YYYY-MM-DD`. Set `updated:` on every meaningful revision
(content change, not whitespace).

**Lists in frontmatter.** YAML inline form: `domain: [primary, secondary]`,
`tags: [tag-1, tag-2]`. Keep lists short — if `tags:` has >5 entries, you're
probably tagging too freely.

**System files.** Anything in `wiki/` named `_*.md` is a system file. Not
indexed. Not lint-counted as a wiki page. Used for templates, operations,
extracted indexes (`_index-by-tag.md` etc.).

**Citations in prose.** Use `[[Source Page]]` to refer to the source page
(not the raw file directly). The source page abstracts the raw file; that
abstraction is what other pages should depend on. Direct references to
`raw/` files only inside source pages or for asset embeds.

**Quoting.** Use blockquote (`>`) for direct quotation. Always attribute. Keep
quotations short — paraphrase + cite is usually better than a long quote.
