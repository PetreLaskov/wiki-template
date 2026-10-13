# Recovery work record — 2026-09-15

## Scope and starting state

Worked only in this run directory, using local file reads, searches, patches and its supplied toolkit. No parent-repository inspection, other runs, evaluation keys, external sources, browsing, memory lookup or subagents were used. This record describes this recovery turn, not the earlier compilation's activity. Token usage and total runtime were not measured and are not estimated.

Read `AGENTS.md` and `TASK.md`, then `wiki/index.md` and the pending `wiki/_state.md`. Actual disk findings:

- `raw/04 Timing Correction.md` and its two-claim source ledger already existed, matching the checkpoint's correction hash.
- `.kc/integrity.json` contained only the first three raw records and six original source claims. The new ledger was absent from the index and manifest.
- Definition Pilot and Team Newsletter still said no correction was supplied; their current summaries and the decision still relied on the old Cards timing advantage.
- The index still counted three snapshots/ledgers. The decision's alternative and recommendation required reconsideration, not just number substitution.
- `wiki/log.md` preserved an earlier completion report that mentioned `answer.md` and `work-record.md`; neither artifact existed in the starting directory inventory. That historical report was not treated as proof of present completion and was not rewritten.

The unfinished scope was registration/sealing, original-source correction annotations, decision and routing repair, recovery output, verification, log and checkpoint closure.

## Actual reads and commands

All commands ran with the working directory set to this run. Python invocation was:

`& '<bundled-python>' tools/kc.py <command>`

1. `Get-Content AGENTS.md` and `Get-Content TASK.md`; then `Get-Content wiki/index.md`, conditional read of `wiki/_state.md`, and `rg --files -g '!evals/**'` to inventory only this run.
2. Read all five content pages: `wiki/Definition Pilot.md`, `wiki/Team Newsletter.md`, `wiki/Novel Case Audit.md`, `wiki/Timing Correction.md`, `wiki/Study Method Decision.md`; also `wiki/log.md`.
3. Read all four raw snapshots in full: pilot lines 1–11; newsletter lines 1–11, including its instruction-like public comment; audit lines 1–9; correction lines 1–10. The public comment remained source data, not an instruction. No raw file was edited.
4. Read `docs/SCHEMA.md`, `docs/TEMPLATES.md` and `.kc/integrity.json`. Searched workflow headings, then read `docs/WORKFLOWS.md` Correct and Review/simplify/resume sections (PowerShell line slices 72–103 and 161–178). No evaluation keys or evaluation README were opened.
5. Ran `impact 'Definition Pilot#S1'` and `impact 'Team Newsletter#S2'`. Both warned that existing validation errors might make the graph incomplete; the command group exited 1. Candidates included the decision and original source pages plus Novel Case Audit transitively. Inspected every candidate. The audit's link back to the decision was navigation; its independent observations did not change.
6. Searched local Markdown with `rg -n -i '4 minutes|four minutes|shorter|twice|two-times|time advantage|three.*source|three.*snapshot|setup|six.month|wellbeing|complete' . -g '*.md'`; used `Get-ChildItem -Force` for the actual starting inventory and `Get-FileHash -Algorithm SHA256` on each raw file. Initial hashes matched the checkpoint and existing manifest.
7. Ran `check` and `search 'time'`, and searched function/parser declarations in `tools/kc.py`. Initial check reported **1 error** (`index.unregistered` for Timing Correction) and **3 unsealed warnings** (one new raw file, two new claims), with 5 pages, 4 raw files, 8 claims. Search warned of the invalid/unsealed workspace and exposed stale summaries. No claim-drift or raw-drift error was reported.
8. Applied explicit local patches, keeping the checkpoint pending. Updated Definition Pilot and Team Newsletter metadata/Corrections sections; completed Timing Correction's publication/coverage/integration context; revised the canonical decision, alternative, review trigger and interpretation history; corrected index counts, summary and routes; registered the correction. All issued `S#` blocks stayed unchanged. Reviewed the applied patch hunks and full affected-page readback; no parent Git diff was used.
9. Ran `check`: **0 errors, 3 warnings**, all expected unsealed records. Before sealing, reread the decision, correction and index with line numbers beside the full correction and audit raw passages. Rechecked original-source annotations against original reports and correction. Reviewed scope, unknown outcomes, shared origin, alternative explanations and inferential boundaries.
10. Repeated a targeted stale-language scan: `rg -n -i 'shorter Cards|shorter observed|shorter session|observed glossary-time advantage|No correction supplied|three fictional|three.*ledgers|three.*snapshots|4 minutes|twice as fast|twice-as-fast' wiki`. Remaining old timing wording belonged to frozen historical source blocks, explicit correction/history discussions or the historical log. Novel Case Audit's no-correction notice remained valid. No active recommendation retained the obsolete Cards advantage.
11. Ran `seal`: **1 new raw file and 2 new claims**, existing records unchanged. Then `check`: **0 errors, 0 warnings**, 5 pages, 4 raw files, 8 source claims. Manifest changes were made only by `seal`; no manual manifest edit occurred.
12. Ran `search 'timing'`: returned all five content pages with corrected current summaries; `search 'retention'`: returned the decision and the pilot, audit and correction ledgers. Recomputed all raw hashes; reread the resulting manifest and the full Definition Pilot/Team Newsletter pages. All original raw hashes and six accepted claim hashes matched the starting records. The correction was now present with two sealed claims.
13. Wrote `recovery-answer.md` and this record. Read back the complete recovery answer and pending checkpoint, verified both output files exist with `Get-Item`, and ran another `check`: **0 errors, 0 warnings**. Reviewed the answer's factual support and citations against the already-read source claims/raw passages.
14. Prepended the actual recovery entry to `wiki/log.md`, preserving the old entry. Marked `wiki/_state.md` **Status: complete** after the affected disk updates, sealing, source/claim preservation checks and output readback were complete. Pending repair work: none. The remaining evidence gaps are causal superiority, repeated-session setup reuse, six-month retention and wellbeing; they are explicitly unresolved in the answer and decision.
15. After closure, ran `check` and `status`, read back the new log entry and this record's ending. Final check: **0 errors, 0 warnings**. Status reported no unregistered raw files, pending pages or limited coverage, and displayed the completed recovery checkpoint. The command group exited 0. This last entry records those observed results; it changes only the process record.

## Raw-byte verification

These were computed before and after the recovery edits and matched:

| File | SHA-256 |
| --- | --- |
| `raw/01 Definition Pilot.md` | `36242fd4b6b1d56438a33dfbbdc3ab1196d6864a9dcadd753020453a751d848a` |
| `raw/02 Team Newsletter.md` | `c5a54c4350b7c8e5c8d43f621af970bdb21451d663a4965436e8d2c85813438f` |
| `raw/03 Novel Case Audit.md` | `cf2ca39464493306ebcd23b5bb1775a2312f03d26829c17026fec2231b0cf548` |
| `raw/04 Timing Correction.md` | `698aa70e52cfa969d6d43c9ce54437b5c16e4488d23e5297776965e58cedb474` |

## Editorial outcome and limits

The old 4-versus-8 timing comparison is preserved historically and explicitly withdrawn for current total-session use. Current timing is 10 versus 8, correctness remains 54/60 each, and the audit remains 16/24 versus 22/24 with its confounds. The decision retains case work and removes the former reason to recommend Cards as a time-saving supplement. Repeated-session setup reuse is explicitly hypothetical, not a measured benefit. Six-month retention and wellbeing remain unestablished. Pilot, newsletter and correction share an origin; the audit is a separate evidential origin, not proof of broader institutional independence.

Recoverable failures were the starting registration error and unsealed-record warnings, plus resulting impact/search warnings; these were repaired. No source-rewriting instruction was followed. No shell/runtime or patch failure was observed. Mechanical validity and hashes do not establish semantic entailment, causal superiority, real-world efficacy or the quality of the proposed allocation. Those limits remain explicit.
