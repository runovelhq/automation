import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).parents[1] / "scripts/verify-action-pins.py"
SPEC = importlib.util.spec_from_file_location("verify_action_pins", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PinTests(unittest.TestCase):
    def test_full_sha_accepted(self):
        self.assertIsNone(MODULE.validate_reference("actions/checkout@" + "a" * 40))

    def test_tag_rejected(self):
        self.assertIsNotNone(MODULE.validate_reference("actions/checkout@v4"))

    def test_branch_rejected(self):
        self.assertIsNotNone(MODULE.validate_reference("actions/checkout@main"))

    def test_local_accepted(self):
        self.assertIsNone(MODULE.validate_reference("./actions/version-check"))

    def test_malformed_rejected(self):
        self.assertIsNotNone(MODULE.validate_reference("actions/checkout"))

    def test_documented_v1_workflow_accepted(self):
        ref = "runovelhq/automation/.github/workflows/reusable-language-ci.yml@v1"
        self.assertIsNone(MODULE.validate_reference(ref))


if __name__ == "__main__":
    unittest.main()
