# Reconstruction — 2026-09-15

Built in a new workspace after auditing the supplied v2/v3 working tree. The original
was preserved. See `docs/PRIOR_AUDIT.md` for exact prior-state evidence.

## Retained

Immutable source snapshots, an agent-maintained linked wiki, a short task router,
source/inference separation, canonical ownership, scoped disagreement, economical
ingestion, and explicit recovery from interrupted work.

## Changed

- Five flexible page types and a smaller metadata contract replace the mandatory
  seven-type/importance/confidence/domain scheme.
- Source citations use exact heading anchors with checked raw locators.
- Additive integrity records catch changed bytes and reused source claim identities,
  including equal-size mutations and attempts to bless them with a new declared hash.
- Reverse-link impact traces possible downstream effects; search exposes page status
  and limited coverage, and warns on integrity failures.
- Intentional partial reading is usable within an explicit scope; unfinished reading
  remains pending. Source correction context is part of reading a claim.
- Inquiry, understanding checks, decisions, and practices connect reusable knowledge
  to the user's questions and observations without forcing a workflow on every lookup.
- Real regression tests, fresh-context development cases, migration guidance, a blank
  instance helper, and a verified Windows launcher ship with the template.

## Evidence boundary

Research contributions were inspected at their primary sources; source reputation and
popularity were not treated as proof of an architectural improvement. Mechanical
checks, agent behavior, and unmeasured comparative claims are reported separately in
`docs/VALIDATION.md`.
