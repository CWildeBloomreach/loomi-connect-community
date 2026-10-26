import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/data-feed-health/scripts/discovery_jobs_summary.py"
FIX = ROOT / "tests/fixtures/platform/data_feed"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


class DiscoveryJobsSummaryTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_access_denied_is_an_error_not_red(self):
        p = run(FIX / "jobs_denied.json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", out["error"])
        self.assertNotIn("status", out)

    def test_date_only_now_and_naive_timestamps_are_utc(self):
        p = run("--now", "2026-10-26", FIX / "jobs_naive.json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["now"], "2026-10-26T00:00:00+00:00")
        self.assertEqual(out["kinds"]["index:update"]["hours_since_success"], 21.5)
        self.assertEqual(out["kinds"]["feed:products"]["hours_since_success"], 22.7)
        self.assertEqual(out["status"], "green")

    def test_bad_now_is_a_clear_error(self):
        p = run("--now", "yesterday", FIX / "jobs_naive.json")
        self.assertEqual(p.returncode, 2)
        self.assertNotIn("Traceback", p.stderr)


if __name__ == "__main__":
    unittest.main()
