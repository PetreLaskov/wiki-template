# Log

Append-only record of operations, newest at top. One entry per session-bounded
operation (a batch wave is one entry, not ten). Rotated at review past ~200 entries
(older → `_log-archive-YYYY.md`).

Entry shape:

    ## [YYYY-MM-DD] op | Subject
    What changed in the model. Pages touched: [[P1]], [[P2]].

`op` ∈ { init, charter, ingest, query, synthesize, lint, review, refactor }.

---

## [2026-07-04] init | Knowledge Compiler v2 initialized
Empty wiki on the v2 contract: charter-first, delta-first ingest, ledger source pages
with claim anchors, `load_when` routing, hub/ownership conventions, `tools/lint.py`
verification. Awaiting charter, then first source.
