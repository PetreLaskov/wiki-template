# Prior template audit

Audited 2026-09-15. Scope: the actual working tree at
`<prior-template>`.
The original was read only. Disposable probes used an isolated temporary directory.

## Conclusion

The prior version has a sound evidence and retrieval philosophy. Its main weakness
is the gap between the operating promises and executable enforcement. Preserve the
useful principles, reduce routine bookkeeping, and make integrity, pending work, and
change impact visible through tools. No evidence from this audit establishes that a
reconstruction improves reasoning or saves total time on a real personal corpus.

## What was actually present

- Git HEAD: `fc5e415` (`v2: re-architect for compounding — delta-first ingest, routing
  layer, mechanized lint`). The working tree contains uncommitted v3 rewrites and new
  documentation/evaluation files. HEAD alone is not the user's latest implementation.
- Production `raw/` has no sources; `wiki/` contains only index, log, operations, and
  templates. This is a blank template, not a populated knowledge base to migrate.
- `tools/lint.py` exists (25,153 bytes), and an evaluation pack exists. Older reports
  that these were absent do not describe the current working tree.
- No `tests/` directory exists. Three documents linked by README are absent:
  `docs/VALIDATION.md`, `docs/RECONSTRUCTION_RESULTS.md`, `docs/MIGRATION_V3.md`.
- The index records a September 10 v3 refactor; the newest log event remains the
  July 4 v2 initialization. Completion records are inconsistent.

## Capabilities worth preserving

| Capability | Why it earns a place | Prior evidence |
| --- | --- | --- |
| Charter and task-based routing | Organizes the corpus around recurring useful questions rather than accumulating summaries. | `AGENTS.md:32–65`; `wiki/index.md` |
| Source statements distinguished from interpretation and inference | Keeps fluent summaries from acquiring more authority than their evidence. | `AGENTS.md:67–94` |
| Source independence and scoped disagreement | Derivative retellings are not replication; different populations or metrics are not automatically contradictory. | `AGENTS.md:69–75`; `wiki/_operations.md`, “Disagreement and correction” |
| Canonical claim ownership | Reduces independently maintained copies of the same conclusion. Brief routing summaries remain useful. | `AGENTS.md:75–79` |
| Immutable evidence, SHA-256, stable source claim identities | Gives future agents something specific to inspect and supports correction without silently changing old citations. | `AGENTS.md:17–20,80–85,132–134` |
| Delta-first ingest and warranted no-op | A confirming source need not produce a new essay or invented theory. | `wiki/_operations.md`, “One coherent unit” |
| Recovery checkpoints and one integrator | A fresh agent can resume multi-file work without trusting completion reports. | `AGENTS.md:145–151`; `wiki/_operations.md`, “Batch and recovery” |
| Honest evaluation boundaries | Explicitly distinguishes structural checks, semantic smoke tests, and evidence of comparative usefulness. | `AGENTS.md:181–187`; `evals/README.md`; `evals/rubric.md` |
| Thin agent adapters | Prevents competing procedures in AGENTS, CLAUDE, and command files. | `CLAUDE.md`; `.claude/commands/ingest.md` |

These are valuable design choices, not empirically proven advantages. The changelog
reports experience from four populated instances, but this audit did not inspect those
instances or reproduce its numerical claims.

## Confirmed gaps and priorities

### P1 — The advertised verification release is incomplete

`README.md:50–69,91` promises tests and links to validation/results/migration documents.
The test command fails because `tests/` is absent; the three linked documents are
missing. The blank template's passing lint result says nothing about nonempty behavior.

**Repair:** ship and run focused positive and negative regression tests, complete the
linked documentation, and publish measured results separately from planned scenarios.

### P1 — Changed raw evidence does not fail the mechanical gate

The checker computes SHA-256 correctly, including equal-length edits. However,
`tools/lint.py:415–417` classifies both missing hashes and hash drift as warnings.
`tools/lint.py:497` exits nonzero only for errors. Changing `40` to `90` in a
fingerprinted source returned zero errors and one `hash-drift` warning.

This is a weak automated gate rather than a claim that the prose permits ignoring
drift: the prose explicitly tells agents to investigate. A careless caller checking
only exit status can nevertheless treat altered evidence as verified.

**Repair:** unresolved fingerprint changes should fail a strict integrity check.
Retain a prior baseline so blindly refreshing metadata does not erase detection.
Do not treat a hash as recovery of unavailable old source text.

### P1 — Evidence promises lack persistent enforcement

The current checker verifies claim identifiers in the current ledger, but has no
previous identity baseline. It cannot detect an issued S1 silently being reassigned
to a different claim. It also does not require a raw locator: removing the entire
`Locator: line 1.` clause from a valid ledger returned zero errors and warnings.

**Repair:** use an unambiguous anchor format, machine-checkable locator syntax and
bounds, and an append-only record of issued claim identities. Keep withdrawal or
correction annotations possible without reassigning the original claim. Mechanical
checks still cannot establish that the cited passage entails the wording.

### P2 — Bootstrap detection accepts its own placeholder after ingest

`tools/lint.py:265–266` rejects a short list of placeholder expressions, but the actual
blank index starts “Bootstrap: no sources have been compiled.” Registering two valid
content pages while retaining that exact charter returned zero errors and warnings.

**Repair:** represent bootstrap/active state explicitly and validate the transition;
do not infer lifecycle state from a few prohibited prose phrases. Charter usefulness
still requires human or agent judgment.

### P2 — Citation parser ignores subsequent suffix anchors

`tools/lint.py:376` reads only the first suffix citation after a wiki link.
`([[Evidence]] S1, S999)` passed although S999 does not exist. The control
`([[Evidence]] S999)` correctly failed with `claim-anchor`.

**Repair:** give each claim a separate explicit link, such as `[[Evidence#S1]]`.
Reject or fully parse the supported grammar. Do not silently accept partly parsed
citations. This probe uses an ambiguous extension of the documented examples, so it
is a robustness issue, not evidence that ordinary single-anchor citations are broken.

### P2 — Change impact and recovery depend on manual diligence

The contract explains correction propagation well, but the implementation supplies no
impact traversal or checkpoint checker. `_state.md` is loaded as a system file but its
pending work is not validated. An agent can pass lint with stale dependent conclusions
or forgotten work; semantic correctness cannot be inferred from file existence.

**Repair:** expose inbound dependencies and unfinished operations as inspectable
tool output. Treat the resulting dependency list as an aid to judgment: a link graph
is not proof of semantic dependence, and missing links remain a risk.

## Complexity to remove or make optional

- Ten mandatory metadata fields impose work on every page. `importance: 1–10`,
  page-wide confidence labels, mandatory domains, and empty alias lists do not earn
  universal enforcement. Preserve useful retrieval intent and provenance; make other
  classification optional or express claim-specific uncertainty in prose.
- Seven content types ask agents to distinguish concept/thesis/synthesis/analysis
  before the distinctions have demonstrated retrieval value. Fewer content types can
  carry the same arguments through useful titles and headings.
- The contract is about 1,614 whitespace-delimited words; operations add 1,756 and
  templates 1,094. These are word counts, not token measurements. Keep the everyday
  contract short and load correction/migration/evaluation procedures when needed.
- Inbound-link, age, size, and page-count heuristics are review prompts. They should
  not pressure agents to manufacture links or rewrite sound material merely to clear
  a warning. The prior prose recognizes this; defaults should reinforce it.
- A source index plus search should remain the low-overhead option. Additional
  compilation should earn its cost through repeated use, corrections, and actual
  retrieval problems rather than a universal schema requirement.

## Checks executed

Python executable:
`<bundled-python>`.
`-B` avoided writing bytecode to the original repository.

| Check | Observed result |
| --- | --- |
| `python -B tools/lint.py --json` on actual prior tree | Exit 0; 0 errors, 0 warnings, 0 content pages, 0 raw files, 1 log event. |
| `python -B -m unittest discover -s tests -v` | Exit 1; `ImportError: Start directory is not importable: 'tests'`. |
| Isolated valid two-page corpus retaining prior bootstrap charter | 0 errors, 0 warnings. |
| Same fixture; equal-byte-length source mutation `40` → `90` | 0 errors; `hash-drift` warning. |
| Same fixture; undefined second suffix anchor S999 | 0 errors, 0 warnings. |
| Control: undefined first suffix anchor S999 | `claim-anchor` error. |
| Same fixture; raw locator removed | 0 errors, 0 warnings. |

The fixture used a SHA-256-fingerprinted one-line source, one source ledger, one
analysis page, mutual links, and both pages registered in the index. Each mutation
was applied separately and reset before the next. These are focused mechanical
probes, not behavior evaluations, adversarial security certification, or a comparison
of answer quality.

## Migration constraints

1. Preserve the original working tree, including its uncommitted changes. A new
   reconstruction should live separately until the user chooses to adopt it.
2. This particular template has no production corpus to migrate. Do not confuse the
   fictional `evals/fixtures` evidence with the user's knowledge.
3. For populated instances, preserve raw bytes, original source claim meanings,
   aliases, human decisions, and historical logs. The wiki is not deterministically
   regenerable from raw files: it also contains judgments and user choices.
4. Convert old `([[Source]] S1)` references deliberately; inspect aliases and ranges.
   Preserve old locators tied to their original fingerprints. Do not manufacture line
   numbers for PDF pages or audiovisual timestamps without a traceable extraction.
5. Prefer staged, reported migration. A current hash establishes the inspected
   snapshot; it cannot retroactively prove earlier evidence was immutable.
