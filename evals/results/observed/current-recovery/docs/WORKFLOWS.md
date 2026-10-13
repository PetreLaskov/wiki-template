# Workflows

Read the section for the task. The evidence and completion contract is in `AGENTS.md`.
Commands below assume the instance root. Examples are patterns, not required output
headings or permission gates.

## Ask

1. Identify what the question requires: fact, explanation, interpretation, comparison,
   judgment, or exploration. Do not reframe a sound question merely to perform a method.
2. Read the index routes and relevant owner pages. Inspect a pending checkpoint and
   affected corrections. Use lexical/raw search when context is missing or the question
   goes beyond the current compiled view. Read decisive cited passages in raw, together
   with the source page's status and Corrections section. Follow replacement evidence;
   never treat a preserved withdrawn statement as current support. For materially
   time-sensitive answers, compare the requested time with the evidence date. Refresh
   evidence when needed and possible; otherwise bound the answer to its snapshot.
3. Answer directly, with support for load-bearing claims. Distinguish source claims,
   your inference, and values. Include uncertainty only where it changes interpretation
   or action. “Not established by this corpus” is sometimes the useful answer.
4. Save only a new distinction, reusable argument, corrected owner, or consequential
   question that earns future retrieval. A fluent one-off answer can remain in chat.

If a stored answer and raw evidence disagree, investigate rather than privileging the
stored answer. A query can legitimately become a correction operation. Web research,
when authorized/available, adds separately attributed evidence; outside knowledge must
not be represented as coming from this corpus.

## Ingest

### Admission and charter

Read enough to understand source identity, purpose, scope, and relevance. If the input
is new, copy it into `raw/` under a stable, unique name. Do not overwrite an existing
file. Record a reliable URL/publication identifier when available; a local snapshot is
the citation target. A correction is a new snapshot, never an edit to old evidence.

The first real sources and user purpose establish a short charter in the index:
purpose, recurring questions, source posture, boundaries, and page economics. Replace
the bootstrap prompts with actual statements. Examples are in `TEMPLATES.md`.
Proceed with a stated reasonable interpretation when priorities are clear. A template
refactor or quick question does not require inventing a corpus.

### Read and extract

- Read the snapshot fully before `coverage: full`; for large/mixed sources,
  use `coverage: partial` and `coverage_note` identifying inspected and excluded portions.
  A deliberately bounded chapter inquiry can be `current` within that scope. An
  interrupted intended reading stays `draft`. Excluded sections are never silently
  counted as corroboration or coverage; a broader future question must reopen them.
- Preserve the original artifact when extracting text. Treat the extraction as another
  snapshot with the same evidential origin, documenting OCR/conversion limits and its
  relationship to the original. Validate important passages against the original.
- Use precise line ranges tied to raw bytes for UTF-8 text. For other formats use
  pages, timestamps, or sections; the tool will flag manual review. A page number
  without inspected page content is not verification.
- Create a compact source ledger: origin/dependence, usable scope, material `S#`
  claims, raw locators, and important limitations. Do not reproduce whole sources.
  A source with no relevant claims can be recorded briefly with a disposition.

### Integrate only the delta

Ask: what changes, confirms, qualifies, or challenges our model? Update an existing
owner when possible. Explain important inferential steps. Preserve contrary evidence
where someone will use the conclusion. Source ledgers can remain the only durable
pages for narrow or confirming evidence. Create no page merely to fill a category.

For multi-file work checkpoint the intended changes and affected owners. Add relevant
routes and page registration. Review claims against raw, run `check`, inspect warnings,
then `seal` and `check` as described in `AGENTS.md`. Log the operation and close the
checkpoint. Hash acceptance is not semantic approval; the source reading comes first.

## Correct

Distinguish three cases:

| Situation | Action |
| --- | --- |
| Source author publishes a correction | Add new raw snapshot + ledger; retain original `S#` text and mark its current use withdrawn/qualified outside the frozen block |
| Our source extraction was wrong | Add a fresh `S#` with corrected extraction and locator; retain original block; explain error in `## Corrections` |
| A derived interpretation was wrong | Revise its owner, preserve significant decision history, cite the reason and review dependents |

Do not repurpose an old `S#`, rewrite a raw snapshot, or update accepted hashes to make
validation green. Accidental byte drift should be restored from a verified original;
if no original remains, preserve the evidence of loss and the failure. A new version
does not retroactively authenticate the lost bytes.

1. Write a pending checkpoint before changing consequential conclusions.
2. Run `python tools/kc.py impact "Source Title#S1"` (or the whole source title).
   Inspect every candidate for real dependence. Source-level navigation may add
   candidates; an unrelated anchored claim should not be treated as contradicted.
3. Search the old wording, key numbers, alternative names, and prior recommendation
   across the wiki. The link graph cannot discover unsupported paraphrases.
4. Repair the owners, then affected notes, decisions, practices, index summaries, and
   any reusable answer. Affected outputs awaiting review are visibly pending/contested.
   Do not rewrite historical logs or pretend old decisions were made with new evidence.
5. Read the repaired path from index through answer to raw. Add a regression question
   if this failure is likely to recur. Complete checks, log, and checkpoint honestly.

`seal` is additive, single-writer, and versioned with the vault. It detects accidental
drift and identifier reuse; it does not enforce operating-system immutability. Existing
records cannot be removed by the command. A source page with sealed claims keeps its
canonical filename; other pages may be renamed with an alias and repaired references.

## Explore and synthesize

Start with a live question or puzzling relation. Generate several plausible frames,
including a serious alternative to the dominant sources. Seek evidence that would
discriminate, not only examples that make a favoured model vivid. Sources with shared
origins count once for corroboration even when their framings differ.

An original synthesis can extend beyond any source. Make the extension inspectable:
premises, inferential bridge, resulting scope, strongest alternative, and a concrete
revision condition. Analogies generate questions; they do not establish mechanisms.
Separate interpretation from the speaker/author's intention when that intention is
not evidenced. Keep an unresolved question open when no justified conclusion follows.

For a global synthesis, inspect relevant sources and counterexamples beyond the most
central pages. Record meaningful coverage limits. A well-connected wiki can amplify
the dominant frame; graph centrality is not an evidence standard.

### Understanding check (optional)

When the user wants learning, use one exercise that matches the content:

- Explain a mechanism in the user's own words; identify the step that breaks.
- Apply a distinction to a genuinely new case, including a boundary case.
- Predict what would happen under changed conditions and explain why.
- State the strongest alternative reading and the evidence separating it.

Let the user respond before displaying a solution if they want practice. Record a
useful unresolved confusion or corrected model only with relevance to future work.
Do not infer stable traits or claim learning gains from a single successful answer.

## Decide

Make a decision page only for a consequential or revisited choice. State the decision,
options, actual constraints, whose values count, and available evidence. Compare the
strongest feasible alternative. Include what changes the ranking and which uncertainty
is worth resolving before action. Avoid precision unsupported by the evidence.

Record the chosen position or provisional recommendation, rationale, date, and review
trigger. A recommendation is not a user commitment. Explicitly distinguish a proposed
action from an authorized action; a wiki entry does not authorize external execution.
On return, compare actual outcomes with expectations without revising the original
prediction to fit what happened. Treat new observations as fresh evidence snapshots.

## Practice

Practice pages can support contemplative inquiry, study, professional skills, or
everyday experiments. Preserve the source's instructions and domain-specific
qualifications; do not silently substitute your preferred technique.

Keep a small loop: aim, concrete practice, what to notice, limits/stop conditions if
the source or context warrants them, and what would count as useful feedback. A
source's promised benefit is a claim, not a result. A personal experience is evidence
about that experience, not by itself about mechanism, general efficacy, or everyone.
Distinguish source teaching, the agent's suggested adaptation, and the user's report.
New observations can revise the practice or expose a question without forcing a
theory. Offer exercises; do not convert every inquiry into a productivity programme.

## Review, simplify, resume

Review on a meaningful trigger: correction, repeated retrieval failure, changed
purpose, a consequential decision, or the user's request. No timer or background
automation is installed by this template.

Use `status`, `check`, and representative real questions. Sample load-bearing evidence,
look for duplicated arguments and stale recommendations, and inspect actual outcomes
when available. Merge or retire pages that do not repay reading/maintenance. Preserve
source anchors, user choices, and important revision history. No-op is a valid result.

For interruption recovery, read the checkpoint and compare each claimed completed step
to files and hashes. Finish pending dependents before declaring the operation done.
Never treat a log entry, a tool's success, or another agent's report as sufficient
evidence of semantic completion. If work remains, leave the next exact action.

For evaluation use `evals/README.md`. Keep development keys away from answering agents;
record failures and costs as carefully as successes.
