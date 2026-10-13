# Log

Append-only record of operations, newest at top. One entry per session-bounded
operation (a batch wave is one entry, not ten). Rotated at review past ~200 entries
(older → `_log-archive-YYYY.md`).

Entry shape:

    ## [YYYY-MM-DD] op | Subject
    What changed in the model. Pages touched: [[P1]], [[P2]].

`op` ∈ { init, charter, ingest, query, synthesize, lint, review, refactor }.

---

## [2026-09-15] ingest | Lumen timing correction

The new same-origin correction replaces the apparent Cards speed advantage with comparable total-session times of Cards 10 minutes and Notebook 8 minutes. Exact-definition correctness remains 54/60 each. Retain Case Notebook provisionally under the accuracy-first priority; the former speed rationale for replacement is removed. Repeated-session efficiency, unfamiliar-case timing, six-month retention, and wellbeing remain unknown.

Added [[Timing Correction]] with raw locators and fingerprint. Preserved issued claims in [[Definition Pilot]] and [[Team Newsletter]], adding explicit correction notices. Updated [[Lumen Study Choice]], index model/routes, checkpoint, and `correction-answer.md`. [[Novel Case Audit]] needed no change: none of its claims depends on the corrected timing premise. Prior log entries and index activity remain historical records.

Verification: read all four raw snapshots and affected owners; checked correction lines 6-10, unchanged accuracy, design limits, and common origin; searched speed/timing references and reviewed local before/after diffs. All four raw SHA-256 hashes match the pre-edit values, and original pilot/newsletter claim lines are unchanged. Baseline lint: 4 pages, 4 raw files, 0 errors, 1 warning (uncompiled correction). Post-write lint: 5 pages, 4 raw files, 0 errors, 0 warnings. Command details and final verification are in `work-record.md`. Mechanical checks do not establish semantic accuracy or comparative superiority.

## [2026-09-15] ingest | Lumen study-method inquiry

Established the charter from all three fictional sources and the user's accuracy-first
priority. Added [[Definition Pilot]], [[Team Newsletter]], [[Novel Case Audit]], and
the sole interpretation owner [[Lumen Study Choice]]; updated index routes and wrote
`answer.md`. Provisional judgment: retain case-based work; equal immediate recall
scores do not establish unfamiliar-case equivalence. The newsletter supplies no
independent evidence or warranted universal speed promise. Six-month retention and
wellbeing remain unknown.

Verification: reread complete raw text and resulting pages; checked reported values,
design caveats, source dependence, locators, and inference boundaries. Reviewed applied
patches and readback; all three original SHA-256 hashes remain unchanged. Baseline
lint had 0 errors and 3 backlog warnings. The first post-write lint found 22 claim-format
errors; corrected definitions to the documented bold S# format, preserving identifiers
and meanings. Subsequent lint: 4 pages, 3 raw files, 0 errors, 0 warnings. Mechanical
checks do not establish semantic accuracy or comparative reasoning superiority.

No remaining compilation work for the supplied text. Causal and long-term evidence
gaps remain explicit; no invented results or actions were added. Existing log history
is preserved.

## [2026-07-04] init | Knowledge Compiler v2 initialized
Empty wiki on the v2 contract: charter-first, delta-first ingest, ledger source pages
with claim anchors, `load_when` routing, hub/ownership conventions, `tools/lint.py`
verification. Awaiting charter, then first source.
