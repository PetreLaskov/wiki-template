---
description: Answer a question from the wiki, with citations; file the answer if reusable
argument-hint: <question>
---

Run the **query** mode to answer: $ARGUMENTS

Procedure (canonical: `AGENTS.md` § Query; extended: `wiki/_operations.md` § 2):

1. Read `wiki/index.md`. Filter by domain or tag if scope is implied.
2. Scan the relevant pages' theses. Read the highest-importance pages first.
3. If the wiki's pages don't carry the load, read the relevant `raw/` files.
4. Synthesize the answer with inline `[[citations]]`. Every load-bearing claim
   must trace to a source page (and from there to a raw file). If a claim
   can't be traced, mark it `(unsupported)` or omit it.
5. **File the answer if reusable.** Detect:
   - **Definitional / single-page lookup** → no new page; the answer points
     into existing pages.
   - **Comparative or investigative** → file as `analysis`.
   - **Open survey** → file as `synthesis`.
   - **Argued position** → file as `thesis`.
   - **Unanswerable from current sources** → file as `question`.
   Use the relevant scaffold from `wiki/_templates.md`.
6. Append a `wiki/log.md` entry.

Surface the answer in the conversation, then mention what (if anything) was
filed for future reference.
