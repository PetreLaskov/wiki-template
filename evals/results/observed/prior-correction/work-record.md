# Work record: timing correction

## Scope and files read

Worked only inside this run. Read `AGENTS.md`, `TASK.md`, `wiki/index.md`, all existing entries of `wiki/log.md`, `wiki/_state.md`, `wiki/Lumen Study Choice.md`, `wiki/Definition Pilot.md`, `wiki/Team Newsletter.md`, `wiki/Novel Case Audit.md`, and all four `raw/*.md` snapshots in full. Read the Ingest, Disagreement and correction, and Batch and recovery sections of `wiki/_operations.md`; read metadata, shared frontmatter, and source-template instructions through line 92 of `wiki/_templates.md`. Header/keyword searches also touched these two manuals. `tools/lint.py` was executed, not manually read. No evaluation keys, other runs, external sources, or agents were consulted.

## Work and checks

- Used `Get-Content` for reads, `rg --files` for this run's inventory, and `rg -n` for workflow headings and timing/speed consumers.
- `Get-FileHash -Algorithm SHA256` recorded all four raw fingerprints before writing. The three prior raw hashes matched their stored values; the correction hash is `698aa70e52cfa969d6d43c9ce54437b5c16e4488d23e5297776965e58cedb474`.
- Python interpreter: `<bundled-python>`.
- Baseline `tools/lint.py`: exit 0; 4 pages, 4 raw files, 0 errors, 1 warning for the uncompiled timing correction.
- Saved six original wiki texts in local temporary `.correction-before.json` for diff inspection. Wrote a pending checkpoint before multi-file changes. Used `apply_patch` for content edits.
- Added `wiki/Timing Correction.md`; annotated the pilot and newsletter without changing issued S# lines; revised the canonical analysis, index, and routes; wrote `correction-answer.md`. Left the independent audit unchanged because its claims do not depend on pilot timing.
- Read back the new source ledger and answer and inspected Python `difflib.unified_diff` output for the four changed content/routing pages. Checked correction locators against numbered raw lines 6-10, arithmetic 4 + 6 = 10, unchanged accuracy, withdrawal scope, common origin, and unmeasured repeated-session and long-term outcomes.
- Python assertions passed: pilot/newsletter issued claim lines exactly match pre-edit text; all four raw SHA-256 hashes are unchanged.
- First post-write `tools/lint.py`: exit 0; 5 pages, 4 raw files, 0 errors, 0 warnings. Subsequent citation cleanup directs current accuracy references to the correction and follows documented claim-reference syntax.
- Pre-existing log entries were retained; the new entry records the propagation and the audit no-op. Final verification and checkpoint closure follow below.

## Limitations and failures

No command or check failure occurred in this correction operation. The baseline backlog warning was resolved by ingest. One Python console readback displayed Unicode punctuation imperfectly; later output was explicitly set to UTF-8. This was a display limitation, not a raw-file edit. Lint and hash checks are mechanical evidence, not proof of entailment or better reasoning. No usage, timing, or comparison metrics were invented.

## Final verification

Final Python verification reran raw-hash and original-claim assertions, confirmed all prior log entries were preserved, reviewed final timing-consumer text and the log diff, and ran `tools/lint.py`: exit 0; 5 pages, 4 raw files, 0 errors, 0 warnings. Marked `wiki/_state.md` complete after those checks. Removed the local temporary before-text snapshot. No pending ingestion work remains; the evidence gaps above remain open.
