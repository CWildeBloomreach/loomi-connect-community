import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-report-explainer/scripts/analysis_summary.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


def has_zone(name):
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo(name)
        return True
    except Exception:
        return False


class AnalysisSummaryTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)
        r = run("result", "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("--tz", r.stdout)

    @unittest.skipUnless(has_zone("Pacific/Kiritimati"), "no IANA time zone data on this machine")
    def test_tz_gives_local_dates_for_utc_plus_14(self):
        r = run("result", FX / "report_daily_kiritimati.json", "--tz", "Pacific/Kiritimati")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("2026-01-05 | 10 | 300.0", r.stdout)
        self.assertIn("2026-01-06 | 12 | 340.50", r.stdout)
        self.assertIn("Dates in Pacific/Kiritimati", r.stdout)

    def test_without_tz_says_what_it_assumes(self):
        r = run("result", FX / "report_daily_kiritimati.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("UTC-10 and UTC+13", r.stdout)
        self.assertIn("| 22 | 640.5", r.stdout)  # "340.50" counts in the total

    def test_utc_plus_13_without_tz(self):
        # Midnight 2026-01-05 at UTC+13 (New Zealand summer) is 2026-01-04 11:00 UTC.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "r.json"
            p.write_text('{"as_dict": {"1767524400": [1]}, "definition": {"server": '
                         '{"rows": [{"attribute": {"type": "timestamp"}}], "metrics": [{"name": "n"}]}}}')
            r = subprocess.run([sys.executable, str(SCRIPT), "result", "r.json"], cwd=tmp,
                               capture_output=True, text=True)
        self.assertIn("2026-01-05 | 1", r.stdout)

    def test_unknown_tz(self):
        r = run("result", FX / "report_daily_kiritimati.json", "--tz", "Mars/Olympus")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Unknown time zone", r.stderr)

    def test_error_response(self):
        r = run("result", FX / "denied.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Loomi Connect returned an error", r.stderr)


if __name__ == "__main__":
    unittest.main()
