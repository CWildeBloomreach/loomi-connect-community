import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-scenario-explainer/scripts/scenario_graph.py"
FIXTURES = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class ScenarioGraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = run(FIXTURES / "scenario_splits.json")
        assert r.returncode == 0, r.stderr
        cls.out = r.stdout

    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_ab_split_branches_by_variant_id(self):
        self.assertIn("(Control) [7] limit", self.out)  # output 4 = variant id 4, not position 3
        self.assertIn("(Free ship) [4]", self.out)

    def test_contextual_split_is_id_plus_one(self):
        self.assertIn("(Ctx A) [11]", self.out)
        self.assertIn("(Ctx B) [12]", self.out)

    def test_limit_outputs(self):
        self.assertIn("(within limit) [8]", self.out)
        self.assertIn("(over limit) [9]", self.out)

    def test_warnings(self):
        warnings = self.out.split("## Warnings", 1)[1]
        self.assertIn("output 3, but no variant has that id", warnings)
        self.assertIn("add up to 90%", warnings)
        self.assertIn("Dangling wait [5]", warnings)
        self.assertNotIn("Dangling wait [9]", warnings)
        self.assertNotIn("Contextual\": variant percentages", warnings)

    def test_error_response(self):
        r = run(FIXTURES / "denied.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)
        self.assertIn("don't treat it as 'nothing found'", r.stderr)


if __name__ == "__main__":
    unittest.main()
