"""Regression checks for safe blank-instance construction."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("new_instance", ROOT / "tools/new_instance.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class NewInstanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.source = self.base / "template"
        for name in module.FILES:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("State: bootstrap\n" if name == "wiki/index.md" else "placeholder\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_new_instance_excludes_private_data_and_eval_keys(self):
        (self.source / "evals").mkdir()
        (self.source / "evals/gold.md").write_text("do not copy", encoding="utf-8")
        (self.source / "wiki/_state.md").write_text("prior task", encoding="utf-8")
        dest = module.create_instance(self.source, self.base / "new")
        self.assertTrue((dest / "raw").is_dir())
        self.assertFalse((dest / "evals").exists())
        self.assertFalse((dest / "wiki/_state.md").exists())
        self.assertEqual((dest / "wiki/index.md").read_text(encoding="utf-8"), module.BOOTSTRAP_INDEX)

    def test_personalized_bootstrap_charter_and_history_are_not_copied(self):
        (self.source / "wiki/index.md").write_text("State: bootstrap\nPrivate career decision\n", encoding="utf-8")
        (self.source / "wiki/log.md").write_text("Private personal history\n", encoding="utf-8")
        dest = module.create_instance(self.source, self.base / "new")
        self.assertEqual((dest / "wiki/index.md").read_text(encoding="utf-8"), module.BOOTSTRAP_INDEX)
        self.assertEqual((dest / "wiki/log.md").read_text(encoding="utf-8"), module.BOOTSTRAP_LOG)

    def test_existing_destination_is_preserved(self):
        dest = self.base / "old"
        dest.mkdir()
        (dest / "mine.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError):
            module.create_instance(self.source, dest)
        self.assertEqual((dest / "mine.txt").read_text(), "keep")

    def test_populated_source_refused(self):
        (self.source / "raw").mkdir()
        (self.source / "raw/private.md").write_text("private", encoding="utf-8")
        with self.assertRaises(ValueError):
            module.create_instance(self.source, self.base / "new")
        self.assertFalse((self.base / "new").exists())

    def test_missing_required_file_does_not_create_destination(self):
        (self.source / "AGENTS.md").unlink()
        with self.assertRaises(ValueError):
            module.create_instance(self.source, self.base / "new")
        self.assertFalse((self.base / "new").exists())


if __name__ == "__main__":
    unittest.main()
