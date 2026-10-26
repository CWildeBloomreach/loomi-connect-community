import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/campaign-planner/scripts/weekly_peaks.py"
FIX = ROOT / "tests/fixtures/platform/campaign"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


class WeeklyPeaksTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_mid_series_week_with_a_missing_day_is_still_a_peak(self):
        p = run(FIX / "trend_mid_gap.json", "--metric", "revenue", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["peaks"][0], "2025-11-17")
        weeks = {w["week_start"]: w for w in out["weeks"]}
        self.assertFalse(weeks["2025-11-17"]["partial"])
        self.assertEqual(weeks["2025-11-17"]["missing_days"], 1)

    def test_na_day_is_left_out_not_counted_as_zero(self):
        out = json.loads(run(FIX / "trend_mid_gap.json", "--metric", "revenue", "--json").stdout)
        self.assertEqual(out["days_without_a_number"], ["2025-11-10"])
        weeks = {w["week_start"]: w for w in out["weeks"]}
        self.assertEqual(weeks["2025-11-10"]["days"], 6)
        self.assertEqual(weeks["2025-11-10"]["total"], 600.0)

    def test_markdown_flags_missing_days(self):
        p = run(FIX / "trend_mid_gap.json", "--metric", "revenue")
        self.assertIn("| 2025-11-17 (1 day(s) missing) |", p.stdout)
        self.assertIn("**No number for:** 2025-11-10", p.stdout)

    def test_error_response_stops(self):
        p = run(FIX / "trend_denied.json")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)
        p = run(FIX / "trend_denied.json", "--json")
        self.assertEqual(p.returncode, 1)
        self.assertFalse(json.loads(p.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
