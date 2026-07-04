---
description: Answer a question from the wiki, with anchored citations; leave a trace
argument-hint: <question>
---

Run the **query** mode to answer: $ARGUMENTS

Procedure (canonical: `AGENTS.md` § Query; extended: `wiki/_operations.md` § 4):

1. Route: `wiki/index.md` → Load Next By Task → hub → owner pages. Read highest
   `importance` first. Budget: answer from ≤ ~5 pages; descend to `raw/` only when the
   pages don't carry the load.
2. Synthesize the answer with **claim-anchor citations** (`[[Source Page]] S#`), explicit
   confidence, and what the wiki does *not* know that bears on the answer. A claim that
   can't be traced is marked `(unsupported)` or omitted.
3. **Leave a trace**:
   - recurring question, or assembly took >3 page reads → file as `analysis`
     (`thesis` if argued, `synthesis` if a survey);
   - unanswerable from current sources → file a `question` page — always;
   - trivial lookup → no page, but note any routing failure for the next review.
4. Append a `wiki/log.md` entry.

Surface the answer in conversation, then say what (if anything) was filed.
