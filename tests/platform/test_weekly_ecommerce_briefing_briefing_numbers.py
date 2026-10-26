import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/weekly-ecommerce-briefing/scripts/briefing_numbers.py"
FIX = ROOT / "tests/fixtures/platform/briefing"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


class BriefingNumbersTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_ok_card(self):
        p = run("--overall", FIX / "overall.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["kpis"]["overall"]["this"]["revenue"], 100000.0)
        self.assertNotIn("missing_values", out)

    def test_na_does_not_crash_and_is_reported(self):
        p = run("--overall", FIX / "overall_na.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["kpis"]["overall"]["this"]["revenue"], 0.0)
        self.assertEqual(out["missing_values"]["count"], 2)
        self.assertTrue(all("overall_na.json current." in m for m in out["missing_values"]["counted_as_zero"]))

    def test_error_response_stops(self):
        p = run("--overall", FIX / "overall.json", "--queries", FIX / "queries_denied.json")
        self.assertEqual(p.returncode, 1)
        self.assertNotIn("Traceback", p.stderr)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("queries_denied.json: Loomi Connect returned an error: [ACCESS_DENIED]", out["error"])


if __name__ == "__main__":
    unittest.main()
