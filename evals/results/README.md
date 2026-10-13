# Observed development evidence

`observed/` contains frozen copies of completed answering workspaces, their outputs,
source snapshots, tool versions, and agent-authored work records. `manifest.json`
records SHA-256 hashes of their files and verifies raw bytes against the supplied
fixtures. This is a small unblinded development comparison; see the template's
`docs/VALIDATION.md` for interpretation and limitations.

`recovery-setup/` preserves the deliberately staged interruption: the correction
snapshot and source ledger were installed, while old source notices, owner advice,
routes, registration, and sealing remained pending. The saved index, decision,
checkpoint, new ledger, and accepted integrity manifest show that state. These are
component snapshots, not a standalone complete vault. The scenario simulates an
interrupted update; no process crash was induced.

The independent semantic review is written to `REVIEW.md`. Condition labels are
visible to its grader. Development keys are available in `../GRADING.md`; they were
excluded from the answering workspaces and prompts. The grader is allowed to use them.

None of this fictional material belongs to the blank production `raw/` or `wiki/`.

## Resolving review evidence paths

The review names the original working run paths it inspected. Their frozen equivalents
ship with the template. Evidence snapshots, claim blocks, integrity records and tool versions are unchanged; three work records have local runtime paths redacted as documented below:

| Reviewed run under `evals/runs/` | Frozen copy under `evals/results/observed/` |
| --- | --- |
| current | current-initial |
| raw | raw-initial |
| prior | prior-initial |
| current-correction | current-correction |
| raw-correction | raw-correction |
| prior-correction | prior-correction |
| current-recovery | current-recovery |

The original temporary working directories are excluded from the release archive;
the frozen copies, hashes, tests, answers, and review are included.

## Publication copies — 13 October 2026

Machine-specific paths were redacted from eight historical documentation/report files for public distribution. Substantive results, fictional raw snapshots, wiki claim records, integrity records and recorded tool versions were preserved. The untouched `observed/manifest.json` records the original collected bytes; its hashes remain historical provenance rather than hashes of the three redacted work-record copies.

[publication-redactions.json](publication-redactions.json) identifies each changed file, its original SHA-256 and its publication SHA-256. To verify the published observed directory, use the publication hash for those three records and the original manifest hash for all other recorded files. The original local reports are retained privately. This redaction does not rerun or strengthen the September comparison.
