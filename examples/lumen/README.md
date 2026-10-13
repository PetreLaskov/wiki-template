# Worked example: a correction changes the reason for a decision

This is fictional development material, kept outside the empty production vault.
It shows the architecture operating on a small inquiry about study methods.

1. Read the [initial answer](initial-answer.md). A small glossary pilot reported
   equal accuracy and shorter time for Cards. The agent preserved causal limits
   and refused to generalize a newsletter's claim to all learning.
2. Read the [new source correction](<raw/04 Timing Correction.md>). The original
   comparison omitted setup time on one side.
3. Read the [revised answer](correction-answer.md) and the
   [decision owner](<wiki/Study Method Decision.md>). The time-saving rationale is
   withdrawn, while the provisional recommendation and unaffected evidence remain
   appropriately bounded.
4. Inspect [the original source ledger](<wiki/Definition Pilot.md>). Its issued S1/S2
   text is unchanged; a correction notice explains what remains usable and points
   to replacement evidence. [The index](wiki/index.md) reflects the current view.

From the template root:

```text
python tools/kc.py --root examples/lumen check
python tools/kc.py --root examples/lumen impact "Definition Pilot#S1"
```

The example also includes local tools and operating files, so it can be copied and
inspected separately. Its evidence and compiled state come from the completed agent
run; operating files were refreshed to the final template version. The exact observed
run remains archived under the template's `evals/results/observed/` directory.

This demonstrates correction mechanics and bounded judgment on one small case. It
does not show that the compiler outperforms raw reading or generalizes to your corpus.
