import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "loomi-discovery" / "skills" / "discovery-trending-searches" / "scripts" / "rank_trends.py"
FIX = ROOT / "tests" / "fixtures" / "discovery"


def run(*args):
    """Run the script by its full path from a fresh working folder, as an assistant would."""
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True, timeout=60)


class RankTrendsTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def result(self, *files):
        p = run("--baseline", "0", "--min-sessions", "30", *files)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def test_flat_query_is_not_falling(self):
        out = self.result(FIX / "rt_queries.json")
        self.assertNotIn("jeans", [i["query"] for i in out["falling"]])
        self.assertNotIn("jeans", [i["query"] for i in out["rising"]])
        self.assertEqual([i["query"] for i in out["falling"]], ["scarf"])

    def test_blank_and_na_numbers(self):
        out = self.result(FIX / "rt_queries.json")
        boots = next(i for i in out["new"] if i["query"] == "boots")
        self.assertIsNone(boots["revenue"])
        self.assertEqual(out["falling"][0]["revenue"], 1200.0)

    def test_case_and_space_variants_are_added_together(self):
        out = self.result(FIX / "rt_queries.json")
        dress = next(i for i in out["rising"] if i["query"] == "dress")
        self.assertEqual((dress["sessions"], dress["prev_sessions"], dress["revenue"]), (140, 110, 110.0))
        self.assertEqual(out["merged_variants"], [{"query": "dress", "merged": ["dress", "Dress "]}])

    def test_same_row_on_two_pages_counts_once(self):
        out = self.result(FIX / "rt_queries.json", FIX / "rt_queries.json")
        dress = next(i for i in out["rising"] if i["query"] == "dress")
        self.assertEqual(dress["sessions"], 140)
        self.assertEqual(out["queries_considered"], 4)

    def test_error_returned_as_data_stops(self):
        p = run("--baseline", "0", FIX / "denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("ACCESS_DENIED", out["error"])


if __name__ == "__main__":
    unittest.main()
