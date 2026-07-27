import importlib.util
import tempfile
import unittest
from pathlib import Path

PATH = Path(__file__).parents[1] / "actions/metadata-check/scripts/check.py"
SPEC = importlib.util.spec_from_file_location("metadata_check", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MetadataTests(unittest.TestCase):
    def test_valid_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n## Versioning\nSemantic Versioning.\n")
            (root / "LICENSE").write_text("Apache License\n")
            (root / "SECURITY.md").write_text("# Security\n")
            (root / "CONTRIBUTING.md").write_text("# Contributing\n")
            self.assertEqual(MODULE.validate(root, False, True), [])

    def test_missing_and_obsolete_namespace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("Alireza" + "Sayyari/project\n")
            errors = MODULE.validate(root, True, True)
            self.assertTrue(any("missing required file" in error for error in errors))
            self.assertTrue(any("obsolete personal namespace" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
