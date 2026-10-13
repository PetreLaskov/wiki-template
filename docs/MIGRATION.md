# Migration and rollback

## This reconstruction

The referenced prior folder was inspected read-only. The new implementation is in this
workspace. Its production `raw/` and `wiki/` are blank. The prior checkout currently
contains no substantive corpus pages to migrate; its uncommitted implementation changes
were audited as they stood. See `PRIOR_AUDIT.md` for the snapshot and limitations.

Create a separate instance for each purpose. Do not overwrite a populated vault with
this template. Keep a verified copy or version-control checkpoint of the original,
including user edits, raw assets, logs, and unfinished work. Rollback means returning
to that preserved copy; the new tooling does not rewrite old raw files.

## Populated v2/v3 vaults

Migrate a small representative set first, then the remainder. This guide deliberately
does not auto-convert prose citations: a syntax replacement cannot verify their meaning.

1. Inventory the original and hash raw files before copying. Copy evidence bytes and
   preserve paths; include assets, metadata, source dates, and extraction relationships.
2. Preserve the actual purpose, question routes, user constraints, open questions,
   decision history, and pending checkpoint. Do not reset a real charter to bootstrap.
3. Convert page frontmatter using the mapping below. Preserve useful custom metadata
   where it serves a purpose; unknown keys may produce review warnings.
4. Convert source claims to `### S1` blocks **without renumbering**. Keep exact claim
   meaning and add verified raw locators. Convert `([[Source]] S1)` to `[[Source#S1]]`.
   Expand suffix ranges or lists only after inspecting every cited claim. Missing or
   reused identifiers are repair work, not permission to guess.
5. Retain withdrawn claims and place disposition/correction notes outside frozen blocks.
   Establish shared origins from evidence, using `unknown` where unresolved. Mark
   partially read sources partial with an explicit `coverage_note`; use draft for
   unfinished intended coverage. Do not backfill full coverage from page presence.
6. Register pages in the index; repair links and aliases. Review affected arguments,
   decisions, and routes against the original, preserving significant user judgments.
7. Run `check`, inspect the diff and semantic samples, then `seal` and `check`. A new
   seal establishes a baseline from the migrated state; it does **not** verify the
   historical identities of source claims or prove fidelity to the old snapshot.
8. Try recurring questions, a correction, and cold recovery before making the new
   instance the default. Compare costs and errors. Preserve the original until useful
   operation and rollback are established.

| Old | New | Judgment required |
| --- | --- | --- |
| `type: source` | `type: source` | Verify raw binding and coverage |
| concept/entity/thesis/synthesis/analysis | `type: note` | Keep role in prose; preserve canonical ownership |
| question | question | Preserve inquiry status separately from page status |
| `thesis` | `summary` | May be descriptive; do not fabricate a strong thesis |
| `load_when` | `read_when` | Preserve useful task trigger |
| `seed` / `live` | draft / current | Current only after content inspection |
| `sources: [raw/...]` on source | `raw: raw/...` | One source snapshot per ledger |
| `src_sha256` | `sha256` | Compare raw bytes, not just field names |
| `confidence: contested` | status contested if central judgment is contested | Keep local uncertainty scoped |
| importance/domain/confidence | optional prose or useful custom field | Remove only if no longer serving retrieval/judgment |

The current source filename is its stable identity after sealing. Keep old titles for
source pages; use aliases for alternative names. Derived pages can be reorganized with
aliases, repaired links, and dependency review. Historical log prose remains history.

## Operational limits

The toolkit assumes one writer for a vault. Filesystem backup, encrypted storage,
version control, synchronization conflict handling, and access management are outside
the compiler. A cloud-synced folder can create conflicting copies; inspect conflicts
before resuming and do not merge accepted manifests blindly. No sources are transmitted
by these Python tools; any agent/model access follows the environment you run it in.
