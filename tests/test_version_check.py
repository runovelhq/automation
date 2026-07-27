import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).parents[1] / "actions/version-check/scripts/check.py"
SPEC = importlib.util.spec_from_file_location("version_check", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VersionTests(unittest.TestCase):
    def test_stable(self):
        self.assertEqual(MODULE.parse("v1.2.3")["prerelease"], "false")

    def test_prerelease(self):
        result = MODULE.parse("v2.0.0-rc.1")
        self.assertEqual(result["normalized_version"], "2.0.0-rc.1")
        self.assertEqual(result["major_minor"], "2.0")

    def test_invalid_versions(self):
        for value in ("1.2.3", "v01.2.3", "v1.2", "v1.2.3-rc.01", "v1.2.3+build"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODULE.parse(value)


if __name__ == "__main__":
    unittest.main()
