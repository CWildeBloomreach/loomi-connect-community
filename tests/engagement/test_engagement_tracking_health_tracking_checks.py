import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins/loomi-engagement/skills/engagement-tracking-health/scripts/tracking_checks.py"
FX = ROOT / "tests/fixtures/engagement"


def run(*args):
    with tempfile.TemporaryDirectory() as tmp:
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=tmp, capture_output=True, text=True)


class TrackingChecksTest(unittest.TestCase):
    def test_help(self):
        self.assertEqual(run("--help").returncode, 0)
        self.assertEqual(run("volumes", "--help").returncode, 0)

    def test_new_event_type_is_new_not_spike(self):
        r = run("volumes", FX / "tracking_schema.json", FX / "tracking_last7.json",
                FX / "tracking_prev7.json", FX / "tracking_last90.json")
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = {row["event_type"]: row for row in json.loads(r.stdout)["event_types"]}
        self.assertEqual(rows["quiz_completed"]["status"], "new")
        self.assertEqual(rows["quiz_completed"]["avg_week_90d"], 0.0)
        self.assertEqual(rows["view_item"]["status"], "ok")
        # baseline excludes the current week: (155000 - 13000) / (83 / 7)
        self.assertAlmostEqual(rows["view_item"]["avg_week_90d"], round(142000 / (83 / 7), 1))

    def test_error_response(self):
        r = run("volumes", FX / "tracking_schema.json", FX / "denied.json", FX / "tracking_prev7.json")
        self.assertEqual(r.returncode, 1)
        out = json.loads(r.stdout)
        self.assertFalse(out["ok"])
        self.assertIn("Loomi Connect returned an error", out["error"])


if __name__ == "__main__":
    unittest.main()
