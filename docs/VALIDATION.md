# Validation record — 2026-09-15

This report separates observed software behavior, agent development cases, and claims
that remain unmeasured. The implementation and the development runs below are complete.

## Environment and reproducibility

- Host: Windows; Python 3.12.14 from the bundled runtime.
- Runtime used: `<bundled-python>`.
- No Python package installation, model API integration, graph database, or external
  service is required by the toolkit.
- Bare `python` was not available on PATH; the registered `py -3` interpreter was
  inaccessible in this sandbox. The included PowerShell launcher successfully used
  the bundled interpreter for `check` and `search`. It does not change execution policy.

```powershell
./tools/kc.ps1 check
# With an available Python 3.10+:
python -m unittest discover -s tests -v
python tools/new_instance.py "C:\path\to\new-absent-folder"
```

## Software checks observed

58 tests discovered: **55 passed, 3 skipped**. The skipped tests exercise real raw-file,
raw-directory, and integrity-directory symlink escapes; this Windows process lacks
the privilege to create symlinks (WinError 1314). Ordinary path traversal checks and
a portable guarded-walk test proving unsafe directories are pruned both passed.
Real symlink behavior is therefore not fully exercised on this host.

Covered behavior includes:

- blank bootstrap and missing/mistyped instance roots;
- populated pages cannot retain the known bootstrap marker;
- metadata types/dates, duplicates, aliases, anchors, locators, and page registration;
- every citation occurrence, including an invalid second citation;
- equal-size raw mutation, blind declared rehashing, deleted/reused source identifiers,
  source rebinding, and refusal to overwrite an accepted integrity record;
- legitimate correction annotations without changing frozen claim blocks;
- exact-claim and transitive impact, with unrelated source claims excluded initially;
- explicit limited coverage, pending work visibility, deterministic bounded search;
- source/page confinement, concurrent seal lock, no-op seal, and safe blank creation.

An independent code review found that copying a live bootstrap index/log could carry
private charter/history text into a new instance. The factory now generates pristine
contents instead, with a regression for personalized bootstrap files. Operating
instructions are intentionally reused; the helper makes no blanket privacy claim
about arbitrary custom instructions.

Production template: **0 errors, 0 warnings; 0 content pages, raw sources, or claims**.
These checks validate syntax and local integrity. They do not prove citation entailment,
complete correction propagation, trustworthy originals, or improved understanding.

## Agent development runs

Initial and correction conditions are run by separate fresh subagent contexts against
isolated directories created by the supplied helpers. Answering agents receive the
workspace and task, not grading keys or this reconstruction conversation. They use
local tools only; no browsing or further delegation. They inherit the same parent
model and reasoning configuration; the tool interface does not expose an exact
backend version or per-agent token accounting for this report.

This is a **development comparison**, not a controlled benchmark: no identical hard
tool/token budget was enforced, initial compilation is additional work, conditions
are not repeated/counterbalanced, and all questions come from this small development
fixture. Grading must inspect actual files; answer quality alone is insufficient.

| Run | State |
| --- | --- |
| Raw sources, initial inquiry | Completed; substantive answer criteria met in independent review |
| Reconstructed compiler, initial inquiry | Completed: 4 pages, 6 source claims, 0 errors/warnings |
| Previous template, initial inquiry | Completed: 4 pages, 0 errors/warnings |
| Raw sources, correction in fresh context | Completed; substantive answer criteria met in independent review |
| Reconstructed compiler, correction in fresh context | Completed: 5 pages, 8 source claims, 0 errors/warnings |
| Previous template, correction in fresh context | Completed: 5 pages, 0 errors/warnings |
| Reconstructed compiler, staged interruption recovery | Completed: 5 pages, 8 source claims, 0 errors/warnings; independent recovery review passed |

Observed answers, operating files, sources, and tool versions are frozen under
`evals/results/observed/` with SHA-256 file manifests. All raw snapshots in the seven
completed runs match the supplied fixture bytes. Initial/correction copies have no
answer-file continuity; wiki conditions retain their compiled pages and history.

The initial compiled content was 1,236 words in the reconstruction and 1,424 in the
previous template; after correction, 1,802 and 2,102 respectively. These whitespace
word counts include metadata and **are not** tokens, reading volume, or cost savings.
Both produced four initial content pages and five after the correction. Raw reading
required no wiki. These observations do not establish an efficiency advantage.

The current initial run used the tool revision just before the final empty-claim and
directory-pruning refinements; later reconstructed runs use the final checker. Each
observed run retains its actual tool bytes in the manifest. The blank factory's
privacy fix was made after initial setup and does not retroactively change those runs.

Recovered execution problems remain in the agent-authored work records: missing `.kc`
on an initial inventory command, rejected duplicate-target patches, and an initial
old-template claim-format lint failure. They are not omitted from the record. These
work records are not full independent tool telemetry.

## Independent semantic findings

[The independent review](../evals/results/REVIEW.md) inspected actual evidence chains,
answers, stored conclusions, source summaries, correction notices, routes, checkpoints,
and integrity records. **No severe failure was found across the seven runs.** The six
initial/correction answers satisfy the substantive fixture expectations. One minor
unsupported simplicity assertion in the prior initial owner is recorded as a partial
calibration grade; it is too small and unreplicated to establish a condition effect.

Both wiki versions propagated the correction, retained unaffected evidence, preserved
issued source claims, and kept historical log content. The reconstruction preserved
all six original claim blocks and accepted manifest entries; the previous template
preserved all nine issued claim lines through agent diligence. Raw-source reading
also answered both stages correctly. **There is no demonstrated winner on general
answer quality or total cost in this small comparison.**

For recovery, the operator deliberately installed a correction ledger while leaving
old source notices, owner advice, index registration, and sealing unfinished. A fresh
agent recovered from that checkpoint, completed the affected updates, retained raw
bytes and old claims, and left the retention/wellbeing guard answer unchanged. The
reviewer independently verified the completed state and reran the checker. This is
**staged interrupted-update recovery**, not induced process-crash or transactional
failure testing. The setup snapshot and completed run are preserved in the evidence.

The [worked example](../examples/lumen/README.md) presents the initial and corrected
views for inspection. It passes the final checker with 5 pages, 4 raw snapshots,
8 source claims, and zero errors/warnings. The pristine template and a separately
generated fresh instance also pass. Saved output: [software tests](../evals/results/software-tests.txt),
[blank check](../evals/results/blank-check.json), and
[fresh-instance check](../evals/results/fresh-instance-check.txt).

## Unmeasured / deliberately not claimed

- Superiority over raw search or the previous template on representative repeated work.
- Sustained gains in this user's learning, wisdom, decisions, or agency.
- Performance across philosophical interpretation, contemplative practice, and other
  domains with different kinds of warrant.
- Large-corpus runtime/memory performance, retrieval recall, calibration, and costs.
- Long-horizon corrections, adversarial tamper resistance, or concurrent vault editing.

The implementation is intended for modest personal vaults, one writer at a time.
The commands currently load/hash the corpus on each invocation. Source assertions,
semantic independence, freshness, useful framing, and uncited dependents remain
editorial responsibilities. `seal` protects against accidental drift within a trusted
local history; modifying/deleting its manifest outside the tool defeats that protection.


## Public release verification — 13 October 2026

The assembled publication copy was checked again: 55 software tests passed, 3 Windows symlink tests skipped, and the blank template, factory-created fresh instance and Lumen example all reported zero errors and warnings. [Release verification](RELEASE_2026-10-13.md) records the scope and commands. The September behavioral comparison above remains historical; its agent conditions were not rerun. Local machine paths in historical reports are redacted in publication copies, with original and publication hashes documented in [the evidence directory](../evals/results/README.md).
