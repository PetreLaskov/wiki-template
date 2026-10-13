> Historical v2 design record, preserved from the previous public release. Its numerical instance observations were reported during that development; they were not independently revalidated for the Astra release. Current behavior is described by AGENTS.md and the main CHANGELOG.md.

# Template Changelog

## v2 — 2026-07-04 — re-architecture for compounding

v1 was written before any instance carried real load. v2 harvests what four live
instances (Carlsmith, Taft, Shamil, Shinzen; ~950 compiled pages between them)
converged on independently, and fixes the incentive bugs their pathologies exposed.

### Evidence → change

| Observed in the wild | v2 change |
|---|---|
| Big instances became 80%+ per-source summaries; thesis/question types nearly extinct (8 theses across ~950 pages); the one instance that *broke* the 1:1 source-page rule (Shamil) produced the best knowledge layer | **Delta-first ingest**: owner pages updated first; source pages become short provenance ledgers with a **novelty budget** (length scales with model delta) |
| Only the instance with a written purpose had healthy page economics; two big instances wrote their own charters from scratch; one never filled the placeholder and drifted | **Charter is mandatory and structured** (question classes, source tiers, page economics); new **charter mode** + `/charter` command; ingest on an uncharted wiki must charter first |
| Instances independently invented `load_when:` frontmatter, "Load Next By Task" index tables, Decision Map sections, hub pages with child-ownership semantics, and claim anchors (S1…Sn) | All canonicalized: `load_when` required, index is a **router** with a Load Next By Task table, **hub role** with Decision Map + ownership ("one claim, one home"), **claim-anchor citations** |
| Status ladder dead everywhere (97% stuck at `working`); emoji/status vocabulary drift; encoding mojibake shipped in wiki pages and even an index | Status collapsed to **`seed | live`**; **`tools/lint.py`** ships with the template — schema/vocab, links+aliases, anchors, raw coverage, registration, **mojibake detection**, plus the review disposal queue |
| Logs grew unbounded (8,787 lines in one instance); one instance capped session log-reads on its own | **Log rotation** at review (~200 entries → `_log-archive-YYYY.md`); session start reads newest ~10; fixed first-read budget in the contract |
| Every big instance improvised batch machinery (`_automation_loop_state.md`, `_ingestion_state.md`, wave plans, gates) | **Batch protocol** first-class: `wiki/_state.md` convention, waves of 5-10, lint gate per wave, conservative autonomous defaults |
| Index bloat forced one instance to invent `_page_catalog.md`; an external audit found "routing bloat, not evidence discipline" was the top blocker | **Catalog extraction** at ~150+ pages; index keeps fixed-size State of the Model (≤300 words) + routing; scaling happens at the bottom of the pyramid |
| mtime-based re-ingest was fragile across copies/Windows | Optional **`src_bytes`** fingerprint on source pages; lint flags drift as re-ingest candidates |
| Tags empty in the big instances; three orthogonal axes over-specified | Tags demoted to optional; the task axis (`load_when`) replaces them as the retrieval dimension |
| AI-generated research reports entering corpora as if primary evidence | Source posture: reliability tiers per source page (usable-for / not-usable-for); AI-generated surveys are falsifiable interpretive priors, never primary evidence |

### Objective function

v1: "maximize future reasoning quality per token loaded" (read side only).
v2 adds the write side — "maximize model improvement per unit of compilation effort" —
and the acid test: *the wiki must beat raw+grep for the charter's question classes,
at a fraction of the tokens, or it is overhead.*

### Migrating a live instance (selective, in value order)

1. **Copy `tools/lint.py` + `tools/lint.cmd`** and run `python tools/lint.py --legacy`.
   Costs nothing, finds real rot (encoding corruption, broken links, unregistered
   pages) immediately. `--legacy` tolerates old status vocabulary and missing
   `load_when`.
2. **Write the charter** into `## Charter` in `index.md` if absent (Taft/Shinzen can
   lift theirs from AGENTS.md § Purpose; reconcile with any `_shape.md`).
3. **Adopt the novelty budget going forward** — stop writing long source essays for
   low-delta sources. No retro-editing needed; the ratio heals as ingestion continues.
4. **Add `load_when:` opportunistically** — on every page you touch anyway, and in one
   pass over the top ~30 pages by importance.
5. **Rotate the log; cap session log-reads at ~10 entries.**
6. Status vocabulary, claim anchors on old source pages, catalog extraction: only when
   review pressure actually demands them. Don't bulk-migrate for its own sake.

## v1 — 2026-04-28

Initial template: compiler abstraction, seven types, compression gradient, six modes,
prose lint invariants, four-state status lifecycle.
