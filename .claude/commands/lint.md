---
description: Run the mechanical lint script, then judgment checks; report violations
---

Run the **lint** mode.

1. **Run the script**: `python tools/lint.py` from the repo root (Windows:
   `tools\lint.cmd`). It checks the mechanical invariants — frontmatter schema and
   vocabulary, `[[link]]` and claim-anchor resolution, raw↔source coverage, index/catalog
   registration, encoding sanity (mojibake), date sanity — and emits diagnostics
   (orphans, high-importance seeds, oversized pages, stale pages, domain swelling,
   log length, `src_bytes` drift). Do not re-count by hand what the script counts.

2. **Judgment layer** — sample recent and high-importance pages for what the script
   cannot see:
   - theses that are topic labels, not claims;
   - `load_when` lines that are circular or missing a real task shape;
   - `confidence` unbacked by the citations actually on the page;
   - smoothed contradictions; laundered rhetoric or consensus tone;
   - Key Points that summarize the body instead of being its spine;
   - routing bloat: index or hub openings that stopped being decision surfaces.

3. Output a structured report: **invariant errors** (never acceptable standing state),
   then **diagnostics** (surface, don't auto-fix). Route findings into `review` or
   `refactor` — lint itself fixes nothing.

Log an entry only if the run reveals violations demanding follow-up; note the suggested
next mode.
