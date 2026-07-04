# Log

Append-only record of every operation on the wiki. Newest entry at the top.

Entry shape:

    ## [YYYY-MM-DD] op | Subject
    Summary of what changed. Pages touched: [[P1]], [[P2]].

`op` ∈ { `init`, `ingest`, `query`, `synthesize`, `lint`, `review`, `refactor` }.
One entry per session-bounded operation — a batch ingest of 10 sources is one
entry, not ten.

---

## [2026-04-28] init | Knowledge Compiler initialized
Wiki created with empty structure. Directories: `raw/`, `raw/assets/`, `wiki/`.
Schema installed as `CLAUDE.md` (mirrored to `AGENTS.md`). System files
(`wiki/_operations.md`, `wiki/_templates.md`) installed. Index, log, and human
README initialized. Ready for first source ingest.
