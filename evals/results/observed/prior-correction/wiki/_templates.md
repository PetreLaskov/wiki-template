# Page templates

Copy only what the page needs. Replace all placeholders and choose confidence from
evidence. Do not preserve explanatory scaffolding, empty sections, or invented links.
The common page fields are owned by `AGENTS.md`.

## Metadata syntax

The dependency-free validator supports a deliberately small YAML subset:
- One `key: value` per line; single-line plain, single-quoted, or double-quoted scalars.
- Inline lists such as `domain: [retrieval, evaluation]`, or indented dash lists.
- Quote strings containing YAML punctuation, commas inside list items, or ambiguous
  values. Use forward slashes in raw paths. Use doubled apostrophes inside single quotes.
- No nested maps, multiline scalars (`|` or `>`), anchors, YAML aliases, duplicate keys,
  or unrecognised fields. The validator reports unsupported syntax instead of guessing.
- Required list fields: `domain` (nonempty), `aliases`, `sources`.
  Optional list: `tags`. `importance` is an integer 1–10; optional `src_bytes` is
  nonnegative. Optional `src_sha256` is a 64-character hexadecimal digest.
- Use real ISO dates. No content frontmatter on index, log, or underscore system files.

Wiki links: `[[Page Title]]` or `[[Page Title|label]]`. Prefer canonical titles.
Source claim citations: `([[Source Ledger]] S2)`, or a contiguous range
`([[Source Ledger]] S2–S4)` only when every claim in that range supports the text.
A Markdown heading link is navigation, not an S# evidence citation.
Code samples and HTML comments do not count as citations or registration.

## Shared frontmatter

```yaml
---
type: concept
thesis: "[Precise claim plus significance, not a topic label.]"
load_when: "[Task whose answer changes after reading this page.]"
status: seed
domain: [primary]
importance: 5
confidence: speculative
aliases: []
sources: []
updated: YYYY-MM-DD
---
```

`speculative` is a conservative placeholder, not a recommended permanent confidence.
Select the correct type, status, domain, confidence, sources, and actual date.
Empty sources on derived pages require a Pure synthesis note and supporting page
citations. A question may have no sources. A source ledger must name exactly one raw file.

## source

Add `src_sha256` to the shared frontmatter and optionally `src_bytes`.
SHA-256 hashes bytes, not decoded or reformatted text. For example:

```powershell
(Get-FileHash -Algorithm SHA256 -LiteralPath 'raw/source.md').Hash.ToLower()
```

```markdown
[Origin, date, format, and why this source matters, in one sentence.]

## Snapshot
- Origin: [author/organisation, publication and acquisition context if known]
- Coverage: [fully read, including relevant assets; otherwise keep ingest pending]
- Evidence posture: [primary record / interpretation / derivative / AI-generated]
- Depends on: [actual evidential origins, or independence unknown]
- Usable for: [claims this source can support]
- Not usable for: [extrapolations it cannot establish]

## Key Claims
- **S1** — [Faithful, scoped source claim.] Locator: [section + paragraph, lines,
  page or timestamp within the fingerprinted raw]. Owner: [[Owner Page]].
- **S2** — [Another material claim.] Locator: [precise location].
  Disposition: [ledger-only because peripheral or confirming; no forced owner].

## Model Delta
[Changed / confirmed / qualified / challenged / no material change, with owner and
dependent pages affected. Distinguish source statement from compiler inference.]

## Audit
- Weakest support: [specific claim and why; or none material identified]
- Important omissions: [limits affecting this charter]
- Tensions/corrections: [scoped disagreement or withdrawn S# and replacement evidence]

## Related
- [[Owner Page]] — [what this evidence changes there]
```

Keep confirming ledgers short. For an assessed source without relevant claims, replace
Key Claims with **No material claims** and a concrete disposition; do not invent S1.
A withdrawn claim keeps its original ID and meaning, labelled withdrawn, with a pointer
to the correction. Do not renumber surviving claims or reuse retired IDs.

## concept / entity

Use a concept for a distinction or mechanism, an entity for a real thing whose
identity or role matters repeatedly. Change the common `type` accordingly.

```markdown
[Definition and significance, one or two sentences.]

## Key Points
- [Central scoped claim.] ([[Source Ledger]] S1)
- [Operational consequence or distinguishing boundary.] ([[Source Ledger]] S2)

## Reasoning and evidence
[Mechanism, examples, or accumulated facts; distinguish inference from source claims.
Include disagreements where their interpretation matters.]

## Boundaries
[Only if misuse or scope confusion is plausible.]

## Related
- [[Relevant Page]] — [why loading it changes interpretation]
```

A seed can stop after one substantive point and a useful connection where one exists.
An entity does not earn a page merely because a source names it.

## thesis

```markdown
[Argued conclusion and governing reason.]

## Key Points
- Evidence: [premise.] ([[Source Ledger]] S1)
- Inference: [step from evidence to conclusion, with scope.]
- Limit: [strongest credible counterconsideration.]

## Argument
[The case and its strongest alternative, judged by the same evidence standard.]

## What would change the conclusion
[A concrete finding or value/constraint change, and how the judgment would move.]

## Related
- [[Premise Owner]] — [claim used in this argument]
```

Keep defeated claims distinguishable from current conclusions. A successor page is
warranted only if it serves retrieval better than revising the existing thesis.

## synthesis / hub

```markdown
[The through-line that organises this domain.]
Pure synthesis: [if sources is empty, identify the existing pages used as premises.]

## Key Points
- [What the evidence collectively supports.] ([[Source Ledger]] S1)
- [Boundary, tension, or missing connection.]

## Decision Map
| Task | Load | Owned claim and guardrail |
| --- | --- | --- |
| [Concrete question] | [[Owner Page]] | [What it owns; what not to infer] |

## Through-line
[Why these findings belong together, and the inference the map supports.]

## Open frontiers
[Consequential unknowns; link a question page only if one exists and earns retrieval.]

## Related
- [[Owner Page]] — owns [specific claim family]
```

A hub routes; children own depth. Brief supported summaries are useful redundancy,
but independently maintained duplicate arguments are not.

## analysis

```markdown
**Question:** [Recurring question.]

**Answer:** [Judgment and governing reason.]

## Key Points
- [Load-bearing reason.] ([[Source Ledger]] S1)
- [Decisive qualification or uncertainty.]

## Reasoning
[Evidence, inferential steps, and relevant alternatives.]

## Revision condition
[What would change the answer; missing evidence if decisive.]

## Related
- [[Owner Page]] — [premise used]
```

Prefer updating an existing answer over filing a near duplicate.

## question

```markdown
**Question:** [Precise unresolved issue.]

**Why it matters:** [Which decision/conclusion changes if answered.]

## What we know
- [Relevant evidence, scoped and cited; absence of evidence if that is the finding.]

## What would resolve it
[Discriminating evidence or test, feasible next source, and how outcomes change judgment.]

## Status
Open. [Or Partial, Resolved → existing answer, or Retired with a reason.]

## Related
- [[Affected Owner]] — [what would change]
```

The body’s inquiry status is separate from `status: seed | live`, which describes
page development. A well-developed map of an open question may be live.
