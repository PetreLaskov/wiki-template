# Operations

Read only the section for the current operation. `AGENTS.md` owns shared invariants;
this manual supplies execution details. Templates are in `_templates.md`.

## Charter

Read representative sources, including any source likely to challenge the dominant
frame. Record what you sampled; do not imply exhaustive coverage. Use the user's stated
purpose to select three to seven question classes. Draft the charter's five parts.
If priorities remain decisive and unknown, ask one focused question with a concrete
draft to react to. Otherwise use the priorities already supplied.

Populate the router only with real pages. With no sources, record bootstrap state and
what input is needed. Revisit the charter when actual use exposes a scope mismatch;
preserve user decisions, and explain a proposed scope change instead of quietly
replacing the user's goal. A refactor of this template is not a corpus ingest.

## Ingest

### One coherent unit

1. **Inspect input.** Read the source fully, including relevant tables/attachments.
   Record origin, genre, date, dependence, and a SHA-256 of its raw bytes. If an asset
   cannot be read, record the exact missing coverage and which claims cannot be compiled.
   Do not call a partial read a full ingest.
2. **Plan the delta.** Route to existing owners. Classify each relevant claim as new,
   confirming, qualifying, challenging, or irrelevant to the charter. Reserve stable
   S# identifiers with raw locators before referencing them in owner pages. For a
   multi-file unit, record the work item in `_state.md`.
3. **Integrate.** Update the canonical owner first in the plan, then its affected
   dependents. The physical save order may vary; the unit is incomplete until evidence
   and derived pages agree. Create an owner only for a distinct, useful retrieval need.
   A confirming or peripheral claim can stay in the source ledger.
4. **Finish the ledger.** Include Snapshot, evidence posture, Key Claims with locators
   and owner pointers, Model Delta, and a compact Audit. A low-novelty source normally
   needs about 150–300 words, fewer if sufficient. This is guidance, not padding or a cap
   that permits omission of decisive caveats.
5. **Verify and close.** Check entailment at the raw locators, inspect affected
   conclusions/routes, run lint, inspect the diff and hashes, reconcile state, and
   write one event. Do not equate a new ledger with an absorbed delta.

A source that contributes no material claims may have a short ledger explicitly saying
**No material claims**, why it was assessed, and why no model update was justified.
An unread source belongs in the backlog, not in a ledger that implies review.

### Disagreement and correction

First ask whether statements concern the same proposition, population, conditions,
metric, and date. Different scopes may coexist. A live conflict records both positions,
their evidence and independence, the practical consequence, and what would resolve it.
Mark the affected central conclusion contested, not every page mentioning either source.

A new correction is a new immutable raw snapshot and its own ledger. Keep the original
ledger's S# meanings; annotate withdrawn claims with the correcting ledger and date.
Update owners that relied on them. Search backlinks/citations to those owners and
sources (for example `rg -n -F '[[Owner Page]]' wiki`, including aliases where needed);
inspect each consequential consumer, not every incidental link. Follow the chain until
no affected conclusion is silently based on old evidence. Stop propagation when a
consumer does not depend on the changed premise; record the disposition.

If the raw file changed externally, lint's hash mismatch is a signal to investigate.
Use version history or an available prior snapshot to identify the difference. Never
pretend a hash contains the old source text. If the previous bytes cannot be recovered,
state that limitation, preserve issued claim IDs, and re-read the current source before
updating its fingerprint. Do not merely refresh the hash to silence the warning.

Changed recommendations must appear in the current model/router if those surfaces carry
the old recommendation. Keep history as history, clearly separated from present claims.

## Batch and recovery

For more than five sources, order by expected model leverage and work in waves of
roughly five to ten, reducing the wave if sources are long or consequential. Each
source still needs complete coverage; batching does not license shallow sampling.
Gate each wave on integrated owners, updated hubs, lint, and a reconciled checkpoint.
Review when repeated patterns or unresolved debt warrant it, often around 25 ingests.

Use this compact shape only when work needs a checkpoint:

```markdown
# Work State
Operation: ingest | correction of the latency evidence
Status: in progress
## Resume Point
Next: inspect [[Rollout Decision]] for reliance on the withdrawn measurement.
Do not treat this operation as complete until the remaining items pass verification.
## Work Item
- Inputs: raw/correction.md; SHA-256: [actual digest]
- Intended delta: [specific claim or recommendation that changes]
- Files owned by integrator: [index, state, log, shared hub]
- Completed and checked: [files and what was verified]
- Remaining: [owner/dependent/ledger/route tasks, exact next action]
- Verification: [command/result or not run; raw-integrity check]
## Queue
- [next bounded work item and why it comes next]
```

On resume, compare checkpoint assertions with the actual pages, input hashes, and diff.
Finish or reconcile partial edits before depending on them. If inputs changed again,
replan the affected delta. Do not duplicate pages or recycle S# identities.
After completion, replace active details with a short “complete; no pending work”
resume point or remove the checkpoint once its durable outcome is logged.

Concurrent workers get disjoint file sets. One integrator edits shared owners, index,
state, and log. Worker reports are leads; the integrator inspects written artifacts and
runs the final checks. Never mark a wave done because every source has a filename.

## Query

Route index → hub → owners; read source ledgers and raw locators when the compiled
layer cannot support the answer, especially on disputed or consequential details.
Treat the five-page target as a retrieval design signal, not a limit on honesty.

Lead with the answer and governing reason. Cite claims using source S# references,
label the wiki's inferences, and state uncertainty that could change the answer.
If evidence is absent, give the supported partial answer or conditional rule; do not
invent a result to make the wiki appear complete.

Leave a proportionate trace:
- Improve an existing owner if it should have answered the question.
- File an analysis for a reusable assembled answer, or a question for a consequential
  unresolved frontier. Check for an existing equivalent first.
- A one-off gap or trivial lookup needs no new content page. Log the result or routing
  issue briefly; repeated use of the same gap is a reason to reconsider its priority.

Read-only or “answer only” user requests override the default trace-writing convention.

## Synthesize

Select a through-line that changes what a future reader can conclude or retrieve.
Use `synthesis` for a map, `thesis` for an argued conclusion, `analysis` for an answer.
Do not create one just because a domain reached a page count.

Read the relevant owners, identify agreement/dependence/conflicts, and test the proposed
conclusion against its strongest credible alternative. Cite the premises, distinguish
the new inference, and name what would change the conclusion. If the through-line is
unsupported, improve the existing map or log the gap instead of manufacturing a thesis.
Add a Decision Map if the page routes a cluster. Link back only where useful.

## Lint

Run `python tools/lint.py`; use `--stats` for distributions or `--json` for structured
diagnostics. The optional root argument selects another isolated wiki.
`--legacy` tolerates old status vocabulary and missing `load_when`; it does not excuse
broken links, malformed syntax, or invalid evidence paths.

Errors are structural violations. Warnings are review candidates, not automatically
bugs. Record relevant dispositions; do not bulk edit solely to silence a heuristic.
Lint cannot verify semantic entailment, source independence, locator accuracy, or the
quality of a decision. Use the semantic checks and evaluation pack as appropriate.

## Review

Review when query failures, corrections, accumulated maintenance, or about 25 ingests
suggest it will repay its cost.

1. Run lint. Fix operation-relevant errors; dispose of warnings by repair, explanation,
   or a concrete deferred task. Prioritize misleading claims and broken routes.
2. Inspect consequential/recent claims: actual evidence support, source independence,
   qualifications lost in summaries, unacknowledged inference, and duplicated ownership.
3. Resolve, reframe, merge, or retire questions based on their current value. Resolve a
   question by linking the answer; preserve useful history without indexing every dead end.
4. Check whether hubs and theses are needed. Counts prompt inspection, not production.
5. Reassess State of the Model against current owners. Rewrite if it is stale; an
   unchanged accurate model is a valid outcome. Keep it at most 300 words.
6. Compress the entry surface. Move exhaustive listings to `_catalog.md` whenever
   the index crowds out routing, even well before 150 pages. All content pages must
   be mentioned in index or catalog; routing links may appear in both.
7. Rotate long logs: preserve old entries verbatim, keep the newest ~50, archive the
   rest by year. Add one review entry with actual dispositions and remaining debt.

## Refactor

Choose the smallest transformation that repairs a retrieval or ownership problem.
A user-authorized reconstruction includes the necessary multi-file changes; do not
create an arbitrary page-count permission gate.

- **Split / hub extraction:** move separable depth into an owner with its own thesis
  and retrieval trigger. Keep the parent as a compact router only if it earns that role.
- **Merge:** choose a canonical name, integrate evidence and disagreements, update
  active consumers, put the previous title in aliases when useful, then remove the
  duplicate after checking that no unique evidence or decision is lost.
- **Rename:** preserve a useful old-title alias and repair active links. Keep historical
  event text intact. Aliases must not collide with other titles or aliases.
- **Source ledger changes:** preserve S# identities and raw locators. Do not collapse
  independent raw files into one ledger merely to improve page counts.

Checkpoint meaningful multi-file changes, inspect inbound links and affected conclusions,
run lint, and log the old → new mapping. Prefer version-control recovery; never assume
the wiki can be regenerated deterministically from raw alone.

## Evaluate

Read `evals/README.md`. Run mechanical regression tests separately from agent behavior
tests. Use isolated copies so fictional fixtures never enter production raw or wiki.
Use fresh contexts and hide grading expectations from the answering agent.

A development smoke pass can reveal concrete bugs. To claim that the reconstruction
beats its predecessor or raw search, run controlled paired comparisons with compilation
cost included. Report the distinction and any untested acceptance cases. Keep a failing
case that drove a useful fix; do not optimize for passing only known wording.
