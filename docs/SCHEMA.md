# Small page contract

The executable parser is `tools/kc.py`. Markdown is ordinary editable text; no plugins
are needed. Content pages live flat in `wiki/`. The filename stem is the page title
and identity, e.g. `Attention and Effort.md`. Avoid filenames differing only in case.
`index.md`, `log.md`, and `_*.md` are operational pages without content frontmatter.

## Metadata

Start each content page with `---` on the first line. End the metadata with `---`.
Use one `key: value` per line. Supported values are plain or JSON double-quoted single-line
scalars and JSON inline string arrays such as `["Former Title", "Short name"]`.
This is a deliberately restricted YAML subset, not a general YAML parser. Do not use
multiline strings, nested maps, block lists, YAML aliases, or duplicate keys.

```yaml
---
type: note
summary: "The current point of this page and why it matters."
read_when: "The question or decision that makes this page useful."
status: current
updated: 2026-09-15
aliases: []
---
```

| Field | Meaning |
| --- | --- |
| `type` | `source`, `note`, `question`, `decision`, or `practice` |
| `summary` | A useful description/claim, not a confidence score |
| `read_when` | A concrete retrieval trigger |
| `status` | `draft` incomplete, `current` usable within scope, `contested` central judgment disputed, `superseded` historical |
| `updated` | Real ISO date of meaningful page change; not evidence freshness |
| `aliases` | Optional unique prior/alternative titles, JSON array |

`current` means editorially usable, not certainly true. A well-developed open question
may be current. Use words and reasoning to express claim-level uncertainty. There is
no mandatory importance score, confidence label, domain taxonomy, or duplicate source
list. New personal fields may be added; unknown keys are flagged for review by the
checker. Keep extensions only when useful.

### Source-only fields

```yaml
raw: "raw/2026-09-15 Study.md"
sha256: "64-character-lowercase-sha256-of-the-raw-bytes"
origin: "study-team-a/trial-1"
coverage: full
```

`raw` is one existing snapshot confined to `raw/`; use forward slashes.
`origin` identifies the evidential origin, not merely the website carrying the text.
Use the same origin for a study, its press release, and derivative summaries when
that relationship is known; describe nuances in the body. `unknown` is acceptable.
The tool does not infer independence from matching or differing strings.
`coverage` is `full` or `partial`. Partial coverage requires a nonempty `coverage_note`
field naming the inspected and excluded portions. Deliberately scoped work may be
`current` within that scope; interrupted intended coverage stays `draft`. Record
coverage details in the body when needed. Publication and acquisition dates,
URL, authorship, and extraction context belong in the source's Snapshot section.

Compute a hash without editing the source:

```powershell
(Get-FileHash -Algorithm SHA256 -LiteralPath 'raw/2026-09-15 Study.md').Hash.ToLower()
```

## Claims, citations, and locations

```markdown
### S1
The authors report the result under the specified conditions; this is not yet
a conclusion about other populations or settings.

Locator: lines 12-18

### S2
A separate source claim, with its scope preserved.

Locator: lines 23-25

## Corrections
S1 is retained as the historical source statement. Its current use is qualified
by [[Later Correction#S1]]. [Explain exactly which part changes.]
```

Use exact `### S1` headings without appended title text. Claim blocks end at the next
heading of level three or above. Put correction annotations under a separate `##`
heading, so accepted claim text can remain unchanged. Do not insert a second heading
with the same identifier, renumber existing claims, or reuse a withdrawn identifier.

Line ranges are 1-based and inclusive, measured on the decoded raw text. The tool
checks bounds, not whether the lines entail the claim. Binary/multimedia locations
use `Locator: page 4`, `Locator: timestamp 00:12:10-00:13:02`, or a precise section;
these require manual verification and produce a warning. Preserve original artifacts
and cross-check converted text where it matters.

Cite beside the supported sentence: `[[Study#S1]]`. An inference can cite several
premises and explain its bridge. `[[Study]]` routes to a page; it does not identify a
claim. For supporting derived arguments cite their actual headings, e.g.
`[[Working Model#Reasoning]]`, and retain the underlying raw support there.
Avoid circular support: linked pages do not independently verify one another.

Ordinary wiki links support optional labels: `[[Study#S1|pilot result]]`.
Anchors refer to exact Markdown heading text. Link a question without pretending it
is supporting evidence. Markdown links can point to raw files and relative documents.
Code examples and comments must not count as real citations.

A read source with no charter-relevant claims uses `disposition: "reason"` in its
frontmatter and the literal sentence `No relevant claims.` in the body. This is a
legitimate no-op, not a reason to invent an anchor.

## Integrity and dependency boundaries

`seal` accepts raw byte hashes and source claim blocks into `.kc/integrity.json`.
It adds new records, refuses changes/deletions of accepted records, and is safe to
repeat when nothing changed. Source claim hashes preserve text with line-ending
normalization. Moving annotations into a block changes its identity; keep them outside.
Keep the manifest in version control/backups along with raw and wiki. It is local
accidental-drift protection, not an authenticated or append-only storage service.

`impact` follows content-page links backwards, transitively. It excludes operational
index/log/state pages: review live index summaries separately. It does not track
exported documents or other vaults. A precise claim target narrows the
initial set; page-level references are conservative candidates. Subsequent links to
an affected interpretation may transmit the change. Navigation links can over-report;
uncited copies under-report. Inspect rather than automatically rewriting candidates.

Register every content page in the index. Source page identities remain stable after
sealing; renaming one breaks the accepted record. For other renames add the former
title to aliases, repair current links/routes, and inspect the impact. The checker
validates structure, not whether the index is a useful map.
