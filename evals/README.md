# Evaluation without pretending it measures wisdom

The pack contains fictional development evidence. It tests mechanical invariants and
observable agent behavior. It is not a sealed benchmark, a cognitive assessment, or
proof of general superiority. Keep it outside production raw/wiki.

## Three distinct evidence levels

1. **Mechanical regression:** repeatable positive/negative tests of the tools. Run
   `python -m unittest discover -s tests -v`. Inspect test meaning, not only count.
2. **Behavioral development:** real agents ingest, answer, correct, and resume on the
   fixtures. Inspect answers and durable files, with source hashes before/after.
3. **Comparative usefulness:** fresh representative corpora and held-out questions,
   matched model/tools/budgets, repeated runs, independent blinded grading, all
   compilation/maintenance costs included. A small development comparison is not this.

## Prepare a fresh answering workspace

```powershell
python evals/prepare.py current evals/runs/current
python evals/prepare.py raw evals/runs/raw
python evals/prepare.py prior evals/runs/prior --prior "C:\path\to\prior-template"
```

Every destination must be absent. No existing directory is merged. `prepare.py` copies
only operational files, initial evidence, and a common task. It excludes this protocol,
grading keys, prior answers, and reconstruction reports. Root instructions may still
be inherited by some agent hosts; record that contamination risk and prefer an
independent task process rooted at the prepared folder. Do not expose `GRADING.md` to
answering agents. Launch a new model context with only the prepared workspace's task.

Read `TASK.md`; produce `answer.md`. Freeze the resulting answer and wiki before adding
the correction. Record model identifier/effort, tool access, prompt, timestamps, any
limits, and actual usage when available. Words, bytes, and file reads are proxies and
must not be called tokens. Save actual source hashes and failed attempts.

## Correction, then recovery

Preserve the initial run and prepare a new correction workspace without its answer
or work-record files:

```text
python evals/prepare_correction.py evals/runs/current evals/runs/current-correction
```

The helper adds `fixtures/correction/04 Timing Correction.md` to the copied raw
directory and writes `TASK.md`. Repeat for the other conditions. Launch a fresh context with:

> Follow this workspace's AGENTS.md. Ingest the new timing correction and propagate
> what changes through stored conclusions and routes if this condition maintains a
> wiki. What changes in the speed claim and study recommendation? What stays valid
> and unknown? Write correction-answer.md and finish the appropriate verification.

A cold correction is not an interruption test. For explicit recovery, freeze a copy,
have the operator install only the correction source ledger and a truthful pending
checkpoint naming unrepaired owners, then start another fresh agent with:

> Recover the unfinished operation from disk, complete affected updates, verify,
> and write recovery-answer.md. Do not treat previous completion statements as proof.

The fixture setup must record exactly what was interrupted. Preserve any accidentally
partly repaired state rather than quietly resetting it to make recovery easier.

## Additional useful probes

- Add the confirming record: short ledger/no substantive model change is legitimate.
- Ask an unsupported long-horizon or wellbeing question; grounded uncertainty matters.
- Ask about previously unread details or a new case outside the summary's frame.
- Test raw drift of equal byte length, then blind field rehashing; integrity should fail.
- Withdraw an extraction by adding a replacement anchor; old citations must keep
  historical identity and readers must see the correction.
- Test selected-scope reading of a large source: full completion is not falsely claimed.
- Ask an unrelated guard question after a correction to detect collateral changes.
- Try a philosophical/interpretive corpus and a practice/observation corpus. The same
  metadata passing does not establish equivalent semantic performance across domains.

## Comparison and stopping rule

Compare the previous template, this reconstruction, and raw sources plus ordinary
search. Give them the same source snapshots, actual question wording, model/effort,
tool access, and query budgets. Record compilation separately and amortize it over a
declared realistic query count. Charge for updates/review too. Model self-reported
effort or a low word count is not measured cost. Do not hide failed runs or retries.

Freeze questions and minimum useful differences before viewing results. Use fresh
contexts, counterbalanced order, blinded answer labels, and independent evidence
grading; a grader should inspect raw support and downstream artifacts. Include new
transfer questions, a separate corpus, and an ablation of the feature credited for a
gain. Report paired outcomes, serious failures, and uncertainty; with a tiny sample
report individual cases instead of spurious statistical significance.

There is no arbitrary universal pass percentage. Source fabrication, hidden use of
withdrawn evidence, or falsely claiming completed repairs are severe failures that
cannot be averaged away with style scores. Prefer the architecture only when its
usefulness repays its total maintenance cost on the user's actual repeated tasks.

See `docs/VALIDATION.md` in the template repository for observed runs and limitations.
