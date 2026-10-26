import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/change-impact-tracker/scripts/did_effect.py"
FIX = ROOT / "tests/fixtures/platform/change_impact"


def run(tmp, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp, capture_output=True, text=True)


class DidEffectTest(unittest.TestCase):
    def test_help(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(tmp, "--help").returncode, 0)

    def test_template_out_writes_a_usable_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = run(tmp, "--template", "--out", "change.json")
            self.assertEqual(p.returncode, 0, p.stderr)
            spec = json.loads((Path(tmp) / "change.json").read_text())
            self.assertIn("treated", spec)
            p = run(tmp, "change.json", "--json")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("verdict", json.loads(p.stdout))

    def test_out_without_template_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(tmp, FIX / "change_7_vs_6_na.json", "--out", "x.json").returncode, 2)

    def test_7_vs_6_days_warns_and_na_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = run(tmp, FIX / "change_7_vs_6_na.json", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        warns = json.loads(p.stdout)["warnings"]
        self.assertTrue(any("not whole weeks" in w for w in warns), warns)
        self.assertTrue(any("No number for treated before revenue" in w for w in warns), warns)


if __name__ == "__main__":
    unittest.main()
