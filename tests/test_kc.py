"""Regression checks for evidence corruption and workflow failure boundaries.

Run: python -m unittest discover -s tests -v
These tests establish mechanical behavior, never source entailment or usefulness.
"""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import kc


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="kc-test-")
        self.root = Path(self.temporary.name)
        (self.root / "wiki").mkdir()
        (self.root / "raw").mkdir()
        self.write("wiki/index.md", "# Index\n")
        self.write("wiki/log.md", "# Log\n")

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8") if isinstance(text, str) else text)
        return target

    def page(self, title, body="A useful note.\n", **metadata):
        values = {"type": "note", "summary": f"Summary of {title}.", "read_when": "Investigating this topic.",
                  "status": "current", "updated": "2026-09-15"}
        values.update(metadata)
        text = "---\n" + "".join(f"{key}: {json.dumps(value, ensure_ascii=False)}\n" for key, value in values.items()) + "---\n\n" + body
        target = self.write(f"wiki/{title}.md", text)
        titles = sorted(p.stem for p in (self.root / "wiki").glob("*.md") if p.stem not in {"index", "log"} and not p.stem.startswith("_"))
        self.write("wiki/index.md", "# Index\n\n" + "\n".join(f"- [[{name}]]" for name in titles) + "\n")
        return target

    def source(self, title="Source", body=None, raw="raw/source.txt", **metadata):
        if not (self.root / raw).exists():
            self.write(raw, "Alpha statement.\nSecond statement.\n")
        values = {"type": "source", "raw": raw,
                  "sha256": hashlib.sha256((self.root / raw).read_bytes()).hexdigest(),
                  "origin": "original interview", "coverage": "full"}
        values.update(metadata)
        if body is None:
            body = f"# {title}\n\n### S1\n\nAlpha statement.\n\nLocator: lines 1-1\n\n## Corrections\n\nNone.\n"
        return self.page(title, body, **values)

    def workspace(self):
        return kc.Workspace(self.root)

    def codes(self, workspace=None):
        return [issue.code for issue in (workspace or self.workspace()).issues]

    def invoke(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = kc.main(["--root", str(self.root), *args])
        return code, stdout.getvalue(), stderr.getvalue()

    def assert_valid(self):
        workspace = self.workspace()
        self.assertEqual([], [i.as_dict() for i in workspace.errors])
        return workspace

    def assert_sealed(self):
        result = self.invoke("seal")
        self.assertEqual(0, result[0], result)
        return json.loads((self.root / ".kc/integrity.json").read_text())

    def test_empty_workspace_passes_without_warnings(self):
        self.assertEqual([], self.workspace().issues)
        code, output, _ = self.invoke("check", "--json")
        self.assertEqual(0, code)
        self.assertEqual(0, json.loads(output)["errors"])

    def test_arbitrary_empty_directory_does_not_pass_as_instance(self):
        (self.root / "wiki/index.md").unlink()
        (self.root / "wiki/log.md").unlink()
        self.assertIn("index.missing", self.codes())
        self.assertIn("log.missing", self.codes())

    def test_compiled_pages_cannot_keep_bootstrap_charter_marker(self):
        self.page("Note")
        self.write("wiki/index.md", "# Index\n\n**State: bootstrap.**\n\n[[Note]]\n")
        self.assertIn("charter.bootstrap", self.codes())

    def test_valid_source_alias_and_exact_ordinary_heading(self):
        self.source(aliases=["Primary interview"])
        self.page("Decision", "## Conclusion\n\nEvidence [[Primary interview#S1|original statement]].\n")
        self.page("Practice", "Use [[Decision#Conclusion]] when relevant.\n", type="practice")
        self.assert_valid()

    def test_every_citation_is_checked_including_second_invalid_claim(self):
        self.source()
        self.page("Note", "[[Source#S1]] and [[Source#S999]] and [[Source#S998]].\n")
        issues = [i for i in self.workspace().issues if i.code == "link.anchor"]
        self.assertEqual(2, len(issues))
        self.assertTrue(any("S999" in i.message for i in issues))
        self.assertEqual(1, self.invoke("check")[0])

    def test_missing_page_is_not_silently_treated_as_external(self):
        self.page("Note", "See [[Unwritten page]].\n")
        self.assertIn("link.page", self.codes())

    def test_code_examples_comments_and_indented_code_are_inactive(self):
        self.page("Note", "# Note\n\n`[[Missing]]` and ``code ` [[Missing#S1]]``.\n\n```markdown\n### S1\n[[Absent]]\n[bad](../../outside)\n```\n\n~~~\n[[Unknown]]\n~~~\n\n    [[Indented]]\n\n<!-- [[Comment]] -->\n")
        self.assert_valid()

    def test_duplicate_source_ids_are_errors(self):
        self.source(body="### S1\nFirst.\nLocator: lines 1-1\n\n### S1\nSecond.\nLocator: lines 2-2\n")
        self.assertIn("heading.duplicate", self.codes())
        self.assertEqual(1, self.invoke("seal")[0])

    def test_claim_ids_require_exact_level_three_headings(self):
        for heading in ("## S1", "### S1 a summary", "### S01", "### S1#", "### S1 ###"):
            with self.subTest(heading=heading):
                self.source(body=f"{heading}\nStatement.\nLocator: lines 1-1\n")
                self.assertIn("claim.heading", self.codes())

    def test_duplicate_ordinary_headings_and_aliases_are_errors(self):
        self.page("First", "## Repeat\nOne.\n## Repeat\nTwo.\n", aliases=["Shared"])
        self.page("Second", aliases=["shared"])
        codes = self.codes()
        self.assertIn("heading.duplicate", codes)
        self.assertIn("alias.duplicate", codes)

    def test_alias_cannot_shadow_a_title(self):
        self.page("First", aliases=["Second"])
        self.page("Second")
        self.assertIn("alias.duplicate", self.codes())

    def test_all_content_pages_need_index_registration(self):
        self.page("Note")
        self.write("wiki/index.md", "# Index\n")
        self.assertIn("index.unregistered", self.codes())
        (self.root / "wiki/index.md").unlink()
        self.assertIn("index.missing", self.codes())

    def test_operational_pages_are_metadata_exempt_but_links_checked(self):
        self.write("wiki/_state.md", "# Recovery\n\nPending work.\n")
        self.assert_valid()
        self.write("wiki/_state.md", "Missing [[Missing]].\n")
        self.assertIn("link.page", self.codes())

    def test_flat_wiki_is_enforced(self):
        self.write("wiki/nested/Hidden.md", "Hidden content.\n")
        self.assertIn("wiki.flat", self.codes())

    def test_malformed_and_duplicate_frontmatter_are_errors(self):
        self.write("wiki/Broken.md", "---\ntype: note\n  nested: wrong\ntype: source\n---\nBody.\n")
        codes = self.codes()
        self.assertIn("metadata.syntax", codes)
        self.assertIn("metadata.duplicate", codes)
        self.assertIn("metadata.required", codes)

    def test_unclosed_frontmatter_is_an_error(self):
        self.write("wiki/Broken.md", "---\ntype: note\nBody.\n")
        self.assertIn("metadata.unclosed", self.codes())

    def test_wrong_metadata_types_report_errors_without_crashing(self):
        self.page("Broken", type=["note"], status=["current"], aliases="Alias", updated=["2026-09-15"])
        self.assertIn("metadata.type", self.codes())
        self.assertEqual(1, self.invoke("check", "--json")[0])
        self.source(coverage=["full"])
        self.assertIn("source.coverage", self.codes())

    def test_invalid_dates_and_unknown_optional_metadata(self):
        self.page("Note", updated="2026-02-30", personal_context="Useful extension")
        codes = self.codes()
        self.assertIn("metadata.date", codes)
        self.assertIn("metadata.unknown", codes)

    def test_partial_source_needs_scope_and_may_be_current_with_declared_scope(self):
        self.source(coverage="partial")
        self.assertIn("source.coverage_note", self.codes())
        self.source(coverage="partial", status="current", coverage_note="Reviewed line 1; line 2 excluded from this inquiry.")
        self.assert_valid()

    def test_explicit_empty_source_requires_disposition(self):
        self.source(body="No relevant claims.\n", disposition="Reviewed; outside this inquiry.")
        self.assert_valid()
        self.source(body="No relevant claims.\n")
        self.assertIn("source.no_claims", self.codes())
        self.source(body="`No relevant claims.`\n", disposition="Not evidence.")
        self.assertIn("source.no_claims", self.codes())

    def test_line_ranges_validate_start_end_and_decoded_raw_count(self):
        for locator in ("lines 0-1", "lines 2-1", "lines 1-3"):
            with self.subTest(locator=locator):
                self.source(body=f"### S1\nA statement.\nLocator: {locator}\n")
                self.assertIn("claim.range", self.codes())
        self.source(body="### S1\nA statement.\nLocator: lines 1-2\n")
        self.assert_valid()

    def test_binary_source_needs_manual_locator(self):
        self.write("raw/audio.bin", b"\xff\xfe\x00")
        self.source(raw="raw/audio.bin", body="### S1\nStatement.\nLocator: lines 1-1\n")
        self.assertIn("claim.binary_lines", self.codes())
        for locator in ("page 3", "timestamp 00:12:08-00:12:20", "section Methods"):
            with self.subTest(locator=locator):
                self.source(raw="raw/audio.bin", body=f"### S1\nStatement.\nLocator: {locator}\n")
                workspace = self.assert_valid()
                self.assertIn("claim.manual_locator", self.codes(workspace))

    def test_missing_duplicate_and_inactive_locators_fail(self):
        for body in ("### S1\nStatement.\n", "### S1\nStatement.\nLocator: lines 1-1\nLocator: lines 2-2\n", "### S1\nStatement.\n`Locator: lines 1-1`\n"):
            with self.subTest(body=body):
                self.source(body=body)
                self.assertIn("claim.locator", self.codes())

    def test_heading_and_locator_do_not_count_as_a_source_statement(self):
        for body in ("### S1\n\nLocator: lines 1-1\n", "### S1\n\n#### Statement\n\n<!-- placeholder -->\nLocator: lines 1-1\n"):
            with self.subTest(body=body):
                self.source(body=body)
                self.assertIn("claim.empty", self.codes())
                self.assertEqual(1, self.invoke("seal")[0])

    def test_source_raw_path_cannot_traverse_outside_raw(self):
        self.page("Source", "### S1\nClaim.\nLocator: lines 1-1\n", type="source", raw="raw/../secret.txt", sha256="0" * 64, origin="unknown", coverage="full")
        self.assertIn("source.raw_path", self.codes())

    def test_relative_markdown_links_validate_files_and_headings(self):
        self.source(raw="raw/source text.txt")
        self.write("docs/guide.md", "# Guide\n\n## A useful heading\n")
        self.page("Note", "[raw](../raw/source%20text.txt) and [guide](../docs/guide.md#a-useful-heading).\n[claim](Source.md#s1)\n[other][g]\n\n[g]: ../docs/guide.md\n")
        self.write("wiki/index.md", "[Source](Source.md)\n[Note](Note.md)\n")
        self.assert_valid()
        self.page("Note", "[missing](../docs/missing.md) and [heading](Source.md#s999).\n")
        self.assertIn("link.file", self.codes())
        self.assertIn("link.anchor", self.codes())

    def test_local_markdown_paths_cannot_escape_workspace(self):
        self.page("Note", "[secret](../../outside.txt) and [encoded](%2Foutside.txt) and [absolute](file:///private.txt).\n")
        self.assertEqual(3, self.codes().count("link.escape"))

    def test_external_links_are_not_fetched_or_claimed_verified(self):
        self.page("Note", "[external](https://example.invalid/never-fetch) [mail](mailto:nobody@example.invalid).\n")
        self.assert_valid()

    def make_symlink(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable on this host: {exc}")

    def test_raw_file_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="kc-outside-") as outside:
            path = Path(outside) / "private.txt"
            path.write_text("Outside.\n")
            self.make_symlink(self.root / "raw/escape.txt", path)
            workspace = self.workspace()
            self.assertIn("path.escape", self.codes(workspace))
            self.assertNotIn("raw/escape.txt", workspace.raw_bytes)

    def test_unsafe_directory_is_pruned_before_walker_can_descend(self):
        # Model a junction whose resolved target is unsafe without requiring OS
        # symlink privileges. The walker checks the same mutable dirs object it
        # would otherwise use for its next recursive descent.
        escape = self.root / "raw/escape"
        escape.mkdir()
        walk = kc.os.walk
        checked = []

        class ConfinedWorkspace(kc.Workspace):
            def confined(inner, path, scope=None):
                return path != escape and super().confined(path, scope)

        def guarded_walk(top, **kwargs):
            if Path(top) == self.root / "raw":
                directories = ["escape"]
                yield str(top), directories, []
                self.assertNotIn("escape", directories, "Scanner would recursively enumerate an escaped target")
                checked.append(True)
            else:
                yield from walk(top, **kwargs)

        with mock.patch.object(kc.os, "walk", side_effect=guarded_walk):
            workspace = ConfinedWorkspace(self.root)
        self.assertEqual([True], checked)
        self.assertIn("path.escape", self.codes(workspace))

    def test_raw_directory_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="kc-outside-") as outside:
            self.make_symlink(self.root / "raw/escape", Path(outside), directory=True)
            self.assertIn("path.escape", self.codes())

    def test_integrity_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="kc-outside-") as outside:
            self.make_symlink(self.root / ".kc", Path(outside), directory=True)
            self.assertIn("path.escape", self.codes())
            self.assertEqual(1, self.invoke("seal")[0])
            self.assertFalse((Path(outside) / "integrity.json").exists())

    def test_seal_is_noop_for_unchanged_accepted_material(self):
        self.source()
        self.assert_sealed()
        path = self.root / ".kc/integrity.json"
        before = (path.read_bytes(), path.stat().st_mtime_ns)
        self.assert_sealed()
        self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))
        self.assertNotIn("integrity.unsealed", self.codes())

    def test_unsealed_source_hash_mismatch_cannot_be_blessed(self):
        self.source()
        self.write("raw/source.txt", "Omega statement.\nSecond statement.\n")
        self.assertIn("source.hash_mismatch", self.codes())
        self.assertEqual(1, self.invoke("seal")[0])
        self.assertFalse((self.root / ".kc/integrity.json").exists())

    def test_same_length_raw_mutation_is_hard_error_and_seal_refused(self):
        self.source()
        self.assert_sealed()
        baseline = (self.root / ".kc/integrity.json").read_bytes()
        self.write("raw/source.txt", "Omega statement.\nSecond statement.\n")
        codes = self.codes()
        self.assertIn("source.hash_mismatch", codes)
        self.assertIn("integrity.changed", codes)
        self.assertEqual(1, self.invoke("seal")[0])
        self.assertEqual(baseline, (self.root / ".kc/integrity.json").read_bytes())

    def test_recomputing_declared_hash_cannot_reseal_changed_raw(self):
        self.source()
        baseline = self.assert_sealed()
        self.write("raw/source.txt", "Omega statement.\nSecond statement.\n")
        self.source()  # Update declared source hash to match changed bytes.
        self.assertNotIn("source.hash_mismatch", self.codes())
        self.assertIn("integrity.changed", self.codes())
        self.assertEqual(1, self.invoke("seal")[0])
        self.assertEqual(baseline, json.loads((self.root / ".kc/integrity.json").read_text()))

    def test_claim_same_length_mutation_and_whitespace_changes_are_detected(self):
        path = self.source()
        self.assert_sealed()
        original = path.read_text(encoding="utf-8")
        for modified in (original.replace("Alpha statement.", "Omega statement."), original.replace("Alpha statement.", "Alpha statement. ")):
            with self.subTest(modified=modified):
                self.write("wiki/Source.md", modified)
                self.assertIn("integrity.changed", self.codes())
                self.assertEqual(1, self.invoke("seal")[0])

    def test_source_markdown_line_ending_changes_do_not_change_claim_identity(self):
        path = self.source()
        self.assert_sealed()
        self.write("wiki/Source.md", path.read_bytes().replace(b"\n", b"\r\n"))
        self.assert_valid()

    def test_deleted_claim_and_reused_id_are_rejected(self):
        path = self.source()
        self.assert_sealed()
        original = path.read_text(encoding="utf-8")
        self.write("wiki/Source.md", original.replace("### S1", "### S2"))
        self.assertIn("integrity.missing", self.codes())
        self.assertEqual(1, self.invoke("seal")[0])
        self.write("wiki/Source.md", original.replace("Alpha statement.", "Other statement."))
        self.assertIn("integrity.changed", self.codes())

    def test_deleted_raw_and_source_page_are_rejected(self):
        self.source()
        self.assert_sealed()
        (self.root / "raw/source.txt").unlink()
        (self.root / "wiki/Source.md").unlink()
        self.write("wiki/index.md", "# Index\n")
        self.assertEqual(2, self.codes().count("integrity.missing"))
        self.assertEqual(1, self.invoke("seal")[0])

    def test_renaming_sealed_source_even_with_alias_does_not_change_identity(self):
        path = self.source()
        self.assert_sealed()
        path.rename(self.root / "wiki/Renamed.md")
        self.write("wiki/index.md", "[[Renamed]]\n")
        self.assertIn("integrity.missing", self.codes())

    def test_same_bytes_new_raw_binding_cannot_rebind_old_claim(self):
        path = self.source()
        self.assert_sealed()
        self.write("raw/copy.txt", (self.root / "raw/source.txt").read_bytes())
        self.write("wiki/Source.md", path.read_text().replace("raw/source.txt", "raw/copy.txt"))
        self.assertIn("integrity.changed", self.codes())
        self.assertEqual(1, self.invoke("seal")[0])

    def test_additive_seal_preserves_all_existing_records(self):
        path = self.source()
        accepted = self.assert_sealed()
        self.write("raw/new.txt", "New external evidence.\n")
        new_claim = "### S2\n\nSecond statement.\n\nLocator: lines 2-2\n\n"
        self.write("wiki/Source.md", path.read_text().replace("## Corrections", new_claim + "## Corrections"))
        self.assert_valid()
        self.assertIn("integrity.unsealed", self.codes())
        after = self.assert_sealed()
        for category in ("raw", "claims"):
            for key, value in accepted[category].items():
                self.assertEqual(value, after[category][key])
        self.assertIn("Source#S2", after["claims"])
        self.assertIn("raw/new.txt", after["raw"])

    def test_corrections_and_derived_pages_can_change_without_rewriting_claim(self):
        path = self.source()
        self.page("Note", "[[Source#S1]] supports a hypothesis.\n")
        self.assert_sealed()
        self.write("wiki/Source.md", path.read_text().replace("None.", "Withdrawn from current use: see [[Note]]."))
        self.page("Note", "## Revised interpretation\n\n[[Source#S1]] is insufficient.\n", status="contested")
        self.assert_valid()

    def test_claim_impact_does_not_conflate_unrelated_claim_ids(self):
        self.source(body="### S1\nAlpha.\nLocator: lines 1-1\n\n### S2\nSecond.\nLocator: lines 2-2\n\n## Corrections\n[[Source#S1]] needs review.\n")
        self.page("Direct", "[[Source#S1]]\n")
        self.page("Unrelated", "[[Source#S2]]\n")
        self.page("Broad", "[[Source]]\n")
        self.page("Downstream", "[[Direct]]\n")
        code, output, _ = self.invoke("impact", "Source#S1")
        self.assertEqual(0, code)
        self.assertIn("direct: Direct", output)
        self.assertIn("direct: Broad", output)
        self.assertIn("transitive: Downstream", output)
        self.assertNotIn("Unrelated", output)
        self.assertNotIn("direct: Source", output)
        self.assertNotIn("direct: index", output)
        self.assertIn("Review index summaries and uncited copies separately", output)

    def test_page_impact_includes_all_claim_references(self):
        self.source()
        self.page("Note", "[[Source#S1]]\n")
        code, output, _ = self.invoke("impact", "Source")
        self.assertEqual(0, code)
        self.assertIn("direct: Note", output)
        self.assertEqual(2, self.invoke("impact", "Source#S999")[0])

    def test_invalid_baseline_cannot_be_replaced_by_seal(self):
        self.source()
        path = self.write(".kc/integrity.json", '{"version": 999, "raw": {}, "claims": {}}')
        before = path.read_bytes()
        self.assertIn("integrity.invalid", self.codes())
        self.assertEqual(1, self.invoke("seal")[0])
        self.assertEqual(before, path.read_bytes())

    def test_seal_lock_refuses_concurrent_writer(self):
        self.source()
        lock = self.write(".kc/seal.lock", "active writer\n")
        self.assertEqual(1, self.invoke("seal")[0])
        self.assertTrue(lock.exists())
        self.assertFalse((self.root / ".kc/integrity.json").exists())

    def test_status_reports_raw_backlog_drafts_contested_and_recovery_text(self):
        self.write("raw/unread.txt", "Unread.\n")
        self.source(status="draft", coverage="partial", coverage_note="Reviewed line 1; line 2 pending.")
        self.page("Contested", status="contested")
        self.write("wiki/_state.md", "# Recovery\n\n- [ ] Review remaining source lines.\n")
        code, output, _ = self.invoke("status")
        self.assertEqual(0, code)
        self.assertIn("raw/unread.txt", output)
        self.assertIn("Source", output)
        self.assertIn("Contested", output)
        self.assertIn("[ ] Review remaining source lines.", output)

    def test_current_partial_source_is_limited_but_not_pending(self):
        self.source(status="current", coverage="partial", coverage_note="Reviewed line 1; line 2 outside scope.")
        code, output, _ = self.invoke("status")
        self.assertEqual(0, code)
        self.assertIn("Pending pages:\n  (none)", output)
        self.assertIn("Limited coverage:\n  Source: Reviewed line 1", output)

    def test_search_is_deterministic_bounded_and_optionally_searches_raw(self):
        self.page("Agency", "## Agency\n\nAgency and action.\n", summary="Agency overview")
        self.page("Planning", "Agency matters in planning.\n")
        self.write("raw/agency.txt", "Agency testimony.\n")
        first = self.invoke("search", "agency", "--limit", "1")
        self.assertEqual(first, self.invoke("search", "agency", "--limit", "1"))
        self.assertIn("wiki/Agency.md", first[1])
        self.assertNotIn("wiki/Planning.md", first[1])
        self.assertNotIn("raw/agency.txt", first[1])
        self.assertIn("raw/agency.txt", self.invoke("search", "agency", "--raw")[1])

    def test_search_surfaces_status_coverage_and_returns_error_for_drift(self):
        self.source(status="current", coverage="partial", coverage_note="Reviewed line 1 only.")
        code, output, error = self.invoke("search", "statement")
        self.assertEqual(0, code)
        self.assertIn("[source; current; coverage=partial]", output)
        self.assertIn("unsealed", error)
        self.assert_sealed()
        self.write("raw/source.txt", "Omega statement.\nSecond statement.\n")
        code, output, error = self.invoke("search", "statement")
        self.assertEqual(1, code)
        self.assertIn("Source.md", output)
        self.assertIn("stale or incomplete", error)

    def test_cli_default_root_and_lint_adapter_run_from_another_directory(self):
        script = Path(kc.__file__).resolve()
        result = subprocess.run([sys.executable, str(script), "--root", str(self.root), "check", "--json"], cwd=self.root / "raw", capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(str(self.root.resolve()), json.loads(result.stdout)["root"])
        adapter = subprocess.run([sys.executable, str(script.with_name("lint.py")), "--root", str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(0, adapter.returncode, adapter.stderr)
        self.assertEqual(0, json.loads(adapter.stdout)["errors"])


if __name__ == "__main__":
    unittest.main()
