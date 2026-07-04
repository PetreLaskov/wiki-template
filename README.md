# Knowledge Compiler

A Karpathy-style wiki maintained by an AI agent. You provide raw sources. The agent
compiles them into an interlinked model of the domain: pages whose frontmatter surfaces
a thesis and a routing trigger, bodies that follow a compression gradient, claims that
trace to numbered anchors in their sources, and hubs that route a future agent to
exactly the pages a task needs.

It works for: research fields tracked over time, a thinker's corpus, internal knowledge
that accumulates across documents, long investigations, technical domains where
understanding builds. It does not work for tiny note collections, real-time data, code
references, or anything that doesn't benefit from interconnection. See
[When this approach is wrong](#when-this-approach-is-wrong).

This document is the operator's manual. The agent's contract is `AGENTS.md`; the
extended manual is `wiki/_operations.md`. Read this first.

---

## The abstraction

The agent is a **compiler**. The mapping is wholesale from software:

| In this repo | Software analog |
|---|---|
| `raw/` | source code (immutable input) |
| `wiki/` | build artifact (regenerable output) |
| the agent | compiler |
| `AGENTS.md` | language spec |
| the charter (in `wiki/index.md`) | build target |
| `tools/lint.py` | static analysis |
| `review` | garbage collection + optimization pass |
| `wiki/log.md` | build log (rotated) |
| `wiki/index.md` | symbol table + linker map |
| `wiki/_state.md` | incremental build state |

Every wiki page is the agent's current best compilation of its sources. If a source
changes, the page can be re-compiled. If the wiki feels off, the fix is usually
upstream (sharper charter, sharper source, sharper request) — not hand-editing output.

The one number that matters: a future agent reasoning from this wiki must beat an agent
given only `raw/` and grep — better answers, fewer tokens. Everything below exists to
win that comparison.

---

## The load-bearing pieces

### Charter

The `## Charter` section of `wiki/index.md`: what the wiki compiles, the **question
classes** a future agent must answer well from it, how sources are to be trusted, and
what deserves a page. It is the wiki's optimization target — page economics, routing,
and synthesis priorities all trace back to it. The observed failure mode without one:
the wiki drifts into a pile of per-file summaries that no future task ever loads.
`/charter` drafts it from your first sources plus one question to you.

### Thesis and load_when

Every page carries two compressed sentences in frontmatter:

```yaml
thesis: "The claim this page stands for — its information-theoretic limit."
load_when: "The task shapes for which a future agent should load this page."
```

Thesis is what the page says; `load_when` is when it's worth reading. If you can't
write the thesis, the topic isn't sharp enough to earn a page. If you can't write
`load_when`, nobody will ever load it — question why it exists.

### Compression gradient

Density matches access pattern: frontmatter (max compression) → opening (1-2 sentences)
→ Key Points (~80% of value, scannable) → body (full depth) → Related (one-liners).
The same gradient governs the whole wiki: State of the Model (≤300 words) → index
routing table → hubs → pages → source ledgers → raw files. Growth is absorbed at the
bottom of the pyramid; the top stays fixed-size so a session's first read never grows.

### Ownership, hubs, claim anchors

- **One claim, one home.** Every claim has exactly one owner page; everything else
  cites or routes to it. Redundancy is how wikis rot.
- **Hubs** route clusters: a Decision Map table (task → child page → guardrail) plus
  Related entries naming what each child owns. Concepts that swell get hub-extracted,
  not longer.
- **Claim anchors**: source pages number their claims (`**S1**`, `**S2**`…); derived
  pages cite `([[Source Page]] S3)`. Any claim in the wiki is auditable to its exact
  spot in the evidence without re-reading raw files.

### Delta-first ingest

The unit of ingest is the **model delta**, not the source summary. The agent updates
the owner pages first — that's where compounding happens — then writes the source page
as a short provenance ledger: snapshot, reliability (usable-for / not-usable-for),
numbered claims with owner pointers, and the Model Delta. Ledger length scales with
novelty: a source that only confirms existing pages gets ~200 words, and the effort
goes into the pages it confirmed. A wiki that is 80% source summaries is compiling
nothing; the derived layer (concepts, theses, syntheses, questions) is the product.

### Mechanical verification

`python tools/lint.py` (Windows: `tools\lint.cmd`) checks everything checkable —
frontmatter vocabulary, link and anchor resolution, raw↔source coverage, index
registration, encoding corruption, staleness, oversized pages, domain swelling — and
prints a disposal queue for review. The agent's context is spent on judgment (are
theses claims? is confidence calibrated?), never on counting. Run it whenever you're
curious; it changes nothing.

### Seven types, two statuses

`source`, `entity`, `concept`, `thesis`, `synthesis`, `analysis`, `question` — each a
different epistemic move; `thesis`/`analysis`/`question` are cheap and should be
plentiful (a wiki that never argues and never asks is a filing cabinet). Status is just
`seed` (placeholder, a commitment) or `live` (built, safe to build on); epistemic
weight lives in `confidence`, including `contested` for live disagreements — which are
information, never smoothed away.

---

## How to use it well

### First moves

1. **Drop 2-3 sources in `raw/`. Run `/charter`.** Answer its one question. This is
   the highest-leverage minute you'll spend on the wiki.
2. **Run `/ingest`.** Read what changed — not just the new source page; look at the
   concept pages it touched.
3. **If a page is wrong, fix upstream**: better source, sharper charter, re-ingest.
   Hand-editing is fine too (it's just markdown) — bump `updated:`, run `/lint`.
4. **Repeat. Watch domains emerge from content**, not intent.
5. **At ~5 sources on one theme, ask for a synthesis.** Early synthesis forces the
   through-line question: is there a there there?

### Patterns that pay off

- **Interrogate it.** `/query` is not just retrieval — every real question either
  proves the routing works or files the gap as a `question` page. A wiki that is only
  written to, never asked, compounds nothing.
- **Review on cadence** (~25 ingests, or after any batch phase). Review is where seeds
  get developed or demoted, synthesis debt gets paid, and the State of the Model gets
  rewritten. Skip it and the wiki silts up.
- **Chase cross-domain links and theses.** The most valuable artifacts are a thesis in
  one domain resting on evidence in another. If months of ingests produce zero thesis
  pages, say so to the agent — that's a compilation failure, not a style choice.
- **Batch with state.** For big corpora, let the agent maintain `wiki/_state.md`
  (queue, waves, resume point) and gate each wave with lint. Order sources
  foundational-first so later ones integrate instead of duplicating.
- **Read the State of the Model occasionally.** It's the wiki's compiled binary. If it
  reads stale or wrong, that's the first thing to fix — everything routes from it.

### Antipatterns

- **Topic-label theses.** "Things about X" is not a claim.
- **Source-page essays.** A long summary whose Model Delta says "no material change"
  is effort spent on the wrong layer. The ledger should be short; the owners rich.
- **Trusting `live` + high importance without lint.** The script exists because
  self-reported maturity drifts.
- **Letting the log or index grow unboundedly.** Rotation and catalog extraction are
  in the contract; if first reads feel long, demand them.
- **Mixing modes in one turn.** Ingest, review, refactor are different cognitive
  operations; one per turn.

---

## When this approach is wrong

The system pays off when the same domain gets revisited, accumulates evidence over
months, and benefits from being interrogable later. If that's not your situation,
don't use it. Specifically wrong for: tiny knowledge bases (<10 sources), real-time or
volatile data, code documentation, highly structured records, single-shot
summarization. If unsure, try five sources and decide; bailing costs one `rm -rf wiki/`.

---

## Files

| Path | Purpose |
|---|---|
| `AGENTS.md` | Canonical agent contract. The spec. |
| `CLAUDE.md` | Thin adapter pointing Claude Code at `AGENTS.md`. |
| `README.md` | This file. |
| `wiki/index.md` | Charter + State of the Model + router. First read, every session. |
| `wiki/log.md` | Append-only event log, newest first, rotated at review. |
| `wiki/_operations.md` | Extended playbooks: charter, ingest, batch, query, review, refactor, scaling. |
| `wiki/_templates.md` | Per-type page scaffolds. |
| `wiki/_state.md` | Batch ingestion state (created when needed). |
| `wiki/_catalog.md` | Exhaustive page register (created past ~150 pages). |
| `tools/lint.py` | Mechanical invariant checker + diagnostics. Stdlib only. |
| `raw/` | Your sources. Immutable. |
| `raw/assets/` | Images, PDFs, attachments. |
| `.claude/commands/` | Slash commands for Claude Code (optional convenience). |

System files inside `wiki/` are prefixed `_` and excluded from the index and lint
counts. The wiki itself stays flat — content pages are siblings.

---

## Working with the agent

**Modes** (slash commands in Claude Code; plain verbs with any agent):
`charter`, `ingest`, `query`, `synthesize`, `lint`, `review`, `refactor`.
One mode per turn. English works too — the modes are the API; English is the wrapper.

**In a session**, the agent reads the index (charter, model, routing) and the newest
~10 log entries, then routes. It does not read the wiki linearly, and its first-read
budget stays fixed no matter how large the wiki grows.

**Multi-agent compatibility:** any agent following `AGENTS.md`/`CLAUDE.md` conventions
operates this wiki identically. Switch between Claude Code, Codex, and Cursor freely;
the contract does not assume Claude.

**Editing by hand:** it's markdown. Keep frontmatter intact, bump `updated:`, run
`/lint` after deletes or renames. Open the repo in [Obsidian](https://obsidian.md) for
graph view and backlinks — no dependency, any editor works.

**Version control:** the repo is a git repo. Committing after sessions gives you
time-travel over the model's evolution and makes refactors fearless. Recommended, not
required.

---

## Suggested cadence

- **Per ingest:** drop source, `/ingest`, glance at the touched owner pages.
- **Per batch wave (5-10 sources):** agent updates hubs, runs lint, one log entry.
- **Every ~25 ingests or after each batch phase:** `/review` — diagnostics disposed,
  synthesis debt paid, State of the Model rewritten.
- **Anytime:** `/query`. It's the point of the whole thing, and it stress-tests
  routing for free.
- **Before sharing or archiving:** `/lint`.

---

## License

The template is a starting point. The wiki you build on it is yours.
