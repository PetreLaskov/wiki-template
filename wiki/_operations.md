# Operations

Extended playbooks for the Knowledge Compiler. Read on demand — `AGENTS.md` is the
contract; this file is the manual. Sections are independent; jump in.

Contents:
1. Charter
2. Ingest (extended)
3. Batch ingest and `_state.md`
4. Query (extended)
5. Synthesize
6. Review
7. Refactor — split, merge, rename, hub-extract
8. Lifecycles — questions, contradictions, seeds, theses
9. Style — voice, rhythm, anti-patterns
10. Quality heuristics — what makes a page good
11. Scaling — index, catalog, log
12. Working with the user
13. Conventions — filenames, dates, assets, citations

---

## 1. Charter

Run at wiki birth, or whenever scope has shifted under the existing charter's feet.
The charter lives as `## Charter` in `wiki/index.md`.

1. Read whatever sources exist in `raw/` (or their opening sections, for large corpora).
   The charter describes what the sources collectively imply, not what anyone intended.
2. Draft the five parts (`AGENTS.md` § Charter): what it compiles; the 3-7 question
   classes a future agent must answer well; source posture with reliability tiers; page
   economics; what it is NOT.
3. Ask the user **one focused exchange**: does this match what you want the wiki to be
   able to do? Sharpen from the answer.
4. Question classes should be concrete enough to test routing against. "Understand X" is
   not a question class; "given a practitioner report, recommend which technique and
   name the safety boundary" is.
5. Log as `charter`. Revising an existing charter also updates the State of the Model
   (the two must not contradict).

The charter is the wiki's optimization target. Every later economics decision — what
deserves a page, what gets a hub, what to synthesize — traces back to it.

## 2. Ingest (extended)

### Single source

1. Read the raw file fully. Note structure, genre, reliability, biases.
2. Extract the claims that bear on the charter's question classes. Number them S1…Sn.
3. **Delta first.** For each claim, find its owner page:
   - **Existing owner**: integrate the claim (cited `[[This Source]] S3`). If it
     contradicts the page, mark both sides `confidence: contested`, link them, open a
     `question` if the tension is live.
   - **No owner and the claim is load-bearing for the charter**: create a seed —
     frontmatter, thesis, `load_when`, ≥1 key point, ≥1 link.
   - **No owner and it's peripheral**: leave it housed only in the source page's claim
     list. Not every claim earns a concept.
4. Write the source page (`_templates.md` § source): Snapshot, Reliability
   (usable-for / not-usable-for), Key Claims with owner pointers, Model Delta, Audit.
5. **Novelty budget.** If the Model Delta is "confirms existing pages, changes little",
   the source page is ~150-300 words and you are done writing it. Spend the saved effort
   on the owner pages. Never produce a long parallel summary of content the model
   already holds.
6. Update Related on touched pages (bidirectional), `index.md` (domain listing, Load
   Next By Task if a new routing need appeared, Recent Activity), one `log.md` entry.

### Re-ingest

Triggered when lint flags `src_bytes` drift, or when you know the raw file changed.

1. Diff new content against the source page's claims.
2. Update the source page; propagate the delta to owner pages.
3. New contradictions → `confidence: contested` on both sides.
4. Bump `updated:` on touched pages; log as `ingest (re-ingest)`.

## 3. Batch ingest and `_state.md`

For >5 sources, improvised ingestion loses its place and its quality gates. Maintain
`wiki/_state.md`:

    # Ingestion State

    [2-4 sentences: what's being ingested, in what order, why that order.]

    ## Resume Point
    [Exactly where the next session picks up: next file(s), wave number.]

    ## Waves
    - Wave 3 (next): [files]
    - Wave 2 (done YYYY-MM-DD): [files] — gate: lint clean, hubs updated
    - Wave 1 (done YYYY-MM-DD): [files] — gate: lint clean

    ## Queue / Backlog
    [Remaining files, priority-ordered. Note exclusions and why.]

Protocol:

- Order the queue by leverage, not alphabet: foundational / definitional sources first,
  so later sources integrate into existing owners instead of creating parallel seeds.
- Work in **waves of 5-10 sources**. After each wave: update the hubs the wave touched,
  run `tools/lint.py`, fix invariant errors, one log entry for the wave.
- Every ~3 waves or ~25 sources: full `review`. Batch ingestion without periodic review
  is how a wiki silts up with unrouted source pages.
- Conservative defaults while the user is away: update existing pages over creating new;
  seeds over speculative elaboration; log questions over inventing answers; defer
  refactors touching >5 pages.
- `_state.md` is a system file: not indexed, not lint-counted, and kept **short** — it
  is a resume point, not a project diary. History belongs in the log.

## 4. Query (extended)

### Routing budget

Index → Load Next By Task → hub → owner pages. Read highest `importance` first; aim to
answer from ≤ ~5 pages. If you needed more, either the routing layer failed (note it for
review) or the question is genuinely synthetic (consider filing the answer).

### Scope detection

- **Definitional** ("What is X?") → owner-page lookup; no new page.
- **Comparative / investigative** → file as `analysis`.
- **Open survey** ("what do we know about Y?") → file as `synthesis`.
- **Argued position** ("should we believe Z?") → file as `thesis`.
- **Unanswerable from current sources** → file as `question`. Always.

### Citation discipline

Every load-bearing claim in an answer traces to a wiki page at claim-anchor level (and
through it to raw), or is marked `(unsupported)`. State confidence explicitly. Name what
the wiki does *not* know that bears on the answer — the gaps are information.

### Filing

File when the question is likely to recur, when assembly took >3 page reads, or when the
answer surfaced a gap or tension. The conversational answer then points at the page.
Trivial lookups leave no page — but a routing failure still gets a note for review.

## 5. Synthesize

When to synthesize:

- A domain has ≥5 substantive pages and no `synthesis` (review flags this as debt).
- A query keeps recurring; the answer deserves a page.
- A through-line has become visible across accumulating evidence — the moment to write
  a `thesis`.
- A domain's pages are individually fine but the territory has no map.

Procedure:

1. Pull the in-scope pages (by domain, hub, or explicit list).
2. Distill the through-line — the single argument or pattern that organizes them. If you
   can't name it in a sentence, the synthesis isn't ready; say so and stop.
3. Write from the scaffold: `synthesis` if it maps territory, `thesis` if it argues.
4. Add Related entries on covered pages (bidirectional). If the synthesis now routes the
   domain, give it a Decision Map and list it as the domain's hub in the index.
5. Log it.

A good synthesis tells you what the field looks like seen whole. A bad one enumerates
pages. If you're listing without distilling, stop and revisit step 2.

## 6. Review

Periodic consolidation. Cadence: every ~25 ingests, after each large batch phase, or
whenever the wiki feels off (a legitimate trigger).

1. **Run `tools/lint.py`.** Fix invariant errors first — they are never acceptable
   standing state. Then work the diagnostics as a **disposal queue**: every item gets an
   action or a one-line logged reason to defer. No silent skips.
   - Orphans → link from a relevant page, merge, or justify isolation.
   - `importance ≥ 7 ∧ status: seed` → develop to `live` or demote importance.
   - Broken links → create the seed or remove the link.
   - Oversized pages → hub-extract (§ 7).
   - Stale pages / `src_bytes` drift → refresh, re-ingest, or mark.
   - Domain swelling → synthesis + catalog migration (§ 11).
2. **Semantic pass** — what the script can't see. Sample recent and high-importance
   pages for: topic-label theses; `confidence` unbacked by the citations actually on the
   page; contested pairs where one side quietly vanished; Key Points that summarize the
   body instead of being its spine; hub openings and the index that have stopped being
   decision surfaces (routing bloat); register drift in voice.
3. **Synthesis debt**: domains with ≥5 substantive pages and no synthesis; concept
   clusters cited by ≥5 sources with no thesis. Write or log why not.
4. **Question backlog**: promote (an answer now exists → analysis/thesis), retire (no
   longer interesting — say why), or re-frame (the question sharpened).
5. **Rewrite the State of the Model** in `index.md`. Not "update" — rewrite from what
   the wiki now holds: through-line, strongest claims, live tensions, maturity, next
   leverage. If nothing changed since last review, either no compilation happened or the
   section wasn't honest.
6. **Rotate the log** past ~200 entries: older entries → `wiki/_log-archive-YYYY.md`,
   newest ~50 stay.
7. One `review` log entry: counts and dispositions ("5 orphans linked, 2 seeds
   developed, 1 hub extracted, model rewritten; deferred X because Y").

## 7. Refactor — split, merge, rename, hub-extract

Always log with the old → new mapping. If a refactor would touch >5 pages and the user
is away, log the intent and defer.

### Hub-extract (pocketing)

Trigger: a concept has swelled past ~2,000 words with separable concerns, or a cluster
of pages needs routing that the index shouldn't carry.

1. Identify the separable concerns. Each child gets its own thesis and `load_when` and
   **owns** its claims.
2. Create the children; move depth into them, cited at anchor level.
3. Reduce the parent to a hub: compact opening, Key Points, **Decision Map**
   (task → child → guardrail), Boundaries, Related naming what each child owns.
4. Re-point inbound links that were really about a child's content.
5. Update index (the hub becomes the domain's routing entry). Run lint.

### Split

Trigger: one page conflating two theses.

1. Find the seam; each side gets its own thesis.
2. Create pages, move content, tighten.
3. Original becomes a hub (if the halves stay related) or is deleted.
4. Re-point inbound links; update index.

### Merge

Trigger: two pages on one concept (stub + richer page, or parallel seeds from different
ingest waves — batch ingestion produces these; review catches them).

1. Choose the canonical title (reads naturally as `[[X]]`, broader scope).
2. Merge bodies; deduplicate; resolve framing conflicts; keep the strongest citations.
3. Loser's title → winner's `aliases:`. Fix inbound links anyway (clean graph beats
   alias dependence). Delete the loser; update index.

### Move / Rename

1. Rename the file (filenames are titles). Old title → `aliases:`.
2. Update inbound links and index. Retire the alias at a later review once links are
   stable.

## 8. Lifecycles

### Questions

Born when a query can't be answered or an ingest surfaces a tension no source resolves.
States: **Open** → **Partial** (some pages bear on it) → **Resolved** (a thesis/analysis
answers it; the question page links to the resolution and remains as a record). Review
disposes of the backlog every cycle: promote, retire, or re-frame.

### Contradictions

When sources disagree: both pages `confidence: contested`, linked in Related, and the
disagreement stated on both — a reader of either page must learn the other side exists.
The contestation itself often becomes a `thesis` (arguing a side) or a `question`
(mapping the disagreement). Never smooth it away; disagreement is information.

### Seeds

A seed is a commitment, not a failure: thesis + `load_when` + ≥1 key point + ≥1 link is
useful standing state. A seed with `importance ≥ 7` lingering across reviews is a red
flag — develop it or demote it. There is no maturity ladder to climb; a page is `seed`
until it's built, then it's `live`, and its epistemic weight is carried by `confidence`.

### Theses

A thesis must be defensible and must say what would change your mind. When new evidence
overturns one: don't delete — restate, lower confidence, add the counter-evidence, and
usually spawn the successor thesis. The history of arguments is part of the model.

## 9. Style

The wiki should read like one careful mind. Conventions:

- **Voice**: declarative, precise; unhedged when evidence is strong, hedged in
  proportion to actual uncertainty. No hype, no throat-clearing.
- **Compression discipline**: every sentence does work. Cut signposting and hedges that
  carry no uncertainty information.
- **No self-reference**: pages don't call themselves articles or conclude with
  "in conclusion".
- **Inline `[[links]]`**: woven into prose, not ghettoized in a footer. Related is for
  the highest-value edges only.
- **Numbers and names trace to a source** — anchor citation or `sources:`.
- **Quoting**: blockquote, attributed, short. Paraphrase + cite beats long quotes.
- **Spelling**: British or American — pick one and hold it.
- If recent pages read in a different register than old ones, match the wiki, not your
  session mood.

## 10. Quality heuristics

A page is **good** when:

- **Thesis predicts content** — a reader could reconstruct the page's shape from the
  thesis alone.
- **`load_when` names real tasks** — the page knows its own retrieval story.
- **Compression gradient holds** — tight frontmatter, dense Key Points, full body.
- **Claims are owned and anchored** — this page's claims live here and cite sources at
  anchor level; borrowed claims cite their owner page.
- **≥1 cross-domain link** — connected to the system, not siloed.
- **Confidence is calibrated** — the label matches the evidence actually cited.

A page is **weak** when:

- Thesis is a topic label ("Things about X").
- `load_when` is circular ("when the user asks about this page's topic" restated).
- Key Points re-summarize the body instead of being its spine.
- It restates claims another page owns (merge or cite instead).
- All links stay in one domain.
- A source page's Summary outweighs its Model Delta — compilation went into paraphrase
  instead of integration.
- `live` status with no inbound links and empty sources (claimed maturity, no roots).

More weak markers than good ones → refactor candidate.

## 11. Scaling — index, catalog, log

The index must stay a first-load router at every size. Two mechanisms:

- **Catalog extraction (~150+ pages).** Move exhaustive per-domain page listings to
  `wiki/_catalog.md` (the register: every page, one line each, grouped by domain). The
  index keeps: Charter, State of the Model, Load Next By Task, Open Questions, Recent
  Activity, and per-domain entries listing **hubs + the top few pages** with a pointer
  into the catalog. Every content page lives in the index or the catalog; lint checks
  the union.
- **Log rotation (~200+ entries).** Older entries → `wiki/_log-archive-YYYY.md`; newest
  ~50 stay in `log.md`. Session start reads only the newest ~10.

What must survive at any scale: the State of the Model stays ≤300 words, the Load Next
By Task table stays one screen, and a session's first-read budget (`AGENTS.md` § First
Read) stays fixed. Growth is absorbed by hubs and the catalog, never by a longer
mandatory first read.

## 12. Working with the user

**Ambiguity protocol.** If a request could mean two reasonable things, name the mode
you'd run and ask one focused question. Not three.

**Surfacing state.** If the wiki's state contradicts the request (source already
ingested, domain doesn't exist, charter missing), surface that in one sentence before
proceeding.

**Scope discipline.** Do what was asked. Adjacent problems you notice go into the log
or a question page for the next review — not into this turn's diff.

**Autonomous batch.** Follow § 3's conservative defaults; leave `_state.md` accurate
enough that any future session (or a different agent) resumes cold.

## 13. Conventions

**Filenames.** Title Case With Spaces, `.md`. The filename is the link target
(`[[Knowledge Compiler]]`); `aliases:` handles alternates. Raw files keep whatever name
they arrived with — fidelity beats tidiness in `raw/`; the source *page* gets a readable
title and records the raw path in `sources:`.

**Dates.** ISO 8601 (`YYYY-MM-DD`). Bump `updated:` on meaningful revision only.

**Frontmatter lists.** Inline YAML: `domain: [a, b]`. Keep short.

**Encoding.** UTF-8 everywhere. Windows tooling introduces mojibake (UTF-8 bytes
re-read as CP1252: A-tilde/a-circumflex chains, corrupted emoji); lint flags it — fix
at the source, don't propagate.

**System files.** `wiki/_*.md`: templates, operations, state, catalog, log archives,
shape experiments. Never content. Not indexed, not lint-counted.

**Citations in prose.** `[[Source Page]]` (with `S#` anchors), never `raw/` paths —
the source page is the abstraction other pages depend on. Direct `raw/` references
appear only inside source pages and asset embeds.

**Assets.** `raw/assets/`, referenced `![alt](../raw/assets/file.ext)`. If an asset is
essential to a source's interpretation, say so in the source page's Key Claims.
