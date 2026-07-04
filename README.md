# Knowledge Compiler

A Karpathy-style wiki maintained by an AI agent. You provide raw sources. The
agent compiles them into interlinked pages with stable structure: frontmatter
that surfaces a thesis, a status, and a confidence level; bodies that follow a
compression gradient; a graph of cross-domain links that turns the whole into
a navigable knowledge system.

It works for: research fields tracked over time, internal company knowledge
that accumulates across documents, long investigations, technical domains
where understanding builds. It does not work for tiny note collections,
real-time data, code references, or anything that doesn't benefit from
interconnection. See [When this approach is wrong](#when-this-approach-is-wrong).

This document is the operator's manual — the abstraction the system rests on,
the load-bearing pieces, how to use it well, and where it fails. The agent's
contract is in `AGENTS.md`. The extended manual is `wiki/_operations.md`.
Read this first.

---

## The abstraction

The agent is a **compiler**. The mapping is wholesale from software:

| In this repo | Software analog |
|---|---|
| `raw/` | source code (immutable input) |
| `wiki/` | build artifact (regenerable output) |
| the agent | compiler |
| `AGENTS.md` | language spec |
| `wiki/_operations.md` | user manual |
| `lint`, `review` | static analysis, garbage collection |
| `refactor` | refactor |
| `wiki/log.md` | build log |
| `wiki/index.md` | symbol table |

Every wiki page is the agent's current best compilation of its sources. If a
source changes, the page can be re-compiled. If the wiki feels off, the fix is
usually upstream (sharper source, sharper request) — not hand-editing the
output.

If that mapping makes sense to you, the rest of this document will feel
familiar. If it doesn't, this system probably won't fit how you work.

---

## The load-bearing pieces

### Thesis

Every page has a `thesis:` in frontmatter — a single sentence that compresses
the page to its information-theoretic limit. Not a topic label. A claim.

```yaml
thesis: "Compression gradient: pages should be densest where first read,
expanded where the reader chooses to dwell."
```

The thesis is the load-bearing field. Every other field qualifies it. The body
elaborates it. The link graph is built from it — the agent decides whether to
link to a page largely by reading its thesis.

If you can't write a thesis, the page should not exist yet. The topic isn't
sharp enough to earn a page.

### Compression gradient

Information density should match access pattern. Frontmatter is read more
often than the opening, the opening more than key points, key points more
than the body. The page's structure mirrors that:

1. **Frontmatter** — max compression. Decision surface.
2. **Opening** — 1-2 sentences. Context.
3. **Key Points** — bullets. Scannable. Carries ~80% of value.
4. **Body** — full elaboration for the reader who chose to dwell.
5. **Related** — one-line cross-links at the close.

This is not a stylistic preference. It's how a page should behave under skim.

### Three orthogonal axes

- **Links** — relational. Page-to-page edges in the graph.
- **Domains** — topical. Organize the index.
- **Tags** — analytical. Cross-cutting facets (methodology, epistemic type,
  whatever sliceable dimension you care about).

Collapse them and you get either a folder hierarchy (domain swallows
everything) or a tag soup (tags swallow everything). Both fail at scale.

The wiki's most valuable graph property is the **cross-domain link** — a
thesis in one domain pointing at evidence or argument in another. These edges
turn a pile of pages into a knowledge system. Look for them. The agent
surfaces them; encourage them.

### Seven types

Each type is a different epistemic move:

| Type | Move |
|---|---|
| `source` | faithful summary of a raw file |
| `entity` | a real-world thing, aggregated across sources |
| `concept` | an abstraction or principle, defined and bounded |
| `thesis` | an argued position with evidence |
| `synthesis` | a map of a domain or topic |
| `analysis` | a crystallized answer to a recurring question |
| `question` | a tracked open frontier |

The types make the wiki's epistemics legible at a glance: which pages are
summaries, which are arguments, which are maps, which are open. Don't invent
new types until the existing seven actually fail to carry the meaning.

### Six modes

Verbs the agent recognizes. In Claude Code these are slash commands; with any
other agent, just say the verb in plain English.

| Mode | What it does |
|---|---|
| `/ingest` | raw source → wiki integration (build) |
| `/query` | answer a question from the wiki, file the answer if reusable |
| `/synthesize` | extract a synthesis or thesis from existing pages |
| `/lint` | verify invariants, surface violations |
| `/review` | periodic consolidation: orphans, stubs, link rot, tag hygiene |
| `/refactor` | split, merge, rename, move pages |

One mode per turn. Mixing them means none of them gets done well.

---

## How to use it well

### First moves

1. **Don't customize before you have content.** The schema works for arbitrary
   topics. The shape of your wiki is a fact about your sources, not a decision
   you make in advance.
2. **Drop a source in `raw/`. Run `/ingest`.** Read the result.
3. **If the page is wrong, the source is usually wrong.** Fix it upstream
   (better PDF, cleaner transcript, a more focused excerpt) or re-ingest with
   a sharper question.
4. **Repeat with three or four more sources.** Watch domains emerge naturally.
   Don't force them.
5. **At ~5 sources, rewrite `wiki/index.md`'s shape paragraph from actual
   content.** Not from intent. The wiki's thesis is whatever the sources
   collectively imply.

### Patterns that pay off

- **Trust the compilation.** If a page reads wrong, the upstream is the lever
  in 80% of cases. Hand-editing is the lever in 20%. Both are fine; know
  which you're doing.
- **Treat questions as first-class.** A long list of well-formed open
  questions is more valuable than a long list of mediocre answers. Use
  `type: question` aggressively. The agent surfaces them in the index.
- **Run reviews.** Cadence: every ~25 ingests, or whenever the wiki feels
  off. Wikis decay without consolidation. Orphans accumulate, tags drift,
  shape paragraphs go stale. `/review` catches all of it.
- **Chase cross-domain links.** When a thesis in one domain bears on
  something in another, ask the agent to wire it. These are the edges that
  separate a knowledge system from a folder of notes.
- **Synthesize on threshold.** When a domain reaches ~5 substantive pages,
  ask for a synthesis. Don't wait for it to feel "ready" — synthesizing
  early forces you to see whether the through-line exists.
- **Keep the shape paragraph honest.** It's the wiki's elevator pitch. If
  it stopped being true, rewrite it during your next review.
- **Edit by hand when needed.** It's just markdown. Update `updated:`
  to today. Run `/lint` after.

### Antipatterns

- **Topic-label theses.** "Things about X" is not a thesis. Either name a
  claim or skip the page.
- **Tagging freely.** Tag singletons proliferate, signal degrades. Wait for
  tags to earn placement across multiple pages.
- **High-importance stubs that linger.** A seed with `importance: 8` after 25
  ingests means you're claiming something is important and not developing
  it. Pick: develop or downgrade `importance`.
- **Smoothing contradictions.** When sources disagree, mark both pages
  `confidence: contested` and link them. Disagreement is information, not a
  defect to paper over.
- **Doing ingest + review + refactor in one turn.** Each is a different
  cognitive operation. Mixing them produces sloppy work.
- **Treating the wiki as a folder hierarchy.** It is flat by design.
  Reach for nesting only when scaling forces it (`wiki/_operations.md`
  § Index scaling).
- **Believing `mature` without checking.** A page can claim maturity and have no
  inbound links and a `sources: []` list. The agent is supposed to catch
  this in `/review`; you're supposed to act on it.

---

## When this approach is wrong

The system pays off when the same domain gets revisited, accumulates evidence
over months, and benefits from being interrogable later. If that's not your
situation, don't use it.

Specifically wrong for:

- **Tiny knowledge bases (<10 sources).** A flat folder of notes is fine.
  The schema overhead doesn't earn its keep until you have enough pages
  that structure starts pulling weight.
- **Real-time or volatile data.** This is a slow medium. The compilation
  cycle is a session, not a millisecond. Use a database or a feed reader.
- **Code documentation.** Codebases have their own conventions (READMEs,
  docstrings, ADRs). This is for human-language knowledge.
- **Highly structured data.** Use a database. Markdown is for reasoning,
  not records.
- **Single-shot summarization.** If you ingest and never come back, the
  schema overhead isn't earning anything.

If you're not sure, try it on five sources and decide. The cost of bailing
is one `rm -rf` of `wiki/`.

---

## Files

| Path | Purpose |
|---|---|
| `AGENTS.md` | Canonical agent contract. The spec. |
| `CLAUDE.md` | Thin adapter that points Claude Code at `AGENTS.md`. |
| `README.md` | This file. |
| `wiki/index.md` | Routing table. Agent reads first every session. |
| `wiki/log.md` | Append-only event log, newest at top. |
| `wiki/_operations.md` | Extended manual: playbooks, lifecycles, style, quality, scaling, conventions. |
| `wiki/_templates.md` | Per-type page scaffolds. |
| `raw/` | Your sources. Immutable. |
| `raw/assets/` | Images, PDFs, attachments referenced by raw sources. |
| `.claude/commands/` | Slash commands for Claude Code (optional convenience). |

System files inside `wiki/` are prefixed `_` and excluded from the index and
lint counts. The wiki itself stays flat — content pages are siblings.

---

## Working with the agent

The contract is in `AGENTS.md`. Read it once. The agent reads it every session.

**In a session,** the agent reads `wiki/index.md` first, then `wiki/log.md`
for recent context. It pulls `wiki/_operations.md` and `wiki/_templates.md`
on demand — when a workflow or a page-type creation is in scope.

**Driving:** name a mode, or describe a task in English. If a request is
ambiguous, the agent will name the mode it would run and ask one focused
question. Answer it. If the request is clear, it does the work and reports.

**Multi-agent compatibility:** any agent that follows the standard
`CLAUDE.md` or `AGENTS.md` conventions operates this wiki the same way.
Identical content. The contract does not assume Claude. If you switch
between Claude Code, Codex, and Cursor against the same repo, the wiki
stays coherent.

**Editing by hand:** It's markdown. Conventions to honor:
- Keep frontmatter intact.
- Bump `updated:` to today on content changes.
- Run `/lint` after deletes or renames.
- A page you create by hand will be integrated by the next `/ingest` or
  `/review`.

Open the repo in [Obsidian](https://obsidian.md) for graph navigation,
backlinks, and full-text search. There's no Obsidian dependency — any
markdown editor works.

---

## Suggested cadence

A workable rhythm, not a prescription:

- **Per ingest:** drop source, `/ingest`, glance at result, sharpen if needed.
- **Every ~25 ingests (or weekly-ish):** `/review`. Investigate diagnostics.
  Resolve cleanly.
- **As theses accumulate:** `/synthesize <domain>` to extract maps.
- **When something stops fitting its page:** `/refactor <target>`.
- **Before sharing or archiving:** `/lint`.

You can ignore all of this and just say what you want in plain English. The
modes are the API; English is the wrapper.

---

## License

The template is a starting point. The wiki you build on it is yours.
