import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/ask-your-data/scripts/summarise_eql.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class SummariseEqlTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_numeric_strings_count_in_total(self):
        r = run(FX / "eql_revenue_by_currency.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Total (all rows, including null/empty/other): 3,750.50", r.stdout)
        self.assertIn("1 row(s) had no numeric value", r.stdout)

    def test_funnel_string_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "f.json").write_text(json.dumps(
                {"success": True, "analysis_type": "funnel",
                 "data": {"total": {"counts": ["1,000", "250"], "times": [-1, "3600"]}}}))
            r = subprocess.run([sys.executable, str(SCRIPT), "f.json"], cwd=tmp, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Step 2: 250  (25.0% of previous, 25.0% of step 1)  avg time from previous: 1.0 h", r.stdout)

    def test_error_response(self):
        r = run(FX / "denied.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", r.stderr)


if __name__ == "__main__":
    unittest.main()
