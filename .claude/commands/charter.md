---
description: Establish or revise the wiki's charter (its optimization target)
argument-hint: [optional: what changed, or guidance on scope]
---

Run the **charter** mode. Context from user: $ARGUMENTS

The charter lives as `## Charter` in `wiki/index.md`. Procedure
(extended: `wiki/_operations.md` § 1):

1. Read the sources in `raw/` (openings suffice for large corpora) — the charter
   describes what the sources collectively imply, not intent alone.
2. Draft the five parts (`AGENTS.md` § Charter):
   - what this wiki compiles and its through-line;
   - the 3-7 **question classes** a future agent must answer well from it — concrete
     enough to test routing against;
   - source posture: reliability tiers, whose frame dominates;
   - page economics: what deserves a page here, what does not;
   - what NOT to treat the wiki as.
3. Ask the user one focused exchange: "does this match what you want the wiki to be
   able to do?" Sharpen from the answer.
4. If revising an existing charter, reconcile the State of the Model with it in the
   same turn — they must not contradict.
5. Append a `charter` entry to `wiki/log.md`.

Do not ingest in the same turn. A wiki without a charter compiles blind — if asked to
ingest on an uncharted wiki, run this first.
