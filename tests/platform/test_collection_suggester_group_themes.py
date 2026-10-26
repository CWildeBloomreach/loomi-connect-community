import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/collection-suggester/scripts/group_themes.py"
FIX = ROOT / "tests/fixtures/platform/collection"

PROFILES = [
    {"source": {"query": "cargo pants"}, "dominant": [{"value": "category=/men/pants", "share": 0.9},
                                                      {"value": "colors=khaki", "share": 0.5}]},
    {"source": {"query": "utility trousers"}, "dominant": [{"value": "category=/men/pants", "share": 0.8},
                                                           {"value": "colors=khaki", "share": 0.6}]},
]


def run(*queries):
    with tempfile.TemporaryDirectory() as tmp:
        prof = Path(tmp) / "profiles.jsonl"
        prof.write_text("\n".join(json.dumps(p) for p in PROFILES) + "\n")
        return subprocess.run([sys.executable, str(SCRIPT), "--baseline", "10", "--queries", *map(str, queries),
                               "--profiles", "profiles.jsonl"], cwd=tmp, capture_output=True, text=True)


class GroupThemesTest(unittest.TestCase):
    def test_help(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)

    def test_na_values_do_not_crash_or_count_as_zero_rates(self):
        p = run(FIX / "queries_30d.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        theme = out["themes"][0]
        self.assertEqual(sorted(theme["queries"]), ["cargo pants", "utility trousers"])
        self.assertEqual(theme["revenue"], 1000.0)
        # Only cargo pants reports a conversion rate, so the theme's rate is its rate, not diluted by NA as 0.
        self.assertEqual(theme["conversion_rate"], 2.0)
        self.assertEqual(out["missing_values"]["queries"], ["utility trousers"])

    def test_same_window_files_merge(self):
        p = run(FIX / "queries_30d.json", FIX / "queries_30d_family.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["themes"][0]["sessions"], 700)

    def test_mixing_7_and_30_day_files_is_rejected(self):
        p = run(FIX / "queries_30d.json", FIX / "queries_7d.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("different windows", out["error"])

    def test_error_response_stops(self):
        p = run(FIX / "queries_denied.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", json.loads(p.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
