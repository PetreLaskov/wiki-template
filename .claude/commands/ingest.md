---
description: Ingest raw source(s) — propagate the model delta, then write the ledger
argument-hint: [path or description; empty = all new sources in raw/]
---

Run the **ingest** mode for: $ARGUMENTS

If no argument: list files in `raw/` (excluding `raw/assets/`) without a source page;
if >5, switch to the batch protocol (`wiki/_operations.md` § 3) and maintain
`wiki/_state.md`.

If `wiki/index.md` has no `## Charter`, run charter mode first — do not compile blind.

Procedure (canonical: `AGENTS.md` § Ingest; extended: `wiki/_operations.md` § 2):

1. Read the source fully. Locate it: genre, date, reliability tier per the charter.
2. Extract the claims that bear on the charter's question classes; number S1…Sn.
3. **Delta first** — for each claim, update its owner page:
   - existing owner → integrate, cite `[[This Source]] S#`;
   - contradiction → both sides `confidence: contested`, linked, `question` page if live;
   - load-bearing claim with no owner → new seed (thesis, `load_when`, ≥1 key point,
     ≥1 link);
   - peripheral claim → stays housed in the source page only.
4. Write the source page as a **ledger** (`wiki/_templates.md` § source): Snapshot,
   Reliability (usable-for / not-usable-for), Key Claims → owners, Model Delta, Audit.
   **Novelty budget**: if the delta is "confirms existing pages", the page is ~150-300
   words — spend the saved effort on owner pages, not on a parallel summary.
5. Update Related (bidirectional), `wiki/index.md` (domain entry, Load Next By Task if
   a new routing need appeared, Recent Activity), and append one `wiki/log.md` entry
   (one entry per batch wave, not per file).

If the source raises a question it doesn't answer, file a `question` page rather than
inventing an answer. If a source page already exists and content has drifted
(`src_bytes` mismatch), treat as re-ingest and mark the log entry accordingly.
