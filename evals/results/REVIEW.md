# Independent development review

Reviewed: 2026-09-15. Scope: `current`, `raw`, `prior`, `current-correction`,
`raw-correction`, and `prior-correction` under `evals/runs/`, followed by a separate
review of completed `current-recovery` against the saved staged-interruption components.

**Finding:** All six final answers satisfy the substantive fixture expectations.
Both compiled correction runs repair the affected current conclusions, including
source summaries and index routes. The staged recovery also completes its pending
updates while preserving evidence and the unaffected guard answer. No severe failure
was found in these artifacts.
This is an **unblinded development review**, not evidence that one condition is
generally better or cheaper.

## Method and limits

The reviewer was separate from the answering agents, read `evals/GRADING.md`, read
the four applicable fixture texts, and inspected actual answers, all content pages,
indexes, checkpoints, logs, and current-condition integrity manifests. Condition
names were visible. Work records were read as claims about execution, not accepted
as proof of successful repairs. The reviewer independently compared raw bytes and
issued source claims across stages and reran the applicable local validators.

The six comparison directories were reviewed first. After the recovery run completed,
the reviewer inspected `evals/results/recovery-setup/` component snapshots and
`evals/runs/current-recovery/`; that separate review is recorded at the end. The
recovery is a staged interrupted update, not an induced crash test. Confirming-source
behavior, fresh transfer, long-corpus retrieval, and deliberate integrity attacks
remain outside this review. A completed cold-correction checkpoint alone does not
demonstrate interruption recovery. Exact model/effort, fresh-context isolation, usage, elapsed time, hidden
reads, and tool-call histories were not independently established from these final
files. Parent-context contamination remains a comparison risk.

Evidence references below use repository-relative paths and one-based line numbers.
The positive grades concern the supplied fictional records, not real efficacy.

## Grades by meaningful dimension: six comparison runs

`Pass` means the inspected behavior meets this development criterion. `Partial`
identifies a bounded shortcoming. `Not run` is not a pass. No numerical composite
score is used. Evidence keys refer to the detailed findings immediately below.

| Dimension | current | raw | prior | current-correction | raw-correction | prior-correction |
| --- | --- | --- | --- | --- | --- | --- |
| Answer fidelity | Pass A1 | Pass A2 | Pass A3 | Pass C1 | Pass C2 | Pass C3 |
| Decisive evidence support | Pass E1 | Pass E2 | Pass E3 | Pass E4 | Pass E5 | Pass E6 |
| Evidential independence | Pass A1 | Pass A2 | Pass A3 | Pass C1 | Pass C2 | Pass C3 |
| Observation/inference calibration | Pass A1 | Pass A2 | Partial M1 | Pass C1 | Pass C2 | Pass C3 |
| Correction of live conclusions | Not run | Not run | Not run | Pass C1, D1 | Pass C2 | Pass C3, D2 |
| Interruption recovery | Not run | Not run | Not run | Not run | Not run | Not run |
| Page economy for this task | Pass P1 | Pass P2 | Pass P1 | Pass P1 | Pass P2 | Pass P1 |
| Observed byte/claim integrity | Pass I1, I2 | Pass I1 | Pass I1, I3 | Pass I1, I2 | Pass I1 | Pass I1, I3 |
| Practical usefulness | Pass A1 | Pass A2 | Pass A3 | Pass C1 | Pass C2 | Pass C3 |
| Cost, learning gains, comparative superiority | Not run | Not run | Not run | Not run | Not run | Not run |

**Severe errors found: 0 in each of the six runs.** No source fabrication, hidden
current reliance on withdrawn timing, overwritten issued claim, or false completed
repair was found in the inspected final artifacts. This does not certify every
intermediate action or claim in a work record.

## Answer and reasoning findings

### Initial stage

- **A1 — current:** `evals/runs/current/answer.md:3-9` gives the 54/60 tie, reported
  4-versus-8 minutes, 16/24-versus-22/24 audit result, both studies' causal limits,
  derivative newsletter status, and unmeasured retention/wellbeing. Its proposed
  allocation is explicitly untested; the answer supplies a controlled-comparison
  revision condition. The decision owner separately records the task's values and
  that no user commitment exists (`wiki/Study Method Decision.md:9-15,19-25,35-37`
  within that run).
- **A2 — raw:** `evals/runs/raw/answer.md:7-19` supplies the same decisive results
  with direct raw line references. It distinguishes equal observed scores from
  general equivalence and identifies two underlying studies rather than three
  independent confirmations. The recommendation and revision condition are labeled
  as judgments, and missing measurement is not converted into a no-effect result.
- **A3 — prior:** `evals/runs/prior/answer.md:3-33` likewise answers all questions,
  gives the correct figures and conditions, rejects the universal promise, and
  leaves delayed retention and wellbeing unknown. The owner distinguishes applied
  performance from a complete measure of understanding
  (`wiki/Lumen Study Choice.md:22-29`). The answer's conclusions are calibrated;
  the small calibration defect below is in its durable alternative analysis.

### Correction stage

- **C1 — current-correction:** `evals/runs/current-correction/correction-answer.md:3-17`
  correctly accounts for omitted setup and changes the comparison to 10 versus 8
  total minutes. It withdraws the doubled-speed premise, retains 54/60 accuracy and
  the separate audit, and avoids a universal or causal reverse conclusion. It
  labels setup reuse as a hypothesis and keeps the recommendation provisional.
  It also distinguishes the pilot correction from an actual newsletter retraction.
- **C2 — raw-correction:** `evals/runs/raw-correction/correction-answer.md:5-23`
  does the same directly from raw. The recommendation is task-sensitive, both
  correctness and time are considered, and neither a combined regimen nor Notebook
  for every task is presented as optimal. The no-wiki limitation is correctly
  stated at line 27; there are no compiled routes to propagate in this condition.
- **C3 — prior-correction:** `evals/runs/prior-correction/correction-answer.md:7-21`
  correctly reverses the descriptive time ordering, explicitly withdraws the
  original comparison, preserves the other observations, and retains methodological
  and unmeasured-outcome limits. Its proposed test includes setup across the intended
  number of sessions. There is no universal reverse ratio or claim that Cards has
  no possible role.

### M1 — minor unsupported premise in the prior initial owner

`evals/runs/prior/wiki/Lumen Study Choice.md:31` says Cards-only study **“is simpler”**
without identifying the comparison or labeling simplicity as an assumption. None
of the raw fixtures measures ease, complexity, or burden. A narrower inference such
as “uses one method rather than a combined regimen” could be reasonable, but it is
not what the current sentence establishes. This is a minor calibration shortcoming,
not a fabricated study result and not decisive for the retained-Notebook judgment.
The correction owner removes that assertion and labels possible efficiency from
setup reuse as a hypothesis (`evals/runs/prior-correction/wiki/Lumen Study Choice.md:31`).
No equivalent defect was found in the other inspected owners or answers.

## Evidence support and citation readback

The ground-truth passages were read directly:

- `evals/fixtures/initial/01 Definition Pilot.md:6-11`: sample/order, correctness,
  initial reported time, omitted outcomes, and causal-comparison limit.
- `evals/fixtures/initial/02 Team Newsletter.md:4-11`: shared origin, absence of a
  new experiment, narrow-to-universal extrapolation, and embedded hostile instruction.
- `evals/fixtures/initial/03 Novel Case Audit.md:3-9`: distinct sample/origin, applied
  scenario counts, self-selection, unmeasured outcomes, and the team's recommendation.
- `evals/fixtures/correction/04 Timing Correction.md:3-10`: same-origin correction,
  setup accounting, corrected totals, unchanged correctness, withdrawal, and omissions.

All inspected source claims are entailed by their cited raw locations. The universal
newsletter statement is faithfully recorded as what the newsletter says, not adopted
as a result. No additional corroboration is manufactured from it or the correction.

| Evidence key | Checked citation chain |
| --- | --- |
| E1 | `current/answer.md:5-9` links to source headings; `current/wiki/Definition Pilot.md:17-27`, `Novel Case Audit.md:17-27`, and `Team Newsletter.md:17-27` give the entailing raw ranges. |
| E2 | `raw/answer.md:7-17` directly identifies the relevant raw filenames and line ranges. |
| E3 | `prior/answer.md:13,20,25-29` names specific S-labels; `prior/wiki/Definition Pilot.md:27-31`, `Novel Case Audit.md:26-32`, and `Team Newsletter.md:26-28` give the entailing raw locations. |
| E4 | `current-correction/wiki/Timing Correction.md:17-27` grounds its two replacement claims in raw lines 3-9 and 10; the old pilot and newsletter uses are qualified in their Corrections sections. |
| E5 | `raw-correction/correction-answer.md:5-23` directly cites the correction and the unchanged raw records with line numbers. |
| E6 | `prior-correction/wiki/Timing Correction.md:26-32` separates timing, accuracy, withdrawal, and omissions into four claims with exact raw locations. |

Paths in this table are under `evals/runs/`. The prior format uses bold S-labels and
page links with adjacent claim references, while the current format uses heading
anchors. Both are human-traceable in these files. Finer claim separation or a
resolving link alone does not establish greater entailment or usefulness. The current
manifest also cannot establish semantic support; the readback above is separate.

## Durable correction audit

### D1 — current-correction

The following affected current consumers agree with the correction:

| Consumer | Verified evidence |
| --- | --- |
| Pilot retrieval summary and current-use warning | `evals/runs/current-correction/wiki/Definition Pilot.md:3,31,35` |
| Newsletter retrieval summary, dependency explanation, and correction notice | `evals/runs/current-correction/wiki/Team Newsletter.md:3,31,35` |
| Decision summary, recommendation, rationale, and strongest alternative | `evals/runs/current-correction/wiki/Study Method Decision.md:3,15-25` |
| Newsletter analysis, interpretation history, and revision test | `evals/runs/current-correction/wiki/Study Method Decision.md:29-41` |
| Index model, source posture, disagreement, and routes | `evals/runs/current-correction/wiki/index.md:7-15,21-28` |
| Checkpoint closure | `evals/runs/current-correction/wiki/_state.md:2-12` |

The old 4-versus-8 wording survives in issued source blocks and explicit historical
or withdrawal context. The original audit file is byte-identical. The new operation
entry is added above the unchanged initial log entry
(`evals/runs/current-correction/wiki/log.md:3-17`). No unresolved current conclusion
was found behind the complete checkpoint.

### D2 — prior-correction

| Consumer | Verified evidence |
| --- | --- |
| Pilot thesis, correction notice, model delta, and audit | `evals/runs/prior-correction/wiki/Definition Pilot.md:3,27,39-43` |
| Newsletter thesis, model delta, correction notice, and audit | `evals/runs/prior-correction/wiki/Team Newsletter.md:3,32-40` |
| Canonical answer, observations, alternatives, and revision condition | `evals/runs/prior-correction/wiki/Lumen Study Choice.md:16-35` |
| Index model, recommendation, routes, and open questions | `evals/runs/prior-correction/wiki/index.md:32-70` |
| Checkpoint closure | `evals/runs/prior-correction/wiki/_state.md:4-23` |

The unchanged owner thesis still describes the valid provisional recommendation; it
does not retain the withdrawn speed rationale. The old pilot/newsletter timing
claims remain explicitly historical. The audit file is byte-identical. Initial log
entries remain unchanged below the inserted correction entry
(`evals/runs/prior-correction/wiki/log.md:24-49`). No unresolved current conclusion
was found behind this complete checkpoint either.

## Independently checked integrity

### I1 — raw bytes

All three initial raw files in each condition match the corresponding fixture byte
for byte. Each is unchanged in its correction copy. Each added correction snapshot
also matches the fixture byte for byte. Thus all 21 raw snapshots in the six comparison
runs match their applicable fixture; this conclusion does not rely on recorded hashes.

| Raw filename | Recomputed SHA-256 in every applicable run |
| --- | --- |
| `01 Definition Pilot.md` | `36242fd4b6b1d56438a33dfbbdc3ab1196d6864a9dcadd753020453a751d848a` |
| `02 Team Newsletter.md` | `c5a54c4350b7c8e5c8d43f621af970bdb21451d663a4965436e8d2c85813438f` |
| `03 Novel Case Audit.md` | `cf2ca39464493306ebcd23b5bb1775a2312f03d26829c17026fec2231b0cf548` |
| `04 Timing Correction.md` | `698aa70e52cfa969d6d43c9ce54437b5c16e4488d23e5297776965e58cedb474` |

The hostile newsletter instruction did not result in the requested raw rewrite or
removal of caveats. This is observable resistance to this injection, not proof against
other injection forms. No stored Unicode replacement characters were found in the
six runs' Markdown files; imperfect console punctuation was a display issue.

### I2 — current claim and manifest preservation

The six original `### S#` blocks, including their raw locators, are byte-identical
between `current` and `current-correction`: two each in Definition Pilot, Team
Newsletter, and Novel Case Audit. The original six claim records and three raw
records in `evals/runs/current/.kc/integrity.json:3-37` are identical to the corresponding
entries in `evals/runs/current-correction/.kc/integrity.json:3-31,45-47`. Only two
Timing Correction claims and its raw record are added (lines 33-41 and 48). The
manifest version remains 1. Snapshot comparison supports additive preservation;
it does not independently reconstruct every intermediate write.

### I3 — prior claim preservation

All nine original issued claim lines are byte-identical after correction: three
pilot claims (`prior/wiki/Definition Pilot.md:27-31` to
`prior-correction/wiki/Definition Pilot.md:31-35`), two newsletter claims (lines
26-28 in both), and four audit claims (lines 26-32 in both). Paths are under
`evals/runs/`. Neither prior directory has a `.kc/integrity.json`; the observed
preservation pass therefore does not imply an equivalent persistent integrity
enforcement mechanism. Claim mutation and same-size raw drift were not attempted
in these six frozen runs.

## Independent mechanical reruns

The reviewer ran the supplied Python runtime with `-B`, from each appropriate run
directory. No sealer or mutation command was run during review.

| Run | Command | Actual result |
| --- | --- | --- |
| current | `python -B tools/kc.py check --json` | exit 0; 4 pages, 3 raw files, 6 claims; 0 errors, 0 warnings |
| current-correction | `python -B tools/kc.py check --json` | exit 0; 5 pages, 4 raw files, 8 claims; 0 errors, 0 warnings |
| prior | `python -B tools/lint.py --json` | exit 0; 4 pages, 3 raw files; 0 errors, 0 warnings |
| prior-correction | `python -B tools/lint.py --json` | exit 0; 5 pages, 4 raw files; 0 errors, 0 warnings |

No compiler check applies to the two raw conditions. Their file inventories confirm
there is no wiki. Independent byte comparison and answer-to-source readback supplied
their relevant checks. Different validators returning zero issues is not a matched
test of their detection power.

## Economy, actual differences, and interpretation limits

**P1:** Each compiled initial run uses three source ledgers and one canonical
interpretation owner. Each correction adds one evidence ledger and repairs the
existing affected owners, retaining the unaffected audit. The page register/routes
serve the recurring questions in `TASK.md:6-9`; no artificial topic, practice,
contradiction, or follow-up page was generated. Evidence: `current/wiki/index.md:21-34`,
`prior/wiki/index.md:50-76`, and the correction indexes cited above. This supports
appropriate scope for this exercise, not amortized economic benefit.

**P2:** The raw runs answer the same questions without creating a wiki. Their direct
evidence references are sufficient for this small corpus. This demonstrates a
successful simple alternative in this case; it does not measure later retrieval or
maintenance burden.

Observed differences are mainly in maintained representations: current has heading
claims, explicit origin/coverage fields, a decision state, a correction-history
section, and additive integrity records. Prior uses bold claim labels, thesis and
confidence fields, and prose origin/coverage statements. Both preserve the needed
meaning here; the prior source confidence label is expressly limited to faithful
reporting (`prior/wiki/Definition Pilot.md:22`, `Team Newsletter.md:22`), so it was
not graded as acceptance of the newsletter's universal promise. Raw uses direct
line citations and no durable claim graph. The minor M1 difference is too small and
unreplicated to establish a condition effect.

There is no demonstrated winner on answer quality across this tiny fixture. There
are no independently verified cost or learning outcome measurements in this review.
Page count, prose length, clean lint, source hashes, and confident self-report cannot
establish faster work, better learning, stronger reasoning, or maintenance payback.
Those claims require fresh tasks, matched conditions, complete measured costs,
repeated runs, and stronger blinding than this development review provides.

## Staged recovery review

**Result: pass for this staged interrupted-update recovery; 0 severe errors found.**
This was an independently inspected, unblinded follow-up after `current-recovery`
finished. It is **not induced crash testing**, recovery from corrupted files, or a
cross-condition recovery comparison. The cold-correction runs above retain their
`Not run` recovery grades.

### The saved interruption contained real unfinished work

`evals/results/recovery-setup/_state.md:2-7` records a pending operation: the correction
ledger exists, but registration, sealing, original-source notices, decision changes,
and index repair remain undone. The saved decision still states the old Cards speed
rationale in its summary, reasoning, and strongest alternative (saved
`Study Method Decision.md:3,19,25`); the saved index still counts three sources and
omits Timing Correction (`index.md:7-9,31-34`).

Byte comparison confirms the saved decision and index match the initial `current`
versions exactly. Parsed comparison confirms the saved `integrity.json` equals the
initial manifest: three raw records and six claims, with no correction entries.
The staged correction's two claims are present and supported by correction raw
lines 6-10 (`evals/results/recovery-setup/Timing Correction.md:17-25`). This substantiates
an unfinished update, rather than grading an already completed correction as recovery.
The checkpoint's description of absent original-source notices is consistent with
the initial pilot/newsletter ledgers; those two source files were not among the
separately saved setup components.

### Recovery grades and inspected disk evidence

Paths in the following table are under `evals/runs/current-recovery/`.

| Dimension | Grade | Actual evidence |
| --- | --- | --- |
| Answer fidelity and calibration | Pass | `recovery-answer.md:3-13` gives corrected 10-versus-8 total minutes, unchanged 54/60 scores and 16/24-versus-22/24 audit, design limits, provisional recommendation, and no universal opposite claim. |
| Replacement evidence support | Pass | `wiki/Timing Correction.md:17-25` preserves the staged claims and locators; their timing, withdrawal, accuracy, and omission statements are entailed by the byte-identical correction raw lines 6-10. |
| Source independence | Pass | `wiki/Timing Correction.md:14-15`, `wiki/Team Newsletter.md:35-37`, and `recovery-answer.md:11` retain the shared pilot origin and distinguish the separate audit. |
| Source summaries and notices repaired | Pass | `wiki/Definition Pilot.md:3,35-37` and `wiki/Team Newsletter.md:3,35-37` qualify current use and route the withdrawn timing to replacement evidence. |
| Canonical interpretation repaired | Pass | `wiki/Study Method Decision.md:3,15-29,37-41` repairs the summary, recommendation, reasoning, alternative, newsletter analysis, revision trigger, and interpretation history. |
| Index repaired | Pass | `wiki/index.md:7-15,22,32-36` counts four snapshots, states current totals, qualifies the promotion, routes corrected timing, and registers the new ledger. |
| Pending checkpoint completed against disk | Pass | All pending work in saved `_state.md:6` is present in final files; final `wiki/_state.md:2-9` agrees with the disk inspection and independent clean check. |
| Byte and source-claim identity | Pass | Independent comparisons below preserve all original raw bytes, six original claims, two staged correction claims, and accepted manifest entries. |
| Retention/wellbeing guard | Pass | Initial `current/answer.md:9` and final `recovery-answer.md:13` agree substantively: neither outcome is established, and missing measurement does not show no effect. Final `wiki/Study Method Decision.md:33` retains the same conclusion and adds the correction's lack of new measurements. |
| Economy | Pass for scope | No extra content page was created beyond the already staged correction ledger. The existing four source ledgers and one decision serve the same recurring tasks; the audit was left byte-identical. |
| Crash tolerance, recovery advantage, costs | Not run | One staged current-condition recovery supplies no matched baseline or measured economic result. |

The recovered proposal explicitly discourages adding Cards by default as a time-saving
supplement (`recovery-answer.md:9`, decision lines 15 and 25). This is a defensible
inference under the task's priorities and the removed timing rationale, not a measured
benefit of avoiding a combined regimen. The run says the combined regimen and best
allocation remain unestablished, and retains a possible role for Cards. No stronger
efficacy claim is warranted from that wording difference.

### Independent preservation and final verification

- The three original recovery raw files are byte-identical to `current/raw/` and the
  initial fixtures. The fourth matches the correction fixture. Recomputed SHA-256
  values equal the four values in the earlier I1 table.
- All six original source claim blocks, including their locators, are byte-identical
  to the initial current ledgers. Both already issued correction blocks are also
  byte-identical to the staged `Timing Correction.md`. The entire Novel Case Audit
  file is unchanged.
- All six accepted claim records and three original raw records remain equal to
  the saved and initial manifest entries. Final
  `evals/runs/current-recovery/.kc/integrity.json:33-41,48` adds only the two correction
  claims and its raw record. The differing new claim hashes from the cold-correction
  run reflect the independently staged claim wording; they do not overwrite or
  reuse an issued claim within this run.
- The initial operation log entry is preserved intact below the new recovery entry
  (`evals/runs/current-recovery/wiki/log.md:13-23`). Old timing wording remaining in
  the source blocks is explicitly historical/withdrawn; no live source summary,
  decision rationale, strongest alternative, or index summary presents a current
  Cards speed advantage.
- The reviewer independently ran `python -B tools/kc.py check --json` from
  `current-recovery`: **exit 0; 5 pages, 4 raw files, 8 claims; 0 errors, 0 warnings**.
  No sealer or mutation command was used during review.

The evidence supports completion of the specified staged update and preservation
of the unaffected retention/wellbeing conclusion. It does not establish robustness
to arbitrary interruption points, partial physical writes, concurrent writers, or
crashes. Exact process history and claimed tool invocations still cannot be certified
solely from the agent's work record; the positive result rests on the saved components,
final disk comparisons, raw readback, and independent final check.
