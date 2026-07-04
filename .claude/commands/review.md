---
description: Periodic consolidation pass — orphans, stubs, link rot, structural debt
---

Run the **review** mode. This is a consolidation pass; do the work, log the
result.

Procedure (canonical: `wiki/_operations.md` § 4):

1. **Orphans.** Pages with no inbound links. For each: link from a relevant
   page if it fits, merge if redundant, archive (`status: evergreen` + note) if
   obsolete, accept isolation only with strong justification.
2. **High-importance stubs.** `importance ≥ 7 ∧ status = seed`. Promote to working
   by adding key points and ≥1 cross-link, or downgrade `importance` if the
   page isn't actually important.
3. **Tag hygiene.** Tally tag frequencies. Collapse near-synonyms. Retire
   singletons that don't pull weight. Promote any tag covering >40% of
   pages (it's a domain in disguise).
4. **Broken links.** `[[X]]` where X has no page or alias. Either create
   a stub or remove the link. Don't leave broken.
5. **Domain swelling.** Any domain >30 pages: extract a synthesis if missing;
   evaluate sub-index extraction (`wiki/_operations.md` § 9).
6. **Stale pages.** `updated:` >90 days for pages contradicted or deprecated
   by recent ingests. Refresh or mark.
7. **Contested-claim audit.** Pages with `confidence: contested` — verify
   the disagreement is still live and both sides remain represented.
8. **Question backlog.** `type: question` pages older than 30 days — promote,
   retire, or re-frame.
9. **Index sanity.** Every wiki page (excl. `_*.md`) appears under exactly
   one domain header.
10. **Shape paragraph.** Re-read the index's shape paragraph. If the wiki has
    grown into a different shape, rewrite it.

Log a single `review` entry summarizing counts and actions
("5 orphans linked, 2 stubs promoted, 1 tag retired, shape paragraph
rewritten"). If a finding is too large for this pass — e.g. a domain that
needs a real refactor — note it in the log and surface it for the next
session.
