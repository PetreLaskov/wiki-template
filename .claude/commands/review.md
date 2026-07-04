---
description: Consolidation pass — work the lint diagnostics, pay synthesis debt, rewrite the model
---

Run the **review** mode. This is a consolidation pass: do the work, log the result.

Procedure (canonical: `AGENTS.md` § Review; extended: `wiki/_operations.md` § 6):

1. **Run `python tools/lint.py`.** Fix invariant errors first. Then work the
   diagnostics as a **disposal queue** — every item gets an action or a one-line logged
   reason to defer. No silent skips:
   - orphans → link, merge, or justify isolation;
   - `importance ≥ 7 ∧ status: seed` → develop to `live` or demote;
   - broken links → create the seed or remove;
   - oversized pages → hub-extract (`wiki/_operations.md` § 7);
   - stale pages / `src_bytes` drift → refresh, re-ingest, or mark;
   - domain swelling → synthesis + catalog migration.
2. **Semantic pass** on recent + high-importance pages: topic-label theses, uncalibrated
   confidence, vanished contradiction sides, Key Points that aren't the spine, routing
   bloat in index/hub openings, register drift.
3. **Synthesis debt**: any domain with ≥5 substantive pages and no synthesis, any
   concept cluster cited by ≥5 sources with no thesis — write it or log why not.
4. **Question backlog**: promote, retire (say why), or re-frame.
5. **Rewrite the State of the Model** in `wiki/index.md` from what the wiki now holds —
   through-line, strongest claims, live tensions, maturity, next leverage. ≤300 words.
6. **Rotate the log** if past ~200 entries (older → `wiki/_log-archive-YYYY.md`,
   newest ~50 stay).
7. One `review` log entry: counts and dispositions, including deferrals with reasons.

If a finding is too large for this pass (a domain needing real refactoring), log it and
surface it for the next session rather than doing it badly now.
