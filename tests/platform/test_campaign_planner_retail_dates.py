import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/campaign-planner/scripts/retail_dates.py"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


class RetailDatesTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_dateless_rows_only_for_years_in_the_window(self):
        p = run("--market", "US,UK,EU", "--from", "2027-10-01", "--to", "2027-12-31", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        moments = json.loads(p.stdout)["moments"]
        self.assertEqual([m for m in moments if m["date"] is None and m["year"] != 2027], [])
        self.assertTrue(all(m["date"] is None or m["date"] <= "2027-12-31" or m["promote_from"] <= "2027-12-31"
                            for m in moments))

    def test_dateless_rows_kept_when_no_window(self):
        p = run("--market", "US,UK,EU", "--year", "2035", "--json")
        moments = json.loads(p.stdout)["moments"]
        self.assertTrue(any(m["date"] is None and m["year"] == 2035 for m in moments))

    def test_markdown_window_has_no_next_year_look_ups(self):
        p = run("--market", "US", "--from", "2027-10-01", "--to", "2027-12-31")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn("| 2028 ? |", p.stdout)


if __name__ == "__main__":
    unittest.main()
