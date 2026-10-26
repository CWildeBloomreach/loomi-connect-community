import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-platform/skills/peak-readiness-check/scripts/check_rule_windows.py"
FIX = ROOT / "tests/fixtures/platform/peak_readiness"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=tmp,
                              capture_output=True, text=True)


class CheckRuleWindowsTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)

    def test_date_only_end_covers_the_whole_last_day(self):
        p = run("--rules", FIX / "rules.json", "--start", "2026-11-27", "--end", "2026-12-01", "--format", "json")
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["summary"]["window"], "2026-11-27 00:00 UTC to 2026-12-01 23:59 UTC")
        # 9001 ends at noon on the last day: flagged. 9002 runs to 23:59:59: fine.
        self.assertEqual([(f["rule"].split()[0], f["check"]) for f in out["findings"]],
                         [("9001", "Event rule ends early")])

    def test_bad_date_is_a_clear_error(self):
        p = run("--rules", FIX / "rules.json", "--start", "2026-11-27", "--end", "2026-13-01")
        self.assertEqual(p.returncode, 2)
        self.assertIn("must be ISO dates or times", p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_end_before_start_is_a_clear_error(self):
        p = run("--rules", FIX / "rules.json", "--start", "2026-12-02", "--end", "2026-12-01")
        self.assertEqual(p.returncode, 2)
        self.assertIn("before --start", p.stderr)

    def test_error_response_stops_markdown(self):
        p = run("--rules", FIX / "rules_denied.json", "--start", "2026-11-27", "--end", "2026-12-01")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout, "")
        self.assertIn("Loomi Connect returned an error: [ACCESS_DENIED]", p.stderr)

    def test_error_response_stops_json(self):
        p = run("--rules", FIX / "rules.json", "--rules", FIX / "rules_denied.json",
                "--start", "2026-11-27", "--end", "2026-12-01", "--format", "json")
        self.assertEqual(p.returncode, 1)
        out = json.loads(p.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("rules_denied.json: Loomi Connect returned an error", out["error"])


if __name__ == "__main__":
    unittest.main()
